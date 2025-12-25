"""Database operations for vlogs CDC pipeline."""

import json
from datetime import UTC, datetime
from typing import NamedTuple

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger, process_config
from longevity_clinic.app.data.schemas.db import (
    CallLog,
    CallTranscript,
    CheckIn,
    FoodLogEntry,
    MedicationEntry,
    SymptomEntry,
    User,
)
from longevity_clinic.app.data.schemas.llm import MetricLogsOutput
from longevity_clinic.app.data.schemas.state import CallLogEntry

from .utils import get_medications, parse_datetime, parse_phone

logger = get_logger("longevity_clinic.vlogs.db")


# =============================================================================
# Query Functions
# =============================================================================


def get_processed_call_ids_sync() -> set[str]:
    """Get call_ids already in DB."""
    with rx.session() as s:
        return set(s.exec(select(CallLog.call_id)).all())


def get_unprocessed_call_logs_sync() -> list[CallLog]:
    """Get call logs not yet LLM-processed."""
    with rx.session() as s:
        return list(s.exec(select(CallLog).where(CallLog.processed_to_metrics == False)).all())  # noqa: E712


def get_user_by_phone_sync(phone: str) -> int | None:
    """Get user_id by phone, returns ghost_user_id if not found."""
    if not phone:
        return process_config.ghost_user_id
    with rx.session() as s:
        if u := s.exec(select(User).where(User.phone == phone)).first():
            return u.id
    return process_config.ghost_user_id


def get_transcript_for_call_log(call_log_id: int) -> str | None:
    """Get transcript for a call log."""
    with rx.session() as s:
        if r := s.exec(select(CallTranscript.raw_transcript).where(CallTranscript.call_log_id == call_log_id)).first():
            return r
    return None


# =============================================================================
# Mutation Functions
# =============================================================================


def reset_all_processed_to_metrics_sync() -> int:
    """Reset all processed_to_metrics flags to False."""
    try:
        with rx.session() as s:
            logs = s.exec(select(CallLog).where(CallLog.processed_to_metrics == True)).all()  # noqa: E712
            for log in logs:
                log.processed_to_metrics = False
                s.add(log)
            s.commit()
            logger.info("Reset %d call logs for reprocessing", len(logs))
            return len(logs)
    except Exception as e:
        logger.error("Failed to reset processed_to_metrics: %s", e)
        return 0


def mark_call_log_processed_sync(call_log_id: int) -> bool:
    """Mark call log as processed."""
    try:
        with rx.session() as s:
            if log := s.get(CallLog, call_log_id):
                log.processed_to_metrics = True
                s.add(log)
                s.commit()
                return True
        return False
    except Exception as e:
        logger.error("Failed to mark call_log %d processed: %s", call_log_id, e)
        return False


class SyncResult(NamedTuple):
    """Result of sync_raw_log_to_db."""
    call_log_id: int | None
    is_new: bool


def sync_raw_log_to_db(log: CallLogEntry) -> int | None:
    """Sync raw call log + transcript to DB. Returns call_log_id or None."""
    if not (call_id := log.get("call_id", "")):
        return None

    try:
        with rx.session() as s:
            # Check existing
            if s.exec(select(CallLog.id).where(CallLog.call_id == call_id)).first():
                return None

            phone = parse_phone(log.get("caller_phone", ""))
            user_id = get_user_by_phone_sync(phone)

            # Create CallLog
            call_log = CallLog(
                call_id=call_id,
                phone_number=phone,
                started_at=parse_datetime(log.get("call_date", "")),
                duration_seconds=log.get("duration", 0),
                direction="inbound",
                status="completed",
                processed_to_metrics=False,
                user_id=user_id,
            )
            s.add(call_log)
            s.flush()

            # Create CallTranscript
            s.add(CallTranscript(
                call_log_id=call_log.id,
                call_id=call_id,
                raw_transcript=log.get("full_transcript", ""),
                language="en",
            ))
            s.commit()
            logger.info("Synced call %s (id=%d, user=%s)", call_id, call_log.id, user_id)
            return call_log.id
    except Exception as e:
        logger.error("Failed to sync call %s: %s", call_id, e)
        return None


def update_call_log_metrics(call_log_id: int, output: MetricLogsOutput, llm_model: str) -> bool:
    """Process call log: create/update CheckIn + health entries, mark processed."""
    try:
        with rx.session() as s:
            if not (call_log := s.get(CallLog, call_log_id)) or not (chk := output.checkin):
                return False

            now = datetime.now(UTC)
            transcript = s.exec(select(CallTranscript.raw_transcript).where(
                CallTranscript.call_log_id == call_log_id)).first() or ""

            # Upsert CheckIn
            if existing := s.exec(select(CheckIn).where(CheckIn.call_log_id == call_log_id)).first():
                existing.summary, existing.health_topics = chk.summary or "", json.dumps(chk.key_topics or [])
                existing.sentiment, existing.is_processed = chk.sentiment or "neutral", True
                existing.llm_model, existing.processed_at, existing.updated_at = llm_model, now, now
                s.add(existing)
                checkin_id = existing.id
            else:
                new = CheckIn(
                    checkin_id=chk.id or f"call_{call_log.call_id}", patient_name=chk.patient_name or "",
                    checkin_type="call", summary=chk.summary or "", raw_content=transcript,
                    health_topics=json.dumps(chk.key_topics or []), sentiment=chk.sentiment or "neutral",
                    is_processed=True, llm_model=llm_model, processed_at=now, status="pending",
                    timestamp=call_log.started_at, user_id=call_log.user_id, call_log_id=call_log_id,
                )
                s.add(new)
                s.flush()
                checkin_id = new.id

            # Batch health entries
            base = {"user_id": call_log.user_id, "checkin_id": checkin_id}
            for m in get_medications(output):
                s.add(MedicationEntry(**base, source="call", mentioned_at=call_log.started_at,
                    name=m.name, dosage=m.dosage, frequency=m.frequency, status=m.status, adherence_rate=m.adherence_rate))
            for f in output.food_entries or []:
                s.add(FoodLogEntry(**base, source="call", logged_at=call_log.started_at, consumed_at=f.time,
                    name=f.name, calories=f.calories, protein=f.protein, carbs=f.carbs, fat=f.fat, meal_type=f.meal_type))
            for sym in output.symptom_entries or []:
                s.add(SymptomEntry(**base, source="call", reported_at=call_log.started_at,
                    name=sym.name, severity=sym.severity, frequency=sym.frequency, trend=sym.trend))

            call_log.processed_to_metrics = True
            s.add(call_log)
            s.commit()

            logger.info("Processed call_log %d: %d meds, %d foods, %d symptoms",
                call_log_id, len(get_medications(output)), len(output.food_entries or []), len(output.symptom_entries or []))
            return True
    except Exception as e:
        logger.error("Failed to update call_log %d: %s", call_log_id, e)
        return False
