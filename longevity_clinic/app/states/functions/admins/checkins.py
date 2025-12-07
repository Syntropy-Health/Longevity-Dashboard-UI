"""Admin check-in functions.

Functions for processing and managing admin check-in data.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from ....config import get_logger

logger = get_logger("longevity_clinic.admin_functions")

# Health keywords for topic extraction
HEALTH_KEYWORDS = [
    "fatigue",
    "tired",
    "energy",
    "sleep",
    "pain",
    "joint",
    "headache",
    "anxiety",
    "stress",
    "blood pressure",
    "heart",
    "blood sugar",
    "diet",
    "medication",
    "exercise",
    "breathing",
]

# Phone to patient name mapping
PHONE_TO_PATIENT = {
    "+12126804645": "Demo Patient (Sarah Chen)",
    "(555) 123-4567": "John Doe",
    "(555) 987-6543": "Jane Smith",
    "(555) 456-7890": "Robert Johnson",
    "(555) 222-3333": "Emily Davis",
    "(555) 444-5555": "Michael Wilson",
}


def normalize_phone(phone: str) -> str:
    """Normalize phone number for comparison.

    Args:
        phone: Phone number string

    Returns:
        Normalized phone without formatting
    """
    return phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")


def get_patient_name_from_phone(phone: str) -> str:
    """Get patient name from phone number.

    Args:
        phone: Phone number (any format)

    Returns:
        Patient name or formatted phone if not found
    """
    normalized = normalize_phone(phone)
    for known_phone, name in PHONE_TO_PATIENT.items():
        if normalize_phone(known_phone) == normalized:
            return name
    return f"Patient ({phone})"


def extract_health_topics(text: str, max_topics: int = 5) -> List[str]:
    """Extract health topics from text.

    Args:
        text: Text to analyze
        max_topics: Maximum number of topics to return

    Returns:
        List of extracted health topics
    """
    text_lower = text.lower()
    topics = [kw for kw in HEALTH_KEYWORDS if kw in text_lower]
    return topics[:max_topics] or ["voice call"]


def transform_call_log_to_admin_checkin(
    call_id: str,
    summary: Dict[str, Any],
) -> Dict[str, Any]:
    """Transform a call log summary into admin check-in format.

    Args:
        call_id: The call log ID
        summary: Call log summary dict

    Returns:
        Admin check-in formatted dict
    """
    phone = summary.get("patient_phone", "")
    name = get_patient_name_from_phone(phone)
    ai_summary = summary.get("ai_summary", "") or summary.get("summary", "")
    topics = extract_health_topics(ai_summary)

    return {
        "id": f"call_{call_id}",
        "patient_id": "demo",
        "patient_name": name,
        "type": "call",
        "summary": ai_summary,
        "timestamp": summary.get("timestamp", ""),
        "submitted_at": summary.get("call_date", ""),
        "sentiment": "neutral",
        "key_topics": topics,
        "status": "pending",
        "provider_reviewed": False,
        "reviewed_by": "",
        "reviewed_at": "",
    }


async def fetch_all_checkins(
    status_filter: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Fetch all check-ins for admin view.

    Args:
        status_filter: Filter by status ('pending', 'reviewed', 'flagged')
        limit: Maximum number of check-ins to return

    Returns:
        List of admin check-in records
    """
    logger.info("Fetching admin checkins (status=%s, limit=%d)", status_filter, limit)

    # TODO: Implement API call
    logger.debug("fetch_all_checkins: Using demo data (API not implemented)")
    return []


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

    # TODO: Implement API call
    logger.debug("update_checkin_status: Not implemented")
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
