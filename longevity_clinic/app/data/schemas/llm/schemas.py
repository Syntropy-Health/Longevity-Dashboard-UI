"""Pydantic schemas for LLM structured output.

These models are used for:
1. LLM structured output extraction (with ToolStrategy pattern)
2. Call log processing
3. Check-in health data extraction

Naming convention: <Entity>Model for Pydantic models that mirror DB entities,
to distinguish from state TypedDicts.
"""

from pydantic import BaseModel, Field

from longevity_clinic.app.data.schemas.db.domain_enums import (
    MealTypeEnum,
    SentimentEnum,
    SeverityLevelEnum,
    SymptomTrendEnum,
)

# =============================================================================
# Health Entry Models (for LLM extraction)
# =============================================================================


class FoodEntryModel(BaseModel):
    """Food/nutrition entry extracted from patient transcript.

    Create ONE entry per distinct food item. If patient mentions "eggs and toast",
    create separate entries for eggs and toast.
    """

    name: str = Field(
        default="",
        description="Food item name. Be specific (e.g., 'scrambled eggs' not just 'eggs').",
    )
    amount: str = Field(
        default="",
        description="Quantity or serving size as stated (e.g., '2 cups', 'a bowl', 'large portion'). Estimate if context suggests size.",
    )
    calories: int = Field(
        default=0,
        description="Estimated calories based on typical serving. Use common food knowledge to estimate.",
    )
    protein: float = Field(
        default=0.0,
        description="Estimated protein in grams. Use common food knowledge (e.g., egg ~6g, chicken breast ~25g).",
    )
    carbs: float = Field(
        default=0.0,
        description="Estimated carbohydrates in grams. Use common food knowledge (e.g., bread slice ~15g, rice cup ~45g).",
    )
    fat: float = Field(
        default=0.0,
        description="Estimated fat in grams. Use common food knowledge (e.g., egg ~5g, avocado ~15g).",
    )
    time: str | None = Field(
        default=None,
        description="Time consumed if explicitly stated (e.g., '8am', 'morning'). None if not mentioned.",
    )
    meal_type: MealTypeEnum = Field(
        default=MealTypeEnum.SNACK,
        description="Meal category. Infer from time of day or context if not stated directly.",
    )
    logged_at: str | None = Field(
        default=None,
        description="ISO timestamp when the entry was logged (set by database).",
    )


class MedicationEntryModel(BaseModel):
    """Medication intake log extracted from patient transcript.

    Create ONE entry per medication/supplement mentioned.
    """

    id: str = Field(
        default="",
        description="Unique identifier (set by database)",
    )
    name: str = Field(
        default="",
        description="Medication or supplement name exactly as mentioned (e.g., 'lisinopril', 'vitamin D').",
    )
    dosage: str = Field(
        default="",
        description="Dosage with units if stated (e.g., '10mg', '500mg'). Leave empty only if truly not mentioned.",
    )
    taken_at: str | None = Field(
        default=None,
        description="When taken if explicitly stated (e.g., 'this morning'). None if not mentioned.",
    )
    notes: str = Field(
        default="",
        description="Additional context like 'with food', 'missed yesterday', 'felt dizzy after'. Keep brief.",
    )


class PatientTreatmentModel(BaseModel):
    """Patient treatment assignment - Pydantic model for state.

    Represents a treatment assigned to a patient, including medications.
    For Medications category: includes dosage and adherence tracking.
    Maps to PatientTreatment database model.
    """

    id: str = Field(default="", description="Unique identifier")
    name: str = Field(default="", description="Treatment name")
    category: str = Field(default="", description="Treatment category")
    dosage: str = Field(default="", description="Dosage (for medications)")
    frequency: str = Field(default="", description="How often")
    instructions: str = Field(default="", description="Taking instructions")
    status: str = Field(default="active", description="active/completed/paused")
    adherence_rate: float = Field(default=100.0, description="Adherence rate 0-100%")
    assigned_by: str = Field(default="", description="Assigning provider")
    sessions_completed: int = Field(default=0, description="Sessions completed")
    sessions_total: int | None = Field(default=None, description="Total sessions")


class Symptom(BaseModel):
    """Symptom or health concern extracted from patient transcript.

    Create ONE entry per distinct symptom. Group related complaints
    (e.g., 'joint pain in knees and shoulders' = one entry for 'joint pain').
    """

    name: str = Field(
        default="",
        description="Symptom name using standard medical terms when possible (e.g., 'headache', 'fatigue', 'nausea').",
    )
    severity: SeverityLevelEnum = Field(
        default=SeverityLevelEnum.UNKNOWN,
        description="Severity level. Infer from patient's language (e.g., 'terrible' → severe, 'a bit' → mild). Use UNKNOWN if unclear.",
    )
    frequency: str = Field(
        default="UNKNOWN",
        description="How often it occurs (e.g., 'daily', 'occasional', 'constant'). Use 'unknown' if not mentioned.",
    )
    trend: SymptomTrendEnum = Field(
        default=SymptomTrendEnum.UNKNOWN,
        description="Change over time. Infer from phrases like 'getting better', 'worse than before'. Use UNKNOWN if first report or unclear.",
    )


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

    id: str = Field(default="", description="Unique identifier (set by database)")
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
    """Check-in summary extracted from patient transcript."""

    id: str = Field(
        default="",
        description="Leave empty - system generated.",
    )
    type: str = Field(
        default="call",
        description="Leave as default - system sets this.",
    )
    summary: str = Field(
        default="",
        description="Concise clinical summary (2-3 sentences). Focus on: main concerns, actions taken, patient mood/outlook.",
    )
    timestamp: str | None = Field(
        default=None,
        description="Only set if a specific date/time is explicitly stated in transcript. None otherwise.",
    )
    sentiment: SentimentEnum = Field(
        default=SentimentEnum.UNKNOWN,
        description="Overall tone. Positive = improving/hopeful, Negative = concerning/frustrated, Neutral = routine update. UNKNOWN if unclear.",
    )
    key_topics: list[str] = Field(
        default_factory=list,
        description="Main health topics (max 5). Use keywords like: sleep, diet, medication, pain, energy, mood, exercise.",
    )
    provider_reviewed: bool = Field(
        default=False,
        description="Always False - system updates after provider review.",
    )
    patient_name: str = Field(
        default="",
        description="Patient name if they identify themselves. Empty if not stated.",
    )


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
    sentiment: SentimentEnum = Field(
        default=SentimentEnum.NEUTRAL,
        description="Sentiment of the check-in: positive, negative, or neutral.",
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
    """Structured health data extracted from patient check-in transcript.

    Extract all health-related information mentioned by the patient.
    Be thorough but avoid duplicates - each distinct item gets ONE entry.
    Use your knowledge to estimate nutritional values for foods.
    """

    checkin: CheckInSummary = Field(
        default_factory=CheckInSummary,
        description="Overall summary of the conversation. Always include.",
    )
    medications_entries: list[MedicationEntryModel] = Field(
        default_factory=list,
        description="ONE entry per medication/supplement mentioned. Do not duplicate if patient mentions same medication twice.",
    )
    food_entries: list[FoodEntryModel] = Field(
        default_factory=list,
        description="ONE entry per distinct food item. 'Eggs and toast' = 2 entries. Estimate nutrition based on typical portions.",
    )
    symptom_entries: list[Symptom] = Field(
        default_factory=list,
        description="ONE entry per symptom type. Group related complaints (e.g., 'knee and hip pain' = one 'joint pain' entry).",
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
