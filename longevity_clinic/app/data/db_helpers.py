"""Database helper functions for common queries.

Provides sync and async wrappers for frequently used database operations.
These replace hardcoded demo data lookups with actual DB queries.
"""

from __future__ import annotations

# Standard library
from typing import TYPE_CHECKING, Any, Dict, List, Optional

# Third-party
import reflex as rx
from sqlmodel import select

# Local application
from longevity_clinic.app.config import get_logger
from longevity_clinic.app.functions.utils import normalize_phone

from .model import BiomarkerDefinition, BiomarkerReading, CallLog, CheckIn, User

if TYPE_CHECKING:
    pass  # Add type-only imports here if needed

logger = get_logger("longevity_clinic.db_helpers")


# =============================================================================
# User Lookup Functions
# =============================================================================


def get_user_by_phone_sync(phone: str) -> Optional[User]:
    """Get user by phone number (sync version).

    Args:
        phone: Phone number (any format)

    Returns:
        User object or None if not found
    """
    if not phone:
        return None

    normalized = normalize_phone(phone)

    try:
        with rx.session() as session:
            # Try exact match first
            result = session.exec(select(User).where(User.phone == phone)).first()

            if result:
                return result

            # Try normalized comparison for all users with phones
            users = session.exec(select(User).where(User.phone.isnot(None))).all()

            for user in users:
                if user.phone and normalize_phone(user.phone) == normalized:
                    return user

            return None
    except Exception as e:
        logger.error("Failed to get user by phone %s: %s", phone, e)
        return None


def get_patient_name_by_phone(phone: str, fallback: str = "Unknown Patient") -> str:
    """Get patient name from phone number via database lookup.

    Args:
        phone: Phone number (any format)
        fallback: Default name if not found

    Returns:
        Patient name or fallback
    """
    user = get_user_by_phone_sync(phone)
    if user:
        return user.name
    return fallback if fallback != "Unknown Patient" else f"Patient ({phone})"


def get_user_by_external_id_sync(external_id: str) -> Optional[User]:
    """Get user by external ID (e.g., 'P001').

    Args:
        external_id: External user ID

    Returns:
        User object or None
    """
    try:
        with rx.session() as session:
            return session.exec(
                select(User).where(User.external_id == external_id)
            ).first()
    except Exception as e:
        logger.error("Failed to get user by external_id %s: %s", external_id, e)
        return None


def get_all_patients_sync() -> List[User]:
    """Get all patient users from database.

    Returns:
        List of User objects with role='patient'
    """
    try:
        with rx.session() as session:
            return list(session.exec(select(User).where(User.role == "patient")).all())
    except Exception as e:
        logger.error("Failed to get all patients: %s", e)
        return []


def get_phone_to_patient_map() -> Dict[str, str]:
    """Build phone-to-patient-name mapping from database.

    This replaces the hardcoded PHONE_TO_PATIENT dict.

    Returns:
        Dict mapping phone numbers to patient names
    """
    try:
        with rx.session() as session:
            users = session.exec(
                select(User).where(User.phone.isnot(None), User.role == "patient")
            ).all()

            return {user.phone: user.name for user in users if user.phone}
    except Exception as e:
        logger.error("Failed to build phone-to-patient map: %s", e)
        return {}


# =============================================================================
# Check-in Functions
# =============================================================================


