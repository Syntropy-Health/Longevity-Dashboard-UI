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

For database loading, use scripts/load_seed_data.py.

Architecture:
- PRIMARY_DEMO_PATIENT: Derived from config.DemoUserConfig (single source of truth)
- All seed data is loaded into SQLite via load_seed_data.py
- Schema can be exported for PostgreSQL migration
"""

from __future__ import annotations

# Re-export all seed data from submodules
from .patients import (
    DemoPatientSeed,
    SECONDARY_DEMO_PATIENTS,
    PHONE_TO_PATIENT_SEED,
    DEMO_PATIENTS,
    DEMO_PHONE_NUMBER,
    DEMO_PATIENTS_STATE,
    get_all_demo_patients,
    get_phone_to_patient_seed,
)

from .notifications import (
    ADMIN_NOTIFICATIONS_SEED,
    PATIENT_NOTIFICATIONS_SEED,
)

from .checkins import (
    CHECKIN_SEED_DATA,
    ADMIN_CHECKINS_SEED,
)

from .treatments import (
    TREATMENT_CATALOG_SEED,
    TREATMENT_PROTOCOL_METRICS_SEED,
    TREATMENT_CHART_SEED,
    PORTAL_TREATMENTS_SEED,
)

from .biomarkers import (
    BIOMARKER_METRIC_SEED_DATA,
    BIOMARKER_CHART_SEED,
    PORTAL_BIOMARKERS_SEED,
)

from .nutrition import (
    NUTRITION_SUMMARY_SEED,
    FOOD_ENTRIES_SEED,
    MEDICATIONS_SEED,
    CONDITIONS_SEED,
    SYMPTOMS_SEED,
    SYMPTOM_LOGS_SEED,
    REMINDERS_SEED,
    SYMPTOM_TRENDS_SEED,
    DATA_SOURCES_SEED,
)

from .appointments import (
    APPOINTMENTS_SEED,
    PORTAL_APPOINTMENTS_SEED,
    TREATMENT_TYPES,
    PROVIDERS,
)

from .clinic_metrics import (
    PATIENT_TREND_SEED,
    PATIENT_VISIT_SEED,
    PROVIDER_METRICS_SEED,
    DAILY_METRICS_SEED,
    BIOMARKER_AGGREGATE_SEED,
    HOURLY_FLOW_SEED,
    ROOM_UTILIZATION_SEED,
)


__all__ = [
    # Patients
    "DemoPatientSeed",
    "SECONDARY_DEMO_PATIENTS",
    "PHONE_TO_PATIENT_SEED",
    "DEMO_PATIENTS",
    "DEMO_PHONE_NUMBER",
    "DEMO_PATIENTS_STATE",
    "get_all_demo_patients",
    "get_phone_to_patient_seed",
    # Notifications
    "ADMIN_NOTIFICATIONS_SEED",
    "PATIENT_NOTIFICATIONS_SEED",
    # Check-ins
    "CHECKIN_SEED_DATA",
    "ADMIN_CHECKINS_SEED",
    # Treatments
    "TREATMENT_CATALOG_SEED",
    "TREATMENT_PROTOCOL_METRICS_SEED",
    "TREATMENT_CHART_SEED",
    "PORTAL_TREATMENTS_SEED",
    # Biomarkers
    "BIOMARKER_METRIC_SEED_DATA",
    "BIOMARKER_CHART_SEED",
    "PORTAL_BIOMARKERS_SEED",
    # Nutrition/Health
    "NUTRITION_SUMMARY_SEED",
    "FOOD_ENTRIES_SEED",
    "MEDICATIONS_SEED",
    "CONDITIONS_SEED",
    "SYMPTOMS_SEED",
    "SYMPTOM_LOGS_SEED",
    "REMINDERS_SEED",
    "SYMPTOM_TRENDS_SEED",
    "DATA_SOURCES_SEED",
    # Appointments
    "APPOINTMENTS_SEED",
    "PORTAL_APPOINTMENTS_SEED",
    "TREATMENT_TYPES",
    "PROVIDERS",
    # Clinic Metrics
    "PATIENT_TREND_SEED",
    "PATIENT_VISIT_SEED",
    "PROVIDER_METRICS_SEED",
    "DAILY_METRICS_SEED",
    "BIOMARKER_AGGREGATE_SEED",
    "HOURLY_FLOW_SEED",
    "ROOM_UTILIZATION_SEED",
]
