"""Treatment database operations."""

from __future__ import annotations

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.db import (
    PatientTreatment,
    Treatment,
    TreatmentCategory,
)
from longevity_clinic.app.data.schemas.state import TreatmentProtocol

logger = get_logger("longevity_clinic.db_utils.treatments")


def get_all_treatments_sync() -> list[Treatment]:
    """Get all treatments from database."""
    try:
        with rx.session() as session:
            return list(session.exec(select(Treatment)).all())
    except Exception as e:
        logger.error("Failed to get all treatments: %s", e)
        return []


def get_treatment_by_id_sync(treatment_id: str) -> Treatment | None:
    """Get treatment by external ID (e.g., 'T001')."""
    try:
        with rx.session() as session:
            return session.exec(
                select(Treatment).where(Treatment.treatment_id == treatment_id)
            ).first()
    except Exception as e:
        logger.error("Failed to get treatment %s: %s", treatment_id, e)
        return None


def get_treatments_as_protocols_sync() -> list[TreatmentProtocol]:
    """Get all treatments converted to TreatmentProtocol TypedDict format.

    Joins with TreatmentCategory to get category name.
    """
    try:
        with rx.session() as session:
            results = session.exec(
                select(Treatment, TreatmentCategory).outerjoin(
                    TreatmentCategory, Treatment.category_id == TreatmentCategory.id
                )
            ).all()
            return [
                TreatmentProtocol(
                    id=t.treatment_id,
                    name=t.name,
                    category=cat.name if cat else "General",
                    description=t.description,
                    duration=t.duration,
                    frequency=t.frequency,
                    cost=t.cost,
                    status=t.status,
                )
                for t, cat in results
            ]
    except Exception as e:
        logger.error("Failed to get treatments as protocols: %s", e)
        return []


def get_patient_treatments_sync(user_id: int, limit: int = 100) -> list[dict]:
    """Get all treatment assignments for a patient with treatment details.

    Args:
        user_id: The user ID to fetch treatments for
        limit: Maximum number of treatments to return

    Returns:
        List of dicts with both PatientTreatment and Treatment fields
    """
    try:
        with rx.session() as session:
            results = session.exec(
                select(PatientTreatment, Treatment, TreatmentCategory)
                .join(Treatment, PatientTreatment.treatment_id == Treatment.id)
                .outerjoin(
                    TreatmentCategory, Treatment.category_id == TreatmentCategory.id
                )
                .where(PatientTreatment.user_id == user_id)
                .limit(limit)
            ).all()
            return [
                {
                    "id": pt.id,
                    "treatment_id": t.treatment_id,
                    "treatment_name": t.name,
                    "treatment_category": cat.name if cat else "General",
                    "treatment_description": t.description,
                    "start_date": pt.start_date,
                    "end_date": pt.end_date,
                    "status": pt.status,
                    "sessions_completed": pt.sessions_completed,
                    "sessions_total": pt.sessions_total,
                    "progress": (
                        int(pt.sessions_completed / pt.sessions_total * 100)
                        if pt.sessions_total and pt.sessions_total > 0
                        else 0
                    ),
                }
                for pt, t, cat in results
            ]
    except Exception as e:
        logger.error("Failed to get patient treatments for user %s: %s", user_id, e)
        return []


def create_treatment_sync(
    treatment_id: str,
    name: str,
    category_id: int | None = None,
    description: str = "",
    duration: str = "",
    frequency: str = "",
    cost: float = 0.0,
    status: str = "Active",
) -> Treatment | None:
    """Create a new treatment in database."""
    try:
        with rx.session() as session:
            treatment = Treatment(
                treatment_id=treatment_id,
                name=name,
                category_id=category_id,
                description=description,
                duration=duration,
                frequency=frequency,
                cost=cost,
                status=status,
            )
            session.add(treatment)
            session.commit()
            session.refresh(treatment)
            return treatment
    except Exception as e:
        logger.error("Failed to create treatment: %s", e)
        return None


def update_treatment_sync(
    treatment_id: str,
    name: str | None = None,
    category_id: int | None = None,
    description: str | None = None,
    duration: str | None = None,
    frequency: str | None = None,
    cost: float | None = None,
    status: str | None = None,
) -> Treatment | None:
    """Update an existing treatment."""
    try:
        with rx.session() as session:
            treatment = session.exec(
                select(Treatment).where(Treatment.treatment_id == treatment_id)
            ).first()
            if not treatment:
                return None

            if name is not None:
                treatment.name = name
            if category_id is not None:
                treatment.category_id = category_id
            if description is not None:
                treatment.description = description
            if duration is not None:
                treatment.duration = duration
            if frequency is not None:
                treatment.frequency = frequency
            if cost is not None:
                treatment.cost = cost
            if status is not None:
                treatment.status = status

            session.add(treatment)
            session.commit()
            session.refresh(treatment)
            return treatment
    except Exception as e:
        logger.error("Failed to update treatment %s: %s", treatment_id, e)
        return None
