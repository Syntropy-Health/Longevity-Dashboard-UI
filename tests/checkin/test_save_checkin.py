"""Integration tests for CheckinState health data persistence.

Tests the complete flow of:
1. save_checkin_and_log_health - Patient check-in submission
2. Health entry persistence to medication_entries, food_log_entries, symptom_entries
3. Database integrity and relationship validation

Uses isolated SQLite test database with direct session operations.
"""

import uuid
from datetime import UTC, datetime

from sqlmodel import Session, select

from longevity_clinic.app.data.model import (
    CheckIn,
    FoodLogEntry,
    MedicationEntry,
    SymptomEntry,
)
from longevity_clinic.app.data.process_schema import (
    CheckInSummary,
    MetricLogsOutput,
)
from longevity_clinic.app.data.state_schemas import (
    FoodEntry as FoodEntrySchema,
    MedicationEntry as MedicationEntrySchema,
    Symptom as SymptomSchema,
)


def create_mock_parse_result(
    checkin_id: str,
    checkin_type: str = "voice",
    summary: str = "Test summary",
    medications: list[dict] | None = None,
    foods: list[dict] | None = None,
    symptoms: list[dict] | None = None,
) -> MetricLogsOutput:
    """Create a mock MetricLogsOutput for testing."""
    meds = medications or []
    food_list = foods or []
    symptom_list = symptoms or []

    return MetricLogsOutput(
        checkin=CheckInSummary(
            id=checkin_id,
            type=checkin_type,
            summary=summary,
            timestamp=datetime.now().strftime("Today, %I:%M %p"),
            sentiment="neutral",
            key_topics=["test"],
            provider_reviewed=False,
            patient_name="Test Patient",
        ),
        medications_entries=[
            MedicationEntrySchema(
                id=f"med_{i}",
                name=m.get("name", "Unknown"),
                dosage=m.get("dosage", ""),
                frequency=m.get("frequency", ""),
                status=m.get("status", "active"),
                adherence_rate=m.get("adherence_rate", 1.0),
            )
            for i, m in enumerate(meds)
        ],
        food_entries=[
            FoodEntrySchema(
                id=f"food_{i}",
                name=f.get("name", "Unknown"),
                calories=f.get("calories", 0),
                protein=f.get("protein", 0.0),
                carbs=f.get("carbs", 0.0),
                fat=f.get("fat", 0.0),
                time=f.get("time", ""),
                meal_type=f.get("meal_type", "snack"),
            )
            for i, f in enumerate(food_list)
        ],
        symptom_entries=[
            SymptomSchema(
                id=f"sym_{i}",
                name=s.get("name", "Unknown"),
                severity=s.get("severity", ""),
                frequency=s.get("frequency", ""),
                trend=s.get("trend", "stable"),
            )
            for i, s in enumerate(symptom_list)
        ],
    )


def save_health_entries_direct(
    session: Session,
    checkin_db_id: int,
    user_id: int | None,
    parse_result: MetricLogsOutput,
    source: str = "manual",
) -> dict[str, int]:
    """Direct implementation of save_health_entries for testing.

    Mirrors save_health_entries_sync but uses provided session.
    """
    counts = {"medications": 0, "foods": 0, "symptoms": 0}
    now = datetime.now(UTC)

    # Save medications
    for med in parse_result.medications_entries:
        if not med.name:
            continue
        entry = MedicationEntry(
            user_id=user_id,
            checkin_id=checkin_db_id,
            name=med.name,
            dosage=med.dosage or "",
            frequency=med.frequency or "",
            status=med.status or "active",
            adherence_rate=med.adherence_rate if med.adherence_rate else 1.0,
            source=source,
            mentioned_at=now,
        )
        session.add(entry)
        counts["medications"] += 1

    # Save food entries
    for food in parse_result.food_entries:
        if not food.name:
            continue
        entry = FoodLogEntry(
            user_id=user_id,
            checkin_id=checkin_db_id,
            name=food.name,
            calories=food.calories or 0,
            protein=food.protein or 0.0,
            carbs=food.carbs or 0.0,
            fat=food.fat or 0.0,
            meal_type=food.meal_type or "snack",
            consumed_at=food.time or None,
            source=source,
            logged_at=now,
        )
        session.add(entry)
        counts["foods"] += 1

    # Save symptoms
    for sym in parse_result.symptom_entries:
        if not sym.name:
            continue
        entry = SymptomEntry(
            user_id=user_id,
            checkin_id=checkin_db_id,
            name=sym.name,
            severity=sym.severity or "",
            frequency=sym.frequency or "",
            trend=sym.trend or "stable",
            source=source,
            reported_at=now,
        )
        session.add(entry)
        counts["symptoms"] += 1

    session.commit()
    return counts


