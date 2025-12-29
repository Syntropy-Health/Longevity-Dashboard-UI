"""Health entry models extracted from check-ins.

Includes medication logs, food entries, and symptom entries.
"""

from datetime import datetime

import reflex as rx
from sqlmodel import Field

from .base import utc_now


class MedicationEntry(rx.Model, table=True):
    """Log of medication taken (extracted from check-ins).

    Tracks when a patient actually took a medication.
    Links to CheckIn and optionally to PatientTreatment (for Medications category).
    """

    __tablename__ = "medication_entries"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    checkin_id: int | None = Field(default=None, foreign_key="checkins.id", index=True)
    patient_treatment_id: int | None = Field(
        default=None, foreign_key="patient_treatments.id", index=True
    )

    # Log data
    name: str = Field(index=True)
    dosage: str = Field(default="")
    taken_at: datetime = Field(default_factory=utc_now)
    notes: str = Field(default="")

    # Source tracking
    source: str = Field(default="manual")  # call | voice | manual | seed
    created_at: datetime = Field(default_factory=utc_now)


class FoodLogEntry(rx.Model, table=True):
    """Food/nutrition entry extracted from check-ins.

    Normalized storage for nutrition tracking and dashboards.
    """

    __tablename__ = "food_log_entries"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    checkin_id: int | None = Field(default=None, foreign_key="checkins.id", index=True)

    # Food data
    name: str
    calories: int = Field(default=0)
    protein: float = Field(default=0.0)
    carbs: float = Field(default=0.0)
    fat: float = Field(default=0.0)
    meal_type: str = Field(default="snack")  # breakfast | lunch | dinner | snack
    consumed_at: str | None = None  # Time string from transcript

    # Source tracking
    source: str = Field(default="manual")  # call | voice | manual | seed
    logged_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class SymptomEntry(rx.Model, table=True):
    """Symptom entry extracted from check-ins.

    Normalized storage for symptom tracking and trend analysis.
    """

    __tablename__ = "symptom_entries"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    checkin_id: int | None = Field(default=None, foreign_key="checkins.id", index=True)

    # Symptom data
    name: str = Field(index=True)
    severity: str = Field(default="UNKNOWN")  # unknown | mild | moderate | severe
    frequency: str = Field(default="UNKNOWN")  # unknown when not specified
    trend: str = Field(default="UNKNOWN")  # unknown | improving | worsening | stable
    notes: str | None = None

    # Source tracking
    source: str = Field(default="manual")  # call | voice | manual | seed
    reported_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)
