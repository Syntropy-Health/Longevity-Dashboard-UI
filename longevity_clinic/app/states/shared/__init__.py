"""Shared state modules.

This package contains shared state classes used across admin and patient views.
"""

from .appointment import AppointmentState
from .checkin import CheckinState
from .dashboard import (
    AdminDashboardState,
    HealthDashboardState,
)
from .notification import NotificationState
from .treatment import TreatmentSearchState, TreatmentState
from .voice_transcription import (
    VoiceTranscriptionState,
    audio_capture,
    voice_recorder_component,
)

__all__ = [
    "AdminDashboardState",
    "AppointmentState",
    "CheckinState",
    "HealthDashboardState",
    "NotificationState",
    "TreatmentSearchState",
    "TreatmentState",
    "VoiceTranscriptionState",
    "audio_capture",
    "voice_recorder_component",
]
