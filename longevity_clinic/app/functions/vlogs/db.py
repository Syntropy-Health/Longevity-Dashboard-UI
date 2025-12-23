"""Database operations for vlogs CDC pipeline."""

import json
from datetime import UTC, datetime

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.model import (
    CallLog,
    CallTranscript,
    CheckIn,
    FoodLogEntry,
    MedicationEntry,
    SymptomEntry,
    User,
)
from longevity_clinic.app.data.process_schema import MetricLogsOutput
from longevity_clinic.app.data.state_schemas import CallLogEntry

from .utils import get_medications, parse_datetime, parse_phone

logger = get_logger("longevity_clinic.vlogs.db")


def get_processed_call_ids_sync() -> set[str]:
    """Get call_ids already in DB."""
    with rx.session() as session:
        return set(session.exec(select(CallLog.call_id)).all())


def get_unprocessed_call_logs_sync() -> list[CallLog]:
    """Get call logs not yet LLM-processed."""
    with rx.session() as session:
        return list(
            session.exec(select(CallLog).where(not CallLog.processed_to_metrics)).all()
        )


def reset_all_processed_to_metrics_sync() -> int:
    """Reset all processed_to_metrics flags to False. Returns count updated."""
    try:
        with rx.session() as session:
            call_logs = session.exec(select(CallLog)).all()
            count = sum(1 for c in call_logs if c.processed_to_metrics)
            for c in call_logs:
                if c.processed_to_metrics:
                    c.processed_to_metrics = False
                    session.add(c)
            session.commit()
            logger.info("Reset %d call logs for reprocessing", count)
            return count
    except Exception as e:
        logger.error("Failed to reset processed_to_metrics: %s", e)
        return 0


def mark_call_log_processed_sync(call_log_id: int) -> bool:
    """Mark call log as processed (processed_to_metrics=True)."""
    try:
        with rx.session() as session:
            if call_log := session.get(CallLog, call_log_id):
                call_log.processed_to_metrics = True
                session.add(call_log)
                session.commit()
                logger.debug("Marked call_log %d as processed", call_log_id)
                return True
        return False
    except Exception as e:
        logger.error("Failed to mark call_log %d as processed: %s", call_log_id, e)
        return False


def get_user_by_phone_sync(phone: str) -> int | None:
    """Get user_id by phone."""
    with rx.session() as session:
        if user := session.exec(select(User).where(User.phone == phone)).first():
            return user.id
        return None


def get_transcript_for_call_log(call_log_id: int) -> str | None:
    """Get transcript for a call log."""
    with rx.session() as session:
        if record := session.exec(
            select(CallTranscript).where(CallTranscript.call_log_id == call_log_id)
        ).first():
            return record.raw_transcript
        return None


def sync_raw_log_to_db(log: CallLogEntry) -> int | None:
    """Sync raw call log + transcript to DB table CallLog and CallTranscript. Returns call_log_id or None."""
    call_id = log.get("call_id", "")
    if not call_id:
        return None

    try:
        with rx.session() as session:
            # Skip if exists
            if session.exec(select(CallLog).where(CallLog.call_id == call_id)).first():
                return None

            # Extract fields
            phone = parse_phone(log.get("caller_phone", ""))
            user_id = get_user_by_phone_sync(phone)
            started_at = parse_datetime(log.get("call_date", ""))
            transcript_text = log.get("full_transcript", "")

            # 1. CallLog
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

            # 2. CallTranscript
            session.add(
                CallTranscript(
                    call_log_id=call_log_id,
                    call_id=call_id,
                    raw_transcript=transcript_text,
                    language="en",
                )
            )

            session.commit()
            logger.info("Synced raw call log %s (id=%d)", call_id, call_log_id)
            return call_log_id
    except Exception as e:
        logger.error("Failed to sync raw call %s: %s", call_id, e)
        return None


