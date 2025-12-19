"""State modules for the Longevity Clinic application.

This package contains Reflex state classes organized by functionality:
- Patient states: Biomarkers
- Admin states: Patient management, dashboard, metrics
- Shared states: Auth, voice transcription, notifications, health dashboard
- Treatment states: Search, management
- Checkin states: Unified patient and admin check-in management
- Appointment states: Scheduling and calendar

Functions are extracted to the functions/ subpackage for better
separation of concerns and testability.
"""

from __future__ import annotations

# Admin metrics state
from .admin_metrics_state import AdminMetricsState

# Auth states
from .auth.base import AuthState

# Patient states
from .patient.biomarker import BiomarkerState
from .patient.state import PatientState

# Shared states
from .shared.dashboard import AdminDashboardState, HealthDashboardState
from .shared.notification import NotificationState
from .shared.voice_transcription import (
    VoiceTranscriptionState,
    audio_capture,
    voice_recorder_component,
)
from .shared.checkin import CheckinState
from .shared.appointment import AppointmentState
from .shared.treatment import TreatmentState, TreatmentSearchState

# TreatmentProtocol TypedDict (for backwards compatibility)
from ..data.state_schemas import TreatmentProtocol

__all__ = [
    # Auth
    "AuthState",
    # Patient states
    "PatientState",
    "BiomarkerState",
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
    # Admin metrics
    "AdminMetricsState",
]
