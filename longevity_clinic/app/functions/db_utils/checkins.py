"""Check-in database operations."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.model import CheckIn, CallTranscript

logger = get_logger("longevity_clinic.db_utils.checkins")


def get_checkins_sync(
    status: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Get check-ins from database."""
    try:
        with rx.session() as session:
            query = (
                select(CheckIn, CallTranscript)
                .join(
                    CallTranscript,
                    CheckIn.id == CallTranscript.call_log_id,
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
) -> List[Dict[str, Any]]:
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
) -> Optional[Dict[str, Any]]:
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
            checkin.reviewed_at = datetime.now(timezone.utc)
            checkin.updated_at = datetime.now(timezone.utc)

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
    user_id: Optional[int] = None,
    raw_content: Optional[str] = None,
    health_topics: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Create a new check-in."""
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
                "patient_name": checkin.patient_name,
                "summary": checkin.summary,
                "status": checkin.status,
            }
    except Exception as e:
        logger.error("Failed to create checkin: %s", e)
        return None
