"""Database models for the Longevity Clinic application.

Uses Reflex's rx.Model (SQLModel) for database operations with SQLite/PostgreSQL.

Models are organized into domain-specific modules:
- user: User accounts
- call_logs: Voice call tracking
- checkins: Patient check-ins
- notifications: System notifications and medication reminders
- appointments: Scheduling
- health_entries: Medication, food, and symptom logs
- conditions: Health conditions and symptom trends
- treatments: Treatment protocols and patient assignments
- biomarkers: Biomarker definitions and readings
- clinic_metrics: Admin dashboard metrics
"""

from .appointments import Appointment
from .base import utc_now
from .biomarkers import BiomarkerDefinition, BiomarkerReading
from .call_logs import CallLog, CallTranscript
from .checkins import CheckIn
from .clinic_metrics import (
    BiomarkerAggregate,
    ClinicDailyMetrics,
    PatientVisit,
    ProviderMetrics,
    TreatmentProtocolMetric,
)
from .conditions import Condition, DataSource, SymptomTrend
from .health_entries import FoodLogEntry, MedicationEntry, SymptomEntry
from .notifications import Notification
from .treatments import PatientTreatment, Treatment
from .user import User

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
    "Condition",
    "DataSource",
    "FoodLogEntry",
    "MedicationEntry",
    "Notification",
    "PatientTreatment",
    "PatientVisit",
    "ProviderMetrics",
    "SymptomEntry",
    "SymptomTrend",
    "Treatment",
    "TreatmentProtocolMetric",
    "User",
    # Helper
    "utc_now",
]
