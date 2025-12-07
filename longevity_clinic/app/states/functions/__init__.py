"""Shared functions for state operations.

This module provides extracted business logic functions that can be used
across state classes without coupling to Reflex state management.

Structure:
- utils.py: Shared utility functions (timestamp formatting, API calls)
- patients/: Patient-specific functions (check-ins, biomarkers, voice)
- admins/: Admin-specific functions (check-in management)
"""

from .utils import (
    format_timestamp,
    extract_topics_from_summary,
    fetch_call_logs,
    fetch_and_process_call_logs,
)
from .patients import (
    # Call logs
    summarize_transcript,
    process_call_logs,
    get_patient_name,
    PHONE_TO_PATIENT_NAME,
    # Check-ins
    extract_checkin_from_text,
    # Voice
    transcribe_audio,
    transcribe_audio_file,
    format_recording_duration,
    # Biomarkers
    fetch_biomarkers,
    fetch_biomarker_history,
    calculate_biomarker_status,
    calculate_biomarker_trend,
    # Analytics
    fetch_analytics_summary,
    calculate_health_score,
    calculate_trend_analysis,
    # Dashboard
    fetch_nutrition_summary,
    fetch_medications,
    fetch_conditions,
    calculate_medication_adherence,
)
from .admins import (
    transform_call_log_to_admin_checkin,
    filter_checkins,
    count_checkins_by_status,
    get_patient_name_from_phone,
    extract_health_topics,
)

__all__ = [
    # Utils (shared)
    "format_timestamp",
    "extract_topics_from_summary",
    "fetch_call_logs",
    "fetch_and_process_call_logs",
    # Patient: Call logs
    "summarize_transcript",
    "process_call_logs",
    "get_patient_name",
    "PHONE_TO_PATIENT_NAME",
    # Patient: Check-ins
    "extract_checkin_from_text",
    # Patient: Voice
    "transcribe_audio",
    "transcribe_audio_file",
    "format_recording_duration",
    # Patient: Biomarkers
    "fetch_biomarkers",
    "fetch_biomarker_history",
    "calculate_biomarker_status",
    "calculate_biomarker_trend",
    # Patient: Analytics
    "fetch_analytics_summary",
    "calculate_health_score",
    "calculate_trend_analysis",
    # Patient: Dashboard
    "fetch_nutrition_summary",
    "fetch_medications",
    "fetch_conditions",
    "calculate_medication_adherence",
    # Admin: Check-ins
    "transform_call_log_to_admin_checkin",
    "filter_checkins",
    "count_checkins_by_status",
    "get_patient_name_from_phone",
    "extract_health_topics",
]
