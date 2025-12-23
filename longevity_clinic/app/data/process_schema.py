"""Pydantic schemas for LLM structured output with ToolStrategy pattern.

Combines multiple output schemas for call log processing.
"""

from pydantic import BaseModel, Field

# Import Pydantic models from central schema module (using canonical names)
from .state_schemas import FoodEntry, MedicationEntry, Symptom


class CheckInSummary(BaseModel):
    """Summary check-in data from call log."""

    id: str = Field(default="", description="Check-in ID")
    type: str = Field(default="call", description="voice/text/call")
    summary: str = Field(default="", description="Clinical summary")
    timestamp: str = Field(default="", description="ISO timestamp")
    sentiment: str = Field(default="neutral", description="positive/negative/neutral")
    key_topics: list[str] = Field(default_factory=list, description="Health topics")
    provider_reviewed: bool = Field(default=False)
    patient_name: str = Field(default="")


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
    medications_entries: list[MedicationEntry] = Field(
        default_factory=list, description="Medications mentioned"
    )
    food_entries: list[FoodEntry] = Field(
        default_factory=list, description="Any Food/nutrition mentioned"
    )
    symptom_entries: list[Symptom] = Field(
        default_factory=list, description="Any health-related symptoms mentioned"
    )
