"""
Schemas module for Longevity Clinic application.

Organized into submodules:
- db/: Database models (rx.Model/SQLModel) and enum tables
- state/: TypedDict schemas for Reflex state management
- llm/: Pydantic models for LLM structured output

Usage:
    from longevity_clinic.app.data.schemas import User, CheckIn, FoodEntry
    from longevity_clinic.app.data.schemas.db import Treatment, BiomarkerDefinition
    from longevity_clinic.app.data.schemas.state import Patient, Notification
    from longevity_clinic.app.data.schemas.llm import MetricLogsOutput, CheckInSummary
"""

# Re-export commonly used schemas for convenience
from .db import (
    # Core models
    Appointment,
    BiomarkerAggregate,
    BiomarkerCategory,
    BiomarkerDefinition,
    BiomarkerReading,
    CallLog,
    CallTranscript,
    CheckIn,
    CheckInType,
    ClinicDailyMetrics,
    FoodLogEntry,
    MedicationEntry,
    Notification,
    PatientTreatment,
    PatientVisit,
    ProviderMetrics,
    SymptomEntry,
    Treatment,
    # Enum tables
    TreatmentCategory,
    TreatmentProtocolMetric,
    TreatmentStatus,
    UrgencyLevel,
    User,
    # Helper
    utc_now,
)
from .llm import (
    CheckInModel,
    CheckInSummary,
    Condition,
    DataSource,
    FoodEntryModel,
    MedicationEntryModel,
    MetricLogsOutput,
    Symptom,
    SymptomEntryModel,
    SymptomTrend,
)
from .state import (
    AdminCheckIn,
    Appointment as AppointmentState,
    Biomarker,
    BiomarkerDataPoint,
    CallLogEntry,
    CheckIn as CheckInState,
    CheckInWithTranscript,
    Notification as NotificationState,
    NutritionSummary,
    Patient,
    PortalAppointment,
    PortalTreatment,
    Reminder,
    TimeSlot,
    TranscriptSummary,
    TreatmentCategoryGroup,
    TreatmentProtocol,
    User as UserState,
)

__all__ = [
    # State schemas
    "AdminCheckIn",
    # Database models
    "Appointment",
    "AppointmentState",
    "Biomarker",
    "BiomarkerAggregate",
    "BiomarkerCategory",
    "BiomarkerDataPoint",
    "BiomarkerDefinition",
    "BiomarkerReading",
    "CallLog",
    "CallLogEntry",
    "CallTranscript",
    "CheckIn",
    # LLM models
    "CheckInModel",
    "CheckInState",
    "CheckInSummary",
    "CheckInType",
    "CheckInWithTranscript",
    "ClinicDailyMetrics",
    "Condition",
    "DataSource",
    "FoodEntryModel",
    "FoodLogEntry",
    "MedicationEntry",
    "MedicationEntryModel",
    "MetricLogsOutput",
    "Notification",
    "NotificationState",
    "NutritionSummary",
    "Patient",
    "PatientTreatment",
    "PatientVisit",
    "PortalAppointment",
    "PortalTreatment",
    "ProviderMetrics",
    "Reminder",
    "Symptom",
    "SymptomEntry",
    "SymptomEntryModel",
    "SymptomTrend",
    "TimeSlot",
    "TranscriptSummary",
    "Treatment",
    # Enum tables
    "TreatmentCategory",
    "TreatmentCategoryGroup",
    "TreatmentProtocol",
    "TreatmentProtocolMetric",
    "TreatmentStatus",
    "UrgencyLevel",
    "User",
    "UserState",
    # Helper
    "utc_now",
]
