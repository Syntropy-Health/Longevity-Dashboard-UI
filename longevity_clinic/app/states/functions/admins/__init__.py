"""Admin-specific functions for state operations."""

# Re-export shared fetch_call_logs for admin use (no phone filter = all logs)
from ..utils import fetch_call_logs

from .checkins import (
    transform_call_log_to_admin_checkin,
    fetch_all_checkins,
    update_checkin_status,
    filter_checkins,
    count_checkins_by_status,
    get_patient_name_from_phone,
    extract_health_topics,
    normalize_phone,
    HEALTH_KEYWORDS,
    PHONE_TO_PATIENT,
)

__all__ = [
    # Shared
    "fetch_call_logs",
    # Check-ins
    "transform_call_log_to_admin_checkin",
    "fetch_all_checkins",
    "update_checkin_status",
    "filter_checkins",
    "count_checkins_by_status",
    "get_patient_name_from_phone",
    "extract_health_topics",
    "normalize_phone",
    "HEALTH_KEYWORDS",
    "PHONE_TO_PATIENT",
]
