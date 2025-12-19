"""Database models for the Longevity Clinic application.

Uses Reflex's rx.Model (SQLModel) for database operations with SQLite.
"""

from datetime import datetime, timezone
from typing import Optional

import reflex as rx
from sqlmodel import Field


def utc_now() -> datetime:
    """Return current UTC datetime (timezone-aware)."""
    return datetime.now(timezone.utc)


# User Model


class User(rx.Model, table=True):
    """User account for patients and admins."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: str = Field(index=True, unique=True)  # e.g., "P001"
    name: str
    email: str = Field(index=True, unique=True)
    phone: Optional[str] = Field(default=None, index=True)
    role: str = Field(default="patient")  # "patient" | "admin" | "provider"
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


# Call Log Models


class CallLog(rx.Model, table=True):
    """Voice call log from the telephony system."""

    __tablename__ = "call_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    call_id: str = Field(index=True, unique=True)  # External call ID from API
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    phone_number: str = Field(index=True)
    direction: str = Field(default="inbound")  # "inbound" | "outbound"
    duration_seconds: int = Field(default=0)
    started_at: datetime
    ended_at: Optional[datetime] = None
    status: str = Field(default="completed")  # "completed" | "missed" | "voicemail"
    processed_to_metrics: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)


class CallTranscript(rx.Model, table=True):
    """Transcript of a voice call."""

    __tablename__ = "call_transcripts"

    id: Optional[int] = Field(default=None, primary_key=True)
    call_log_id: int = Field(foreign_key="call_logs.id", index=True)
    call_id: str = Field(index=True)  # Denormalized for quick lookup
    raw_transcript: str  # Full transcript text
    speaker_labels: Optional[str] = None  # JSON string of speaker segments
    language: str = Field(default="en")
    confidence_score: Optional[float] = None
    created_at: datetime = Field(default_factory=utc_now)


class CallSummary(rx.Model, table=True):
    """AI-generated summary and extracted data from a call.

    DEPRECATED: This table is kept for backward compatibility.
    New code should use CheckIn.is_processed and health entry tables directly.
    The CheckIn table now stores processing metadata (is_processed, llm_model, etc.)
    """

    __tablename__ = "call_summaries"

    id: Optional[int] = Field(default=None, primary_key=True)
    call_log_id: int = Field(foreign_key="call_logs.id", index=True)
    call_id: str = Field(index=True)  # Denormalized for quick lookup
    summary: str  # AI-generated summary text
    health_topics: Optional[str] = None  # JSON array of topics
    sentiment: Optional[str] = None  # "positive" | "neutral" | "negative"
    urgency_level: str = Field(default="routine")  # "routine" | "follow_up" | "urgent"

    # Extracted structured data (JSON strings)
    medications_json: Optional[str] = None
    food_entries_json: Optional[str] = None
    symptoms_json: Optional[str] = None

    # Flags
    has_medications: bool = Field(default=False)
    has_nutrition: bool = Field(default=False)
    has_symptoms: bool = Field(default=False)

    # Processing metadata
    llm_model: Optional[str] = None
    processed_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


# Check-in Models


class CheckIn(rx.Model, table=True):
    """Patient check-in record (manual, voice, or from call).

    Consolidates check-in data with LLM-processing metadata.
    Health entries (medications, food, symptoms) link back to this table.
    """

    __tablename__ = "checkins"

    id: Optional[int] = Field(default=None, primary_key=True)
    checkin_id: str = Field(index=True, unique=True)  # External ID like "CHK-001"
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    call_log_id: Optional[int] = Field(default=None, foreign_key="call_logs.id")

    # Check-in content
    patient_name: str
    checkin_type: str = Field(default="manual")  # "manual" | "voice" | "call"
    summary: str
    raw_content: Optional[str] = None  # Original text/transcript

    # Health data (from LLM extraction)
    health_topics: Optional[str] = None  # JSON array
    sentiment: Optional[str] = None  # "positive" | "neutral" | "negative"
    mood: Optional[str] = None
    energy_level: Optional[int] = None  # 1-10
    urgency_level: str = Field(default="routine")  # "routine" | "follow_up" | "urgent"

    # Extracted data flags
    has_medications: bool = Field(default=False)
    has_nutrition: bool = Field(default=False)
    has_symptoms: bool = Field(default=False)

    # Processing metadata
    is_processed: bool = Field(default=False)
    llm_model: Optional[str] = None
    processed_at: Optional[datetime] = None

    # Status tracking
    status: str = Field(
        default="pending"
    )  # "pending" | "reviewed" | "flagged" | "archived"
    provider_reviewed: bool = Field(default=False)
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None

    # Timestamps
    timestamp: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


# Notification Model


class Notification(rx.Model, table=True):
    """System notification for users."""

    __tablename__ = "notifications"

    id: Optional[int] = Field(default=None, primary_key=True)
    notification_id: str = Field(index=True, unique=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    recipient_role: str = Field(default="patient")  # "patient" | "admin"

    title: str
    message: str
    notification_type: str = Field(
        default="info"
    )  # "info" | "lab" | "treatment" | "appointment" | "warning" | "success"

    is_read: bool = Field(default=False)
    patient_id: Optional[str] = None  # Reference to patient external_id

    created_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Appointment Model
# =============================================================================


class Appointment(rx.Model, table=True):
    """Patient appointment for scheduling treatments and consultations."""

    __tablename__ = "appointments"

    id: Optional[int] = Field(default=None, primary_key=True)
    appointment_id: str = Field(index=True, unique=True)  # External ID like "APT001"
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)

    # Appointment details
    title: str
    description: Optional[str] = None
    date: str = Field(index=True)  # ISO date string "2025-01-16"
    time: str  # Time string "09:00"
    duration_minutes: int = Field(default=60)

    # Treatment info
    treatment_type: str = Field(default="Consultation")
    patient_id: Optional[str] = None  # Reference to patient external_id
    patient_name: str

    # Provider info
    provider: str  # e.g., "Dr. Johnson"

    # Status tracking
    status: str = Field(
        default="scheduled"
    )  # scheduled | confirmed | completed | cancelled
    notes: Optional[str] = None

    # Timestamps
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Extracted Health Data Tables (from LLM processing)
# =============================================================================


class MedicationEntry(rx.Model, table=True):
    """MedicationEntry entry extracted from check-ins.

    Normalized storage for dashboard queries and aggregations.
    Links back to CheckIn for traceability.
    """

    __tablename__ = "medication_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    call_log_id: Optional[int] = Field(
        default=None, foreign_key="call_logs.id", index=True
    )
    checkin_id: Optional[int] = Field(
        default=None, foreign_key="checkins.id", index=True
    )

    # MedicationEntry data (mirrors Pydantic MedicationEntry schema)
    name: str = Field(index=True)
    dosage: str = Field(default="")
    frequency: str = Field(default="")
    status: str = Field(default="active")  # active | discontinued | as-needed
    adherence_rate: float = Field(default=1.0)

    # Source tracking
    source: str = Field(default="call_log")  # call_log | voice | manual | seed
    mentioned_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class FoodLogEntry(rx.Model, table=True):
    """Food/nutrition entry extracted from check-ins.

    Normalized storage for nutrition tracking and dashboards.
    Links back to CheckIn for traceability.
    """

    __tablename__ = "food_log_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    call_log_id: Optional[int] = Field(
        default=None, foreign_key="call_logs.id", index=True
    )
    checkin_id: Optional[int] = Field(
        default=None, foreign_key="checkins.id", index=True
    )

    # Food data (mirrors Pydantic FoodEntry schema)
    name: str
    calories: int = Field(default=0)
    protein: float = Field(default=0.0)
    carbs: float = Field(default=0.0)
    fat: float = Field(default=0.0)
    meal_type: str = Field(default="snack")  # breakfast | lunch | dinner | snack
    consumed_at: Optional[str] = None  # Time string from transcript

    # Source tracking
    source: str = Field(default="call_log")  # call_log | voice | manual | seed
    logged_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class SymptomEntry(rx.Model, table=True):
    """Symptom entry extracted from check-ins.

    Normalized storage for symptom tracking and trend analysis.
    Links back to CheckIn for traceability.
    """

    __tablename__ = "symptom_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    call_log_id: Optional[int] = Field(
        default=None, foreign_key="call_logs.id", index=True
    )
    checkin_id: Optional[int] = Field(
        default=None, foreign_key="checkins.id", index=True
    )

    # Symptom data (mirrors Pydantic Symptom schema)
    name: str = Field(index=True)
    severity: str = Field(default="")  # mild | moderate | severe
    severity_score: int = Field(default=0)  # 0-10 scale
    frequency: str = Field(default="")
    trend: str = Field(default="stable")  # improving | worsening | stable
    notes: Optional[str] = None

    # Source tracking
    source: str = Field(default="call_log")  # call_log | voice | manual | seed
    reported_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Clinic Metrics Models (for admin dashboard charts)
# =============================================================================


class PatientVisit(rx.Model, table=True):
    """Patient visit record for tracking clinic trends.

    Tracks monthly patient visit statistics for admin dashboard charts.
    """

    __tablename__ = "patient_visits"

    id: Optional[int] = Field(default=None, primary_key=True)
    period: str = Field(index=True)  # e.g., "Jan", "Feb", "2025-01", etc.
    period_type: str = Field(default="month")  # "day" | "week" | "month" | "quarter"
    active_patients: int = Field(default=0)  # Count of active patients in period
    new_patients: int = Field(default=0)  # New patients added in period
    total_visits: int = Field(default=0)  # Total visits in period
    notes: Optional[str] = None
    recorded_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class TreatmentProtocolMetric(rx.Model, table=True):
    """Treatment protocol metrics for admin dashboard charts.

    Tracks aggregate treatment counts for admin dashboard.
    Renamed from TreatmentProtocol to avoid conflict with state TypedDict.
    """

    __tablename__ = "treatment_protocol_metrics"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "IV Therapy", "Cryo", etc.
    category: str = Field(default="general")  # Category of treatment
    active_count: int = Field(default=0)  # Number of active protocols
    completed_count: int = Field(default=0)  # Number of completed protocols
    success_rate: float = Field(default=0.0)  # Completion success rate %
    avg_duration_days: int = Field(default=0)  # Average protocol duration
    notes: Optional[str] = None
    updated_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class BiomarkerAggregate(rx.Model, table=True):
    """Aggregated biomarker scores for trend tracking.

    Tracks average biomarker improvements across patient cohorts.
    """

    __tablename__ = "biomarker_aggregates"

    id: Optional[int] = Field(default=None, primary_key=True)
    period: str = Field(index=True)  # e.g., "Wk 1", "Wk 4", "Month 1"
    period_type: str = Field(default="week")  # "week" | "month" | "quarter"
    avg_score: float = Field(default=0.0)  # Average biomarker score
    patient_count: int = Field(default=0)  # Number of patients in cohort
    improvement_pct: float = Field(default=0.0)  # % improvement from baseline
    notes: Optional[str] = None
    recorded_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class ClinicDailyMetrics(rx.Model, table=True):
    """Daily clinic operational metrics.

    Tracks daily throughput, wait times, room utilization.
    """

    __tablename__ = "clinic_daily_metrics"

    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(index=True)
    hour: Optional[int] = None  # 0-23, None for daily aggregate

    # Patient flow
    scheduled_appointments: int = Field(default=0)
    walkin_appointments: int = Field(default=0)
    completed_appointments: int = Field(default=0)
    no_shows: int = Field(default=0)

    # Efficiency metrics
    avg_wait_time_minutes: float = Field(default=0.0)
    avg_appointment_duration_minutes: float = Field(default=0.0)
    patient_throughput: float = Field(default=0.0)  # Patients per hour

    # Room utilization
    room_id: Optional[str] = None  # None for clinic-wide aggregates
    room_occupancy_pct: float = Field(default=0.0)
    treatments_completed: int = Field(default=0)

    created_at: datetime = Field(default_factory=utc_now)


class ProviderMetrics(rx.Model, table=True):
    """Provider performance metrics.

    Tracks provider efficiency and patient load.
    """

    __tablename__ = "provider_metrics"

    id: Optional[int] = Field(default=None, primary_key=True)
    provider_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    provider_name: str = Field(index=True)
    period: str = Field(index=True)  # e.g., "2025-01" for monthly
    period_type: str = Field(default="month")

    # Performance metrics
    patient_count: int = Field(default=0)
    efficiency_score: float = Field(default=0.0)  # 0-100%
    on_time_rate: float = Field(default=0.0)  # % appointments started on time
    avg_rating: float = Field(default=0.0)  # Patient satisfaction 0-5

    created_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Treatment Models (with user relationships)
# =============================================================================


class Treatment(rx.Model, table=True):
    """Treatment/protocol definition available at the clinic.

    This is the catalog of treatments that can be assigned to patients.
    """

    __tablename__ = "treatments"

    id: Optional[int] = Field(default=None, primary_key=True)
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

    Tracks which treatments are assigned to which patients.
    """

    __tablename__ = "patient_treatments"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    treatment_id: int = Field(foreign_key="treatments.id", index=True)

    # Assignment details
    assigned_by: Optional[str] = None  # Provider name or ID
    start_date: datetime = Field(default_factory=utc_now)
    end_date: Optional[datetime] = None
    status: str = Field(default="active")  # active | completed | paused | cancelled
    notes: Optional[str] = None

    # Progress tracking
    sessions_completed: int = Field(default=0)
    sessions_total: Optional[int] = None
    last_session_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Biomarker Models
