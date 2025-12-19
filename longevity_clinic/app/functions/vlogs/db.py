"""Database sync operations for vlogs CDC pipeline.

Key functions:
- sync_raw_log_to_db: Sync raw call log + transcript to DB (CDC step 1-2)
- update_call_log_metrics: Process call log with LLM and create CheckIn + health entries (CDC step 3-4)
- create_checkin_with_health_data: Create CheckIn from voice/text input with health extraction
"""

import json
from datetime import datetime, timezone
from typing import Optional

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import VlogsConfig, get_logger
from longevity_clinic.app.data.model import (
    CallLog,
    CallSummary,  # Kept for backward compat, deprecated
    CallTranscript,
    CheckIn,
    FoodLogEntry,
    MedicationEntry,
    SymptomEntry,
    User,
)
from longevity_clinic.app.data.process_schema import CallLogsOutput, CheckInSummary
from longevity_clinic.app.data.state_schemas import CallLogEntry, TranscriptSummary

from .utils import get_medications, json_dumps_or_none, parse_datetime, parse_phone

logger = get_logger("longevity_clinic.vlogs.db")


def get_processed_call_ids_sync() -> set[str]:
    """Get set of call_ids already in database."""
    with rx.session() as session:
        return set(session.exec(select(CallLog.call_id)).all())


def get_unprocessed_call_logs_sync() -> list[CallLog]:
    """Get call logs that haven't been LLM-processed yet."""
    with rx.session() as session:
        return list(
            session.exec(
                select(CallLog).where(CallLog.processed_to_metrics == False)
            ).all()
        )


def reset_all_processed_to_metrics_sync() -> int:
    """Reset all call logs' processed_to_metrics to False.

    Returns the number of records updated.
    """
    try:
        with rx.session() as session:
            call_logs = session.exec(select(CallLog)).all()
            count = 0
            for call_log in call_logs:
                if call_log.processed_to_metrics:
                    call_log.processed_to_metrics = False
                    session.add(call_log)
                    count += 1
            session.commit()
            logger.info("Reset %d call logs' processed_to_metrics to False", count)
            return count
    except Exception as e:
        logger.error("Failed to reset processed_to_metrics: %s", e)
        return 0


def mark_call_log_processed_sync(call_log_id: int) -> bool:
    """Mark a call log as processed for metrics."""
    try:
        with rx.session() as session:
            if call_log := session.get(CallLog, call_log_id):
                call_log.processed_to_metrics = True
                session.add(call_log)
                session.commit()
                return True
        return False
    except Exception as e:
        logger.error("Failed to mark call_log %d as processed: %s", call_log_id, e)
        return False


def get_user_by_phone_sync(phone: str) -> Optional[int]:
    """Get user_id by phone number."""
    with rx.session() as session:
        if user := session.exec(select(User).where(User.phone == phone)).first():
            return user.id
        return None


def get_transcript_for_call_log(call_log_id: int) -> Optional[str]:
    """Get transcript text for a call log."""
    with rx.session() as session:
        if record := session.exec(
            select(CallTranscript).where(CallTranscript.call_log_id == call_log_id)
        ).first():
            return record.raw_transcript
        return None


def sync_raw_log_to_db(log: CallLogEntry) -> Optional[int]:
    """Sync raw call log and transcript to DB (without metrics)."""
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


def sync_single_to_db(
    log: CallLogEntry,
    output: CallLogsOutput,
    summary: TranscriptSummary,
    config: VlogsConfig,
) -> Optional[int]:
    """Sync a single processed call log to database.

    DEPRECATED: Use sync_raw_log_to_db + update_call_log_metrics instead.

    This function combines raw sync and processing in one step.
    The preferred approach is the CDC pattern:
    1. sync_raw_log_to_db() - sync raw call log
    2. update_call_log_metrics() - process with LLM later

    Returns the call_log_id if successful.
    """
    # First sync raw log
    call_log_id = sync_raw_log_to_db(log)
    if not call_log_id:
        # May already exist, try to find it
        call_id = log.get("call_id", "")
        with rx.session() as session:
            existing = session.exec(
                select(CallLog).where(CallLog.call_id == call_id)
            ).first()
            if existing:
                call_log_id = existing.id
            else:
                return None

    # Then process with LLM output
    llm_model = config.llm_model if config.extract_with_llm else None
    if update_call_log_metrics(call_log_id, output, llm_model or ""):
        return call_log_id
    return None


