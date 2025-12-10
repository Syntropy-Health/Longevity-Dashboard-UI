"""State modules for the Longevity Clinic application.

This package contains Reflex state classes organized by functionality:
- Patient states: Biomarkers, analytics
- Admin states: Patient management, dashboard
- Shared states: Auth, voice transcription, notifications, health dashboard
- Treatment states: Search, management
- Checkin states: Unified patient and admin check-in management
- Appointment states: Scheduling and calendar

Functions are extracted to the functions/ subpackage for better
separation of concerns and testability.
"""

# Auth states
from .auth.auth_state import AuthState

# Patient states (from patient package)
from .patient.state import PatientState
from .patient.biomarker_state import PatientBiomarkerState
from .patient.analytics_state import PatientAnalyticsState

# Aliases for cleaner naming
BiomarkerState = PatientBiomarkerState
AnalyticsState = PatientAnalyticsState

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
from .shared.dashboard_state import (
    HealthDashboardState,
    AdminDashboardState,
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
    "BiomarkerState",
    "AnalyticsState",
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
    # Dashboard states
    "HealthDashboardState",
    "AdminDashboardState",
]
