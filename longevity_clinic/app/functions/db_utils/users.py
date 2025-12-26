"""User database operations."""

from __future__ import annotations

from datetime import UTC, datetime

import reflex as rx
from sqlmodel import func, select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.db import User
from longevity_clinic.app.functions.utils import normalize_phone

logger = get_logger("longevity_clinic.db_utils.users")


def create_user_sync(
    name: str,
    phone: str,
    role: str = "patient",
    email: str | None = None,
) -> User | None:
    """Create a new user in the database.

    Args:
        name: User's full name
        phone: Phone number (E.164 format preferred)
        role: User role ('patient' or 'admin')
        email: Optional email address

    Returns:
        Created User object or None on failure
    """
    if not name or not phone:
        logger.warning("create_user_sync: name and phone are required")
        return None

    try:
        with rx.session() as session:
            # Check if user already exists
            existing = session.exec(select(User).where(User.phone == phone)).first()
            if existing:
                logger.info("User already exists for phone %s", phone)
                return existing

            # Generate external_id (P + next number)
            max_id = session.exec(
                select(func.max(User.id)).where(User.role == "patient")
            ).first()
            next_num = (max_id or 0) + 1
            external_id = f"P{next_num:03d}"

            now = datetime.now(UTC)
            user = User(
                name=name,
                email=email or f"{external_id.lower()}@patient.longevityclinic.com",
                phone=phone,
                role=role,
                external_id=external_id,
                created_at=now,
                updated_at=now,
            )
            session.add(user)
            session.commit()
            session.refresh(user)

            logger.info(
                "Created new user: id=%d, name=%s, phone=%s, external_id=%s",
                user.id,
                name,
                phone,
                external_id,
            )
            return user
    except Exception as e:
        logger.error("Failed to create user (name=%s, phone=%s): %s", name, phone, e)
        return None


def get_user_by_phone_sync(phone: str) -> User | None:
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


def get_user_by_external_id_sync(external_id: str) -> User | None:
    """Get user by external ID (e.g., 'P001')."""
    try:
        with rx.session() as session:
            return session.exec(
                select(User).where(User.external_id == external_id)
            ).first()
    except Exception as e:
        logger.error("Failed to get user by external_id %s: %s", external_id, e)
        return None


def get_user_by_id_sync(user_id: int) -> User | None:
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


def get_all_patients_sync() -> list[User]:
    """Get all patient users from database."""
    try:
        with rx.session() as session:
            return list(session.exec(select(User).where(User.role == "patient")).all())
    except Exception as e:
        logger.error("Failed to get all patients: %s", e)
        return []


def get_phone_to_patient_map() -> dict[str, str]:
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


def get_recently_active_patients_sync(limit: int = 5) -> list[User]:
    """Get most recently active patients based on check-in activity.

    Falls back to all patients sorted by updated_at if no check-ins exist.

    Args:
        limit: Maximum number of patients to return

    Returns:
        List of User objects ordered by most recent activity
    """
    from sqlmodel import desc, func

    from longevity_clinic.app.data.schemas.db import CheckIn

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

            # If no patients with check-ins, fallback to all patients
            if result:
                return list(result)

            logger.info("No check-ins found, falling back to all patients")
            return list(
                session.exec(
                    select(User)
                    .where(User.role == "patient")
                    .order_by(desc(User.updated_at))
                    .limit(limit)
                ).all()
            )
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
