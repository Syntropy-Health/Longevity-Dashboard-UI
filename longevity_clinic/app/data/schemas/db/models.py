"""Database models for the Longevity Clinic application.

Uses Reflex's rx.Model (SQLModel) for database operations with SQLite/PostgreSQL.
"""

from datetime import UTC, datetime

import reflex as rx
from sqlmodel import Field


def utc_now() -> datetime:
    """Return current UTC datetime (timezone-aware)."""
    return datetime.now(UTC)


# =============================================================================
# User Model
# =============================================================================


class User(rx.Model, table=True):
    """User account for patients and admins."""

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    external_id: str = Field(index=True, unique=True)  # e.g., "P001"
    name: str
    email: str = Field(index=True, unique=True)
    phone: str | None = Field(default=None, index=True)
    role: str = Field(default="patient")  # "patient" | "admin" | "provider"
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Call Log Models
# =============================================================================


class CallLog(rx.Model, table=True):
    """Voice call log from the telephony system."""

    __tablename__ = "call_logs"

    id: int | None = Field(default=None, primary_key=True)
    call_id: str = Field(index=True, unique=True)  # External call ID from API
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    phone_number: str = Field(index=True)
    direction: str = Field(default="inbound")  # "inbound" | "outbound"
    duration_seconds: int = Field(default=0)
    started_at: datetime
    ended_at: datetime | None = None
    status: str = Field(default="completed")  # "completed" | "missed" | "voicemail"
    processed_to_metrics: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)


class CallTranscript(rx.Model, table=True):
    """Transcript of a voice call."""

    __tablename__ = "call_transcripts"

    id: int | None = Field(default=None, primary_key=True)
    call_log_id: int = Field(foreign_key="call_logs.id", index=True)
    call_id: str = Field(index=True)  # Denormalized for quick lookup
    raw_transcript: str  # Full transcript text
    speaker_labels: str | None = None  # JSON string of speaker segments
    language: str = Field(default="en")
    confidence_score: float | None = None
    created_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Check-in Models
# =============================================================================


class CheckIn(rx.Model, table=True):
    """Patient check-in record (manual, voice, or from call).

    Consolidates check-in data with LLM-processing metadata.
    Health entries (medications, food, symptoms) link back to this table.
    """

    __tablename__ = "checkins"

    id: int | None = Field(default=None, primary_key=True)
    checkin_id: str = Field(index=True, unique=True)  # External ID like "CHK-001"
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    call_log_id: int | None = Field(default=None, foreign_key="call_logs.id")

    # Check-in content
    patient_name: str
    checkin_type: str = Field(default="manual")  # "manual" | "voice" | "call"
    summary: str
    raw_content: str | None = None  # Original text/transcript

    # Health data (from LLM extraction)
    health_topics: str | None = None  # JSON array
    sentiment: str | None = None  # "positive" | "neutral" | "negative"
    mood: str | None = None
    energy_level: int | None = None  # 1-10
    urgency_level: str = Field(default="routine")  # "routine" | "follow_up" | "urgent"

    # Processing metadata
    is_processed: bool = Field(default=False)
    llm_model: str | None = None
    processed_at: datetime | None = None

    # Status tracking
    status: str = Field(
        default="pending"
    )  # "pending" | "reviewed" | "flagged" | "archived"
    provider_reviewed: bool = Field(default=False)
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None

    # Timestamps
    timestamp: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Notification Model
# =============================================================================


class Notification(rx.Model, table=True):
    """System notification for users."""

    __tablename__ = "notifications"

    id: int | None = Field(default=None, primary_key=True)
    notification_id: str = Field(index=True, unique=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    recipient_role: str = Field(default="patient")  # "patient" | "admin"

    title: str
    message: str
    notification_type: str = Field(
        default="info"
    )  # "info" | "lab" | "treatment" | "appointment" | "warning" | "success"

    is_read: bool = Field(default=False)
    patient_id: str | None = None  # Reference to patient external_id

    created_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Appointment Model
# =============================================================================


class Appointment(rx.Model, table=True):
    """Patient appointment for scheduling treatments and consultations."""

    __tablename__ = "appointments"

    id: int | None = Field(default=None, primary_key=True)
    appointment_id: str = Field(index=True, unique=True)  # External ID like "APT001"
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)

    # Appointment details
    title: str
    description: str | None = None
    date: str = Field(index=True)  # ISO date string "2025-01-16"
    time: str  # Time string "09:00"
    duration_minutes: int = Field(default=60)

    # Treatment info
    treatment_type: str = Field(default="Consultation")
    patient_id: str | None = None  # Reference to patient external_id
    patient_name: str

    # Provider info
    provider: str  # e.g., "Dr. Johnson"

    # Status tracking
    status: str = Field(
        default="scheduled"
    )  # scheduled | confirmed | completed | cancelled
    notes: str | None = None

    # Timestamps
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Extracted Health Data Tables (from LLM processing)
# =============================================================================


class MedicationEntry(rx.Model, table=True):
    """Medication entry extracted from check-ins.

    Normalized storage for dashboard queries and aggregations.
    Links to CheckIn as the single source of truth.
    """

    __tablename__ = "medication_entries"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    checkin_id: int | None = Field(default=None, foreign_key="checkins.id", index=True)

    # Medication data
    name: str = Field(index=True)
    dosage: str = Field(default="")
    frequency: str = Field(default="")
    status: str = Field(default="active")  # active | discontinued | as-needed
    adherence_rate: float = Field(default=1.0)

    # Source tracking
    source: str = Field(default="manual")  # call | voice | manual | seed
    mentioned_at: datetime = Field(default_factory=utc_now)
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
    severity: str = Field(default="")  # mild | moderate | severe
    severity_score: int = Field(default=0)  # 0-10 scale
    frequency: str = Field(default="")
    trend: str = Field(default="stable")  # improving | worsening | stable
    notes: str | None = None

    # Source tracking
    source: str = Field(default="manual")  # call | voice | manual | seed
    reported_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Clinic Metrics Models (for admin dashboard charts)
