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

# TreatmentProtocol TypedDict (for backwards compatibility)
from ..data.schemas.state import TreatmentProtocol

# Admin metrics state
from .admin_metrics_state import AdminMetricsState

# Auth states
from .auth.base import AuthState

# Patient states
from .patient.biomarker import BiomarkerState
from .patient.state import PatientState
from .shared.appointment import AppointmentState
from .shared.checkin import CheckinState

# Shared states
# Decomposed dashboard states
from .shared.dashboard import (
    AdminDashboardState,
    ConditionState,
    DataSourceState,
    FoodState,
    MedicationState,
    SettingsState,
    SymptomState,
    TreatmentPortalState,
)
from .shared.notification import NotificationState
from .shared.treatment import TreatmentSearchState, TreatmentState
from .shared.voice_transcription import (
    VoiceTranscriptionState,
    audio_capture,
    voice_recorder_component,
)

__all__ = [
    "AdminDashboardState",
    # Admin metrics
    "AdminMetricsState",
    "AppointmentState",
    # Auth
    "AuthState",
    "BiomarkerState",
    # Check-in states (unified)
    "CheckinState",
    # Dashboard states (decomposed)
    "ConditionState",
    "DataSourceState",
    "FoodState",
    "MedicationState",
    # Notification & Appointment
    "NotificationState",
    # Patient states
    "PatientState",
    "SettingsState",
    "SymptomState",
    "TreatmentPortalState",
    "TreatmentProtocol",
    "TreatmentSearchState",
    "TreatmentState",
    # Voice
    "VoiceTranscriptionState",
    "audio_capture",
    "voice_recorder_component",
]
