"""User database operations."""

from __future__ import annotations

from typing import Dict, List, Optional

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.model import User
from longevity_clinic.app.functions.utils import normalize_phone

logger = get_logger("longevity_clinic.db_utils.users")


def get_user_by_phone_sync(phone: str) -> Optional[User]:
    """Get user by phone number (sync)."""
    if not phone:
        return None

    normalized = normalize_phone(phone)

    try:
        with rx.session() as session:
            result = session.exec(select(User).where(User.phone == phone)).first()
            if result:
                return result

            users = session.exec(select(User).where(User.phone.isnot(None))).all()
            for user in users:
                if user.phone and normalize_phone(user.phone) == normalized:
                    return user
            return None
    except Exception as e:
        logger.error("Failed to get user by phone %s: %s", phone, e)
        return None


def get_user_by_external_id_sync(external_id: str) -> Optional[User]:
    """Get user by external ID (e.g., 'P001')."""
    try:
        with rx.session() as session:
            return session.exec(
                select(User).where(User.external_id == external_id)
            ).first()
    except Exception as e:
        logger.error("Failed to get user by external_id %s: %s", external_id, e)
        return None


def get_user_by_id_sync(user_id: int) -> Optional[User]:
    """Get user by database ID."""
    try:
        with rx.session() as session:
            return session.exec(select(User).where(User.id == user_id)).first()
    except Exception as e:
        logger.error("Failed to get user by id %s: %s", user_id, e)
        return None


def get_patient_name_by_phone(phone: str, fallback: str = "Unknown Patient") -> str:
    """Get patient name from phone number via database lookup."""
    user = get_user_by_phone_sync(phone)
    if user:
        return user.name
    return fallback if fallback != "Unknown Patient" else f"Patient ({phone})"


def get_all_patients_sync() -> List[User]:
    """Get all patient users from database."""
    try:
        with rx.session() as session:
            return list(session.exec(select(User).where(User.role == "patient")).all())
    except Exception as e:
        logger.error("Failed to get all patients: %s", e)
        return []


def get_phone_to_patient_map() -> Dict[str, str]:
    """Build phone-to-patient-name mapping from database."""
    try:
        with rx.session() as session:
            users = session.exec(
                select(User).where(User.phone.isnot(None), User.role == "patient")
            ).all()
            return {user.phone: user.name for user in users if user.phone}
    except Exception as e:
        logger.error("Failed to build phone-to-patient map: %s", e)
        return {}


def get_primary_demo_user_id() -> Optional[int]:
    """Get the database ID of the primary demo user (Sarah Chen / P001)."""
    user = get_user_by_external_id_sync("P001")
    return user.id if user else None


def get_recently_active_patients_sync(limit: int = 5) -> List[User]:
    """Get most recently active patients based on check-in activity.

    Args:
        limit: Maximum number of patients to return

    Returns:
        List of User objects ordered by most recent activity
    """
    from longevity_clinic.app.data.model import CheckIn
    from sqlmodel import desc, func

    try:
        with rx.session() as session:
            # Get patients with most recent check-ins
            # Uses a subquery to get latest check-in per user
            subquery = (
                select(
                    CheckIn.user_id, func.max(CheckIn.timestamp).label("last_activity")
                )
                .where(CheckIn.user_id.isnot(None))
                .group_by(CheckIn.user_id)
                .subquery()
            )

            result = session.exec(
                select(User)
                .join(subquery, User.id == subquery.c.user_id)
                .where(User.role == "patient")
                .order_by(desc(subquery.c.last_activity))
                .limit(limit)
            ).all()

            return list(result)
    except Exception as e:
        logger.error("Failed to get recently active patients: %s", e)
        # Fallback: return all patients sorted by updated_at
        try:
            with rx.session() as session:
                return list(
                    session.exec(
                        select(User)
                        .where(User.role == "patient")
                        .order_by(desc(User.updated_at))
                        .limit(limit)
                    ).all()
                )
        except Exception as fallback_error:
            logger.error("Fallback query also failed: %s", fallback_error)
            return []
