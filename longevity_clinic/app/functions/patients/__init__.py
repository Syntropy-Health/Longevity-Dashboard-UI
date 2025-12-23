"""Patient-specific functions for state operations."""

from __future__ import annotations

# Re-export fetch_call_logs from utils for convenience
from ..utils import fetch_call_logs

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

__all__ = [
    "calculate_health_score",
    "calculate_medication_adherence",
    "calculate_trend_analysis",
    # Analytics
    "fetch_analytics_summary",
    "fetch_appointments",
    "fetch_biomarker_analytics_data",
    "fetch_biomarker_history",
    # Biomarkers
    "fetch_biomarkers",
    # Call logs
    "fetch_call_logs",
    # Dashboard
    "fetch_conditions",
    "fetch_data_sources",
    # Patients
    "fetch_patients",
    "fetch_reminders",
    "fetch_symptoms",
    "fetch_treatment_data",
    "fetch_treatments",
    "fetch_trend_data",
    "format_recording_duration",
    "get_openai_client",
    "load_all_biomarker_data",
    "load_all_dashboard_data",
    "load_all_patient_data",
    # Voice
    "transcribe_audio",
    "transcribe_audio_file",
]
