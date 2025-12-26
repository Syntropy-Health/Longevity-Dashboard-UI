"""Database operations for vlogs CDC pipeline."""

import json
from datetime import UTC, datetime
from typing import NamedTuple

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.db import (
    CallLog,
    CallTranscript,
    CheckIn,
    FoodLogEntry,
    MedicationEntry,
    SymptomEntry,
)
from longevity_clinic.app.data.schemas.llm import MetricLogsOutput
from longevity_clinic.app.data.schemas.state import CallLogEntry
from longevity_clinic.app.functions.db_utils import (
    create_user_sync,
    get_user_by_phone_sync as db_get_user_by_phone,
)

from .utils import get_medications, parse_datetime, parse_phone

logger = get_logger("longevity_clinic.vlogs.db")


# =============================================================================
# Query Functions
# =============================================================================


def get_latest_call_date_sync(phone_number: str | None = None) -> str | None:
    """Get the most recent call_date from DB for smart incremental fetch.

    Args:
        phone_number: Filter by phone (None = all logs)

    Returns:
        ISO date string of most recent call, or None if no calls exist
    """
    with rx.session() as s:
        query = select(CallLog.started_at).order_by(CallLog.started_at.desc()).limit(1)
        if phone_number:
            query = query.where(CallLog.phone_number == phone_number)
        result = s.exec(query).first()
        if result:
            return result.isoformat()
    return None


def get_processed_call_ids_sync() -> set[str]:
    """Get call_ids already in DB."""
    with rx.session() as s:
        return set(s.exec(select(CallLog.call_id)).all())


def get_unprocessed_call_logs_sync() -> list[CallLog]:
    """Get call logs not yet LLM-processed."""
    with rx.session() as s:
        return list(
            s.exec(select(CallLog).where(CallLog.processed_to_metrics.is_(False))).all()
        )


def claim_unprocessed_call_logs_sync(limit: int = 10) -> list[CallLog]:
    """Atomically claim unprocessed call logs for processing.

    This prevents race conditions by marking logs as processed BEFORE
    returning them, ensuring no other process can claim the same logs.

    Args:
        limit: Maximum number of logs to claim

    Returns:
        List of CallLog objects that have been claimed (marked processed)
    """
    try:
        with rx.session() as s:
            # Find unprocessed logs
            unprocessed = list(
                s.exec(
                    select(CallLog)
                    .where(CallLog.processed_to_metrics.is_(False))
                    .limit(limit)
                ).all()
            )

            if not unprocessed:
                return []

            # Mark them as processed immediately to prevent re-claiming
            for log in unprocessed:
                log.processed_to_metrics = True
                s.add(log)
            s.commit()

            # Refresh to get updated state
            for log in unprocessed:
                s.refresh(log)

            logger.debug("Claimed %d call logs for processing", len(unprocessed))
            return unprocessed
    except Exception as e:
        logger.error("Failed to claim unprocessed logs: %s", e)
        return []


def unclaim_call_log_sync(call_log_id: int) -> bool:
    """Unclaim a call log (set processed_to_metrics back to False).

    Used when LLM processing fails and we want to retry later.
    """
    try:
        with rx.session() as s:
            if log := s.get(CallLog, call_log_id):
                log.processed_to_metrics = False
                s.add(log)
                s.commit()
                return True
        return False
    except Exception as e:
        logger.error("Failed to unclaim call_log %d: %s", call_log_id, e)
        return False


def get_or_create_user_by_phone(
    phone: str, customer_name: str | None = None
) -> int | None:
    """Get user_id by phone, or create new user if name is provided.

    Args:
        phone: Phone number (E.164 format)
        customer_name: Customer name from API (used to create user if not found)

    Returns:
        User ID or None if no phone and no name provided
    """

    if not phone:
        return None

    # Try to find existing user
    if user := db_get_user_by_phone(phone):
        return user.id

    # No user found - create one if we have a name
    if customer_name:
        new_user = create_user_sync(name=customer_name, phone=phone, role="patient")
        if new_user:
            logger.info(
                "Created user from API caller_phone: id=%d, name=%s, phone=%s",
                new_user.id,
                customer_name,
                phone,
            )
            return new_user.id

    # No name available, return None (caller will need to handle)
    logger.warning(
        "No user found for phone %s and no customer_name to create one", phone
    )
    return None


def get_transcript_for_call_log(call_log_id: int) -> str | None:
    """Get transcript for a call log."""
    with rx.session() as s:
        if r := s.exec(
            select(CallTranscript.raw_transcript).where(
                CallTranscript.call_log_id == call_log_id
            )
        ).first():
            return r
    return None


# =============================================================================
# Mutation Functions
# =============================================================================


def reset_all_processed_to_metrics_sync() -> int:
    """Reset all processed_to_metrics flags to False."""
    try:
        with rx.session() as s:
            logs = s.exec(
                select(CallLog).where(CallLog.processed_to_metrics.is_(True))
            ).all()
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


