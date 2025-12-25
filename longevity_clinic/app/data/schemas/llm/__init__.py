"""
LLM-related Pydantic models for structured output.

Contains schemas used for:
- LLM structured output extraction
- Check-in processing
- Health data parsing

Usage:
    from longevity_clinic.app.data.schemas.llm import MetricLogsOutput, CheckInSummary
"""

from .schemas import (
    CheckInModel,
    CheckInSummary,
    Condition,
    DataSource,
    FoodEntryModel,
    MedicationEntryModel,
    MedicationSubscriptionModel,  # Alias → PatientTreatmentModel (backward compat)
    MetricLogsOutput,
    PatientTreatmentModel,
    Symptom,
    SymptomEntryModel,
    SymptomTrend,
)

__all__ = [
    "CheckInModel",
    "CheckInSummary",
    "Condition",
    "DataSource",
    "FoodEntryModel",
    "MedicationEntryModel",
    "MedicationSubscriptionModel",  # Alias → PatientTreatmentModel (backward compat)
    "MetricLogsOutput",
    "PatientTreatmentModel",
    "Symptom",
    "SymptomEntryModel",
    "SymptomTrend",
]
