"""Check-in database operations."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.db import (
    CallTranscript,
    CheckIn,
    FoodLogEntry as FoodLogEntryDB,
    MedicationEntry as MedicationEntryDB,
    SymptomEntry as SymptomEntryDB,
)

if TYPE_CHECKING:
    from longevity_clinic.app.data.schemas.llm import MetricLogsOutput

logger = get_logger("longevity_clinic.db_utils.checkins")


def get_checkins_sync(
    status: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Get check-ins from database."""
    try:
        with rx.session() as session:
            query = (
                select(CheckIn, CallTranscript)
                .join(
                    CallTranscript,
                    CheckIn.call_log_id == CallTranscript.call_log_id,
                    isouter=True,
                )
                .order_by(CheckIn.timestamp.desc())
                .limit(limit)
            )

            if status and status != "all":
                query = query.where(CheckIn.status == status)

            results = session.exec(query).all()

            return [
                {
                    "id": c.checkin_id,
                    "patient_id": c.user_id or "unknown",
                    "patient_name": c.patient_name,
                    "type": c.checkin_type,
                    "summary": c.summary,
                    "raw_transcript": transcript.raw_transcript if transcript else "",
                    "timestamp": c.timestamp.isoformat() if c.timestamp else "",
                    "submitted_at": c.created_at.isoformat() if c.created_at else "",
                    "sentiment": "neutral",
                    "key_topics": [],
                    "status": c.status,
                    "provider_reviewed": c.provider_reviewed,
                    "reviewed_by": c.reviewed_by or "",
                    "reviewed_at": c.reviewed_at.isoformat() if c.reviewed_at else "",
                }
                for c, transcript in results
            ]
    except Exception as e:
        logger.error("Failed to get checkins: %s", e)
        return []