def _extract_caller_info(caller_phone_raw) -> tuple[str, str | None]:
    """Extract phone number and customer name from caller_phone field.

    Args:
        caller_phone_raw: Either a string (phone number) or CallerPhoneExpanded dict

    Returns:
        Tuple of (phone_number, customer_name or None)
    """
    if isinstance(caller_phone_raw, dict):
        phone = caller_phone_raw.get("phone_number", "")
        customer_name = caller_phone_raw.get("customer_name")
        return phone, customer_name
    return caller_phone_raw or "", None


def sync_raw_log_to_db(log: CallLogEntry) -> int | None:
    """Sync raw call log + transcript to DB. Returns call_log_id or None.

    If caller_phone is expanded (dict with customer_name), will create a new
    user if one doesn't exist for that phone number.
    """
    if not (call_id := log.get("call_id", "")):
        return None

    try:
        with rx.session() as s:
            # Check existing
            if s.exec(select(CallLog.id).where(CallLog.call_id == call_id)).first():
                return None

            # Extract phone and customer name from caller_phone
            phone, customer_name = _extract_caller_info(log.get("caller_phone", ""))
            phone = parse_phone(phone) if phone else ""

            # Get or create user - will create if customer_name is available
            user_id = get_or_create_user_by_phone(phone, customer_name)

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
            s.add(
                CallTranscript(
                    call_log_id=call_log.id,
                    call_id=call_id,
                    raw_transcript=log.get("full_transcript", ""),
                    language="en",
                )
            )
            s.commit()
            logger.info(
                "Synced call %s (id=%d, user=%s)", call_id, call_log.id, user_id
            )
            return call_log.id
    except Exception as e:
        logger.error("Failed to sync call %s: %s", call_id, e)
        return None


def update_call_log_metrics(
    call_log_id: int, output: MetricLogsOutput, llm_model: str
) -> bool:
    """Process call log: create/update CheckIn + health entries, mark processed."""
    try:
        with rx.session() as s:
            if not (call_log := s.get(CallLog, call_log_id)) or not (
                chk := output.checkin
            ):
                return False

            now = datetime.now(UTC)
            transcript = (
                s.exec(
                    select(CallTranscript.raw_transcript).where(
                        CallTranscript.call_log_id == call_log_id
                    )
                ).first()
                or ""
            )

            # Upsert CheckIn
            if existing := s.exec(
                select(CheckIn).where(CheckIn.call_log_id == call_log_id)
            ).first():
                existing.summary, existing.health_topics = (
                    chk.summary or "",
                    json.dumps(chk.key_topics or []),
                )
                existing.sentiment, existing.is_processed = (
                    chk.sentiment or "UNKNOWN",
                    True,
                )
                existing.llm_model, existing.processed_at, existing.updated_at = (
                    llm_model,
                    now,
                    now,
                )
                s.add(existing)
                checkin_id = existing.id
            else:
                new = CheckIn(
                    checkin_id=chk.id or f"call_{call_log.call_id}",
                    patient_name=chk.patient_name or "",
                    checkin_type="call",
                    summary=chk.summary or "",
                    raw_content=transcript,
                    health_topics=json.dumps(chk.key_topics or []),
                    sentiment=chk.sentiment or "UNKNOWN",
                    is_processed=True,
                    llm_model=llm_model,
                    processed_at=now,
                    status="pending",
                    timestamp=call_log.started_at,
                    user_id=call_log.user_id,
                    call_log_id=call_log_id,
                )
                s.add(new)
                s.flush()
                checkin_id = new.id

            # Batch health entries
            base = {"user_id": call_log.user_id, "checkin_id": checkin_id}
            for m in get_medications(output):
                s.add(
                    MedicationEntry(
                        **base,
                        source="call",
                        taken_at=call_log.started_at,
                        name=m.name,
                        dosage=m.dosage,
                        notes=m.notes,
                    )
                )
            for f in output.food_entries or []:
                s.add(
                    FoodLogEntry(
                        **base,
                        source="call",
                        logged_at=call_log.started_at,
                        consumed_at=f.time,
                        name=f.name,
                        calories=f.calories,
                        protein=f.protein,
                        carbs=f.carbs,
                        fat=f.fat,
                        meal_type=f.meal_type,
                    )
                )
            for sym in output.symptom_entries or []:
                s.add(
                    SymptomEntry(
                        **base,
                        source="call",
                        reported_at=call_log.started_at,
                        name=sym.name,
                        severity=sym.severity,
                        frequency=sym.frequency,
                        trend=sym.trend,
                    )
                )

            call_log.processed_to_metrics = True
            s.add(call_log)
            s.commit()

            logger.info(
                "Processed call_log %d: %d meds, %d foods, %d symptoms",
                call_log_id,
                len(get_medications(output)),
                len(output.food_entries or []),
                len(output.symptom_entries or []),
            )
            return True
    except Exception as e:
        logger.error("Failed to update call_log %d: %s", call_log_id, e)
        return False
