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

# Conditions, trends, sources, medication notifications
from .conditions import (
    create_condition_sync,
    create_data_source_sync,
    create_medication_notification_sync,
    create_symptom_trend_sync,
    get_conditions_sync,
    get_data_sources_sync,
    get_medication_notifications_sync,
    get_symptom_trends_sync,
    toggle_data_source_connection_sync,
    toggle_medication_completed_sync,
    update_condition_status_sync,
)

# Health entries
from .health import (
    create_food_entry_sync,
    create_medication_entry_sync,
    create_symptom_sync,
    get_food_entries_sync,
    get_medication_entries_sync,
    get_medications_sync,  # Legacy alias
    get_prescriptions_sync,
    get_symptom_logs_sync,
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
    create_user_sync,
    get_all_patients_sync,
    get_demo_patients_sync,
    get_patient_name_by_phone,
    get_phone_to_patient_map,
    get_providers_sync,
    get_recently_active_patients_sync,
    get_user_by_external_id_sync,
    get_user_by_id_sync,
    get_user_by_phone_sync,
)

# =============================================================================
# Utility functions (no database table)
# =============================================================================


def get_reminders_sync(user_id: int | None = None, limit: int = 50) -> list[dict]:
    """Get health reminders (medication notifications) from database.

    Args:
        user_id: User ID to filter reminders
        limit: Maximum number of reminders to return

    Returns:
        List of reminder/notification dictionaries
    """
    if not user_id:
        return []
    return get_medication_notifications_sync(user_id, limit=limit)


__all__ = [
    "create_appointment_sync",
    "create_checkin_sync",
    "create_condition_sync",
    "create_data_source_sync",
    "create_food_entry_sync",
    "create_medication_entry_sync",
    "create_medication_notification_sync",
    "create_symptom_sync",
    "create_symptom_trend_sync",
    "create_treatment_sync",
    "create_user_sync",
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
    "get_conditions_sync",
    "get_data_sources_sync",
    "get_demo_patients_sync",
    "get_food_entries_sync",
    "get_medication_entries_sync",
    "get_medication_notifications_sync",
    "get_medications_sync",  # Legacy alias for get_medication_entries_sync
    "get_notifications_for_role_sync",
    "get_notifications_for_user_sync",
    "get_patient_biomarkers_sync",
    "get_patient_name_by_phone",
    "get_patient_treatments_sync",
    "get_phone_to_patient_map",
    "get_prescriptions_sync",
    "get_providers_sync",
    "get_recently_active_patients_sync",
    "get_reminders_sync",
    "get_symptom_logs_sync",
    "get_symptom_trends_sync",
    "get_symptoms_sync",
    "get_treatment_by_id_sync",
    "get_treatments_as_protocols_sync",
    "get_user_by_external_id_sync",
    "get_user_by_id_sync",
    "get_user_by_phone_sync",
    "mark_notification_read_sync",
    "normalize_phone",
    "save_health_entries_sync",
    "toggle_data_source_connection_sync",
    "toggle_medication_completed_sync",
    "update_appointment_status_sync",
    "update_checkin_status_sync",
    "update_checkin_sync",
    "update_condition_status_sync",
    "update_treatment_sync",
]
