"""Utility functions for vlogs processing."""

import json
from datetime import datetime, timezone
from typing import Optional

from longevity_clinic.app.functions.db_utils import get_patient_name_by_phone
from longevity_clinic.app.data.process_schema import CallLogsOutput


def get_patient_name(phone: str) -> str:
    """Get patient name from phone number via database lookup."""
    return get_patient_name_by_phone(phone, fallback="Unknown Patient")


def json_dumps_or_none(
    items: list, transform=lambda x: x.model_dump()
) -> Optional[str]:
    """JSON serialize list or return None if empty."""
    return json.dumps([transform(i) for i in items]) if items else None


def get_medications(output: CallLogsOutput) -> list:
    """Extract medications from output (handles both field names)."""
    return output.medications_entries


def parse_phone(raw_phone) -> str:
    """Extract phone string from raw phone (dict or str)."""
    return (
        raw_phone.get("phone_number", "") if isinstance(raw_phone, dict) else raw_phone
    )


def parse_datetime(date_str: str) -> datetime:
    """Parse ISO datetime string, fallback to now if invalid."""
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return datetime.now(timezone.utc)


def get_best_summary(api_summary: str, full_transcript: str) -> str:
    """Extract best summary from API or transcript."""
    if api_summary and len(api_summary.strip()) > 20:
        return api_summary.strip()

    if full_transcript:
        transcript = full_transcript.strip()
        user_lines = [
            line[5:].strip()
            for line in transcript.split("\n")
            if line.strip().lower().startswith("user:") and line[5:].strip()
        ]

        if user_lines:
            user_summary = " ".join(user_lines)
            return (
                user_summary[:200] + "..." if len(user_summary) > 200 else user_summary
            )

        if len(transcript) > 100 and not transcript.lower().startswith("ai:"):
            return transcript[:300] + "..." if len(transcript) > 300 else transcript

        if len(transcript) < 100:
            return "Brief call - conversation incomplete"

    return "Voice call check-in"
