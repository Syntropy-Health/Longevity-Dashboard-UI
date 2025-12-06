"""
State schema definitions (TypedDicts and Pydantic models) used across state management.

This module centralizes all TypedDict definitions that are used in Reflex state
classes, separating data structure definitions from state logic.
"""

from typing import List, TypedDict
from pydantic import BaseModel, Field


# =============================================================================
# Patient Schemas (from demo.py)
# =============================================================================


class Patient(TypedDict):
    """Patient data type."""

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


class ChartData(TypedDict):
    """Chart data type for patient analytics."""

    name: str
    value: int
    value2: int


# =============================================================================
# Patient Dashboard Schemas (from demo.py)
# =============================================================================


class NutritionSummary(TypedDict):
    """Nutrition summary type."""

    total_calories: int
    goal_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float
    water_intake: float


class FoodEntry(TypedDict):
    """Food entry type."""

    id: str
    name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    time: str
    meal_type: str


class Medication(TypedDict):
    """Medication type."""

    id: str
    name: str
    dosage: str
    frequency: str
    status: str
    adherence_rate: float


class Condition(TypedDict):
    """Health condition type."""

    id: str
    name: str
    icd_code: str
    diagnosed_date: str
    status: str
    severity: str
    treatments: str


class Symptom(TypedDict):
    """Symptom type."""

    id: str
    name: str
    severity: str
    frequency: str
    trend: str


class SymptomLog(TypedDict):
    """Symptom log entry type."""

    id: str
    symptom_name: str
    severity: int
    notes: str
    timestamp: str


class Reminder(TypedDict):
    """Health reminder type."""

    id: str
    title: str
    description: str
    time: str
    type: str  # medication, appointment, checkup, exercise
    completed: bool


class SymptomTrend(TypedDict):
    """Symptom trend data type."""

    id: str
    symptom_name: str
    current_severity: int
    previous_severity: int
    trend: str  # improving, worsening, stable
    change_percent: float
    period: str


class DataSource(TypedDict):
    """Data source type."""

    id: str
    name: str
    type: str
    status: str
    icon: str
    image: str
    last_sync: str
    connected: bool


class CheckIn(TypedDict):
    """Check-in entry type."""

    id: str
    type: str
    summary: str
    timestamp: str
    sentiment: str
    key_topics: List[str]
    provider_reviewed: bool
    patient_name: str  # Added for admin view


class CheckInModel(BaseModel):
    """Pydantic model for structured LLM output of check-in summaries."""

    id: str = Field(description="Unique identifier for the check-in")
    type: str = Field(description="Type of check-in: 'voice', 'text', or 'call'")
    summary: str = Field(
        description="Concise clinical summary of the check-in focusing on key health concerns, symptoms, and updates"
    )
    timestamp: str = Field(description="ISO timestamp of when the check-in occurred")
    sentiment: str = Field(
        default="neutral",
        description="Sentiment of the check-in: 'positive', 'negative', or 'neutral'",
    )
    key_topics: List[str] = Field(
        default_factory=list,
        description="List of key health topics mentioned (e.g., 'fatigue', 'sleep', 'pain')",
    )
    provider_reviewed: bool = Field(
        default=False,
        description="Whether a healthcare provider has reviewed this check-in",
    )
    patient_name: str = Field(
        default="", description="Name of the patient associated with this check-in"
    )

    def to_dict(self) -> CheckIn:
        """Convert Pydantic model to TypedDict for state storage."""
        return {
            "id": self.id,
            "type": self.type,
            "summary": self.summary,
            "timestamp": self.timestamp,
            "sentiment": self.sentiment,
            "key_topics": self.key_topics,
            "provider_reviewed": self.provider_reviewed,
            "patient_name": self.patient_name,
        }


# =============================================================================
# Call Log Schemas (from patient_state.py)
# =============================================================================


class CallLogEntry(TypedDict):
    """Call log entry from the API."""

    id: int
    caller_phone: str
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
# Admin Check-in Schemas (from admin_checkins_state.py)
# =============================================================================


class AdminCheckIn(TypedDict):
    """Admin check-in entry type."""

    id: str
    patient_id: str
    patient_name: str
    type: str  # voice, text, or call
    summary: str
    timestamp: str
    submitted_at: str  # For sorting
    sentiment: str
    key_topics: List[str]
    status: str  # pending, reviewed, flagged
    provider_reviewed: bool
    reviewed_by: str
    reviewed_at: str


# =============================================================================
# Auth Schemas (from auth_state.py)
# =============================================================================


class User(TypedDict):
    """User account type."""

    id: str
    username: str
    email: str
    role: str
    full_name: str


# =============================================================================
# Biomarker Schemas (from patient_biomarker_state.py)
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
# Notification Schemas (from notification_state.py)
# =============================================================================


class Notification(TypedDict):
    """Structure for a notification."""

    id: str
    title: str
    message: str
    type: (
        str  # "info", "warning", "success", "error", "appointment", "treatment", "lab"
    )
    is_read: bool
    created_at: str
    recipient_role: str  # "admin", "patient", "all"
    patient_id: str | None


# =============================================================================
# Treatment Schemas (from treatment_state.py)
# =============================================================================


class TreatmentProtocol(TypedDict):
    """Treatment protocol definition."""

    id: str
    name: str
    category: str
    description: str
    duration: str
    frequency: str
    cost: float
    status: str


# =============================================================================
# Appointment Schemas (from appointment_state.py)
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
    status: str  # "scheduled", "confirmed", "completed", "cancelled"
    notes: str


class TimeSlot(TypedDict):
    """Available time slot structure."""

    time: str
    is_available: bool
