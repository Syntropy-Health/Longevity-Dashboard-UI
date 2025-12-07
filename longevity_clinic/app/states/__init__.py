"""State modules for the Longevity Clinic application.

This package contains Reflex state classes organized by functionality:
- Patient states: Dashboard, biomarkers, check-ins, analytics
- Admin states: Check-in management
- Shared states: Auth, voice transcription
- Treatment states: Search, management

Functions are extracted to the functions/ subpackage for better
separation of concerns and testability.
"""

from .auth_state import AuthState
from .patient_state import PatientState
from .patient_biomarker_state import PatientBiomarkerState
from .patient_analytics_state import PatientAnalyticsState
from .treatment_state import TreatmentState
from .treatment_search_state import TreatmentSearchState
from .patient_dashboard_state import PatientDashboardState
from .patient_checkin_state import PatientCheckinState
from .notification_state import NotificationState
from .appointment_state import AppointmentState
from .voice_transcription_state import (
    VoiceTranscriptionState,
    audio_capture,
    voice_recorder_component,
)

# Admin states - use refactored version from admin/
from .admin.checkins_state import AdminCheckinsState

__all__ = [
    # Auth
    "AuthState",
    # Patient states
    "PatientState",
    "PatientBiomarkerState",
    "PatientAnalyticsState",
    "PatientDashboardState",
    "PatientCheckinState",
    # Treatment states
    "TreatmentState",
    "TreatmentSearchState",
    # Notification & Appointment
    "NotificationState",
    "AppointmentState",
    # Voice
    "VoiceTranscriptionState",
    "audio_capture",
    "voice_recorder_component",
    # Admin
    "AdminCheckinsState",
]
