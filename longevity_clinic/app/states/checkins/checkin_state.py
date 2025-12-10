"""Unified check-in state management for both admin and patient views.

Combines admin_checkins_state.py and patient_checkin_state.py into a single
comprehensive state management module for check-ins across the application.
"""

import asyncio
import uuid
from datetime import datetime
from typing import List, Dict, Any

import reflex as rx

from ...config import get_logger
from ...data.demo import DEMO_CHECKINS, DEMO_PHONE_NUMBER, DEMO_ADMIN_CHECKINS
from ...data.state_schemas import CheckIn, AdminCheckIn
from ...data.process_schema import CallLogsOutput
from ..functions import VlogsAgent, VlogsConfig
from ..functions.patients import extract_checkin_from_text
from ..functions.admins import (
    filter_checkins,
    count_checkins_by_status,
    fetch_all_checkins,
)
from ..shared.voice_transcription_state import VoiceTranscriptionState

logger = get_logger("longevity_clinic.checkins")


class CheckinState(rx.State):
    """Unified state management for check-ins.

    Handles:
    - Patient check-in modal and operations (voice/text)
    - Admin check-in viewing and management
    - Call log syncing
    - Status updates and search/filtering
    """

    # =========================================================================
    # Patient Check-in Data
    # =========================================================================
    checkins: List[CheckIn] = DEMO_CHECKINS

    # =========================================================================
    # Admin Check-in Data
    # =========================================================================
    all_checkins: List[AdminCheckIn] = DEMO_ADMIN_CHECKINS
    call_log_checkins: List[AdminCheckIn] = []
    active_status_tab: str = "pending"
    search_query: str = ""

    # =========================================================================
    # Patient Check-in Modal State
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
    transcription_status: str = ""

    # =========================================================================
    # Admin Modals State
    # =========================================================================
    show_checkin_detail_modal: bool = False
    show_status_update_modal: bool = False
    show_transcript_modal: bool = False
    selected_checkin: Dict[str, Any] = {}
    selected_status: str = ""

    # =========================================================================
    # Call Logs Sync State
    # =========================================================================
    call_logs_syncing: bool = False
    call_logs_sync_error: str = ""
    last_sync_time: str = ""
    _processed_call_ids: List[str] = []

    # =========================================================================
    # Admin Loading State
    # =========================================================================
    is_loading: bool = False
    _admin_data_loaded: bool = False

    # =========================================================================
    # Patient Computed Variables
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
        return len(self.checkins)

    # =========================================================================
    # Admin Computed Variables
    # =========================================================================

    @rx.var
    def combined_checkins(self) -> List[AdminCheckIn]:
        """Combine all checkins and call log checkins."""
        return self.all_checkins + self.call_log_checkins

    @rx.var
    def filtered_checkins(self) -> List[AdminCheckIn]:
        """Filter checkins by status and search query."""
        return filter_checkins(
            self.combined_checkins,
            status=self.active_status_tab,
            search_query=self.search_query,
        )

    @rx.var
    def pending_count(self) -> int:
        """Count pending checkins."""
        return len([c for c in self.combined_checkins if c["status"] == "pending"])

    @rx.var
    def reviewed_count(self) -> int:
        """Count reviewed checkins."""
        return len([c for c in self.combined_checkins if c["status"] == "reviewed"])

    @rx.var
    def flagged_count(self) -> int:
        """Count flagged checkins."""
        return len([c for c in self.combined_checkins if c["status"] == "flagged"])

    @rx.var
    def total_count(self) -> int:
        """Total checkin count."""
        return len(self.combined_checkins)

    @rx.var
    def selected_checkin_transcript(self) -> str:
        """Get full transcript from selected checkin."""
        return self.selected_checkin.get(
            "full_transcript", self.selected_checkin.get("summary", "")
        )

    @rx.var
    def selected_checkin_topics(self) -> List[str]:
        """Get key topics from selected checkin."""
        return self.selected_checkin.get("key_topics", [])

    @rx.var
    def selected_checkin_status(self) -> str:
        """Get status from selected checkin."""
        return self.selected_checkin.get("status", "")

    @rx.var
    def selected_checkin_patient_name(self) -> str:
        """Get patient name from selected checkin."""
        return self.selected_checkin.get("patient_name", "")

    @rx.var
    def selected_checkin_timestamp(self) -> str:
        """Get timestamp from selected checkin."""
        return self.selected_checkin.get("timestamp", "")

    @rx.var
    def selected_checkin_type(self) -> str:
        """Get type from selected checkin."""
        return self.selected_checkin.get("type", "")

    @rx.var
    def selected_checkin_summary(self) -> str:
        """Get summary from selected checkin."""
        return self.selected_checkin.get("summary", "")

    @rx.var
    def selected_checkin_id(self) -> str:
        """Get id from selected checkin."""
        return self.selected_checkin.get("id", "")

    # =========================================================================
    # Patient Check-in Type and Text
    # =========================================================================

    @rx.event
    async def set_checkin_type(self, checkin_type: str):
        """Set check-in type."""
        self.checkin_type = checkin_type
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
        """Stop voice recording."""
        self.is_recording = False
        self.transcription_status = "done"

    @rx.event
    async def toggle_recording(self):
        """Toggle voice recording on/off."""
        if not self.is_recording:
            yield CheckinState.start_recording
            yield CheckinState.increment_recording_duration
        else:
            yield CheckinState.stop_recording

    @rx.event(background=True)
    async def increment_recording_duration(self):
        """Increment the recording duration timer."""
        async with self:
            if not self.is_recording:
                return

        while True:
            await asyncio.sleep(1)
            async with self:
                if not self.is_recording:
                    return
                self.recording_duration += 1.0

    # =========================================================================
    # Patient Check-in Modal Operations
    # =========================================================================

    @rx.event
    async def open_checkin_modal(self):
        """Open check-in modal."""
        logger.info("open_checkin_modal called - setting show_checkin_modal=True")
        self.show_checkin_modal = True
        self.checkin_type = "voice"
        self.checkin_text = ""
        self.selected_topics = []
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.transcription_status = "idle"

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

        voice_state = await self.get_state(VoiceTranscriptionState)
        voice_state.transcript = ""
        voice_state.has_error = False
        voice_state.error_message = ""

    def set_show_checkin_modal(self, value: bool):
        """Set show checkin modal state."""
        self.show_checkin_modal = value

    # =========================================================================
    # Save Patient Check-in
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
        """Save a new check-in via voice."""
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
    # Admin Check-in Management
    # =========================================================================

    def set_active_status_tab(self, tab: str):
        """Set active status filter tab."""
        self.active_status_tab = tab

    def set_search_query(self, query: str):
        """Set search query for filtering checkins."""
        self.search_query = query

    def open_checkin_detail(self, checkin: Dict[str, Any]):
        """Open check-in detail modal."""
        self.selected_checkin = checkin
        self.show_checkin_detail_modal = True

    def close_checkin_detail(self):
        """Close check-in detail modal."""
        self.show_checkin_detail_modal = False
        self.selected_checkin = {}

    def set_show_checkin_detail_modal(self, value: bool):
        """Set show checkin detail modal state."""
        self.show_checkin_detail_modal = value
        if not value:
            self.selected_checkin = {}

    # =========================================================================
    # Status Update Modal
    # =========================================================================

    def open_status_update_modal(self, checkin: Dict[str, Any]):
        """Open status update modal."""
        self.selected_checkin = checkin
        self.selected_status = checkin.get("status", "pending")
        self.show_status_update_modal = True

    def close_status_update_modal(self):
        """Close status update modal."""
        self.show_status_update_modal = False
        self.selected_checkin = {}
        self.selected_status = ""

    def set_selected_status(self, status: str):
        """Set selected status for update."""
        self.selected_status = status

    @rx.event
    async def update_checkin_status(self):
        """Update check-in status."""
        if not self.selected_checkin or not self.selected_status:
            return

        checkin_id = self.selected_checkin.get("id")
        if not checkin_id:
            return

        self._update_checkin(checkin_id, self.selected_status)
        self.show_status_update_modal = False
        self.selected_checkin = {}
        self.selected_status = ""

    def _update_checkin(self, checkin_id: str, status: str):
        """Update checkin status in both lists."""
        update = lambda lst: [
            (
                {
                    **c,
                    "status": status,
                    "provider_reviewed": True,
                    "reviewed_by": "Dr. Admin",
                    "reviewed_at": "Just now",
                }
                if c["id"] == checkin_id
                else c
            )
            for c in lst
        ]
        self.all_checkins = update(self.all_checkins)
        self.call_log_checkins = update(self.call_log_checkins)

    def mark_as_reviewed(self, checkin_id: str):
        """Mark check-in as reviewed."""
        self._update_checkin(checkin_id, "reviewed")

    def flag_checkin(self, checkin_id: str):
        """Flag check-in for attention."""
        self._update_checkin(checkin_id, "flagged")

    # =========================================================================
    # Transcript Modal
    # =========================================================================

    def open_transcript_modal(self, checkin: Dict[str, Any]):
        """Open transcript modal."""
        self.selected_checkin = checkin
        self.show_transcript_modal = True

    def close_transcript_modal(self):
        """Close transcript modal."""
        self.show_transcript_modal = False

    def set_show_transcript_modal(self, value: bool):
        """Set show transcript modal state."""
        self.show_transcript_modal = value

    # =========================================================================
    # Call Logs Sync (Admin)
    # =========================================================================

    @rx.event(background=True)
    async def load_admin_checkins(self):
        """Load admin check-ins data.

        Respects IS_DEMO env var: when True, returns demo data;
        when False, calls the API.
        """
        # Prevent duplicate loads
        async with self:
            if self._admin_data_loaded:
                logger.debug("load_admin_checkins: Data already loaded, skipping")
                return
            self.is_loading = True

        logger.info("load_admin_checkins: Starting")

        try:
            # Fetch data using extracted function (respects IS_DEMO config)
            checkins = await fetch_all_checkins()

            async with self:
                self.all_checkins = checkins
                self.is_loading = False
                self._admin_data_loaded = True

            logger.info("load_admin_checkins: Complete (%d checkins)", len(checkins))
        except Exception as e:
            logger.error("load_admin_checkins: Failed - %s", e)
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def sync_call_logs_to_admin(self):
        """Sync call logs from PatientState to admin view.

        Also loads demo data if not already loaded.
        """
        print("[DEBUG] sync_call_logs_to_admin ENTERED", flush=True)
        logger.info("sync_call_logs_to_admin: Starting sync (background)")

        # Load demo data if not already loaded
        async with self:
            if not self._admin_data_loaded:
                self.is_loading = True

        if not self._admin_data_loaded:
            try:
                checkins = await fetch_all_checkins()
                async with self:
                    self.all_checkins = checkins
                    self._admin_data_loaded = True
                logger.info(
                    "sync_call_logs_to_admin: Loaded %d demo checkins", len(checkins)
                )
            except Exception as e:
                logger.error(
                    "sync_call_logs_to_admin: Failed to load demo data - %s", e
                )

        # Small delay to allow UI to render
        await asyncio.sleep(1)

        # Get existing IDs
        async with self:
            existing_ids = {c["id"] for c in self.call_log_checkins}
            self.is_loading = False

        # Transform call logs to admin check-ins
        # Note: This would sync from PatientState.transcript_summaries
        # For now, placeholder implementation
        new_checkins = []

        if new_checkins:
            async with self:
                self.call_log_checkins = self.call_log_checkins + new_checkins
            logger.info(
                f"sync_call_logs_to_admin: Added {len(new_checkins)} new checkins"
            )
        else:
            logger.info("sync_call_logs_to_admin: No new checkins to sync")

    # =========================================================================
    # Call Logs Sync (Patient)
    # =========================================================================

    @rx.event(background=True)
    async def refresh_call_logs(self):
        """Fetch call logs and sync to checkins using VlogsAgent."""
        logger.info("refresh_call_logs: Starting")

        async with self:
            self.call_logs_syncing = True
            self.call_logs_sync_error = ""
            processed_ids = set(self._processed_call_ids)
            current_checkins = list(self.checkins)

        try:
            # Use VlogsAgent for structured processing
            agent = VlogsAgent(config=VlogsConfig(parse_with_llm=False))
            new_count, outputs, new_summaries = await agent.process_logs(
                phone_number=DEMO_PHONE_NUMBER,
                processed_ids=processed_ids,
            )
            logger.info("refresh_call_logs: Processed %d new logs", new_count)

            # Convert CallLogsOutput to checkin dicts
            existing_ids = {c["id"] for c in current_checkins}
            new_checkins = []
            for output in outputs:
                checkin_dict = output.to_checkin_dict()
                if checkin_dict["id"] not in existing_ids:
                    new_checkins.append(checkin_dict)

            # Sort by timestamp descending
            sorted_new = sorted(
                new_checkins, key=lambda x: x.get("timestamp", ""), reverse=True
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

        except Exception as e:
            logger.error("refresh_call_logs: Failed - %s", e)
            async with self:
                self.call_logs_sync_error = str(e)
                self.call_logs_syncing = False
