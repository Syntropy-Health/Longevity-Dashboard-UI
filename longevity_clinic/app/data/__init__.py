"""
Data module for schemas, constants, and seed data.

This module provides:
- Schemas: Database models (db/), state TypedDicts (state/), LLM Pydantic (llm/), API (api/)
- Domain enums: Treatment/biomarker categories via StrEnum (schemas/db/domain_enums.py)
- Seed Data: Demo data for development/testing (seed/)

Usage:
    # Database models
    from longevity_clinic.app.data.schemas.db import User, Treatment, CheckIn

    # State TypedDicts
    from longevity_clinic.app.data.schemas.state import Patient, Notification

    # LLM Pydantic models
    from longevity_clinic.app.data.schemas.llm import MetricLogsOutput, CheckInSummary

    # API schemas
    from longevity_clinic.app.data.schemas.api import CallLogsAPIConfig

    # Domain enums (StrEnum)
    from longevity_clinic.app.data.schemas.db import TreatmentCategoryEnum, BiomarkerCategoryEnum

    # Legacy constants (list[str])
    from longevity_clinic.app.data import TREATMENT_CATEGORIES, BIOMARKER_CATEGORIES

    # Seed data
    from longevity_clinic.app.data.seed import DEMO_PATIENTS, CHECKIN_SEED_DATA
"""

# =============================================================================
# Domain Enums (from schemas/db/domain_enums.py)
# =============================================================================
from .schemas.db import (
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

# =============================================================================
# State TypedDicts (from schemas/state/)
# =============================================================================
from .schemas.state import (
    BiomarkerCategoryPanel,
    BiomarkerMetric,
    BiomarkerMetricSeed,
)

# =============================================================================
# Utility Functions
# =============================================================================
# NOTE: Function imports removed to avoid circular dependency.
# Import directly from functions modules:
#   - from longevity_clinic.app.functions.utils import generate_biomarker_history
#   - from longevity_clinic.app.functions.db_utils import get_biomarker_panels_sync
# =============================================================================
# Seed Data - Demo data for development/testing (seed/)
# =============================================================================
from .seed import (
    # Admin check-ins
    ADMIN_CHECKINS_SEED,
    # Notifications
    ADMIN_NOTIFICATIONS_SEED,
    BIOMARKER_CHART_SEED,
    # Biomarkers
    BIOMARKER_METRIC_SEED_DATA,
    # Check-ins
    CHECKIN_SEED_DATA,
    CONDITIONS_SEED,
    DATA_SOURCES_SEED,
    # Patients
    DEMO_PATIENTS,
    DEMO_PATIENTS_STATE,
    DEMO_PHONE_NUMBER,
    FOOD_ENTRIES_SEED,
    MEDICATIONS_SEED,
    # Patient dashboard
    NUTRITION_SUMMARY_SEED,
    PATIENT_NOTIFICATIONS_SEED,
    # Charts
    PATIENT_TREND_SEED,
    PHONE_TO_PATIENT_SEED,
    REMINDERS_SEED,
    SYMPTOM_LOGS_SEED,
    SYMPTOM_TRENDS_SEED,
    SYMPTOMS_SEED,
    TREATMENT_CHART_SEED,
)

# NOTE: Display-related config (e.g., TREATMENT_CATEGORY_COLORS) is in styles module
# NOTE: Database helpers are in longevity_clinic.app.functions.db_utils

# =============================================================================
# Backwards Compatibility Aliases
# =============================================================================
# Old names -> new enum names for smoother migration
BiomarkerCategory = BiomarkerCategoryPanel  # TypedDict for UI panels
BiomarkerMetricName = BiomarkerMetricNameEnum
BiomarkerStatus = BiomarkerStatusEnum
BiomarkerTrend = BiomarkerTrendEnum
MeasurementUnit = MeasurementUnitEnum
TreatmentCategory = TreatmentCategoryEnum
TreatmentFrequency = TreatmentFrequencyEnum
TreatmentStatus = TreatmentStatusEnum
PatientStatus = PatientStatusEnum
HealthKeyword = HealthKeywordEnum


__all__ = [
    # ==========================================================================
    # Seed Data
    # ==========================================================================
    "ADMIN_CHECKINS_SEED",
    "ADMIN_NOTIFICATIONS_SEED",
    "BIOMARKER_CATEGORIES",
    "BIOMARKER_CHART_SEED",
    "BIOMARKER_METRIC_SEED_DATA",
    "BIOMARKER_SIMPLE_CATEGORIES",
    "BIOMARKER_STATUSES",
    "BIOMARKER_TRENDS",
    "CHECKIN_SEED_DATA",
    "CONDITIONS_SEED",
    "DATA_SOURCES_SEED",
    "DEMO_PATIENTS",
    "DEMO_PATIENTS_STATE",
    "DEMO_PHONE_NUMBER",
    "FOOD_ENTRIES_SEED",
    "HEALTH_KEYWORDS",
    "MEDICATIONS_SEED",
    "NUTRITION_SUMMARY_SEED",
    "PATIENT_NOTIFICATIONS_SEED",
    "PATIENT_STATUSES",
    "PATIENT_TREND_SEED",
    "PHONE_TO_PATIENT_SEED",
    "REMINDERS_SEED",
    "SYMPTOMS_SEED",
    "SYMPTOM_LOGS_SEED",
    "SYMPTOM_TRENDS_SEED",
    "TREATMENT_CATEGORIES",
    "TREATMENT_CHART_SEED",
    "TREATMENT_FREQUENCIES",
    "TREATMENT_STATUSES",
    # ==========================================================================
    # Utility Functions (see functions/ modules directly)
    # ==========================================================================
    # ==========================================================================
    # Backwards Compatibility Aliases
    # ==========================================================================
    "BiomarkerCategory",
    # Biomarker
    "BiomarkerCategoryEnum",
    # ==========================================================================
    # State TypedDicts
    # ==========================================================================
    "BiomarkerCategoryPanel",
    "BiomarkerMetric",
    "BiomarkerMetricName",
    "BiomarkerMetricNameEnum",
    "BiomarkerMetricSeed",
    "BiomarkerSimpleCategoryEnum",
    "BiomarkerStatus",
    "BiomarkerStatusEnum",
    "BiomarkerTrend",
    "BiomarkerTrendEnum",
    "HealthKeyword",
    # Health keywords
    "HealthKeywordEnum",
    "MeasurementUnit",
    "MeasurementUnitEnum",
    "PatientStatus",
    "PatientStatusEnum",
    "TreatmentCategory",
    # ==========================================================================
    # Domain Enums (StrEnum)
    # ==========================================================================
    # Treatment
    "TreatmentCategoryEnum",
    "TreatmentFrequency",
    "TreatmentFrequencyEnum",
    "TreatmentStatus",
    "TreatmentStatusEnum",
]
