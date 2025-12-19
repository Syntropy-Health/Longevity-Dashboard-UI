"""Pydantic schemas for LLM structured output with ToolStrategy pattern.

Combines multiple output schemas for call log processing.
"""

from typing import List
from pydantic import BaseModel, Field

# Import Pydantic models from central schema module (using canonical names)
from .state_schemas import MedicationEntry, FoodEntry, Symptom


class CheckInSummary(BaseModel):
    """Summary check-in data from call log."""

    id: str = Field(default="", description="Check-in ID")
    type: str = Field(default="call", description="voice/text/call")
    summary: str = Field(default="", description="Clinical summary")
    timestamp: str = Field(default="", description="ISO timestamp")
    sentiment: str = Field(default="neutral", description="positive/negative/neutral")
    key_topics: List[str] = Field(default_factory=list, description="Health topics")
    provider_reviewed: bool = Field(default=False)
    patient_name: str = Field(default="")


class CallLogsOutput(BaseModel):
    """Combined structured output from call log processing.

    ToolStrategy pattern: single schema combining all extractable data.
    """

    checkin: CheckInSummary = Field(
        default_factory=CheckInSummary, description="Check-in summary data"
    )
    medications_entries: List[MedicationEntry] = Field(
        default_factory=list, description="Medications mentioned"
    )
    food_entries: List[FoodEntry] = Field(
        default_factory=list, description="Food/nutrition mentioned"
    )
    symptom_entries: List[Symptom] = Field(
        default_factory=list, description="Symptoms mentioned"
    )
    has_medications: bool = Field(
        default=False, description="True if medications were discussed"
    )
    has_nutrition: bool = Field(
        default=False, description="True if ingesting anything was discussed"
    )
    has_symptoms: bool = Field(
        default=False, description="True if symptoms were discussed"
    )

    def to_checkin_dict(self) -> dict:
        """Convert checkin to dict for state storage."""
        return self.checkin.model_dump()
