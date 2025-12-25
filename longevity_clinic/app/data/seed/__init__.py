"""Seed data modules for the Longevity Clinic application.

This package contains modular seed data for database initialization:
- patients.py: Patient seed data and DemoPatientSeed class
- notifications.py: Admin and patient notification seeds
- checkins.py: Patient check-in seed data
- treatments.py: Treatment catalog and protocol metrics
- biomarkers.py: Biomarker metric seed data
- nutrition.py: Food, medication, symptom seed data
- appointments.py: Appointment and provider seed data
- clinic_metrics.py: Admin dashboard chart data

Seed data uses dict format compatible with SQLModel.model_validate() for type safety.
For database loading, use scripts/load_seed_data.py.

Architecture:
- PRIMARY_DEMO_PATIENT: Derived from config.DemoUserConfig (single source of truth)
- All seed data is loaded into SQLite via load_seed_data.py
- Schema can be exported for PostgreSQL migration
"""

from __future__ import annotations

from .appointments import (
    APPOINTMENTS_SEED,
    PORTAL_APPOINTMENTS_SEED,
    PROVIDERS,
    TREATMENT_TYPES,
)
from .biomarkers import (
    BIOMARKER_CHART_SEED,
    BIOMARKER_METRIC_SEED_DATA,
    PORTAL_BIOMARKERS_SEED,
)
from .checkins import (
    ADMIN_CHECKINS_SEED,
    CHECKIN_SEED_DATA,
)
from .clinic_metrics import (
    BIOMARKER_AGGREGATE_SEED,
    DAILY_METRICS_SEED,
    HOURLY_FLOW_SEED,
    PATIENT_TREND_SEED,
    PATIENT_VISIT_SEED,
    PROVIDER_METRICS_SEED,
    ROOM_UTILIZATION_SEED,
)
from .notifications import (
    ADMIN_NOTIFICATIONS_SEED,
    PATIENT_NOTIFICATIONS_SEED,
)
from .medication_subscriptions import (
    MEDICATION_SUBSCRIPTIONS_SEED,
    get_medication_subscriptions_for_user,
)
from .nutrition import (
    CONDITIONS_SEED,
    DATA_SOURCES_SEED,
    FOOD_ENTRIES_SEED,
    MEDICATIONS_SEED,
    NUTRITION_SUMMARY_SEED,
    REMINDERS_SEED,
    SYMPTOM_LOGS_SEED,
    SYMPTOM_TRENDS_SEED,
    SYMPTOMS_SEED,
)

# Re-export all seed data from submodules
from .patients import (
    DEMO_PATIENTS,
    DEMO_PATIENTS_STATE,
    DEMO_PHONE_NUMBER,
    PHONE_TO_PATIENT_SEED,
    SECONDARY_DEMO_PATIENTS,
    DemoPatientSeed,
    get_all_demo_patients,
    get_phone_to_patient_seed,
)
from .treatments import (
    PATIENT_TREATMENT_ASSIGNMENTS_SEED,
    PORTAL_TREATMENTS_SEED,
    TREATMENT_CATALOG_SEED,
    TREATMENT_CHART_SEED,
    TREATMENT_PROTOCOL_METRICS_SEED,
)

__all__ = [
    "ADMIN_CHECKINS_SEED",
    # Notifications
    "ADMIN_NOTIFICATIONS_SEED",
    # Appointments
    "APPOINTMENTS_SEED",
    "BIOMARKER_AGGREGATE_SEED",
    "BIOMARKER_CHART_SEED",
    # Biomarkers
    "BIOMARKER_METRIC_SEED_DATA",
    # Check-ins
    "CHECKIN_SEED_DATA",
    "CONDITIONS_SEED",
    "DAILY_METRICS_SEED",
    "DATA_SOURCES_SEED",
    "DEMO_PATIENTS",
    "DEMO_PATIENTS_STATE",
    "DEMO_PHONE_NUMBER",
    "FOOD_ENTRIES_SEED",
    "HOURLY_FLOW_SEED",
    # Medication Subscriptions
    "MEDICATION_SUBSCRIPTIONS_SEED",
    "MEDICATIONS_SEED",
    # Nutrition/Health
    "NUTRITION_SUMMARY_SEED",
    "PATIENT_NOTIFICATIONS_SEED",
    "PATIENT_TREATMENT_ASSIGNMENTS_SEED",
    # Clinic Metrics
    "PATIENT_TREND_SEED",
    "PATIENT_VISIT_SEED",
    "PHONE_TO_PATIENT_SEED",
    "PORTAL_APPOINTMENTS_SEED",
    "PORTAL_BIOMARKERS_SEED",
    "PORTAL_TREATMENTS_SEED",
    "PROVIDERS",
    "PROVIDER_METRICS_SEED",
    "REMINDERS_SEED",
    "ROOM_UTILIZATION_SEED",
    "SECONDARY_DEMO_PATIENTS",
    "SYMPTOMS_SEED",
    "SYMPTOM_LOGS_SEED",
    "SYMPTOM_TRENDS_SEED",
    # Treatments
    "TREATMENT_CATALOG_SEED",
    "TREATMENT_CHART_SEED",
    "TREATMENT_PROTOCOL_METRICS_SEED",
    "TREATMENT_TYPES",
    # Patients
    "DemoPatientSeed",
    "get_all_demo_patients",
    "get_medication_subscriptions_for_user",
    "get_phone_to_patient_seed",
]
