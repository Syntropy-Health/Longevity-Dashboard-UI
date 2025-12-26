"""Admin check-in functions.

Functions for processing and managing admin check-in data.
All data is loaded from the database.
Seed data with: python scripts/load_seed_data.py
"""

from datetime import datetime

from ...config import get_logger
from ...data.schemas.db import HealthKeywordEnum as HealthKeyword
from ...data.schemas.state import AdminCheckIn, CheckInStatusUpdate
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
) -> list[AdminCheckIn]:
    """Fetch all check-ins for admin view from database."""
    logger.info("Fetching admin checkins (status=%s, limit=%d)", status_filter, limit)
    checkins = get_checkins_sync(status=status_filter, limit=limit)
    if not checkins:
        logger.warning(
            "No check-ins found. Run 'python scripts/load_seed_data.py' to seed."
        )
    return checkins


async def update_checkin_status(
    checkin_id: str,
    status: str,
    reviewed_by: str,
) -> CheckInStatusUpdate:
    """Update check-in status."""
    logger.info("Updating checkin %s to %s by %s", checkin_id, status, reviewed_by)
    result = update_checkin_status_sync(checkin_id, status, reviewed_by)
    if result:
        return result
    # Fallback for demo/in-memory data
    return CheckInStatusUpdate(
        id=checkin_id,
        status=status,
        reviewed_by=reviewed_by,
        reviewed_at=datetime.now().isoformat(),
    )


def filter_checkins(
    checkins: list[AdminCheckIn],
    status: str | None = None,
    search_query: str | None = None,
) -> list[AdminCheckIn]:
    """Filter check-ins by status and search query."""
    results = checkins

    if status and status != "all":
        results = [c for c in results if c.get("status") == status]

    if search_query and (q := search_query.strip().lower()):
        results = [
            c
            for c in results
            if q in c.get("patient_name", "").lower()
            or q in c.get("summary", "").lower()
            or any(q in t.lower() for t in c.get("key_topics", []))
        ]

    return sorted(results, key=lambda x: x.get("timestamp", ""), reverse=True)


def count_checkins_by_status(checkins: list[AdminCheckIn]) -> dict[str, int]:
    """Count check-ins by status."""
    counts = {"pending": 0, "reviewed": 0, "flagged": 0, "total": len(checkins)}
    for checkin in checkins:
        if (status := checkin.get("status", "pending")) in counts:
            counts[status] += 1
    return counts
