"""
State schemas for Reflex state management.

Contains:
- TypedDict definitions for type hints and dict-based state
- Pydantic models (suffixed with StateModel) for Reflex foreach compatibility

Usage:
    from longevity_clinic.app.data.schemas.state import Patient, FoodEntryStateModel
"""

from .schemas import (
    AdminCheckIn,
    Appointment,
    Biomarker,
    BiomarkerCategoryPanel,
    BiomarkerDataPoint,
    BiomarkerMetric,
    BiomarkerMetricSeed,
    CallerPhoneExpanded,
    CallLogEntry,
    CheckIn,
    CheckInBasic,
    CheckInCreated,
    CheckInStatusUpdate,
    CheckInWithTranscript,
    FoodEntry,
    FoodEntryStateModel,
    MedicationLogEntry,
    MedicationLogEntryStateModel,
    Notification,
    NutritionSummary,
    Patient,
    PortalAppointment,
    PortalTreatment,
    Prescription,
    PrescriptionStateModel,
    Reminder,
    SymptomLogEntry,
    TimeSlot,
    TranscriptSummary,
    TreatmentCategoryGroup,
    TreatmentProtocol,
    User,
)

__all__ = [
    "AdminCheckIn",
    "Appointment",
    "Biomarker",
    "BiomarkerCategoryPanel",
    "BiomarkerDataPoint",
    "BiomarkerMetric",
    "BiomarkerMetricSeed",
    "CallLogEntry",
    "CallerPhoneExpanded",
    "CheckIn",
    "CheckInBasic",
    "CheckInCreated",
    "CheckInStatusUpdate",
    "CheckInWithTranscript",
    "FoodEntry",
    "FoodEntryStateModel",
    "MedicationLogEntry",
    "MedicationLogEntryStateModel",
    "Notification",
    "NutritionSummary",
    "Patient",
    "PortalAppointment",
    "PortalTreatment",
    "Prescription",
    "PrescriptionStateModel",
    "Reminder",
    "SymptomLogEntry",
    "TimeSlot",
    "TranscriptSummary",
    "TreatmentCategoryGroup",
    "TreatmentProtocol",
    "User",
]
