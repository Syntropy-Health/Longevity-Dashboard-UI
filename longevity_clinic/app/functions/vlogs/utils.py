"""Utility functions for vlogs processing."""

from datetime import UTC, datetime

from longevity_clinic.app.data.process_schema import MetricLogsOutput
from longevity_clinic.app.functions.db_utils import get_patient_name_by_phone


def get_patient_name(phone: str) -> str:
    """Get patient name from phone number via database lookup."""
    return get_patient_name_by_phone(phone, fallback="Unknown Patient")


def get_medications(output: MetricLogsOutput) -> list:
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
        return datetime.now(UTC)


def tag_checkin_with_metadata(
    output: MetricLogsOutput,
    checkin_id: str,
    checkin_type: str,
    timestamp: str,
    patient_name: str,
    fallback_summary: str,
) -> MetricLogsOutput:
    """Override system-generated fields in checkin with provided metadata.

    Args:
        output: The MetricLogsOutput from LLM parsing
        checkin_id: Unique identifier for this checkin
        checkin_type: Type of checkin ("text", "call", "voice")
        timestamp: Formatted timestamp string
        patient_name: Patient name (uses LLM-extracted if empty)
        fallback_summary: Content to use if summary is empty

    Returns:
        Updated MetricLogsOutput with tagged metadata
    """
    output.checkin.id = checkin_id
    output.checkin.type = checkin_type
    output.checkin.timestamp = timestamp
    output.checkin.provider_reviewed = False
    output.checkin.patient_name = patient_name or output.checkin.patient_name
    output.checkin.summary = output.checkin.summary or fallback_summary
    output.checkin.key_topics = output.checkin.key_topics or []

    return output

    return "Voice call check-in"
