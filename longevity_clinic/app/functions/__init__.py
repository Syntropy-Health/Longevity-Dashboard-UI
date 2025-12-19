"""Shared functions for state operations.

This module provides extracted business logic functions that can be used
across state classes without coupling to Reflex state management.

Structure:
- utils.py: Shared utility functions (timestamp formatting, API calls)
- llm/: Reusable LLM initialization and structured output helpers
- patients/: Patient-specific functions (check-ins, biomarkers, voice)
- admins/: Admin-specific functions (check-in management)
- vlogs/: Call log processing with CDC pattern
"""

from __future__ import annotations

# Local application - config
from longevity_clinic.app.config import VlogsConfig

# Local application - LLM utilities
from .llm import (
    get_chat_model,
    get_structured_output_model,
    parse_with_structured_output,
)

# Local application - admins
from .admins import (
    count_checkins_by_status,
    extract_health_topics,
    filter_checkins,
    get_patient_name_from_phone,
)

# Local application - patients
from .patients import (
    calculate_health_score,
    calculate_medication_adherence,
    calculate_trend_analysis,
    fetch_analytics_summary,
    fetch_biomarker_history,
    fetch_biomarkers,
    fetch_conditions,
    format_recording_duration,
    transcribe_audio,
    transcribe_audio_file,
)

# Local application - utils & agent
from .utils import fetch_call_logs, format_timestamp
from .vlogs import VlogsAgent

__all__ = [
    # LLM utilities
    "get_chat_model",
    "get_structured_output_model",
    "parse_with_structured_output",
    # Utils (shared)
    "format_timestamp",
    "fetch_call_logs",
    # VlogsAgent
    "VlogsAgent",
    "VlogsConfig",
    # Patient: Voice
    "transcribe_audio",
    "transcribe_audio_file",
    "format_recording_duration",
    # Patient: Biomarkers
    "fetch_biomarkers",
    "fetch_biomarker_history",
    # Patient: Analytics
    "fetch_analytics_summary",
    "calculate_health_score",
    "calculate_trend_analysis",
    # Patient: Dashboard
    "fetch_conditions",
    "calculate_medication_adherence",
    # Admin: Check-ins
    "filter_checkins",
    "count_checkins_by_status",
    "get_patient_name_from_phone",
    "extract_health_topics",
]
