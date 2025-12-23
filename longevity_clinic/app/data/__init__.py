"""
Data module for shared categories, constants, schemas, and database models.

This module exports:
- Constants: Treatment/biomarker categories, statuses, and configuration
- State Schemas: TypedDict/Pydantic models for component state (state_schemas.py)
- API Schemas: Request/response models for external APIs (api_schemas.py)
- DB Models: SQLModel database tables (model.py)
- Seed Data: Demo data for development/testing (seed/)
"""

# =============================================================================
# Constants and Enums (categories.py, biomarkers.py)
# =============================================================================
# =============================================================================
# API Schemas - Request/Response models for external APIs (api_schemas.py)
# =============================================================================
from .api_schemas import (
    CallLogsAPIConfig,
    CallLogsQueryParams,
    TranscriptSummarizationRequest,
)
from .biomarkers import (
    BIOMARKER_CATEGORIES,
    BIOMARKER_SIMPLE_CATEGORIES,
    BIOMARKER_STATUSES,
    BIOMARKER_TRENDS,
    BiomarkerCategory,
    BiomarkerCategoryEnum,
    BiomarkerMetric,
    BiomarkerMetricName,
    BiomarkerSimpleCategoryEnum,
    BiomarkerStatus,
    BiomarkerTrend,
    MeasurementUnit,
    generate_history,
    get_biomarker_panels,
)
from .categories import (
    HEALTH_KEYWORDS,
    PATIENT_STATUSES,
    TREATMENT_CATEGORIES,
    TREATMENT_CATEGORY_COLORS,
    TREATMENT_FREQUENCIES,
    TREATMENT_STATUSES,
    HealthKeyword,
)

# =============================================================================
# Database Models - SQLModel/rx.Model tables (model.py)
# Naming convention: <Schema>DBModel to distinguish from state TypedDicts/Pydantic
# =============================================================================
from .model import (
    CallLog as CallLogDBModel,
    CallTranscript as CallTranscriptDBModel,
    CheckIn as CheckInDBModel,
    FoodLogEntry as FoodLogEntryDBModel,
    MedicationEntry as MedicationEntryDBModel,
    Notification as NotificationDBModel,
    SymptomEntry as SymptomEntryDBModel,
    User as UserDBModel,
)

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

# =============================================================================
# State Schemas - TypedDict/Pydantic for Reflex component state (state_schemas.py)
# =============================================================================
from .state_schemas import (
    AdminCheckIn,
    # Appointments
    Appointment,
    Biomarker,
    # Biomarkers
    BiomarkerDataPoint,
    # Call logs
    CallLogEntry,
    # Check-ins
    CheckIn,
    CheckInModel,
    CheckInWithTranscript,
    Condition,
    DataSource,
    FoodEntry,
    MedicationEntry,
    # Notifications
    Notification,
    # Patient dashboard
    NutritionSummary,
    # Patient profile
    Patient,
    # Portal views
    PortalAppointment,
    PortalTreatment,
    Reminder,
    Symptom,
    SymptomEntry,
    SymptomTrend,
    TimeSlot,
    TranscriptSummary,
    # Treatments
    TreatmentProtocol,
    # Auth
    User,
)

# NOTE: Database helpers have moved to longevity_clinic.app.functions.db_utils
# Import from there instead of data.db_helpers

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
    # ==========================================================================
    # Constants and Enums
    # ==========================================================================
    "TREATMENT_CATEGORIES",
    "TREATMENT_CATEGORY_COLORS",
    "TREATMENT_CHART_SEED",
    "TREATMENT_FREQUENCIES",
    "TREATMENT_STATUSES",
    "AdminCheckIn",
    # Appointments
    "Appointment",
    "Biomarker",
    "BiomarkerCategory",
    "BiomarkerCategoryEnum",
    # Biomarkers
    "BiomarkerDataPoint",
    "BiomarkerMetric",
    "BiomarkerMetricName",
    "BiomarkerSimpleCategoryEnum",
    "BiomarkerStatus",
    "BiomarkerTrend",
    "CallLogDBModel",
    # Call logs
    "CallLogEntry",
    "CallLogsAPIConfig",
    # ==========================================================================
    # API Schemas
    # ==========================================================================
    "CallLogsQueryParams",
    "CallTranscriptDBModel",
    # Check-ins
    "CheckIn",
    "CheckInDBModel",
    "CheckInModel",
    "CheckInWithTranscript",
    "Condition",
    "DataSource",
    "FoodEntry",
    "FoodLogEntryDBModel",
    "HealthKeyword",
    # Biomarker types/enums
    "MeasurementUnit",
    "MedicationEntry",
    "MedicationEntryDBModel",
    # Notifications
    "Notification",
    "NotificationDBModel",
    # Patient dashboard
    "NutritionSummary",
    # ==========================================================================
    # State Schemas (TypedDict/Pydantic for component state)
    # ==========================================================================
    # Patient
    "Patient",
    # Portal views
    "PortalAppointment",
    "PortalTreatment",
    "Reminder",
    "Symptom",
    "SymptomEntry",
    "SymptomEntryDBModel",
    "SymptomTrend",
    "TimeSlot",
    "TranscriptSummarizationRequest",
    "TranscriptSummary",
    # Treatments
    "TreatmentProtocol",
    # Auth
    "User",
    # ==========================================================================
    # Database Models (SQLModel) - use <Name>DBModel naming
    # ==========================================================================
    "UserDBModel",
    "generate_history",
    "get_biomarker_panels",
    # NOTE: Database helpers have moved to longevity_clinic.app.functions.db_utils
]