def get_checkins_for_user_sync(
    user_id: int,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Get check-ins for a specific user."""
    try:
        with rx.session() as session:
            checkins = session.exec(
                select(CheckIn)
                .where(CheckIn.user_id == user_id)
                .order_by(CheckIn.timestamp.desc())
                .limit(limit)
            ).all()

            return [
                {
                    "id": c.checkin_id,
                    "type": c.checkin_type,
                    "summary": c.summary,
                    "timestamp": c.timestamp.isoformat() if c.timestamp else "",
                    "status": c.status,
                }
                for c in checkins
            ]
    except Exception as e:
        logger.error("Failed to get checkins for user %s: %s", user_id, e)
        return []


def update_checkin_status_sync(
    checkin_id: str,
    status: str,
    reviewed_by: str,
) -> dict[str, Any] | None:
    """Update check-in status in database."""
    try:
        with rx.session() as session:
            checkin = session.exec(
                select(CheckIn).where(CheckIn.checkin_id == checkin_id)
            ).first()

            if not checkin:
                logger.warning("Check-in not found: %s", checkin_id)
                return None

            checkin.status = status
            checkin.provider_reviewed = True
            checkin.reviewed_by = reviewed_by
            checkin.reviewed_at = datetime.now(UTC)
            checkin.updated_at = datetime.now(UTC)

            session.add(checkin)
            session.commit()
            session.refresh(checkin)

            return {
                "id": checkin.checkin_id,
                "status": checkin.status,
                "reviewed_by": checkin.reviewed_by,
                "reviewed_at": checkin.reviewed_at.isoformat(),
            }
    except Exception as e:
        logger.error("Failed to update checkin %s: %s", checkin_id, e)
        return None


def create_checkin_sync(
    checkin_id: str,
    patient_name: str,
    summary: str,
    checkin_type: str = "manual",
    user_id: int | None = None,
    raw_content: str | None = None,
    health_topics: str | None = None,
) -> dict[str, Any] | None:
    """Create a new check-in.

    Returns dict with both external 'id' (checkin_id) and 'db_id' (PK)
    to avoid needing a separate query for the database ID.
    """
    try:
        with rx.session() as session:
            checkin = CheckIn(
                checkin_id=checkin_id,
                user_id=user_id,
                patient_name=patient_name,
                checkin_type=checkin_type,
                summary=summary,
                raw_content=raw_content,
                health_topics=health_topics,
                status="pending",
            )
            session.add(checkin)
            session.commit()
            session.refresh(checkin)

            return {
                "id": checkin.checkin_id,
                "db_id": checkin.id,  # Return DB PK to avoid extra query
                "patient_name": checkin.patient_name,
                "summary": checkin.summary,
                "status": checkin.status,
            }
    except Exception as e:
        logger.error("Failed to create checkin: %s", e)
        return None


def update_checkin_sync(
    checkin_id: str,
    summary: str | None = None,
    raw_content: str | None = None,
) -> bool:
    """Update check-in content (summary/raw_content)."""
    try:
        with rx.session() as session:
            checkin = session.exec(
                select(CheckIn).where(CheckIn.checkin_id == checkin_id)
            ).first()
            if not checkin:
                logger.warning("Check-in not found: %s", checkin_id)
                return False

            if summary is not None:
                checkin.summary = summary
            if raw_content is not None:
                checkin.raw_content = raw_content
            checkin.updated_at = datetime.now(UTC)

            session.add(checkin)
            session.commit()
            logger.info("Updated checkin %s", checkin_id)
            return True
    except Exception as e:
        logger.error("Failed to update checkin %s: %s", checkin_id, e)
        return False


def delete_checkin_sync(checkin_id: str) -> bool:
    """Delete a check-in by ID."""
    try:
        with rx.session() as session:
            checkin = session.exec(
                select(CheckIn).where(CheckIn.checkin_id == checkin_id)
            ).first()
            if not checkin:
                logger.warning("Check-in not found for deletion: %s", checkin_id)
                return False

            session.delete(checkin)
            session.commit()
            logger.info("Deleted checkin %s", checkin_id)
            return True
    except Exception as e:
        logger.error("Failed to delete checkin %s: %s", checkin_id, e)
        return False


def save_health_entries_sync(
    checkin_db_id: int,
    user_id: int | None,
    parse_result: MetricLogsOutput,
    source: str = "manual",
) -> dict[str, int]:
    """Save health entries (medications, food, symptoms) from LLM parse result.

    Persists extracted health data to normalized tables, linked to the CheckIn.
    Called after create_checkin_sync to complete the health data persistence.
    Uses batch add_all() for better performance.

    Args:
        checkin_db_id: The database ID of the CheckIn record (internal PK)
        user_id: The user's database ID
        parse_result: MetricLogsOutput from VlogsAgent.parse_checkin_with_health_data
        source: Source type for entries (manual, voice, call)

    Returns:
        Dict with counts: {"medications": N, "foods": N, "symptoms": N}
    """
    counts = {"medications": 0, "foods": 0, "symptoms": 0}
    now = datetime.now(UTC)
    entries: list = []  # Batch all entries for single add_all()

    try:
        # Build medication entries
        for med in parse_result.medications_entries:
            if not med.name:
                continue
            entries.append(
                MedicationEntryDB(
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
            )
            counts["medications"] += 1

        # Build food entries
        for food in parse_result.food_entries:
            if not food.name:
                continue
            entries.append(
                FoodLogEntryDB(
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
            )
            counts["foods"] += 1

        # Build symptom entries
        for sym in parse_result.symptom_entries:
            if not sym.name:
                continue
            entries.append(
                SymptomEntryDB(
                    user_id=user_id,
                    checkin_id=checkin_db_id,
                    name=sym.name,
                    severity=sym.severity or "",
                    frequency=sym.frequency or "",
                    trend=sym.trend or "stable",
                    source=source,
                    reported_at=now,
                )
            )
            counts["symptoms"] += 1

        # Batch insert all entries in single operation
        with rx.session() as session:
            if entries:
                session.add_all(entries)
            session.commit()

            logger.debug(
                "Saved health entries for checkin_id=%d: %d meds, %d foods, %d symptoms",
                checkin_db_id,
                counts["medications"],
                counts["foods"],
                counts["symptoms"],
            )
            return counts

    except Exception as e:
        logger.error(
            "Failed to save health entries for checkin %d: %s", checkin_db_id, e
        )
        return counts


def get_checkin_db_id_sync(checkin_id: str) -> int | None:
    """Get the database ID (PK) for a checkin by its external checkin_id."""
    try:
        with rx.session() as session:
            checkin = session.exec(
                select(CheckIn).where(CheckIn.checkin_id == checkin_id)
            ).first()
            return checkin.id if checkin else None
    except Exception as e:
        logger.error("Failed to get checkin db_id for %s: %s", checkin_id, e)
        return None
