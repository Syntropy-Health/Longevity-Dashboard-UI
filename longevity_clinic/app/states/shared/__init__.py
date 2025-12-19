"""Shared state modules.

This package contains shared state classes used across admin and patient views.
"""

from .notification import NotificationState
from .voice_transcription import (
    VoiceTranscriptionState,
    audio_capture,
    voice_recorder_component,
)
from .dashboard import (
    HealthDashboardState,
    AdminDashboardState,
)
from .checkin import CheckinState
from .appointment import AppointmentState
from .treatment import TreatmentState, TreatmentSearchState

__all__ = [
    "NotificationState",
    "VoiceTranscriptionState",
    "audio_capture",
    "voice_recorder_component",
    "HealthDashboardState",
    "AdminDashboardState",
    "CheckinState",
    "AppointmentState",
    "TreatmentState",
    "TreatmentSearchState",
]