def update_call_log_metrics(
    call_log_id: int, output: CallLogsOutput, llm_model: str
) -> bool:
    """Process call log with LLM output: create/update CheckIn and health entries.

    This is the main processing function for call logs. It:
    1. Creates or updates a CheckIn record with processing metadata
    2. Creates normalized health entries (medications, food, symptoms)
    3. Marks the call log as processed

    Args:
        call_log_id: Database ID of the call log
        output: LLM-extracted CallLogsOutput with checkin and health data
        llm_model: Name of the LLM model used for extraction

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
                    "CallLogsOutput.checkin is None for call_log %d", call_log_id
                )
                return False

            # Prepare data with safe defaults
            summary_text = checkin_data.summary or ""
            key_topics = checkin_data.key_topics or []
            sentiment = checkin_data.sentiment or "neutral"
            medications = get_medications(output)
            symptoms = getattr(output, "symptom_entries", []) or []
            food_entries = output.food_entries or []
            now = datetime.now(timezone.utc)

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
                existing_checkin.has_medications = output.has_medications
                existing_checkin.has_nutrition = output.has_nutrition
                existing_checkin.has_symptoms = getattr(output, "has_symptoms", False)
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
                    has_medications=output.has_medications,
                    has_nutrition=output.has_nutrition,
                    has_symptoms=getattr(output, "has_symptoms", False),
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
                "call_log_id": call_log_id,
                "checkin_id": checkin_db_id,
            }

            for med in medications:
                session.add(
                    MedicationEntry(
                        **entry_base,
                        source="call_log",
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
                        source="call_log",
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
                        source="call_log",
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


def create_checkin_with_health_data(
    user_id: int,
    patient_name: str,
    checkin_type: str,
    raw_content: str,
    output: CallLogsOutput,
    llm_model: Optional[str] = None,
) -> Optional[int]:
    """Create a CheckIn with associated health entries from voice/text input.

    This function is used for manual/voice check-ins (not call logs).
    It creates a CheckIn record and linked health entries in a single transaction.

    Args:
        user_id: Database user ID
        patient_name: Patient's display name
        checkin_type: "voice" or "text"
        raw_content: Original transcript/text
        output: LLM-extracted CallLogsOutput with checkin and health data
        llm_model: Name of the LLM model used (if any)

    Returns:
        The CheckIn database ID if successful, None otherwise
    """
    try:
        with rx.session() as session:
            checkin_data = output.checkin
            now = datetime.now(timezone.utc)

            # Prepare data
            summary_text = checkin_data.summary or raw_content[:500]
            key_topics = checkin_data.key_topics or []
            sentiment = checkin_data.sentiment or "neutral"
            medications = get_medications(output)
            symptoms = getattr(output, "symptom_entries", []) or []
            food_entries = output.food_entries or []

            # Create CheckIn
            checkin = CheckIn(
                checkin_id=checkin_data.id,
                patient_name=patient_name,
                checkin_type=checkin_type,
                summary=summary_text,
                raw_content=raw_content,
                health_topics=json.dumps(key_topics),
                sentiment=sentiment,
                has_medications=output.has_medications,
                has_nutrition=output.has_nutrition,
                has_symptoms=getattr(output, "has_symptoms", False),
                is_processed=True,
                llm_model=llm_model,
                processed_at=now,
                status="pending",
                timestamp=now,
                user_id=user_id,
                call_log_id=None,  # Not from a call
            )
            session.add(checkin)
            session.flush()
            checkin_db_id = checkin.id

            # Create health entries linked to CheckIn
            entry_base = {
                "user_id": user_id,
                "call_log_id": None,
                "checkin_id": checkin_db_id,
            }

            for med in medications:
                session.add(
                    MedicationEntry(
                        **entry_base,
                        source=checkin_type,
                        mentioned_at=now,
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
                        source=checkin_type,
                        logged_at=now,
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
                        source=checkin_type,
                        reported_at=now,
                        name=sym.name,
                        severity=sym.severity,
                        frequency=sym.frequency,
                        trend=sym.trend,
                    )
                )

            session.commit()
            logger.info(
                "Created CheckIn %d (%s): %d meds, %d foods, %d symptoms",
                checkin_db_id,
                checkin_type,
                len(medications),
                len(food_entries),
                len(symptoms),
            )
            return checkin_db_id

    except Exception as e:
        logger.error("Failed to create checkin: %s", e)
        return None
