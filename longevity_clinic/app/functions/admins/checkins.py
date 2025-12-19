"""Admin check-in functions.

Functions for processing and managing admin check-in data.
When is_demo=True, returns demo data. Otherwise queries the database.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from ...config import get_logger, current_config
from ..db_utils import (
    normalize_phone,
    get_patient_name_by_phone,
    get_checkins_sync,
    update_checkin_status_sync,
)
from ...data.categories import HealthKeyword

logger = get_logger("longevity_clinic.admin_functions")


def _get_demo_admin_checkins():
    """Lazy-load demo admin checkins."""
    from ...data.seed import ADMIN_CHECKINS_SEED

    return ADMIN_CHECKINS_SEED


# Re-export normalize_phone from db_helpers for backwards compatibility
__all__ = [
    "normalize_phone",
    "get_patient_name_from_phone",
    "extract_health_topics",
    "fetch_all_checkins",
    "update_checkin_status",
    "filter_checkins",
    "count_checkins_by_status",
]


def get_patient_name_from_phone(phone: str) -> str:
    """Get patient name from phone number.

    Uses database lookup, falls back to formatted phone if not found.

    Args:
        phone: Phone number (any format)

    Returns:
        Patient name or formatted phone if not found
    """
    return get_patient_name_by_phone(phone, fallback=f"Patient ({phone})")


def extract_health_topics(text: str, max_topics: int = 5) -> List[str]:
    """Extract health topics from text.

    Args:
        text: Text to analyze
        max_topics: Maximum number of topics to return

    Returns:
        List of extracted health topics
    """
    text_lower = text.lower()
    topics = [kw.value for kw in HealthKeyword if kw.value in text_lower]
    return topics[:max_topics] or ["voice call"]


async def fetch_all_checkins(
    status_filter: Optional[str] = None,
    limit: int = 100,
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch all check-ins for admin view.

    Args:
        status_filter: Filter by status ('pending', 'reviewed', 'flagged')
        limit: Maximum number of check-ins to return
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of admin check-in records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching admin checkins (status=%s, limit=%d, demo=%s)",
        status_filter,
        limit,
        is_demo,
    )

    if is_demo:
        logger.debug("fetch_all_checkins: Returning demo data")
        checkins = _get_demo_admin_checkins()[:limit]
        if status_filter:
            checkins = [c for c in checkins if c.get("status") == status_filter]
        return checkins

    # Query from database
    logger.debug("fetch_all_checkins: Querying database")
    return get_checkins_sync(status=status_filter, limit=limit)


async def update_checkin_status(
    checkin_id: str,
    status: str,
    reviewed_by: str,
) -> Dict[str, Any]:
    """Update check-in status.

    Args:
        checkin_id: Check-in ID
        status: New status
        reviewed_by: Reviewer name/ID

    Returns:
        Updated check-in record
    """
    logger.info(
        "Updating checkin %s status to %s by %s", checkin_id, status, reviewed_by
    )

    # Try database update first
    result = update_checkin_status_sync(checkin_id, status, reviewed_by)
    if result:
        return result

    # Fallback for demo/in-memory data
    logger.debug("update_checkin_status: DB update failed, returning placeholder")
    return {
        "id": checkin_id,
        "status": status,
        "reviewed_by": reviewed_by,
        "reviewed_at": datetime.now().isoformat(),
    }


def filter_checkins(
    checkins: List[Dict[str, Any]],
    status: Optional[str] = None,
    search_query: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter check-ins by status and search query.

    Args:
        checkins: List of check-in records
        status: Filter by status (None or 'all' = no filter)
        search_query: Search in patient name, summary, topics

    Returns:
        Filtered list of check-ins
    """
    results = checkins

    # Filter by status
    if status and status != "all":
        results = [c for c in results if c.get("status") == status]

    # Filter by search query
    if search_query and search_query.strip():
        q = search_query.lower()
        results = [
            c
            for c in results
            if q in c.get("patient_name", "").lower()
            or q in c.get("summary", "").lower()
            or any(q in t.lower() for t in c.get("key_topics", []))
        ]

    # Sort by submission date (newest first)
    return sorted(results, key=lambda x: x.get("submitted_at", ""), reverse=True)


def count_checkins_by_status(
    checkins: List[Dict[str, Any]],
) -> Dict[str, int]:
    """Count check-ins by status.

    Args:
        checkins: List of check-in records

    Returns:
        Dict with counts per status
    """
    counts = {
        "pending": 0,
        "reviewed": 0,
        "flagged": 0,
        "total": len(checkins),
    }

    for checkin in checkins:
        status = checkin.get("status", "pending")
        if status in counts:
            counts[status] += 1

    return counts
