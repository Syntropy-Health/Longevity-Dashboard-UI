"""Shared utility functions for state operations."""

from datetime import datetime
from typing import Optional

import httpx

from ...config import current_config, get_logger
from ...data.api_schemas import CallLogsQueryParams, CallLogsAPIConfig
from ...data.state_schemas import CallLogEntry, TranscriptSummary

logger = get_logger("longevity_clinic.functions")

# Shared API config
_call_logs_api_config = CallLogsAPIConfig(
    base_url=current_config.call_logs_api_base,
    api_token=current_config.call_api_token,
)


def format_timestamp(date_str: str, fmt: str = "%B %d, %Y at %I:%M %p") -> str:
    """Format ISO date string to human-readable timestamp."""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime(fmt)
    except (ValueError, AttributeError):
        return date_str or datetime.now().strftime(fmt)


def extract_topics_from_summary(summary: str) -> list[str]:
    """Extract key topics from summary (basic fallback)."""
    return ["voice call"] if not summary else ["health update"]


async def fetch_call_logs(
    phone_number: Optional[str] = None,
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
        logger.info("Fetched %d call logs", len(call_logs))
        return call_logs


async def fetch_and_process_call_logs(
    phone_number: Optional[str] = None,
    processed_ids: Optional[set[str]] = None,
    use_llm_summary: bool = False,
    limit: int = 50,
) -> tuple[int, list[dict], dict[str, TranscriptSummary]]:
    """Fetch call logs from API and process them into checkins/summaries.

    Combined function for fetching and processing call logs in one call.

    Args:
        phone_number: Filter by phone (None = all logs)
        processed_ids: Set of call_ids already processed (skip these)
        use_llm_summary: Use LLM for AI summary (slower but richer)
        limit: Max records to fetch

    Returns:
        Tuple of (new_logs_count, new_checkins, new_summaries)
    """
    from .patients.call_logs import process_call_logs

    processed_ids = processed_ids or set()

    # Fetch from API
    call_logs = await fetch_call_logs(phone_number=phone_number, limit=limit)

    # Process into checkins/summaries
    return await process_call_logs(call_logs, processed_ids, use_llm_summary)
