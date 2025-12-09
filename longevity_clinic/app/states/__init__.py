"""State modules for the Longevity Clinic application.

This package contains Reflex state classes organized by functionality:
- Patient states: Dashboard, biomarkers, analytics
- Admin states: Check-in management
- Shared states: Auth, voice transcription, notifications
- Treatment states: Search, management
- Checkin states: Unified patient and admin check-in management
- Appointment states: Scheduling and calendar

Functions are extracted to the functions/ subpackage for better
separation of concerns and testability.
"""

# Auth states
from .auth.auth_state import AuthState

# Patient states
from .patient.patient_state import PatientState
from .patient.patient_biomarker_state import PatientBiomarkerState
from .patient.patient_analytics_state import PatientAnalyticsState
from .patient.patient_dashboard_state import PatientDashboardState

# Treatment states
from .treatments.treatment_state import TreatmentState
from .treatments.treatment_search_state import TreatmentSearchState, TreatmentProtocol

# Shared states
from .shared.notification_state import NotificationState
from .shared.voice_transcription_state import (
    VoiceTranscriptionState,
    audio_capture,
    voice_recorder_component,
)

# Appointment states
from .appointments.appointment_state import AppointmentState

# Check-in states
from .checkins.checkin_state import CheckinState

__all__ = [
    # Auth
    "AuthState",
    # Patient states
    "PatientState",
    "PatientBiomarkerState",
    "PatientAnalyticsState",
    "PatientDashboardState",
    # Treatment states
    "TreatmentState",
    "TreatmentSearchState",
    "TreatmentProtocol",
    # Check-in states (unified)
    "CheckinState",
    # Notification & Appointment
    "NotificationState",
    "AppointmentState",
    # Voice
    "VoiceTranscriptionState",
    "audio_capture",
    "voice_recorder_component",
]
