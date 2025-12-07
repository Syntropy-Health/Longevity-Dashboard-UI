"""Patient check-in state management.

Handles check-in modal, voice recording, and call log sync functionality.
Extracted from PatientDashboardState for better separation of concerns.
"""

import asyncio
import uuid
from datetime import datetime
from typing import List

import reflex as rx

from ..config import get_logger
from ..data.demo import DEMO_CHECKINS, DEMO_PHONE_NUMBER
from ..data.state_schemas import CheckIn
from .functions import fetch_and_process_call_logs
from .functions.patients import extract_checkin_from_text
from .voice_transcription_state import VoiceTranscriptionState

logger = get_logger("longevity_clinic.checkins")


class PatientCheckinState(rx.State):
    """State management for patient check-ins.

    Handles:
    - Check-in modal state and operations
    - Voice recording for check-ins
    - Call log fetching and sync to checkins
    """

    # =========================================================================
    # Check-in Data
    # =========================================================================
    checkins: List[CheckIn] = DEMO_CHECKINS

    # =========================================================================
    # Check-in Modal State
    # =========================================================================
    show_checkin_modal: bool = False
    checkin_type: str = "voice"
    checkin_text: str = ""
    selected_topics: List[str] = []

    # =========================================================================
    # Voice Recording State
    # =========================================================================
    is_recording: bool = False
    recording_session_id: str = ""
    recording_duration: float = 0.0
    transcribed_text: str = ""
    transcription_status: str = (
        ""  # 'idle', 'recording', 'transcribing', 'done', 'error'
    )

    # =========================================================================
    # Call Logs Sync State
    # =========================================================================
    call_logs_syncing: bool = False
    call_logs_sync_error: str = ""
    last_sync_time: str = ""
    _processed_call_ids: List[
        str
    ] = []  # Track processed call IDs (List for Reflex compatibility)

    # =========================================================================
    # Computed Variables
    # =========================================================================

    @rx.var
    def unreviewed_checkins_count(self) -> int:
        """Count unreviewed check-ins."""
        return len([c for c in self.checkins if not c["provider_reviewed"]])

    @rx.var
    def voice_call_checkins_count(self) -> int:
        """Count check-ins created from voice calls."""
        return len([c for c in self.checkins if c.get("type") == "call"])

    @rx.var
    def checkins_this_week_count(self) -> int:
        """Count check-ins from this week."""
        # For demo purposes, count all checkins (in production, filter by date)
        return len(self.checkins)

    # =========================================================================
    # Check-in Type and Text
    # =========================================================================

    @rx.event
    async def set_checkin_type(self, checkin_type: str):
        """Set check-in type."""
        self.checkin_type = checkin_type
        # Reset recording state when switching types
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.transcription_status = "idle"

        voice_state = await self.get_state(VoiceTranscriptionState)
        voice_state.transcript = ""
        voice_state.has_error = False
        voice_state.error_message = ""

    def set_checkin_text(self, text: str):
        """Set the check-in text content."""
        self.checkin_text = text

    def toggle_topic(self, topic: str):
        """Toggle a topic selection."""
        if topic in self.selected_topics:
            self.selected_topics = [t for t in self.selected_topics if t != topic]
        else:
            self.selected_topics = [*self.selected_topics, topic]

    def is_topic_selected(self, topic: str) -> bool:
        """Check if a topic is selected."""
        return topic in self.selected_topics

    # =========================================================================
    # Voice Recording
    # =========================================================================

    @rx.event
    async def start_recording(self):
        """Start voice recording."""
        self.is_recording = True
        self.transcription_status = "recording"
        self.recording_duration = 0.0
        self.recording_session_id = f"rec_{uuid.uuid4().hex[:8]}"

    @rx.event
    async def stop_recording(self):
        """Stop voice recording - transcript comes from VoiceTranscriptionState."""
        self.is_recording = False
        self.transcription_status = "done"

    @rx.event
    async def toggle_recording(self):
        """Toggle voice recording on/off."""
        if not self.is_recording:
            # Start recording
            yield PatientCheckinState.start_recording
            # Start duration timer in background
            yield PatientCheckinState.increment_recording_duration
        else:
            # Stop recording
            yield PatientCheckinState.stop_recording

    @rx.event(background=True)
    async def increment_recording_duration(self):
        """Increment the recording duration timer."""
        async with self:
            # Check initial state
            if not self.is_recording:
                return

        while True:
            await asyncio.sleep(1)
            async with self:
                # Check if still recording before incrementing
                if not self.is_recording:
                    return
                self.recording_duration += 1.0

    # =========================================================================
    # Check-in Modal Operations
    # =========================================================================

    @rx.event
    async def open_checkin_modal(self):
        """Open check-in modal."""
        logger.info("open_checkin_modal called - setting show_checkin_modal=True")
        self.show_checkin_modal = True
        # Reset local state
        self.checkin_type = "voice"
        self.checkin_text = ""
        self.selected_topics = []
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.transcription_status = "idle"

        # Clear voice transcription state directly
        logger.debug("Clearing VoiceTranscriptionState")
        voice_state = await self.get_state(VoiceTranscriptionState)
        voice_state.transcript = ""
        voice_state.has_error = False
        voice_state.error_message = ""
        logger.info("open_checkin_modal completed")

    @rx.event
    async def close_checkin_modal(self):
        """Close check-in modal."""
        self.show_checkin_modal = False
        self.is_recording = False
        self.transcription_status = "idle"

        # Clear voice transcription state directly
        voice_state = await self.get_state(VoiceTranscriptionState)
        voice_state.transcript = ""
        voice_state.has_error = False
        voice_state.error_message = ""

    def set_show_checkin_modal(self, value: bool):
        """Set show checkin modal state."""
        self.show_checkin_modal = value

    # =========================================================================
    # Save Check-in
    # =========================================================================

    @rx.event
    async def save_checkin(self):
        """Save a new check-in using LLM for structured extraction."""
        content = (
            self.transcribed_text
            if self.checkin_type == "voice"
            else self.checkin_text.strip()
        )

        if len(content) < 10:
            return

        checkin_model = await extract_checkin_from_text(content, self.checkin_type)
        self.checkins = [checkin_model.to_dict(), *self.checkins]

        self.show_checkin_modal = False
        self._reset_checkin_state()

    @rx.event
    async def save_checkin_with_voice(self):
        """Save a new check-in via voice"""
        voice_state = await self.get_state(VoiceTranscriptionState)
        content = (
            voice_state.transcript
            if self.checkin_type == "voice"
            else self.checkin_text.strip()
        )

        if not content.strip():
            return

        checkin_model = await extract_checkin_from_text(content, self.checkin_type)
        self.checkins = [checkin_model.to_dict(), *self.checkins]

        self.show_checkin_modal = False
        self._reset_checkin_state()

        # Clear voice state
        voice_state.transcript = ""
        voice_state.has_error = False
        voice_state.error_message = ""

    def _reset_checkin_state(self):
        """Reset check-in modal state."""
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.checkin_text = ""
        self.selected_topics = []
        self.transcription_status = "idle"

    # =========================================================================
    # Call Logs Sync
    # =========================================================================

    @rx.event(background=True)
    async def refresh_call_logs(self):
        """Fetch call logs and sync to checkins (background task).

        Background task pattern per https://reflex.dev/docs/events/background-events:
        - Minimize time inside `async with self` (state lock)
        - Do heavy I/O outside the lock
        - Use on_load (not on_mount) so task terminates on navigation
        """
        print("[DEBUG] refresh_call_logs: ENTERED", flush=True)
        logger.info("refresh_call_logs: Starting")

        # 1. Quick lock to set syncing flag and copy needed state
        print("[DEBUG] refresh_call_logs: Acquiring lock for setup...", flush=True)
        async with self:
            self.call_logs_syncing = True
            self.call_logs_sync_error = ""
            processed_ids = set(self._processed_call_ids)
            current_checkins = list(self.checkins)  # Copy current checkins
        print("[DEBUG] refresh_call_logs: Lock released, starting fetch...", flush=True)

        try:
            # 2. Heavy I/O OUTSIDE the lock
            print(
                "[DEBUG] refresh_call_logs: Calling fetch_and_process_call_logs...",
                flush=True,
            )
            new_count, new_checkins, new_summaries = await fetch_and_process_call_logs(
                phone_number=DEMO_PHONE_NUMBER,
                processed_ids=processed_ids,
                use_llm_summary=False,
            )
            print(
                f"[DEBUG] refresh_call_logs: Fetch complete, {new_count} new logs",
                flush=True,
            )
            logger.info("refresh_call_logs: Processed %d new logs", new_count)

            # 3. Process results OUTSIDE the lock
            existing_ids = {c["id"] for c in current_checkins}
            to_add = [c for c in new_checkins if c["id"] not in existing_ids]
            if to_add:
                sorted_new = sorted(
                    to_add, key=lambda x: x.get("timestamp", ""), reverse=True
                )
            else:
                sorted_new = []

            # 4. Quick lock to update state
            print(
                "[DEBUG] refresh_call_logs: Acquiring lock to save results...",
                flush=True,
            )
            async with self:
                if sorted_new:
                    self.checkins = sorted_new + list(self.checkins)
                    logger.info("refresh_call_logs: Added %d checkins", len(sorted_new))

                self._processed_call_ids = list(
                    processed_ids | set(new_summaries.keys())
                )
                self.last_sync_time = datetime.now().strftime("%I:%M %p")
                self.call_logs_syncing = False
            print("[DEBUG] refresh_call_logs: COMPLETED successfully", flush=True)

        except Exception as e:
            print(f"[DEBUG] refresh_call_logs: FAILED - {e}", flush=True)
            logger.error("refresh_call_logs: Failed - %s", e)
            async with self:
                self.call_logs_sync_error = str(e)
                self.call_logs_syncing = False
