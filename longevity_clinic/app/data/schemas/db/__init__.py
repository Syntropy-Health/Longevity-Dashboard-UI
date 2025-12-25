"""
Database models (rx.Model/SQLModel) for Longevity Clinic.

Contains:
- models.py: Core database table definitions
- enums.py: Enum/choice tables for referential integrity
- domain_enums.py: StrEnum definitions for type-safe domain values

Usage:
    from longevity_clinic.app.data.schemas.db import User, Treatment, TreatmentCategory
    from longevity_clinic.app.data.schemas.db import TreatmentCategoryEnum, BiomarkerCategoryEnum
"""

from .domain_enums import (
    # Treatment enums
    PATIENT_STATUSES,
    TREATMENT_CATEGORIES,
    TREATMENT_FREQUENCIES,
    TREATMENT_STATUSES,
    PatientStatusEnum,
    TreatmentCategoryEnum,
    TreatmentFrequencyEnum,
    TreatmentStatusEnum,
    # Biomarker enums
    BIOMARKER_CATEGORIES,
    BIOMARKER_SIMPLE_CATEGORIES,
    BIOMARKER_STATUSES,
    BIOMARKER_TRENDS,
    BiomarkerCategoryEnum,
    BiomarkerMetricNameEnum,
    BiomarkerSimpleCategoryEnum,
    BiomarkerStatusEnum,
    BiomarkerTrendEnum,
    MeasurementUnitEnum,
    # Health keywords
    HEALTH_KEYWORDS,
    HealthKeywordEnum,
)
from .enums import (
    BiomarkerCategory,
    CheckInType,
    TreatmentCategory,
    TreatmentStatus,
    UrgencyLevel,
)
from .models import (
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
    MedicationSubscription,
    Notification,
    PatientTreatment,
    PatientVisit,
    ProviderMetrics,
    SymptomEntry,
    Treatment,
    TreatmentProtocolMetric,
    User,
    utc_now,
)

__all__ = [
    # Core models
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
    "MedicationSubscription",
    "Notification",
    "PatientTreatment",
    "PatientVisit",
    "ProviderMetrics",
    "SymptomEntry",
    "Treatment",
    "TreatmentProtocolMetric",
    "User",
    # Enum tables (rx.Model)
    "BiomarkerCategory",
    "CheckInType",
    "TreatmentCategory",
    "TreatmentStatus",
    "UrgencyLevel",
    # Domain enums (StrEnum) - Treatment
    "TreatmentCategoryEnum",
    "TreatmentFrequencyEnum",
    "TreatmentStatusEnum",
    "PatientStatusEnum",
    "TREATMENT_CATEGORIES",
    "TREATMENT_FREQUENCIES",
    "TREATMENT_STATUSES",
    "PATIENT_STATUSES",
    # Domain enums (StrEnum) - Biomarker
    "BiomarkerCategoryEnum",
    "BiomarkerSimpleCategoryEnum",
    "MeasurementUnitEnum",
    "BiomarkerMetricNameEnum",
    "BiomarkerStatusEnum",
    "BiomarkerTrendEnum",
    "BIOMARKER_CATEGORIES",
    "BIOMARKER_SIMPLE_CATEGORIES",
    "BIOMARKER_STATUSES",
    "BIOMARKER_TRENDS",
    # Domain enums (StrEnum) - Health Keywords
    "HealthKeywordEnum",
    "HEALTH_KEYWORDS",
    # Helpers
    "utc_now",
]
