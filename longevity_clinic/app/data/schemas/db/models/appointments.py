"""Appointment model for scheduling.

Refactored design:
- patient_user_id: FK to users.id (patient)
- provider_user_id: FK to users.id (provider/admin)
- Keeps legacy fields for backward compatibility during migration
"""

from datetime import datetime

import reflex as rx
from sqlmodel import Field

from .base import utc_now


class Appointment(rx.Model, table=True):
    """Patient appointment for scheduling treatments and consultations.

    Represents a meeting between two users:
    - patient_user_id: The patient attending the appointment
    - provider_user_id: The healthcare provider conducting it
    """

    __tablename__ = "appointments"

    id: int | None = Field(default=None, primary_key=True)
    appointment_id: str = Field(index=True, unique=True)  # External ID like "APT001"

    # =========================================================================
    # User Relationships (normalized)
    # =========================================================================
    # Patient FK - who the appointment is for
    patient_user_id: int | None = Field(
        default=None, foreign_key="users.id", index=True
    )
    # Provider FK - who is conducting the appointment
    provider_user_id: int | None = Field(
        default=None, foreign_key="users.id", index=True
    )

    # Legacy field (deprecated, use patient_user_id)
    user_id: int | None = Field(default=None, index=True)

    # =========================================================================
    # Appointment Details
    # =========================================================================
    title: str
    description: str | None = None
    date: str = Field(index=True)  # ISO date string "2025-01-16"
    time: str  # Time string "09:00"
    duration_minutes: int = Field(default=60)

    # Treatment info
    treatment_type: str = Field(default="Consultation")
    treatment_id: int | None = Field(
        default=None, foreign_key="treatments.id", index=True
    )

    # =========================================================================
    # Denormalized Fields (for display, backward compatibility)
    # =========================================================================
    # These duplicate FK data but are kept for:
    # 1. Display performance (avoid JOINs)
    # 2. Historical record (patient/provider name at time of booking)
    patient_id: str | None = None  # Legacy: external_id reference
    patient_name: str = Field(default="")  # Snapshot at booking time
    provider: str = Field(default="")  # Provider name snapshot

    # =========================================================================
    # Status & Metadata
    # =========================================================================
    status: str = Field(
        default="scheduled"
    )  # scheduled | confirmed | completed | cancelled
    notes: str | None = None
    location: str | None = None  # Room/location for in-person appointments
    is_virtual: bool = Field(default=False)  # Telehealth appointment
    meeting_url: str | None = None  # Video call URL if virtual

    # Timestamps
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
