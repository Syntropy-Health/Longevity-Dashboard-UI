"""Shared state modules.

This package contains shared state classes used across admin and patient views.
"""

from .appointment import AppointmentState
from .checkin import CheckinState

# Full dashboard states
from .dashboard import (
    ConditionState,
    DataSourceState,
    FoodState,
    MedicationState,
    SettingsState,
    SymptomState,
)
from .notification import NotificationState
from .treatment import TreatmentSearchState, TreatmentState
from .voice_transcription import (
    VoiceTranscriptionState,
    audio_capture,
    voice_recorder_component,
)

__all__ = [
    "AppointmentState",
    "CheckinState",
    "ConditionState",
    "DataSourceState",
    "FoodState",
    "MedicationState",
    "NotificationState",
    "SettingsState",
    "SymptomState",
    "TreatmentSearchState",
    "TreatmentState",
    "VoiceTranscriptionState",
    "audio_capture",
    "voice_recorder_component",
]
