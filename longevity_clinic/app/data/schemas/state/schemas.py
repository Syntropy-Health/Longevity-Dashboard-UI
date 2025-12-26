"""
State schema definitions (TypedDicts) for Reflex state management.

This module contains TypedDict definitions that are used in Reflex state
classes for type-safe state management. These are NOT Pydantic models -
use schemas/llm/ for LLM-related Pydantic models.

Naming convention: Plain names for TypedDicts (e.g., Patient, CheckIn)
since they're used directly in component props.
"""

from typing import TypedDict

# =============================================================================
# Patient Schemas
# =============================================================================


class Patient(TypedDict):
    """Patient data type for admin patient list views."""

    id: str
    full_name: str
    email: str
    phone: str
    age: int
    gender: str
    last_visit: str
    status: str
    biomarker_score: int
    medical_history: str
    next_appointment: str
    assigned_treatments: list[dict]


# =============================================================================
# Patient Dashboard Schemas
# =============================================================================


class NutritionSummary(TypedDict):
    """Nutrition summary for patient dashboard."""

    total_calories: int
    goal_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float
    water_intake: float


class Reminder(TypedDict):
    """Health reminder type."""

    id: str
    title: str
    description: str
    time: str
    type: str  # medication, appointment, checkup, exercise
    completed: bool


# =============================================================================
# Check-in Schemas
# =============================================================================


class CheckIn(TypedDict):
    """Check-in entry type for patient views."""

    id: str
    type: str
    summary: str
    timestamp: str
    sentiment: str
    key_topics: list[str]
    provider_reviewed: bool
    patient_name: str


class CheckInWithTranscript(TypedDict):
    """Check-in with raw_transcript for display fallback."""

    id: str
    type: str
    summary: str
    raw_transcript: str
    timestamp: str
    sentiment: str
    key_topics: list[str]
    provider_reviewed: bool
    patient_name: str
    status: str


class AdminCheckIn(TypedDict):
    """Admin check-in entry type with additional fields."""

    id: str
    patient_id: str
    patient_name: str
    type: str  # voice, text, or call
    summary: str
    raw_transcript: str
    timestamp: str
    submitted_at: str
    sentiment: str
    key_topics: list[str]
    status: str  # pending, reviewed, flagged
    provider_reviewed: bool
    reviewed_by: str
    reviewed_at: str


class CheckInBasic(TypedDict):
    """Minimal check-in for user lists."""

    id: str
    type: str
    summary: str
    timestamp: str
    status: str


class CheckInStatusUpdate(TypedDict):
    """Result of status update operation."""

    id: str
    status: str
    reviewed_by: str
    reviewed_at: str


class CheckInCreated(TypedDict):
    """Result of check-in creation."""

    id: str
    db_id: int
    patient_name: str
    summary: str
    status: str


# =============================================================================
# Call Log Schemas
# =============================================================================


class CallerPhoneExpanded(TypedDict, total=False):
    """Expanded caller phone information from API."""

    phone_number: str
    customer_name: str | None
    first_call_date: str | None
    last_call_date: str | None
    notes: str | None
    calls: list[int]


class CallLogEntry(TypedDict):
    """Call log entry from the API.

    caller_phone can be either a string (E.164 format) or CallerPhoneExpanded dict
    when using fields=*.* in API request.
    """

    id: int
    caller_phone: str | CallerPhoneExpanded
    call_date: str
    call_duration: int
    summary: str
    full_transcript: str
    notes: str
    call_id: str


class TranscriptSummary(TypedDict):
    """Processed transcript summary for display."""

    call_id: str
    patient_phone: str
    call_date: str
    summary: str
    ai_summary: str
    type: str  # "call" to distinguish from regular check-ins
    timestamp: str


# =============================================================================
# Auth Schemas
# =============================================================================


class User(TypedDict):
    """User account type for auth state."""

    id: str
    username: str
    email: str
    role: str
    full_name: str


# =============================================================================
# Biomarker Schemas
# =============================================================================


class BiomarkerDataPoint(TypedDict):
    """Single biomarker measurement data point."""

    date: str
    value: float


class Biomarker(TypedDict):
    """Complete biomarker with history and thresholds."""

    id: str
    name: str
    category: str
    unit: str
    description: str
    optimal_min: float
    optimal_max: float
    critical_min: float
    critical_max: float
    current_value: float
    status: str
    trend: str
    history: list[BiomarkerDataPoint]


class BiomarkerMetricSeed(TypedDict):
    """Seed data used to build biomarker metrics with generated history.

    Used in seed/biomarkers.py to define initial biomarker test values.
    """

    metric: str  # BiomarkerMetricNameEnum value
    value: float
    unit: str  # MeasurementUnitEnum value
    status: str  # BiomarkerStatusEnum value
    reference_range: str
    history_seed: tuple[float, float]  # (base_value, volatility)


class BiomarkerMetric(TypedDict):
    """Single biomarker metric for display in panels."""

    name: str
    value: float
    unit: str
    status: str
    reference_range: str
    history: list[dict]


class BiomarkerCategoryPanel(TypedDict):
    """Biomarker category panel grouping multiple metrics."""

    category: str
    metrics: list[BiomarkerMetric]


class PortalAppointment(TypedDict):
    """Patient portal appointment type."""

    id: str
    title: str
    date: str
    time: str
    type: str
    provider: str


class PortalTreatment(TypedDict):
    """Patient portal treatment type."""

    id: str
    name: str
    frequency: str
    duration: str
    category: str
    status: str


# =============================================================================
# Notification Schemas
# =============================================================================


class Notification(TypedDict):
    """Structure for a notification."""

    id: str
    title: str
    message: str
    type: str  # info, warning, success, error, appointment, treatment, lab
    is_read: bool
    created_at: str
    recipient_role: str  # admin, patient, all
    patient_id: str | None


# =============================================================================
# Treatment Schemas
# =============================================================================


class TreatmentProtocol(TypedDict):
    """Treatment protocol definition for state/UI."""

    id: str
    name: str
    category: str
    description: str
    duration: str
    frequency: str
    cost: float
    status: str


class TreatmentCategoryGroup(TypedDict):
    """Grouped treatments by category for collapsible display."""

    category: str
    treatments: list[TreatmentProtocol]
    count: int


# =============================================================================
# Appointment Schemas
# =============================================================================


class Appointment(TypedDict):
    """Structure for an appointment."""

    id: str
    title: str
    description: str
    date: str  # ISO format YYYY-MM-DD
    time: str  # HH:MM format
    duration_minutes: int
    treatment_type: str
    patient_id: str
    patient_name: str
    provider: str
    status: str  # scheduled, confirmed, completed, cancelled
    notes: str


class TimeSlot(TypedDict):
    """Available time slot structure."""

    time: str
    is_available: bool


__all__ = [
    "AdminCheckIn",
    "Appointment",
    "Biomarker",
    "BiomarkerCategoryPanel",
    "BiomarkerDataPoint",
    "BiomarkerMetric",
    "BiomarkerMetricSeed",
    "CallLogEntry",
    "CheckIn",
    "CheckInWithTranscript",
    "Notification",
    "NutritionSummary",
    "Patient",
    "PortalAppointment",
    "PortalTreatment",
    "Reminder",
    "TimeSlot",
    "TranscriptSummary",
    "TreatmentCategoryGroup",
    "TreatmentProtocol",
    "User",
]