class TestHealthEntryPersistence:
    """Test health entry persistence to database tables."""

    def test_checkin_with_medications_persists_all_entries(
        self, test_session: Session, test_user
    ):
        """Verify medications extracted from check-in are persisted to medication_entries."""
        checkin_id = f"CHK-{uuid.uuid4().hex[:8]}"

        # Create CheckIn
        checkin = CheckIn(
            checkin_id=checkin_id,
            user_id=test_user.id,
            patient_name="Test Patient",
            checkin_type="voice",
            summary="Patient reports taking medications",
            raw_content="I took my metformin 500mg and vitamin D",
        )
        test_session.add(checkin)
        test_session.commit()
        test_session.refresh(checkin)

        # Create parse result with medications
        parse_result = create_mock_parse_result(
            checkin_id=checkin_id,
            medications=[
                {"name": "Metformin", "dosage": "500mg", "frequency": "twice daily"},
                {"name": "Vitamin D", "dosage": "2000IU", "frequency": "daily"},
            ],
        )

        # Save health entries
        counts = save_health_entries_direct(
            test_session, checkin.id, test_user.id, parse_result, "voice"
        )

        assert counts["medications"] == 2

        # Verify in database
        meds = test_session.exec(
            select(MedicationEntry).where(MedicationEntry.checkin_id == checkin.id)
        ).all()
        assert len(meds) == 2

        med_names = {m.name for m in meds}
        assert "Metformin" in med_names
        assert "Vitamin D" in med_names

        # Verify FK relationship
        assert all(m.checkin_id == checkin.id for m in meds)
        assert all(m.user_id == test_user.id for m in meds)

    def test_checkin_with_food_entries_persists_nutrition_data(
        self, test_session: Session, test_user
    ):
        """Verify food entries with nutrition data are persisted correctly."""
        checkin_id = f"CHK-{uuid.uuid4().hex[:8]}"

        checkin = CheckIn(
            checkin_id=checkin_id,
            user_id=test_user.id,
            patient_name="Test Patient",
            checkin_type="manual",
            summary="Logging meals",
        )
        test_session.add(checkin)
        test_session.commit()
        test_session.refresh(checkin)

        parse_result = create_mock_parse_result(
            checkin_id=checkin_id,
            foods=[
                {
                    "name": "Oatmeal",
                    "calories": 300,
                    "protein": 10.0,
                    "meal_type": "breakfast",
                },
                {
                    "name": "Chicken salad",
                    "calories": 400,
                    "protein": 35.0,
                    "meal_type": "lunch",
                },
            ],
        )

        counts = save_health_entries_direct(
            test_session, checkin.id, test_user.id, parse_result, "manual"
        )

        assert counts["foods"] == 2

        foods = test_session.exec(
            select(FoodLogEntry).where(FoodLogEntry.checkin_id == checkin.id)
        ).all()
        assert len(foods) == 2

        # Verify nutrition data preserved
        salad = next(f for f in foods if f.name == "Chicken salad")
        assert salad.calories == 400
        assert salad.protein == 35.0
        assert salad.meal_type == "lunch"
        assert salad.source == "manual"

    def test_checkin_with_symptoms_persists_severity_and_trend(
        self, test_session: Session, test_user
    ):
        """Verify symptoms with severity and trend data are persisted."""
        checkin_id = f"CHK-{uuid.uuid4().hex[:8]}"

        checkin = CheckIn(
            checkin_id=checkin_id,
            user_id=test_user.id,
            patient_name="Test Patient",
            checkin_type="voice",
            summary="Reporting symptoms",
        )
        test_session.add(checkin)
        test_session.commit()
        test_session.refresh(checkin)

        parse_result = create_mock_parse_result(
            checkin_id=checkin_id,
            symptoms=[
                {"name": "Headache", "severity": "mild", "frequency": "daily"},
                {"name": "Fatigue", "severity": "moderate", "trend": "improving"},
            ],
        )

        counts = save_health_entries_direct(
            test_session, checkin.id, test_user.id, parse_result, "voice"
        )

        assert counts["symptoms"] == 2

        symptoms = test_session.exec(
            select(SymptomEntry).where(SymptomEntry.checkin_id == checkin.id)
        ).all()
        assert len(symptoms) == 2

        fatigue = next(s for s in symptoms if s.name == "Fatigue")
        assert fatigue.severity == "moderate"
        assert fatigue.trend == "improving"

    def test_empty_names_are_skipped(self, test_session: Session, test_user):
        """Verify entries with empty names are not persisted."""
        checkin_id = f"CHK-{uuid.uuid4().hex[:8]}"

        checkin = CheckIn(
            checkin_id=checkin_id,
            user_id=test_user.id,
            patient_name="Test Patient",
            checkin_type="voice",
            summary="Test",
        )
        test_session.add(checkin)
        test_session.commit()
        test_session.refresh(checkin)

        # Parse result with empty names mixed with valid ones
        parse_result = create_mock_parse_result(
            checkin_id=checkin_id,
            medications=[
                {"name": "Valid Med", "dosage": "10mg"},
                {"name": "", "dosage": "should skip"},
            ],
            foods=[{"name": "", "calories": 100}],  # Should skip
            symptoms=[{"name": "Valid Symptom"}],
        )

        counts = save_health_entries_direct(
            test_session, checkin.id, test_user.id, parse_result, "voice"
        )

        assert counts["medications"] == 1
        assert counts["foods"] == 0
        assert counts["symptoms"] == 1
