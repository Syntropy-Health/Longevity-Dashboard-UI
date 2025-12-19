"""Database utility functions for Longevity Clinic.

Centralized database access layer for all state operations.
Replaces data/db_helpers.py with organized submodules.

Modules:
- users.py: User lookup and management
- checkins.py: Check-in CRUD operations
- notifications.py: Notification CRUD operations
- appointments.py: Appointment CRUD operations
- biomarkers.py: Biomarker definitions and readings
- health.py: Health entries (medications, food, symptoms)
"""

from __future__ import annotations

# Utilities (re-exported for backwards compatibility)
from longevity_clinic.app.functions.utils import normalize_phone

# Users
from .users import (
    get_user_by_phone_sync,
    get_user_by_external_id_sync,
    get_user_by_id_sync,
    get_patient_name_by_phone,
    get_all_patients_sync,
    get_phone_to_patient_map,
    get_primary_demo_user_id,
    get_recently_active_patients_sync,
)

# Check-ins
from .checkins import (
    get_checkins_sync,
    get_checkins_for_user_sync,
    update_checkin_status_sync,
    create_checkin_sync,
)

# Notifications
from .notifications import (
    get_notifications_for_role_sync,
    get_notifications_for_user_sync,
    mark_notification_read_sync,
    delete_notification_sync,
)

# Appointments
from .appointments import (
    get_appointments_sync,
    get_appointments_for_user_sync,
    get_appointments_for_patient_sync,
    update_appointment_status_sync,
    create_appointment_sync,
)

# Biomarkers
from .biomarkers import (
    get_biomarker_definitions_sync,
    get_patient_biomarkers_sync,
    get_biomarker_panels_sync,
)

# Health entries
from .health import (
    get_medications_sync,
    get_food_entries_sync,
    get_symptoms_sync,
    create_medication_sync,
    create_food_entry_sync,
    create_symptom_sync,
)

# Treatments
from .treatments import (
    get_all_treatments_sync,
    get_treatment_by_id_sync,
    get_treatments_as_protocols_sync,
    get_patient_treatments_sync,
    create_treatment_sync,
    update_treatment_sync,
)

__all__ = [
    # Users
    "normalize_phone",
    "get_user_by_phone_sync",
    "get_user_by_external_id_sync",
    "get_user_by_id_sync",
    "get_patient_name_by_phone",
    "get_all_patients_sync",
    "get_phone_to_patient_map",
    "get_primary_demo_user_id",
    "get_recently_active_patients_sync",
    # Check-ins
    "get_checkins_sync",
    "get_checkins_for_user_sync",
    "update_checkin_status_sync",
    "create_checkin_sync",
    # Notifications
    "get_notifications_for_role_sync",
    "get_notifications_for_user_sync",
    "mark_notification_read_sync",
    "delete_notification_sync",
    # Appointments
    "get_appointments_sync",
    "get_appointments_for_user_sync",
    "get_appointments_for_patient_sync",
    "update_appointment_status_sync",
    "create_appointment_sync",
    # Biomarkers
    "get_biomarker_definitions_sync",
    "get_patient_biomarkers_sync",
    "get_biomarker_panels_sync",
    # Health
    "get_medications_sync",
    "get_food_entries_sync",
    "get_symptoms_sync",
    "create_medication_sync",
    "create_food_entry_sync",
    "create_symptom_sync",
    # Treatments
    "get_all_treatments_sync",
    "get_treatment_by_id_sync",
    "get_treatments_as_protocols_sync",
    "get_patient_treatments_sync",
    "create_treatment_sync",
    "update_treatment_sync",
]