def get_checkins_sync(
    status: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Get check-ins from database.

    Args:
        status: Filter by status ('pending', 'reviewed', 'flagged')
        limit: Maximum records to return

    Returns:
        List of check-in dicts in admin format
    """
    try:
        with rx.session() as session:
            query = select(CheckIn).order_by(CheckIn.timestamp.desc()).limit(limit)

            if status and status != "all":
                query = query.where(CheckIn.status == status)

            checkins = session.exec(query).all()

            return [
                {
                    "id": c.checkin_id,
                    "patient_id": c.user_id or "unknown",
                    "patient_name": c.patient_name,
                    "type": c.checkin_type,
                    "summary": c.summary,
                    "timestamp": c.timestamp.isoformat() if c.timestamp else "",
                    "submitted_at": c.created_at.isoformat() if c.created_at else "",
                    "sentiment": "neutral",
                    "key_topics": [],  # TODO: parse from health_topics JSON
                    "status": c.status,
                    "provider_reviewed": c.provider_reviewed,
                    "reviewed_by": c.reviewed_by or "",
                    "reviewed_at": c.reviewed_at.isoformat() if c.reviewed_at else "",
                }
                for c in checkins
            ]
    except Exception as e:
        logger.error("Failed to get checkins: %s", e)
        return []


def update_checkin_status_sync(
    checkin_id: str,
    status: str,
    reviewed_by: str,
) -> Optional[Dict[str, Any]]:
    """Update check-in status in database.

    Args:
        checkin_id: Check-in ID (external)
        status: New status
        reviewed_by: Reviewer name/ID

    Returns:
        Updated check-in dict or None on failure
    """
    from datetime import datetime, timezone

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


# =============================================================================
# Biomarker Functions
# =============================================================================


def get_biomarker_definitions_sync() -> List[Dict[str, Any]]:
    """Get all biomarker definitions from database.

    Returns:
        List of biomarker definition dicts
    """
    try:
        with rx.session() as session:
            defs = session.exec(select(BiomarkerDefinition)).all()
            return [
                {
                    "id": d.code,
                    "name": d.name,
                    "category": d.category,
                    "unit": d.unit,
                    "description": d.description,
                    "optimal_min": d.optimal_min,
                    "optimal_max": d.optimal_max,
                    "critical_min": d.critical_min,
                    "critical_max": d.critical_max,
                }
                for d in defs
            ]
    except Exception as e:
        logger.error("Failed to get biomarker definitions: %s", e)
        return []


def get_patient_biomarkers_sync(
    user_id: Optional[int] = None,
    external_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Get biomarkers with latest readings for a patient.

    Args:
        user_id: Database user ID
        external_id: External user ID (e.g., 'P001')

    Returns:
        List of biomarker dicts with current value and history
    """
    try:
        # Resolve user_id from external_id if needed
        if not user_id and external_id:
            user = get_user_by_external_id_sync(external_id)
            user_id = user.id if user else None

        if not user_id:
            logger.warning("get_patient_biomarkers_sync: No user_id provided")
            return []

        with rx.session() as session:
            # Get all definitions with their readings for this user
            defs = session.exec(select(BiomarkerDefinition)).all()

            result = []
            for d in defs:
                # Get readings for this biomarker, ordered by date
                readings = session.exec(
                    select(BiomarkerReading)
                    .where(
                        BiomarkerReading.user_id == user_id,
                        BiomarkerReading.biomarker_id == d.id,
                    )
                    .order_by(BiomarkerReading.measured_at.desc())
                ).all()

                if not readings:
                    continue

                latest = readings[0]
                history = [
                    {"date": r.measured_at.strftime("%b"), "value": r.value}
                    for r in reversed(readings[-6:])  # Last 6 readings
                ]

                result.append(
                    {
                        "id": d.code,
                        "name": d.name,
                        "category": d.category,
                        "unit": d.unit,
                        "description": d.description,
                        "optimal_min": d.optimal_min,
                        "optimal_max": d.optimal_max,
                        "critical_min": d.critical_min,
                        "critical_max": d.critical_max,
                        "current_value": latest.value,
                        "status": latest.status.capitalize(),
                        "trend": latest.trend,
                        "history": history,
                    }
                )

            return result
    except Exception as e:
        logger.error("Failed to get patient biomarkers: %s", e)
        return []


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "normalize_phone",
    "get_user_by_phone_sync",
    "get_patient_name_by_phone",
    "get_user_by_external_id_sync",
    "get_all_patients_sync",
    "get_phone_to_patient_map",
    "get_checkins_sync",
    "update_checkin_status_sync",
    "get_biomarker_definitions_sync",
    "get_patient_biomarkers_sync",
]
