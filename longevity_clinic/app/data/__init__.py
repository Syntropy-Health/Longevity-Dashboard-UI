"""
Data module for shared categories, constants, and data schemas.
"""

from .categories import (
    TREATMENT_CATEGORIES,
    TREATMENT_CATEGORY_COLORS,
    TREATMENT_FREQUENCIES,
    TREATMENT_STATUSES,
    PATIENT_STATUSES,
    HEALTH_KEYWORDS,
    HealthKeyword,
)

from .biomarkers import (
    BIOMARKER_CATEGORIES,
    BIOMARKER_SIMPLE_CATEGORIES,
    BIOMARKER_STATUSES,
    BIOMARKER_TRENDS,
    BiomarkerMetric,
    BiomarkerCategory,
    MeasurementUnit,
    BiomarkerMetricName,
    BiomarkerStatus,
    BiomarkerTrend,
    BiomarkerCategoryEnum,
    BiomarkerSimpleCategoryEnum,
    generate_history,
    get_biomarker_panels,
)

from .state_schemas import (
    # Patient schemas
    Patient,
    ChartData,
    # Patient dashboard schemas
    NutritionSummary,
    FoodEntry,
    MedicationEntry,
    Condition,
    Symptom,
    SymptomEntry,
    Reminder,
    SymptomTrend,
    DataSource,
    CheckIn,
    CheckInModel,
    # Call Log schemas
    CallLogEntry,
    TranscriptSummary,
    # Admin Check-in schemas
    AdminCheckIn,
    # Auth schemas
    User,
    # Biomarker schemas
    BiomarkerDataPoint,
    Biomarker,
    PortalAppointment,
    PortalTreatment,
    # Notification schemas
    Notification,
    # Treatment schemas
    TreatmentProtocol,
    # Appointment schemas
    Appointment,
    TimeSlot,
)

from .api_schemas import (
    # Call Logs API schemas
    CallLogsQueryParams,
    CallLogsAPIConfig,
    TranscriptSummarizationRequest,
)

# Seed data (modular replacement for demo.py)
from .seed import (
    # Canonical seed data names
    BIOMARKER_METRIC_SEED_DATA,
    ADMIN_NOTIFICATIONS_SEED,
    PATIENT_NOTIFICATIONS_SEED,
    DEMO_PATIENTS,
    DEMO_PHONE_NUMBER,
    NUTRITION_SUMMARY_SEED,
    FOOD_ENTRIES_SEED,
    MEDICATIONS_SEED,
    CONDITIONS_SEED,
    SYMPTOMS_SEED,
    SYMPTOM_LOGS_SEED,
    REMINDERS_SEED,
    SYMPTOM_TRENDS_SEED,
    DATA_SOURCES_SEED,
    CHECKIN_SEED_DATA,
    DEMO_PATIENTS_STATE,
    PATIENT_TREND_SEED,
    TREATMENT_CHART_SEED,
    BIOMARKER_CHART_SEED,
    PHONE_TO_PATIENT_SEED,
)

# Database models (SQLModel/rx.Model)
from .model import (
    User as UserModel,
    CallLog as CallLogModel,
    CallTranscript as CallTranscriptModel,
    CallSummary as CallSummaryModel,
    CheckIn as CheckInModel_DB,
    Notification as NotificationModel,
    MedicationEntry as MedicationEntryModel,
    FoodLogEntry as FoodLogEntryModel,
    SymptomEntry as SymptomEntryModel,
)

# NOTE: Database helpers have moved to longevity_clinic.app.functions.db_utils
# Import from there instead of data.db_helpers

__all__ = [
    # Categories and constants
    "TREATMENT_CATEGORIES",
    "TREATMENT_CATEGORY_COLORS",
    "BIOMARKER_CATEGORIES",
    "BIOMARKER_SIMPLE_CATEGORIES",
    "TREATMENT_FREQUENCIES",
    "TREATMENT_STATUSES",
    "PATIENT_STATUSES",
    "HEALTH_KEYWORDS",
    "HealthKeyword",
    "BIOMARKER_STATUSES",
    "BIOMARKER_TRENDS",
    # Biomarker types
    "MeasurementUnit",
    "BiomarkerMetricName",
    "BiomarkerStatus",
    "BiomarkerTrend",
    "BiomarkerCategoryEnum",
    "BiomarkerSimpleCategoryEnum",
    "BiomarkerMetric",
    "BiomarkerCategory",
    "generate_history",
    "get_biomarker_panels",
    # State schemas - Patient
    "Patient",
    "ChartData",
    # State schemas - Patient dashboard
    "NutritionSummary",
    "FoodEntry",
    "MedicationEntry",
    "Condition",
    "Symptom",
    "SymptomEntry",
    "Reminder",
    "SymptomTrend",
    "DataSource",
    "CheckIn",
    "CheckInModel",
    # State schemas - Call logs
    "CallLogEntry",
    "TranscriptSummary",
    # State schemas - Admin
    "AdminCheckIn",
    # State schemas - Auth
    "User",
    # State schemas - Biomarker state
    "BiomarkerDataPoint",
    "Biomarker",
    "PortalAppointment",
    "PortalTreatment",
    # State schemas - Notification
    "Notification",
    # State schemas - Treatment
    "TreatmentProtocol",
    # State schemas - Appointment
    "Appointment",
    "TimeSlot",
    # API schemas
    "CallLogsQueryParams",
    "CallLogsAPIConfig",
    "TranscriptSummarizationRequest",
    # Seed data constants (canonical names)
    "BIOMARKER_METRIC_SEED_DATA",
    "ADMIN_NOTIFICATIONS_SEED",
    "PATIENT_NOTIFICATIONS_SEED",
    "DEMO_PATIENTS",
    "DEMO_PHONE_NUMBER",
    "NUTRITION_SUMMARY_SEED",
    "FOOD_ENTRIES_SEED",
    "MEDICATIONS_SEED",
    "CONDITIONS_SEED",
    "SYMPTOMS_SEED",
    "SYMPTOM_LOGS_SEED",
    "REMINDERS_SEED",
    "SYMPTOM_TRENDS_SEED",
    "DATA_SOURCES_SEED",
    "CHECKIN_SEED_DATA",
    "DEMO_PATIENTS_STATE",
    "PATIENT_TREND_SEED",
    "TREATMENT_CHART_SEED",
    "BIOMARKER_CHART_SEED",
    "PHONE_TO_PATIENT_SEED",
    # Database models
    "UserModel",
    "CallLogModel",
    "CallTranscriptModel",
    "CallSummaryModel",
    "CheckInModel_DB",
    "NotificationModel",
    "MedicationEntryModel",
    "FoodLogEntryModel",
    "SymptomEntryModel",
    # NOTE: Database helpers have moved to longevity_clinic.app.functions.db_utils
]