# =============================================================================


class PatientVisit(rx.Model, table=True):
    """Patient visit record for tracking clinic trends."""

    __tablename__ = "patient_visits"

    id: int | None = Field(default=None, primary_key=True)
    period: str = Field(index=True)  # e.g., "Jan", "Feb", "2025-01", etc.
    period_type: str = Field(default="month")  # "day" | "week" | "month" | "quarter"
    active_patients: int = Field(default=0)
    new_patients: int = Field(default=0)
    total_visits: int = Field(default=0)
    notes: str | None = None
    recorded_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class TreatmentProtocolMetric(rx.Model, table=True):
    """Treatment protocol metrics for admin dashboard charts."""

    __tablename__ = "treatment_protocol_metrics"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: str = Field(default="general")
    active_count: int = Field(default=0)
    completed_count: int = Field(default=0)
    success_rate: float = Field(default=0.0)
    avg_duration_days: int = Field(default=0)
    notes: str | None = None
    updated_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class BiomarkerAggregate(rx.Model, table=True):
    """Aggregated biomarker scores for trend tracking."""

    __tablename__ = "biomarker_aggregates"

    id: int | None = Field(default=None, primary_key=True)
    period: str = Field(index=True)
    period_type: str = Field(default="week")
    avg_score: float = Field(default=0.0)
    patient_count: int = Field(default=0)
    improvement_pct: float = Field(default=0.0)
    notes: str | None = None
    recorded_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class ClinicDailyMetrics(rx.Model, table=True):
    """Daily clinic operational metrics."""

    __tablename__ = "clinic_daily_metrics"

    id: int | None = Field(default=None, primary_key=True)
    date: datetime = Field(index=True)
    hour: int | None = None

    # Patient flow
    scheduled_appointments: int = Field(default=0)
    walkin_appointments: int = Field(default=0)
    completed_appointments: int = Field(default=0)
    no_shows: int = Field(default=0)

    # Efficiency metrics
    avg_wait_time_minutes: float = Field(default=0.0)
    avg_appointment_duration_minutes: float = Field(default=0.0)
    patient_throughput: float = Field(default=0.0)

    # Room utilization
    room_id: str | None = None
    room_occupancy_pct: float = Field(default=0.0)
    treatments_completed: int = Field(default=0)

    created_at: datetime = Field(default_factory=utc_now)


class ProviderMetrics(rx.Model, table=True):
    """Provider performance metrics."""

    __tablename__ = "provider_metrics"

    id: int | None = Field(default=None, primary_key=True)
    provider_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    provider_name: str = Field(index=True)
    period: str = Field(index=True)
    period_type: str = Field(default="month")

    # Performance metrics
    patient_count: int = Field(default=0)
    efficiency_score: float = Field(default=0.0)
    on_time_rate: float = Field(default=0.0)
    avg_rating: float = Field(default=0.0)

    created_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Treatment Models
# =============================================================================


class Treatment(rx.Model, table=True):
    """Treatment/protocol definition available at the clinic.

    This is the catalog of treatments that can be assigned to patients.
    """

    __tablename__ = "treatments"

    id: int | None = Field(default=None, primary_key=True)
    treatment_id: str = Field(index=True, unique=True)  # External ID like "T001"
    name: str = Field(index=True)
    category: str = Field(default="General")  # IV Therapy, Cryotherapy, etc.
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

    # Progress tracking
    sessions_completed: int = Field(default=0)
    sessions_total: int | None = None
    last_session_at: datetime | None = None

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Biomarker Models
# =============================================================================


class BiomarkerDefinition(rx.Model, table=True):
    """Biomarker definition catalog (reference data).

    Defines what biomarkers exist, their categories, units, and ranges.
    """

    __tablename__ = "biomarker_definitions"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g. "VITAMIN_D", "HS_CRP"
    name: str = Field(index=True)
    category: str = Field(index=True)  # Metabolic, Inflammation, Hormones, etc.
    unit: str
    description: str = Field(default="")

    # Reference ranges
    optimal_min: float = Field(default=0.0)
    optimal_max: float = Field(default=0.0)
    critical_min: float = Field(default=0.0)
    critical_max: float = Field(default=0.0)

    created_at: datetime = Field(default_factory=utc_now)


class BiomarkerReading(rx.Model, table=True):
    """Individual biomarker reading for a patient."""

    __tablename__ = "biomarker_readings"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    biomarker_id: int = Field(foreign_key="biomarker_definitions.id", index=True)

    value: float
    status: str = Field(default="optimal")  # optimal | warning | critical
    trend: str = Field(default="stable")  # up | down | stable

    # Source tracking
    source: str = Field(default="lab")  # lab | manual | device
    measured_at: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Export all models
# =============================================================================

__all__ = [
    # Core models
    "Appointment",
    "BiomarkerAggregate",
    "BiomarkerDefinition",
    "BiomarkerReading",
    "CallLog",
    "CallTranscript",
    "CheckIn",
    "ClinicDailyMetrics",
    "FoodLogEntry",
    "MedicationEntry",
    "Notification",
    "PatientTreatment",
    "PatientVisit",
    "ProviderMetrics",
    "SymptomEntry",
    "Treatment",
    "TreatmentProtocolMetric",
    "User",
    # Helper
    "utc_now",
]
