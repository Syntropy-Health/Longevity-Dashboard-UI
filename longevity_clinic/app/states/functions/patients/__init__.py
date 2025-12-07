"""Patient-specific functions for state operations."""

from .call_logs import (
    summarize_transcript,
    process_call_logs,
    get_patient_name,
    PHONE_TO_PATIENT_NAME,
)
from .checkins import extract_checkin_from_text
from .voice import (
    transcribe_audio,
    transcribe_audio_file,
    format_recording_duration,
    get_openai_client,
)
from .biomarkers import (
    fetch_biomarkers,
    fetch_biomarker_history,
    fetch_treatments,
    fetch_appointments,
    calculate_biomarker_status,
    calculate_biomarker_trend,
    format_biomarker_value,
    load_all_biomarker_data,
    get_biomarker_by_name,
    get_biomarker_optimal_range,
)
from .analytics import (
    fetch_analytics_summary,
    fetch_biomarker_panels,
    generate_analytics_report,
    calculate_health_score,
    calculate_trend_analysis,
    format_analytics_value,
)
from .dashboard import (
    fetch_nutrition_summary,
    fetch_medications,
    fetch_conditions,
    fetch_symptoms,
    fetch_data_sources,
    fetch_food_entries,
    fetch_reminders,
    load_all_dashboard_data,
    sync_data_source,
    calculate_medication_adherence,
    categorize_conditions,
    calculate_symptom_trends,
)
from .patients import (
    fetch_patients,
    fetch_trend_data,
    fetch_treatment_data,
    fetch_biomarker_analytics_data,
    load_all_patient_data,
)

# Re-export fetch_call_logs from utils for convenience
from ..utils import fetch_call_logs

__all__ = [
    # Call logs
    "fetch_call_logs",
    "summarize_transcript",
    "process_call_logs",
    "get_patient_name",
    "PHONE_TO_PATIENT_NAME",
    # Check-ins
    "extract_checkin_from_text",
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
    "calculate_biomarker_status",
    "calculate_biomarker_trend",
    "format_biomarker_value",
    "load_all_biomarker_data",
    "get_biomarker_by_name",
    "get_biomarker_optimal_range",
    # Analytics
    "fetch_analytics_summary",
    "fetch_biomarker_panels",
    "generate_analytics_report",
    "calculate_health_score",
    "calculate_trend_analysis",
    "format_analytics_value",
    # Dashboard
    "fetch_nutrition_summary",
    "fetch_medications",
    "fetch_conditions",
    "fetch_symptoms",
    "fetch_data_sources",
    "fetch_food_entries",
    "fetch_reminders",
    "load_all_dashboard_data",
    "sync_data_source",
    "calculate_medication_adherence",
    "categorize_conditions",
    "calculate_symptom_trends",
    # Patients
    "fetch_patients",
    "fetch_trend_data",
    "fetch_treatment_data",
    "fetch_biomarker_analytics_data",
    "load_all_patient_data",
]
