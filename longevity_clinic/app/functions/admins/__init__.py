"""Admin-specific functions for state operations."""

from __future__ import annotations

# Local application - DB helpers (direct database access) - use db_utils
from ..db_utils import (
    get_checkins_sync,
    get_patient_name_by_phone,
    get_phone_to_patient_map,
)

# Re-export shared fetch_call_logs for admin use (no phone filter = all logs)
from ..utils import fetch_call_logs

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

__all__ = [
    "count_checkins_by_status",
    "extract_health_topics",
    # Check-ins
    "fetch_all_checkins",
    # Shared
    "fetch_call_logs",
    "filter_checkins",
    "get_checkins_sync",
    "get_patient_name_by_phone",
    "get_patient_name_from_phone",
    # DB helpers
    "get_phone_to_patient_map",
    "normalize_phone",
    "update_checkin_status",
]
