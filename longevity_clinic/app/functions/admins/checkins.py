"""Admin check-in functions.

Functions for processing and managing admin check-in data.
All data is loaded from the database.
Seed data with: python scripts/load_seed_data.py
"""

from datetime import datetime
from typing import Any

from ...config import get_logger
from ...data.categories import HealthKeyword
from ..db_utils import (
    get_checkins_sync,
    get_patient_name_by_phone,
    normalize_phone,
    update_checkin_status_sync,
)

logger = get_logger("longevity_clinic.admin_functions")


# Re-export normalize_phone from db_helpers for backwards compatibility
__all__ = [
    "count_checkins_by_status",
    "extract_health_topics",
    "fetch_all_checkins",
    "filter_checkins",
    "get_patient_name_from_phone",
    "normalize_phone",
    "update_checkin_status",
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


def extract_health_topics(text: str, max_topics: int = 5) -> list[str]:
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
    status_filter: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Fetch all check-ins for admin view from database.

    Args:
        status_filter: Filter by status ('pending', 'reviewed', 'flagged')
        limit: Maximum number of check-ins to return

    Returns:
        List of admin check-in records

    Note: Requires seeded database. Run: python scripts/load_seed_data.py
    """
    logger.info(
        "Fetching admin checkins (status=%s, limit=%d)",
        status_filter,
        limit,
    )

    # Query from database
    logger.debug("fetch_all_checkins: Querying database")
    checkins = get_checkins_sync(status=status_filter, limit=limit)
    if not checkins:
        logger.warning(
            "No check-ins found in database. "
            "Run 'python scripts/load_seed_data.py' to seed data."
        )
    return checkins


async def update_checkin_status(
    checkin_id: str,
    status: str,
    reviewed_by: str,
) -> dict[str, Any]:
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
    checkins: list[dict[str, Any]],
    status: str | None = None,
    search_query: str | None = None,
) -> list[dict[str, Any]]:
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
    checkins: list[dict[str, Any]],
) -> dict[str, int]:
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
