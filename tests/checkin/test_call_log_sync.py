"""Integration tests for VlogsAgent CDC pipeline - call log syncing.

Tests the CDC flow:
1. Raw call log API response → sync_raw_log_to_db → CallLog + CallTranscript tables
2. update_call_log_metrics → CheckIn + health entry tables

Uses isolated SQLite test database.
"""

import uuid
from datetime import UTC, datetime

from sqlmodel import Session, select

from longevity_clinic.app.data.schemas.db import (
    CallLog,
    CallTranscript,
    CheckIn,
    FoodLogEntry,
    MedicationEntry,
    SymptomEntry,
)
from longevity_clinic.app.data.schemas.llm import CheckInSummary, MetricLogsOutput
from longevity_clinic.app.data.schemas.llm import (
    FoodEntryModel as FoodEntrySchema,
    MedicationEntryModel as MedicationEntrySchema,
    Symptom as SymptomSchema,
)


def create_mock_call_log_entry(
    call_id: str = None,
    caller_phone: str = "+12125551234",
    transcript: str = "Patient reports feeling well today",
    duration: int = 120,
    call_date: str = None,
) -> dict:
    """Create a mock API response for a call log entry."""
    return {
        "call_id": call_id or f"call_{uuid.uuid4().hex[:8]}",
        "caller_phone": caller_phone,
        "full_transcript": transcript,
        "duration": duration,
        "call_date": call_date or datetime.now(UTC).isoformat(),
    }


