"""Appointment seed data loader.

Loads appointment seed data into the database from APPOINTMENTS_SEED.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Session

from .base import SeedResult

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


def load_appointments(engine: "Engine", user_id_map: dict[str, int]) -> SeedResult:
    """Load appointment seed data into database.

    Args:
        engine: SQLAlchemy engine
        user_id_map: Mapping of external_id -> database id for users

    Returns:
        SeedResult with counts and any errors
    """
    from longevity_clinic.app.data.model import Appointment
    from longevity_clinic.app.data.seed import APPOINTMENTS_SEED

    errors: list[str] = []
    loaded = 0
    skipped = 0

    with Session(engine) as session:
        for apt_data in APPOINTMENTS_SEED:
            # Check if already exists
            existing = (
                session.query(Appointment)
                .filter(Appointment.appointment_id == apt_data["id"])
                .first()
            )
            if existing:
                skipped += 1
                continue

            # Map patient_id to user_id if available
            user_id = None
            patient_id = apt_data.get("patient_id")
            if patient_id and patient_id in user_id_map:
                user_id = user_id_map[patient_id]

            try:
                appointment = Appointment(
                    appointment_id=apt_data["id"],
                    user_id=user_id,
                    title=apt_data.get("title", ""),
                    description=apt_data.get("description"),
                    date=apt_data.get("date", ""),
                    time=apt_data.get("time", ""),
                    duration_minutes=apt_data.get("duration_minutes", 60),
                    treatment_type=apt_data.get("treatment_type", "Consultation"),
                    patient_id=patient_id,
                    patient_name=apt_data.get("patient_name", ""),
                    provider=apt_data.get("provider", ""),
                    status=apt_data.get("status", "scheduled"),
                    notes=apt_data.get("notes"),
                )
                session.add(appointment)
                loaded += 1
            except Exception as e:
                errors.append(f"Failed to load appointment {apt_data['id']}: {e}")

        session.commit()

    return SeedResult(
        name="appointments", loaded=loaded, skipped=skipped, errors=errors
    )
