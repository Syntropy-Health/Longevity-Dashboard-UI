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
    # Biomarker enums
    BIOMARKER_CATEGORIES,
    BIOMARKER_SIMPLE_CATEGORIES,
    BIOMARKER_STATUSES,
    BIOMARKER_TRENDS,
    # Health keywords
    HEALTH_KEYWORDS,
    # Treatment enums
    PATIENT_STATUSES,
    TREATMENT_CATEGORIES,
    TREATMENT_FREQUENCIES,
    TREATMENT_STATUSES,
    BiomarkerCategoryEnum,
    BiomarkerMetricNameEnum,
    BiomarkerSimpleCategoryEnum,
    BiomarkerStatusEnum,
    BiomarkerTrendEnum,
    HealthKeywordEnum,
    MeasurementUnitEnum,
    PatientStatusEnum,
    TreatmentCategoryEnum,
    TreatmentFrequencyEnum,
    TreatmentStatusEnum,
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
    "BIOMARKER_CATEGORIES",
    "BIOMARKER_SIMPLE_CATEGORIES",
    "BIOMARKER_STATUSES",
    "BIOMARKER_TRENDS",
    "HEALTH_KEYWORDS",
    "PATIENT_STATUSES",
    "TREATMENT_CATEGORIES",
    "TREATMENT_FREQUENCIES",
    "TREATMENT_STATUSES",
    # Core models
    "Appointment",
    "BiomarkerAggregate",
    # Enum tables (rx.Model)
    "BiomarkerCategory",
    # Domain enums (StrEnum) - Biomarker
    "BiomarkerCategoryEnum",
    "BiomarkerDefinition",
    "BiomarkerMetricNameEnum",
    "BiomarkerReading",
    "BiomarkerSimpleCategoryEnum",
    "BiomarkerStatusEnum",
    "BiomarkerTrendEnum",
    "CallLog",
    "CallTranscript",
    "CheckIn",
    "CheckInType",
    "ClinicDailyMetrics",
    "FoodLogEntry",
    # Domain enums (StrEnum) - Health Keywords
    "HealthKeywordEnum",
    "MeasurementUnitEnum",
    "MedicationEntry",
    "Notification",
    "PatientStatusEnum",
    "PatientTreatment",
    "PatientVisit",
    "ProviderMetrics",
    "SymptomEntry",
    "Treatment",
    "TreatmentCategory",
    # Domain enums (StrEnum) - Treatment
    "TreatmentCategoryEnum",
    "TreatmentFrequencyEnum",
    "TreatmentProtocolMetric",
    "TreatmentStatus",
    "TreatmentStatusEnum",
    "UrgencyLevel",
    "User",
    # Helpers
    "utc_now",
]
