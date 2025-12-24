"""Pydantic schemas for LLM structured output.

These models are used for:
1. LLM structured output extraction (with ToolStrategy pattern)
2. Call log processing
3. Check-in health data extraction

Naming convention: <Entity>Model for Pydantic models that mirror DB entities,
to distinguish from state TypedDicts.
"""

from pydantic import BaseModel, Field


# =============================================================================
# Health Entry Models (for LLM extraction)
# =============================================================================


class FoodEntryModel(BaseModel):
    """Food entry - Pydantic model for LLM extraction.

    Used by MetricLogsOutput for structured extraction from transcripts.
    Maps to FoodLogEntry database model.
    """

    name: str = Field(default="", description="Food, supplement or edible item name")
    calories: int = Field(default=0, description="Estimated calories")
    protein: float = Field(default=0.0, description="Protein in grams")
    carbs: float = Field(default=0.0, description="Carbs in grams")
    fat: float = Field(default=0.0, description="Fat in grams")
    time: str = Field(default="", description="Time consumed")
    meal_type: str = Field(
        default="snack", description="breakfast/lunch/dinner/snack/supplement"
    )


class MedicationEntryModel(BaseModel):
    """Medication entry - Pydantic model for LLM extraction.

    Used by MetricLogsOutput for structured extraction from transcripts.
    Maps to MedicationEntry database model.
    """

    id: str = Field(default="", description="Unique identifier")
    name: str = Field(default="", description="Medication name")
    dosage: str = Field(default="", description="Dosage amount and unit")
    frequency: str = Field(default="", description="How often taken")
    status: str = Field(default="active", description="active/discontinued/as-needed")
    adherence_rate: float = Field(default=1.0, description="Adherence rate 0-1")


class Symptom(BaseModel):
    """Symptom - Pydantic model for LLM extraction.

    Used by MetricLogsOutput for structured extraction from transcripts.
    Maps to SymptomEntry database model.
    """

    name: str = Field(default="", description="Symptom name")
    severity: str = Field(default="", description="Severity level")
    frequency: str = Field(default="", description="Frequency of occurrence")
    trend: str = Field(default="", description="Trend direction")


class SymptomEntryModel(BaseModel):
    """Symptom log entry - Pydantic model for LLM extraction.

    Used for detailed symptom tracking with timestamps.
    """

    id: str = Field(default="", description="Unique identifier")
    symptom_name: str = Field(default="", description="Symptom name")
    severity: int = Field(default=0, description="Severity rating 0-10")
    notes: str = Field(default="", description="Additional notes")
    timestamp: str = Field(default="", description="Log timestamp")


class Condition(BaseModel):
    """Health condition - Pydantic model for LLM extraction.

    Used for extracting medical conditions from transcripts.
    """

    name: str = Field(default="", description="Condition name")
    icd_code: str = Field(default="", description="ICD diagnosis code")
    diagnosed_date: str = Field(default="", description="Date diagnosed")
    status: str = Field(default="active", description="active/managed/resolved")
    severity: str = Field(default="", description="Severity level")
    treatments: str = Field(default="", description="Current treatments")


class SymptomTrend(BaseModel):
    """Symptom trend - Pydantic model for tracking changes over time."""

    id: str = Field(default="", description="Unique identifier")
    symptom_name: str = Field(default="", description="Symptom name")
    current_severity: int = Field(default=0, description="Current severity 0-10")
    previous_severity: int = Field(default=0, description="Previous severity 0-10")
    trend: str = Field(default="stable", description="improving/worsening/stable")
    change_percent: float = Field(default=0.0, description="Percent change")
    period: str = Field(default="", description="Time period")


class DataSource(BaseModel):
    """Data source - Pydantic model for device/app integrations."""

    id: str = Field(default="", description="Unique identifier")
    name: str = Field(default="", description="Data source name")
    type: str = Field(default="", description="wearable/scale/cgm/app/ehr")
    status: str = Field(default="disconnected", description="connected/disconnected")
    icon: str = Field(default="", description="Icon name")
    image: str = Field(default="", description="Image URL")
    last_sync: str = Field(default="", description="Last sync time")
    connected: bool = Field(default=False, description="Connection status")


# =============================================================================
# Check-in Models (for LLM extraction)
# =============================================================================


class CheckInSummary(BaseModel):
    """Summary check-in data from call log.

    Used by MetricLogsOutput as the check-in component.
    """

    id: str = Field(default="", description="Check-in ID")
    type: str = Field(default="call", description="voice/text/call")
    summary: str = Field(default="", description="Clinical summary")
    timestamp: str = Field(default="", description="ISO timestamp")
    sentiment: str = Field(default="neutral", description="positive/negative/neutral")
    key_topics: list[str] = Field(default_factory=list, description="Health topics")
    provider_reviewed: bool = Field(default=False)
    patient_name: str = Field(default="")


class CheckInModel(BaseModel):
    """Pydantic model for structured LLM output of check-in summaries.

    More detailed than CheckInSummary, with full descriptions for LLM guidance.
    """

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
    key_topics: list[str] = Field(
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


# =============================================================================
# Combined Output Models (ToolStrategy pattern)
# =============================================================================


class MetricLogsOutput(BaseModel):
    """Combined structured output from call log processing.

    ToolStrategy pattern: single schema combining all extractable data.
    Used by both patient check-ins (voice/text) and CDC call log processing.

    Data Flow:
    1. Patient check-ins: save_checkin_and_log_health() → parse_checkin_with_health_data()
       → MetricLogsOutput → create_checkin_sync() + save_health_entries_sync()
    2. Call logs: VlogsAgent.process_unprocessed_logs() → update_call_log_metrics()
       → Persists to CheckIn, MedicationEntry, FoodLogEntry, SymptomEntry tables

    Dashboard data is fetched via HealthDashboardState using get_*_sync() functions.
    """

    checkin: CheckInSummary = Field(
        default_factory=CheckInSummary, description="Check-in summary data"
    )
    medications_entries: list[MedicationEntryModel] = Field(
        default_factory=list, description="Medications"
    )
    food_entries: list[FoodEntryModel] = Field(
        default_factory=list, description="Food or Nutrition"
    )
    symptom_entries: list[Symptom] = Field(
        default_factory=list, description="Health-related symptoms"
    )


__all__ = [
    "CheckInModel",
    "CheckInSummary",
    "Condition",
    "DataSource",
    "FoodEntryModel",
    "MedicationEntryModel",
    "MetricLogsOutput",
    "Symptom",
    "SymptomEntryModel",
    "SymptomTrend",
]
