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
    """AI-generated summary and extracted data from a call."""

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
    """Patient check-in record (manual or from call)."""

    __tablename__ = "checkins"

    id: Optional[int] = Field(default=None, primary_key=True)
    checkin_id: str = Field(index=True, unique=True)  # External ID like "CHK-001"
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    call_log_id: Optional[int] = Field(default=None, foreign_key="call_logs.id")

    # Check-in content
    patient_name: str
    checkin_type: str = Field(default="manual")  # "manual" | "voice" | "call_log"
    summary: str
    raw_content: Optional[str] = None  # Original text/transcript

    # Health data
    health_topics: Optional[str] = None  # JSON array
    mood: Optional[str] = None
    energy_level: Optional[int] = None  # 1-10

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
# Extracted Health Data Tables (from LLM processing)
# =============================================================================


class MedicationEntry(rx.Model, table=True):
    """MedicationEntry entry extracted from call logs.

    Normalized storage for dashboard queries and aggregations.
    Source of truth: CallSummary.medications_json (denormalized)
    """

    __tablename__ = "medication_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    call_log_id: Optional[int] = Field(
        default=None, foreign_key="call_logs.id", index=True
    )
    summary_id: Optional[int] = Field(
        default=None, foreign_key="call_summaries.id", index=True
    )

    # MedicationEntry data (mirrors Pydantic MedicationEntry schema)
    name: str = Field(index=True)
    dosage: str = Field(default="")
    frequency: str = Field(default="")
    status: str = Field(default="active")  # active | discontinued | as-needed
    adherence_rate: float = Field(default=1.0)

    # Source tracking
    source: str = Field(default="call_log")  # call_log | manual | import
    mentioned_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class FoodLogEntry(rx.Model, table=True):
    """Food/nutrition entry extracted from call logs.

    Normalized storage for nutrition tracking and dashboards.
    Source of truth: CallSummary.food_entries_json (denormalized)
    """

    __tablename__ = "food_log_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    call_log_id: Optional[int] = Field(
        default=None, foreign_key="call_logs.id", index=True
    )
    summary_id: Optional[int] = Field(
        default=None, foreign_key="call_summaries.id", index=True
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
    source: str = Field(default="call_log")  # call_log | manual | import
    logged_at: datetime = Field(default_factory=utc_now)
    created_at: datetime = Field(default_factory=utc_now)


class SymptomEntry(rx.Model, table=True):
    """Symptom entry extracted from call logs.

    Normalized storage for symptom tracking and trend analysis.
    Source of truth: CallSummary.symptoms_json (denormalized)
    """

    __tablename__ = "symptom_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    call_log_id: Optional[int] = Field(
        default=None, foreign_key="call_logs.id", index=True
    )
    summary_id: Optional[int] = Field(
        default=None, foreign_key="call_summaries.id", index=True
    )

    # Symptom data (mirrors Pydantic Symptom schema)
    name: str = Field(index=True)
    severity: str = Field(default="")  # mild | moderate | severe
    severity_score: int = Field(default=0)  # 0-10 scale
    frequency: str = Field(default="")
    trend: str = Field(default="stable")  # improving | worsening | stable
    notes: Optional[str] = None

    # Source tracking
    source: str = Field(default="call_log")  # call_log | manual | import
    reported_at: datetime = Field(default_factory=utc_now)
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
]