# =============================================================================


class BiomarkerDefinition(rx.Model, table=True):
    """Biomarker definition catalog (reference data).

    Defines what biomarkers exist, their categories, units, and ranges.
    This is shared across all patients.
    """

    __tablename__ = "biomarker_definitions"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g. "VITAMIN_D", "HS_CRP"
    name: str = Field(index=True)  # Human-readable name
    category: str = Field(index=True)  # Metabolic, Inflammation, Hormones, etc.
    unit: str  # ng/mL, mg/dL, etc.
    description: str = Field(default="")

    # Reference ranges
    optimal_min: float = Field(default=0.0)
    optimal_max: float = Field(default=0.0)
    critical_min: float = Field(default=0.0)
    critical_max: float = Field(default=0.0)

    created_at: datetime = Field(default_factory=utc_now)


class BiomarkerReading(rx.Model, table=True):
    """Individual biomarker reading for a patient.

    Stores historical values for tracking trends over time.
    """

    __tablename__ = "biomarker_readings"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    biomarker_id: int = Field(foreign_key="biomarker_definitions.id", index=True)

    value: float
    status: str = Field(default="optimal")  # optimal | warning | critical
    trend: str = Field(default="stable")  # up | down | stable

    # Source tracking
    source: str = Field(default="lab")  # lab | manual | device
    measured_at: datetime = Field(index=True)  # When the reading was taken
    created_at: datetime = Field(default_factory=utc_now)


# =============================================================================
# Export all models
# =============================================================================

__all__ = [
    "User",
    "CallLog",
    "CallTranscript",
    "CallSummary",
    "CheckIn",
    "Notification",
    "MedicationEntry",
    "FoodLogEntry",
    "SymptomEntry",
    # Treatments
    "Treatment",
    "PatientTreatment",
    # Clinic metrics
    "PatientVisit",
    "TreatmentProtocolMetric",
    "BiomarkerAggregate",
    "ClinicDailyMetrics",
    "ProviderMetrics",
    # Biomarkers
    "BiomarkerDefinition",
    "BiomarkerReading",
]
