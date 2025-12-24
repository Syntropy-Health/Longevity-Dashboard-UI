"""Shared utility functions for state operations."""

from __future__ import annotations

# Standard library
import random
from datetime import datetime
from typing import Any

# Third-party
import httpx

# Local application
from longevity_clinic.app.config import current_config, get_logger
from longevity_clinic.app.data.schemas.api import CallLogsAPIConfig, CallLogsQueryParams
from longevity_clinic.app.data.schemas.state import CallLogEntry

logger = get_logger("longevity_clinic.functions")

# Shared API config
_call_logs_api_config = CallLogsAPIConfig(
    base_url=current_config.call_logs_api_base,
    api_token=current_config.call_api_token,
)


# =============================================================================
# Phone/String Utilities
# =============================================================================


def normalize_phone(phone: str) -> str:
    """Normalize phone number for comparison.

    Removes formatting characters: spaces, dashes, parentheses.

    Args:
        phone: Phone number string in any format

    Returns:
        Normalized phone number with only digits and optional +
    """
    if not phone:
        return ""
    return phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")


def format_phone_display(phone: str) -> str:
    """Format phone number for professional display.

    Converts normalized phone numbers like '+11234567890' to '+1 (123) 456-7890'.
    Handles US numbers with country code.
    Args:
        phone: Phone number string (normalized or with formatting)

    Returns:
        Formatted phone number for display, or original if format not recognized
    """
    if not phone:
        return ""

    # Normalize first
    clean = normalize_phone(phone)

    # US number with country code: +1XXXXXXXXXX (12 chars total)
    if clean.startswith("+1") and len(clean) == 12:
        return f"+1({clean[2:5]}){clean[5:8]}-{clean[8:]}"

    # US number without country code: XXXXXXXXXX (10 digits)
    if not clean.startswith("+") and len(clean) == 10:
        return f"({clean[0:3]}) {clean[3:6]}-{clean[6:]}"

    # International or unrecognized format - return as-is
    return phone


# =============================================================================
# Data Generation Utilities
# =============================================================================


def generate_biomarker_history(
    base_val: float, volatility: float
) -> list[dict[str, Any]]:
    """Generate historical biomarker data with random variations.

    This is used to create mock historical data for display purposes.

    Args:
        base_val: Starting value for the biomarker
        volatility: Maximum variation (+/-) for each data point

    Returns:
        List of dictionaries with date and value for the last 6 months
    """
    data = []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    current = base_val
    for m in months:
        current += random.uniform(-volatility, volatility)
        data.append({"date": m, "value": round(current, 1)})
    return data


# =============================================================================
# Timestamp Utilities
# =============================================================================


def format_timestamp(date_str: str, fmt: str = "%B %d, %Y at %I:%M %p") -> str:
    """Format ISO date string to human-readable timestamp."""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime(fmt)
    except (ValueError, AttributeError):
        return date_str or datetime.now().strftime(fmt)


async def fetch_call_logs(
    phone_number: str | None = None,
    limit: int = 50,
    offset: int = 0,
    page: int = 1,
    require_transcript: bool = True,
) -> list[CallLogEntry]:
    """Fetch call logs from API.

    Args:
        phone_number: Filter by phone (None = all logs for admin)
        limit: Max records to return (1-100)
        offset: Records to skip
        page: Page number
        require_transcript: Only return records with transcripts

    Returns:
        List of call log entries
    """
    logger.info(
        "Fetching call logs (phone=%s, limit=%d, page=%d)", phone_number, limit, page
    )

    query_params = CallLogsQueryParams(
        caller_phone=phone_number,
        require_transcript=require_transcript,
        limit=limit,
        offset=offset,
        page=page,
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            _call_logs_api_config.base_url,
            params=query_params.to_api_params(),
            headers=_call_logs_api_config.get_headers(),
            timeout=_call_logs_api_config.timeout,
        )
        response.raise_for_status()
        data = response.json()
        call_logs = data.get("data", [])
        return call_logs