def update_call_log_metrics(
    call_log_id: int, output: MetricLogsOutput, llm_model: str
) -> bool:
    """Process call log: create/update CheckIn + health entries, mark as processed.

    Called by VlogsAgent.process_unprocessed_logs() during CDC pipeline.

    Database Tables Updated:
    - checkins: CheckIn record linked to call_log_id
    - medication_entries: MedicationEntry records from output.medications_entries
    - food_log_entries: FoodLogEntry records from output.food_entries
    - symptom_entries: SymptomEntry records from output.symptom_entries
    - call_logs: Sets processed_to_metrics=True

    Args:
        call_log_id: Database ID of the CallLog to process
        output: MetricLogsOutput from LLM extraction
        llm_model: Name of LLM model used for extraction

    Returns:
        True if successful, False otherwise
    """
    try:
        with rx.session() as session:
            call_log = session.get(CallLog, call_log_id)
            if not call_log:
                logger.error("CallLog %d not found for update", call_log_id)
                return False

            # Defensive check: ensure checkin exists in output
            checkin_data = output.checkin
            if checkin_data is None:
                logger.error(
                    "MetricLogsOutput.checkin is None for call_log %d", call_log_id
                )
                return False

            # Prepare data with safe defaults
            summary_text = checkin_data.summary or ""
            key_topics = checkin_data.key_topics or []
            sentiment = checkin_data.sentiment or "neutral"
            medications = get_medications(output)
            symptoms = getattr(output, "symptom_entries", []) or []
            food_entries = output.food_entries or []
            now = datetime.now(UTC)

            # Get transcript for raw_content
            transcript_text = (
                session.exec(
                    select(CallTranscript.raw_transcript).where(
                        CallTranscript.call_log_id == call_log_id
                    )
                ).first()
                or ""
            )

            # Check if CheckIn exists for this call
            existing_checkin = session.exec(
                select(CheckIn).where(CheckIn.call_log_id == call_log_id)
            ).first()

            if existing_checkin:
                # Update existing CheckIn with LLM results
                existing_checkin.summary = summary_text
                existing_checkin.health_topics = json.dumps(key_topics)
                existing_checkin.sentiment = sentiment
                existing_checkin.is_processed = True
                existing_checkin.llm_model = llm_model
                existing_checkin.processed_at = now
                existing_checkin.updated_at = now
                session.add(existing_checkin)
                checkin_db_id = existing_checkin.id
            else:
                # Create new CheckIn
                checkin = CheckIn(
                    checkin_id=checkin_data.id or f"call_{call_log.call_id}",
                    patient_name=checkin_data.patient_name or "",
                    checkin_type="call",
                    summary=summary_text,
                    raw_content=transcript_text,
                    health_topics=json.dumps(key_topics),
                    sentiment=sentiment,
                    is_processed=True,
                    llm_model=llm_model,
                    processed_at=now,
                    status="pending",
                    timestamp=call_log.started_at,
                    user_id=call_log.user_id,
                    call_log_id=call_log_id,
                )
                session.add(checkin)
                session.flush()
                checkin_db_id = checkin.id

            # Create normalized health entries (linked to CheckIn)
            entry_base = {
                "user_id": call_log.user_id,
                "checkin_id": checkin_db_id,
            }

            for med in medications:
                session.add(
                    MedicationEntry(
                        **entry_base,
                        source="call",
                        mentioned_at=call_log.started_at,
                        name=med.name,
                        dosage=med.dosage,
                        frequency=med.frequency,
                        status=med.status,
                        adherence_rate=med.adherence_rate,
                    )
                )

            for food in food_entries:
                session.add(
                    FoodLogEntry(
                        **entry_base,
                        source="call",
                        logged_at=call_log.started_at,
                        consumed_at=food.time,
                        name=food.name,
                        calories=food.calories,
                        protein=food.protein,
                        carbs=food.carbs,
                        fat=food.fat,
                        meal_type=food.meal_type,
                    )
                )

            for sym in symptoms:
                session.add(
                    SymptomEntry(
                        **entry_base,
                        source="call",
                        reported_at=call_log.started_at,
                        name=sym.name,
                        severity=sym.severity,
                        frequency=sym.frequency,
                        trend=sym.trend,
                    )
                )

            # Mark call log as processed
            call_log.processed_to_metrics = True
            session.add(call_log)

            session.commit()
            logger.info(
                "Processed call_log %d: CheckIn=%d, %d meds, %d foods, %d symptoms",
                call_log_id,
                checkin_db_id,
                len(medications),
                len(food_entries),
                len(symptoms),
            )
            return True

    except Exception as e:
        logger.error("Failed to update call_log %d metrics: %s", call_log_id, e)
        return False
