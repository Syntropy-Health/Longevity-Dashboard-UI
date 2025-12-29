"""Treatment models for treatment protocols and patient assignments."""

from datetime import datetime

import reflex as rx
from sqlmodel import Field

from .base import utc_now


class Treatment(rx.Model, table=True):
    """Treatment/protocol definition available at the clinic.

    This is the catalog of treatments that can be assigned to patients.
    Category links to TreatmentCategory reference table via category_id FK.
    """

    __tablename__ = "treatments"

    id: int | None = Field(default=None, primary_key=True)
    treatment_id: str = Field(index=True, unique=True)  # External ID like "T001"
    name: str = Field(index=True)

    # Category - FK to treatment_categories table (unidirectional, no back-populate)
    category_id: int | None = Field(
        default=None, foreign_key="treatment_categories.id", index=True
    )

    description: str = Field(default="")
    duration: str = Field(default="")  # "60 mins", "3 mins", etc.
    frequency: str = Field(default="")  # Weekly, Daily, As-needed
    cost: float = Field(default=0.0)
    status: str = Field(default="Active")  # Active | Inactive | Deprecated

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class PatientTreatment(rx.Model, table=True):
    """Junction table for patient-treatment assignments.

    Tracks which treatments are assigned to which patients with progress.
    For Medications category: includes dosage and adherence tracking.
    """

    __tablename__ = "patient_treatments"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    treatment_id: int = Field(foreign_key="treatments.id", index=True)

    # Assignment details
    assigned_by: str | None = None
    start_date: datetime = Field(default_factory=utc_now)
    end_date: datetime | None = None
    status: str = Field(default="active")  # active | completed | paused | cancelled
    notes: str | None = None

    # Medication-specific fields (for category=Medications)
    dosage: str = Field(default="")  # e.g., "500mg", "10mg"
    instructions: str = Field(default="")  # e.g., "Take with food"
    adherence_rate: float = Field(default=100.0)  # Percentage 0-100

    # Progress tracking
    sessions_completed: int = Field(default=0)
    sessions_total: int | None = None
    last_session_at: datetime | None = None

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