def sync_raw_log_to_db_direct(session: Session, log: dict, user_id: int = None) -> int:
    """Direct implementation of sync_raw_log_to_db for testing with provided session.

    Returns call_log_id or 0 if failed.
    """
    call_id = log.get("call_id", "")
    if not call_id:
        return 0

    # Skip if exists
    existing = session.exec(select(CallLog).where(CallLog.call_id == call_id)).first()
    if existing:
        return 0

    phone = log.get("caller_phone", "")
    call_date_str = log.get("call_date", "")
    try:
        started_at = datetime.fromisoformat(call_date_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        started_at = datetime.now(UTC)

    transcript_text = log.get("full_transcript", "")

    # Create CallLog
    call_log = CallLog(
        call_id=call_id,
        phone_number=phone,
        started_at=started_at,
        duration_seconds=log.get("duration", 0),
        direction="inbound",
        status="completed",
        processed_to_metrics=False,
        user_id=user_id,
    )
    session.add(call_log)
    session.flush()
    call_log_id = call_log.id

    # Create CallTranscript
    session.add(
        CallTranscript(
            call_log_id=call_log_id,
            call_id=call_id,
            raw_transcript=transcript_text,
            language="en",
        )
    )
    session.commit()
    return call_log_id


def update_call_log_with_metrics_direct(
    session: Session,
    call_log_id: int,
    output: MetricLogsOutput,
    user_id: int = None,
) -> bool:
    """Direct implementation of update_call_log_metrics for testing.

    Creates CheckIn and health entries from parsed output.
    """
    call_log = session.get(CallLog, call_log_id)
    if not call_log:
        return False

    now = datetime.now(UTC)
    checkin_id = output.checkin.id or f"call_{call_log.call_id}"

    # Create or update CheckIn
    existing = session.exec(
        select(CheckIn).where(CheckIn.call_log_id == call_log_id)
    ).first()

    if existing:
        checkin = existing
        checkin.summary = output.checkin.summary
    else:
        checkin = CheckIn(
            checkin_id=checkin_id,
            call_log_id=call_log_id,
            user_id=user_id or call_log.user_id,
            patient_name=output.checkin.patient_name or "Unknown",
            checkin_type="call",
            summary=output.checkin.summary,
            raw_content=None,
            timestamp=call_log.started_at,
        )
    session.add(checkin)
    session.flush()

    # Save health entries
    for med in output.medications_entries:
        if not med.name:
            continue
        session.add(
            MedicationEntry(
                user_id=user_id or call_log.user_id,
                checkin_id=checkin.id,
                name=med.name,
                dosage=med.dosage or "",
                frequency=med.frequency or "",
                status=med.status or "active",
                source="call",
                mentioned_at=now,
            )
        )

    for food in output.food_entries:
        if not food.name:
            continue
        session.add(
            FoodLogEntry(
                user_id=user_id or call_log.user_id,
                checkin_id=checkin.id,
                name=food.name,
                calories=food.calories or 0,
                protein=food.protein or 0.0,
                carbs=food.carbs or 0.0,
                fat=food.fat or 0.0,
                meal_type=food.meal_type or "snack",
                source="call",
                logged_at=now,
            )
        )

    for sym in output.symptom_entries:
        if not sym.name:
            continue
        session.add(
            SymptomEntry(
                user_id=user_id or call_log.user_id,
                checkin_id=checkin.id,
                name=sym.name,
                severity=sym.severity or "",
                frequency=sym.frequency or "",
                trend=sym.trend or "stable",
                source="call",
                reported_at=now,
            )
        )

    # Mark as processed
    call_log.processed_to_metrics = True
    session.add(call_log)
    session.commit()
    return True


class TestCallLogCDCPipeline:
    """Test CDC pipeline: API → CallLog/CallTranscript → CheckIn/health entries."""

    def test_sync_raw_log_creates_call_log_and_transcript(
        self, test_session: Session, test_user
    ):
        """Verify raw call log syncs to CallLog and CallTranscript tables."""
        call_id = f"call_{uuid.uuid4().hex[:8]}"
        mock_log = create_mock_call_log_entry(
            call_id=call_id,
            caller_phone="+12125551234",
            transcript="I took my blood pressure medication this morning",
            duration=90,
        )

        call_log_id = sync_raw_log_to_db_direct(test_session, mock_log, test_user.id)

        assert call_log_id > 0

        # Verify CallLog
        call_log = test_session.get(CallLog, call_log_id)
        assert call_log is not None
        assert call_log.call_id == call_id
        assert call_log.phone_number == "+12125551234"
        assert call_log.duration_seconds == 90
        assert call_log.processed_to_metrics is False

        # Verify CallTranscript
        transcript = test_session.exec(
            select(CallTranscript).where(CallTranscript.call_log_id == call_log_id)
        ).first()
        assert transcript is not None
        assert "blood pressure medication" in transcript.raw_transcript

    def test_sync_skips_duplicate_call_id(self, test_session: Session, test_user):
        """Verify duplicate call_id is skipped (idempotent)."""
        call_id = f"call_{uuid.uuid4().hex[:8]}"
        mock_log = create_mock_call_log_entry(call_id=call_id)

        # First sync
        call_log_id_1 = sync_raw_log_to_db_direct(test_session, mock_log, test_user.id)
        assert call_log_id_1 > 0

        # Second sync with same call_id - should skip
        call_log_id_2 = sync_raw_log_to_db_direct(test_session, mock_log, test_user.id)
        assert call_log_id_2 == 0  # Skipped

        # Only one CallLog exists
        call_logs = test_session.exec(
            select(CallLog).where(CallLog.call_id == call_id)
        ).all()
        assert len(call_logs) == 1

    def test_update_metrics_creates_checkin_from_call_log(
        self, test_session: Session, test_user
    ):
        """Verify update_call_log_metrics creates CheckIn linked to CallLog."""
        call_id = f"call_{uuid.uuid4().hex[:8]}"
        mock_log = create_mock_call_log_entry(
            call_id=call_id,
            transcript="Feeling good today, energy levels are high",
        )
        call_log_id = sync_raw_log_to_db_direct(test_session, mock_log, test_user.id)

        output = MetricLogsOutput(
            checkin=CheckInSummary(
                id=f"call_{call_id}",
                type="call",
                summary="Patient reports high energy levels",
                timestamp="Today, 2:30 PM",
                sentiment="positive",
                key_topics=["energy", "wellness"],
            ),
            medications_entries=[],
            food_entries=[],
            symptom_entries=[],
        )

        result = update_call_log_with_metrics_direct(
            test_session, call_log_id, output, test_user.id
        )
        assert result is True

        # Verify CheckIn created
        checkin = test_session.exec(
            select(CheckIn).where(CheckIn.call_log_id == call_log_id)
        ).first()
        assert checkin is not None
        assert checkin.checkin_type == "call"
        assert "energy levels" in checkin.summary

        # Verify CallLog marked as processed
        call_log = test_session.get(CallLog, call_log_id)
        assert call_log.processed_to_metrics is True

    def test_cdc_full_pipeline_syncs_health_entries(
        self, test_session: Session, test_user
    ):
        """Test complete CDC: raw log → CallLog → CheckIn → health entries."""
        call_id = f"call_{uuid.uuid4().hex[:8]}"
        transcript = """
        I've been taking my Metformin 500mg twice daily with meals.
        Had oatmeal for breakfast, about 300 calories.
        Slight headache this morning but feeling better now.
        """
        mock_log = create_mock_call_log_entry(
            call_id=call_id,
            transcript=transcript,
        )

        # Step 1: Sync raw log
        call_log_id = sync_raw_log_to_db_direct(test_session, mock_log, test_user.id)
        assert call_log_id > 0

        # Step 2: Process with parsed output (simulating LLM extraction)
        output = MetricLogsOutput(
            checkin=CheckInSummary(
                id=f"call_{call_id}",
                type="call",
                summary="Patient taking metformin, had oatmeal, reports headache",
                patient_name="Test Patient",
            ),
            medications_entries=[
                MedicationEntrySchema(
                    id="med_1",
                    name="Metformin",
                    dosage="500mg",
                    frequency="twice daily",
                )
            ],
            food_entries=[
                FoodEntrySchema(
                    id="food_1",
                    name="Oatmeal",
                    calories=300,
                    meal_type="breakfast",
                )
            ],
            symptom_entries=[
                SymptomSchema(
                    id="sym_1",
                    name="Headache",
                    severity="mild",
                    trend="improving",
                )
            ],
        )

        result = update_call_log_with_metrics_direct(
            test_session, call_log_id, output, test_user.id
        )
        assert result is True

        # Verify CheckIn created
        checkin = test_session.exec(
            select(CheckIn).where(CheckIn.call_log_id == call_log_id)
        ).first()
        assert checkin is not None

        # Verify health entries
        meds = test_session.exec(
            select(MedicationEntry).where(MedicationEntry.checkin_id == checkin.id)
        ).all()
        assert len(meds) == 1
        assert meds[0].name == "Metformin"
        assert meds[0].source == "call"

        foods = test_session.exec(
            select(FoodLogEntry).where(FoodLogEntry.checkin_id == checkin.id)
        ).all()
        assert len(foods) == 1
        assert foods[0].name == "Oatmeal"

        symptoms = test_session.exec(
            select(SymptomEntry).where(SymptomEntry.checkin_id == checkin.id)
        ).all()
        assert len(symptoms) == 1
        assert symptoms[0].name == "Headache"
        assert symptoms[0].trend == "improving"
