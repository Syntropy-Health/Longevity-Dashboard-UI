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
    BiomarkerDefinition,
    BiomarkerReading,
    CallLog,
    CallTranscript,
    CheckIn,
    ClinicDailyMetrics,
    FoodLogEntry,
    MedicationEntry,
    Notification,
    PatientTreatment,
    PatientVisit,
    ProviderMetrics,
    SymptomEntry,
    Treatment,
    TreatmentProtocolMetric,
    User,
    # Enum tables
    TreatmentCategory,
    TreatmentStatus,
    BiomarkerCategory,
    CheckInType,
    UrgencyLevel,
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
    # Database models
    "Appointment",
    "BiomarkerAggregate",
    "BiomarkerDefinition",
    "BiomarkerReading",
    "CallLog",
    "CallTranscript",
    "CheckIn",
    "ClinicDailyMetrics",
    "FoodLogEntry",
    "MedicationEntry",
    "Notification",
    "PatientTreatment",
    "PatientVisit",
    "ProviderMetrics",
    "SymptomEntry",
    "Treatment",
    "TreatmentProtocolMetric",
    "User",
    # Enum tables
    "TreatmentCategory",
    "TreatmentStatus",
    "BiomarkerCategory",
    "CheckInType",
    "UrgencyLevel",
    # LLM models
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
    # State schemas
    "AdminCheckIn",
    "AppointmentState",
    "Biomarker",
    "BiomarkerDataPoint",
    "CallLogEntry",
    "CheckInState",
    "CheckInWithTranscript",
    "NotificationState",
    "NutritionSummary",
    "Patient",
    "PortalAppointment",
    "PortalTreatment",
    "Reminder",
    "TimeSlot",
    "TranscriptSummary",
    "TreatmentCategoryGroup",
    "TreatmentProtocol",
    "UserState",
    # Helper
    "utc_now",
]
