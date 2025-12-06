"""
Data module for shared categories, constants, and data schemas.
"""

from .categories import (
    TREATMENT_CATEGORIES,
    TREATMENT_CATEGORY_COLORS,
    TREATMENT_FREQUENCIES,
    TREATMENT_STATUSES,
    PATIENT_STATUSES,
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
    Medication,
    Condition,
    Symptom,
    SymptomLog,
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

from .demo import (
    # Demo data constants
    BIOMARKER_METRIC_DEMO_DATA,
    ADMIN_NOTIFICATIONS_DEMO,
    PATIENT_NOTIFICATIONS_DEMO,
    DEMO_PATIENTS,
    DEMO_PHONE_NUMBER,
    DEMO_NUTRITION_SUMMARY,
    DEMO_FOOD_ENTRIES,
    DEMO_MEDICATIONS,
    DEMO_CONDITIONS,
    DEMO_SYMPTOMS,
    DEMO_SYMPTOM_LOGS,
    DEMO_REMINDERS,
    DEMO_SYMPTOM_TRENDS,
    DEMO_DATA_SOURCES,
    DEMO_CHECKINS,
    DEMO_PATIENTS_STATE,
    DEMO_TREND_DATA,
    DEMO_TREATMENT_DATA,
    DEMO_BIOMARKER_DATA,
)

__all__ = [
    # Categories and constants
    "TREATMENT_CATEGORIES",
    "TREATMENT_CATEGORY_COLORS",
    "BIOMARKER_CATEGORIES",
    "BIOMARKER_SIMPLE_CATEGORIES",
    "TREATMENT_FREQUENCIES",
    "TREATMENT_STATUSES",
    "PATIENT_STATUSES",
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
    "Medication",
    "Condition",
    "Symptom",
    "SymptomLog",
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
    # Demo data constants
    "BIOMARKER_METRIC_DEMO_DATA",
    "ADMIN_NOTIFICATIONS_DEMO",
    "PATIENT_NOTIFICATIONS_DEMO",
    "DEMO_PATIENTS",
    "DEMO_PHONE_NUMBER",
    "DEMO_NUTRITION_SUMMARY",
    "DEMO_FOOD_ENTRIES",
    "DEMO_MEDICATIONS",
    "DEMO_CONDITIONS",
    "DEMO_SYMPTOMS",
    "DEMO_SYMPTOM_LOGS",
    "DEMO_REMINDERS",
    "DEMO_SYMPTOM_TRENDS",
    "DEMO_DATA_SOURCES",
    "DEMO_CHECKINS",
    "DEMO_PATIENTS_STATE",
    "DEMO_TREND_DATA",
    "DEMO_TREATMENT_DATA",
    "DEMO_BIOMARKER_DATA",
]
