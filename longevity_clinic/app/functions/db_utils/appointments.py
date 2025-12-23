"""Database utilities for appointment queries.

Provides synchronous database operations for appointments.
Used by AppointmentState for DB-first data loading with seed fallback.
"""

import reflex as rx

from longevity_clinic.app.data.model import Appointment


def get_appointments_sync(
    status: str | None = None,
    limit: int = 100,
) -> list[dict]:
    """Get appointments with optional status filter.

    Args:
        status: Filter by status (scheduled, confirmed, completed, cancelled)
        limit: Maximum number of appointments to return

    Returns:
        List of appointment dicts
    """
    try:
        with rx.session() as session:
            query = session.query(Appointment)

            if status:
                query = query.filter(Appointment.status == status)

            query = query.order_by(
                Appointment.date.desc(), Appointment.time.desc()
            ).limit(limit)

            appointments = query.all()
            return [
                {
                    "id": apt.appointment_id,
                    "title": apt.title,
                    "description": apt.description or "",
                    "date": apt.date,
                    "time": apt.time,
                    "duration_minutes": apt.duration_minutes,
                    "treatment_type": apt.treatment_type,
                    "patient_id": apt.patient_id or "",
                    "patient_name": apt.patient_name,
                    "provider": apt.provider,
                    "status": apt.status,
                    "notes": apt.notes or "",
                }
                for apt in appointments
            ]
    except Exception:
        return []


def get_appointments_for_user_sync(
    user_id: int,
    limit: int = 50,
) -> list[dict]:
    """Get appointments for a specific user.

    Args:
        user_id: The user's database ID
        limit: Maximum number of appointments to return

    Returns:
        List of appointment dicts for the user
    """
    try:
        with rx.session() as session:
            appointments = (
                session.query(Appointment)
                .filter(Appointment.user_id == user_id)
                .order_by(Appointment.date.desc(), Appointment.time.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": apt.appointment_id,
                    "title": apt.title,
                    "description": apt.description or "",
                    "date": apt.date,
                    "time": apt.time,
                    "duration_minutes": apt.duration_minutes,
                    "treatment_type": apt.treatment_type,
                    "patient_id": apt.patient_id or "",
                    "patient_name": apt.patient_name,
                    "provider": apt.provider,
                    "status": apt.status,
                    "notes": apt.notes or "",
                }
                for apt in appointments
            ]
    except Exception:
        return []


def get_appointments_for_patient_sync(
    patient_id: str,
    limit: int = 50,
) -> list[dict]:
    """Get appointments for a specific patient by external ID.

    Args:
        patient_id: The patient's external ID (e.g., "P001")
        limit: Maximum number of appointments to return

    Returns:
        List of appointment dicts for the patient
    """
    try:
        with rx.session() as session:
            appointments = (
                session.query(Appointment)
                .filter(Appointment.patient_id == patient_id)
                .order_by(Appointment.date.desc(), Appointment.time.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": apt.appointment_id,
                    "title": apt.title,
                    "description": apt.description or "",
                    "date": apt.date,
                    "time": apt.time,
                    "duration_minutes": apt.duration_minutes,
                    "treatment_type": apt.treatment_type,
                    "patient_id": apt.patient_id or "",
                    "patient_name": apt.patient_name,
                    "provider": apt.provider,
                    "status": apt.status,
                    "notes": apt.notes or "",
                }
                for apt in appointments
            ]
    except Exception:
        return []


def update_appointment_status_sync(
    appointment_id: str,
    new_status: str,
) -> bool:
    """Update the status of an appointment.

    Args:
        appointment_id: The appointment's external ID (e.g., "APT001")
        new_status: New status (scheduled, confirmed, completed, cancelled)

    Returns:
        True if successful, False otherwise
    """
    try:
        with rx.session() as session:
            appointment = (
                session.query(Appointment)
                .filter(Appointment.appointment_id == appointment_id)
                .first()
            )
            if appointment:
                appointment.status = new_status
                session.add(appointment)
                session.commit()
                return True
            return False
    except Exception:
        return False


def create_appointment_sync(
    appointment_data: dict,
    user_id: int | None = None,
) -> str | None:
    """Create a new appointment in the database.

    Args:
        appointment_data: Dict with appointment fields
        user_id: Optional user database ID to link the appointment

    Returns:
        The new appointment_id if successful, None otherwise
    """
    try:
        with rx.session() as session:
            appointment = Appointment(
                appointment_id=appointment_data.get("id", ""),
                user_id=user_id or appointment_data.get("user_id"),
                title=appointment_data.get("title", ""),
                description=appointment_data.get("description"),
                date=appointment_data.get("date", ""),
                time=appointment_data.get("time", ""),
                duration_minutes=appointment_data.get("duration_minutes", 60),
                treatment_type=appointment_data.get("treatment_type", "Consultation"),
                patient_id=appointment_data.get("patient_id"),
                patient_name=appointment_data.get("patient_name", ""),
                provider=appointment_data.get("provider", ""),
                status=appointment_data.get("status", "scheduled"),
                notes=appointment_data.get("notes"),
            )
            session.add(appointment)
            session.commit()
            session.refresh(appointment)
            return appointment.appointment_id
    except Exception:
        return None
