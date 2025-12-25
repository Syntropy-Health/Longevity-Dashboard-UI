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

# Appointments
from .appointments import (
    create_appointment_sync,
    get_appointments_for_patient_sync,
    get_appointments_for_user_sync,
    get_appointments_sync,
    update_appointment_status_sync,
)

# Biomarkers
from .biomarkers import (
    get_biomarker_definitions_sync,
    get_biomarker_panels_sync,
    get_patient_biomarkers_sync,
)

# Check-ins
from .checkins import (
    create_checkin_sync,
    delete_checkin_sync,
    get_checkin_db_id_sync,
    get_checkins_for_user_sync,
    get_checkins_sync,
    save_health_entries_sync,
    update_checkin_status_sync,
    update_checkin_sync,
)

# Health entries
from .health import (
    create_food_entry_sync,
    create_medication_entry_sync,
    create_symptom_sync,
    get_food_entries_sync,
    get_medication_entries_sync,
    get_medication_subscriptions_sync,
    get_medications_sync,  # Legacy alias
    get_symptoms_sync,
)

# Notifications
from .notifications import (
    delete_notification_sync,
    get_notifications_for_role_sync,
    get_notifications_for_user_sync,
    mark_notification_read_sync,
)

# Treatments
from .treatments import (
    create_treatment_sync,
    get_all_treatments_sync,
    get_patient_treatments_sync,
    get_treatment_by_id_sync,
    get_treatments_as_protocols_sync,
    update_treatment_sync,
)

# Users
from .users import (
    get_all_patients_sync,
    get_patient_name_by_phone,
    get_phone_to_patient_map,
    get_recently_active_patients_sync,
    get_user_by_external_id_sync,
    get_user_by_id_sync,
    get_user_by_phone_sync,
)

__all__ = [
    "create_appointment_sync",
    "create_checkin_sync",
    "create_food_entry_sync",
    "create_medication_entry_sync",
    "create_symptom_sync",
    "create_treatment_sync",
    "delete_checkin_sync",
    "delete_notification_sync",
    "get_all_patients_sync",
    "get_all_treatments_sync",
    "get_appointments_for_patient_sync",
    "get_appointments_for_user_sync",
    "get_appointments_sync",
    "get_biomarker_definitions_sync",
    "get_biomarker_panels_sync",
    "get_checkin_db_id_sync",
    "get_checkins_for_user_sync",
    "get_checkins_sync",
    "get_food_entries_sync",
    "get_medication_entries_sync",
    "get_medication_subscriptions_sync",
    "get_medications_sync",  # Legacy alias for get_medication_entries_sync
    "get_notifications_for_role_sync",
    "get_notifications_for_user_sync",
    "get_patient_biomarkers_sync",
    "get_patient_name_by_phone",
    "get_patient_treatments_sync",
    "get_phone_to_patient_map",
    "get_recently_active_patients_sync",
    "get_symptoms_sync",
    "get_treatment_by_id_sync",
    "get_treatments_as_protocols_sync",
    "get_user_by_external_id_sync",
    "get_user_by_id_sync",
    "get_user_by_phone_sync",
    "mark_notification_read_sync",
    "normalize_phone",
    "save_health_entries_sync",
    "update_appointment_status_sync",
    "update_checkin_status_sync",
    "update_checkin_sync",
    "update_treatment_sync",
]
