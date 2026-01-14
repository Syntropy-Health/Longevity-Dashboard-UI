"""Transcription state for Syntropy chat audio input."""

import reflex as rx


class TranscriptionState(rx.State):
    """State for handling audio transcription in Syntropy chat."""

    transcript: str = ""
    is_transcribing: bool = False
    error_message: str = ""
    device_id: str = ""

    @rx.event
    def on_error(self, error: str):
        """Handle transcription errors."""
        self.error_message = error
        self.is_transcribing = False

    @rx.event
    def set_transcript(self, text: str):
        """Set the transcript text."""
        self.transcript = text
        self.is_transcribing = False

    @rx.event
    def set_device_id(self, device_id: str):
        """Set the audio input device ID."""
        self.device_id = device_id

    @rx.event
    def clear_transcript(self):
        """Clear the current transcript."""
        self.transcript = ""
        self.error_message = ""

    @rx.event
    def start_transcription(self):
        """Mark transcription as started."""
        self.is_transcribing = True
        self.error_message = ""

    @rx.event
    def stop_transcription(self):
        """Mark transcription as stopped."""
        self.is_transcribing = False
