"""Patient-specific functions for state operations."""

from __future__ import annotations

# Local application - analytics
from .analytics import (
    calculate_health_score,
    calculate_trend_analysis,
    fetch_analytics_summary,
)

# Local application - biomarkers
from .biomarkers import (
    fetch_appointments,
    fetch_biomarker_history,
    fetch_biomarkers,
    fetch_treatments,
    load_all_biomarker_data,
)

# Local application - dashboard
from .dashboard import (
    calculate_medication_adherence,
    fetch_conditions,
    fetch_data_sources,
    fetch_reminders,
    fetch_symptoms,
    load_all_dashboard_data,
)

# Local application - patients
from .patients import (
    fetch_biomarker_analytics_data,
    fetch_patients,
    fetch_treatment_data,
    fetch_trend_data,
    load_all_patient_data,
)

# Local application - voice
from .voice import (
    format_recording_duration,
    get_openai_client,
    transcribe_audio,
    transcribe_audio_file,
)

# Re-export fetch_call_logs from utils for convenience
from ..utils import fetch_call_logs

__all__ = [
    # Call logs
    "fetch_call_logs",
    # Voice
    "transcribe_audio",
    "transcribe_audio_file",
    "format_recording_duration",
    "get_openai_client",
    # Biomarkers
    "fetch_biomarkers",
    "fetch_biomarker_history",
    "fetch_treatments",
    "fetch_appointments",
    "load_all_biomarker_data",
    # Analytics
    "fetch_analytics_summary",
    "calculate_health_score",
    "calculate_trend_analysis",
    # Dashboard
    "fetch_conditions",
    "fetch_symptoms",
    "fetch_data_sources",
    "fetch_reminders",
    "load_all_dashboard_data",
    "calculate_medication_adherence",
    # Patients
    "fetch_patients",
    "fetch_trend_data",
    "fetch_treatment_data",
    "fetch_biomarker_analytics_data",
    "load_all_patient_data",
]
