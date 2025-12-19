"""Admin-specific functions for state operations."""

from __future__ import annotations

# Local application - DB helpers (direct database access) - use db_utils
from ..db_utils import (
    get_checkins_sync,
    get_patient_name_by_phone,
    get_phone_to_patient_map,
)

# Local application - checkins module
from .checkins import (
    count_checkins_by_status,
    extract_health_topics,
    fetch_all_checkins,
    filter_checkins,
    get_patient_name_from_phone,
    normalize_phone,
    update_checkin_status,
)

# Re-export shared fetch_call_logs for admin use (no phone filter = all logs)
from ..utils import fetch_call_logs

__all__ = [
    # Shared
    "fetch_call_logs",
    # Check-ins
    "fetch_all_checkins",
    "update_checkin_status",
    "filter_checkins",
    "count_checkins_by_status",
    "get_patient_name_from_phone",
    "extract_health_topics",
    "normalize_phone",
    # DB helpers
    "get_phone_to_patient_map",
    "get_patient_name_by_phone",
    "get_checkins_sync",
]
