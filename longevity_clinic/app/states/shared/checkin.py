"""Unified check-in state management for both admin and patient views."""

from __future__ import annotations

import asyncio
import re
import uuid
from datetime import datetime
from typing import List

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import current_config, get_logger
from longevity_clinic.app.data.model import CallTranscript
from longevity_clinic.app.data.model import CheckIn as CheckInDB
from longevity_clinic.app.data.state_schemas import (
    AdminCheckIn,
    CheckIn,
    CheckInWithTranscript,
)
from longevity_clinic.app.functions.db_utils import create_checkin_sync

from ..auth.base import AuthState
from ...functions import VlogsAgent
from ...functions.admins import filter_checkins
from .voice_transcription import VoiceTranscriptionState

logger = get_logger("longevity_clinic.checkins")


class CheckinState(rx.State):
    """Unified state for check-ins (patient and admin views)."""

    # Unified check-in data (role-based filtering via computed vars)
    checkins: List[CheckInWithTranscript] = []
    active_status_tab: str = "pending"
    search_query: str = ""

    # Patient modal state
    show_checkin_modal: bool = False
    checkin_type: str = "voice"
    checkin_text: str = ""
    selected_topics: List[str] = []

    # Voice recording state
    is_recording: bool = False
    recording_session_id: str = ""
    recording_duration: float = 0.0
    transcribed_text: str = ""
    transcription_status: str = ""

    # Admin modals state
    show_checkin_detail_modal: bool = False
    show_status_update_modal: bool = False
    show_transcript_modal: bool = False
    selected_checkin: CheckInWithTranscript = {}  # type: ignore[assignment]
    selected_status: str = ""

    # Call logs sync state
    call_logs_syncing: bool = False
    call_logs_sync_error: str = ""
    last_sync_time: str = ""
    is_processing_background: bool = False

    # Admin loading state
    is_loading: bool = False
    _admin_data_loaded: bool = False

    # Checkin saving state
    checkin_saving: bool = False

    # Pagination state
    current_page: int = 1

    # ===================================================================
    # Patient Computed Variables
    # ==================================================================

    @rx.var
    def unreviewed_checkins_count(self) -> int:
        return len([c for c in self.checkins if not c.get("provider_reviewed")])

    @rx.var
    def voice_call_checkins_count(self) -> int:
        return len([c for c in self.checkins if c.get("type") == "call"])

    @rx.var
    def checkins_this_week_count(self) -> int:
        return len(self.checkins)

    # =================================================================
    # Admin Computed Variables
    # =================================================================

    @rx.var
    def combined_checkins(self) -> List[AdminCheckIn]:
        """Return all checkins for admin view."""
        return self.checkins

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
        return len([c for c in self.combined_checkins if c["status"] == "pending"])

    @rx.var
    def reviewed_count(self) -> int:
        return len([c for c in self.combined_checkins if c["status"] == "reviewed"])

    @rx.var
    def flagged_count(self) -> int:
        return len([c for c in self.combined_checkins if c["status"] == "flagged"])

    @rx.var
    def total_count(self) -> int:
        return len(self.combined_checkins)

    @rx.var
    def selected_checkin_transcript(self) -> str:
        """Full transcript for modal display - prefers raw_transcript."""
        if raw := self.selected_checkin.get("raw_transcript", ""):
            return raw
        return self.selected_checkin.get("summary", "")

    @rx.var
    def selected_checkin_topics(self) -> List[str]:
        return self.selected_checkin.get("key_topics", [])

    @rx.var
    def selected_checkin_status(self) -> str:
        return self.selected_checkin.get("status", "")

    @rx.var
    def selected_checkin_patient_name(self) -> str:
        return self.selected_checkin.get("patient_name", "")

    @rx.var
    def selected_checkin_timestamp(self) -> str:
        return self.selected_checkin.get("timestamp", "")

    @rx.var
    def selected_checkin_type(self) -> str:
        return self.selected_checkin.get("type", "")

    @rx.var
    def selected_checkin_summary(self) -> str:
        """Falls back to raw_transcript preview if summary is empty."""
        if summary := self.selected_checkin.get("summary", ""):
            return summary
        if raw := self.selected_checkin.get("raw_transcript", ""):
            preview = raw[:200].strip()
            return f"{preview}..." if len(raw) > 200 else preview
        return ""

    @rx.var
    def selected_checkin_raw_transcript(self) -> str:
        return self.selected_checkin.get("raw_transcript", "")

    @rx.var
    def selected_checkin_id(self) -> str:
        return self.selected_checkin.get("id", "")

    # -------------------------------------------------------------------------
    # Patient Check-in Type and Text
    # -------------------------------------------------------------------------

    @rx.event
    async def set_checkin_type(self, checkin_type: str):
        self.checkin_type = checkin_type
        self._reset_checkin_state()
        await self._reset_voice_state()

    def set_checkin_text(self, text: str):
        self.checkin_text = text

    def toggle_topic(self, topic: str):
        if topic in self.selected_topics:
            self.selected_topics = [t for t in self.selected_topics if t != topic]
        else:
            self.selected_topics = [*self.selected_topics, topic]

    def is_topic_selected(self, topic: str) -> bool:
        return topic in self.selected_topics

    # -------------------------------------------------------------------------
    # Voice Recording
    # -------------------------------------------------------------------------

    @rx.event
    async def start_recording(self):
        self.is_recording = True
        self.transcription_status = "recording"
        self.recording_duration = 0.0
        self.recording_session_id = f"rec_{uuid.uuid4().hex[:8]}"

    @rx.event
    async def stop_recording(self):
        self.is_recording = False
        self.transcription_status = "done"

    @rx.event
    async def toggle_recording(self):
        if not self.is_recording:
            yield CheckinState.start_recording
            yield CheckinState.increment_recording_duration
        else:
            yield CheckinState.stop_recording

    @rx.event(background=True)
    async def increment_recording_duration(self):
        async with self:
            if not self.is_recording:
                return
        while True:
            await asyncio.sleep(1)
            async with self:
                if not self.is_recording:
                    return
                self.recording_duration += 1.0

    # -------------------------------------------------------------------------
    # Patient Check-in Modal Operations
    # -------------------------------------------------------------------------

    @rx.event
    async def open_checkin_modal(self):
        logger.debug("Opening checkin modal")
        self.show_checkin_modal = True
        self.checkin_type = "voice"
        self._reset_checkin_state()
        await self._reset_voice_state()

    @rx.event
    async def close_checkin_modal(self):
        self.show_checkin_modal = False
        self._reset_checkin_state()
        await self._reset_voice_state()

    def set_show_checkin_modal(self, value: bool):
        self.show_checkin_modal = value

    # -------------------------------------------------------------------------
    # Save Patient Check-in
    # -------------------------------------------------------------------------
    async def _create_checkin_from_summary(
        self, checkin_summary, raw_transcript: str = "", persist_to_db: bool = True
    ) -> CheckInWithTranscript:
        """Create CheckInWithTranscript from parsed summary and optionally persist to DB.
        
        Args:
            checkin_summary: Parsed CheckinSummary from VlogsAgent
            raw_transcript: Original transcript text
            persist_to_db: If True, save to database (default: True)
            
        Returns:
            CheckInWithTranscript dict for state
        """
        checkin_id = checkin_summary.id
        checkin_data: CheckInWithTranscript = {
            "id": checkin_id,
            "type": checkin_summary.type,
            "summary": checkin_summary.summary,
            "raw_transcript": raw_transcript,
            "timestamp": checkin_summary.timestamp,
            "sentiment": checkin_summary.sentiment,
            "key_topics": checkin_summary.key_topics,
            "provider_reviewed": checkin_summary.provider_reviewed,
            "patient_name": checkin_summary.patient_name,
            "status": "pending",
        }
        
        # Persist to database if requested
        if persist_to_db:
            auth_state = await self.get_state(AuthState)
            user_id = auth_state.user_id if auth_state.user_id else None
            
            # Serialize health_topics to JSON string for DB
            import json
            health_topics_json = json.dumps(checkin_summary.key_topics) if checkin_summary.key_topics else None
            
            db_result = create_checkin_sync(
                checkin_id=checkin_id,
                patient_name=checkin_summary.patient_name,
                summary=checkin_summary.summary,
                checkin_type=checkin_summary.type,
                user_id=user_id,
                raw_content=raw_transcript or None,
                health_topics=health_topics_json,
            )
            if db_result:
                logger.info("Persisted checkin %s to database", checkin_id)
            else:
                logger.warning("Failed to persist checkin %s to database", checkin_id)
        
        return checkin_data

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

        checkin_summary = await VlogsAgent.parse_user_checkin(
            content, self.checkin_type
        )
        new_checkin = await self._create_checkin_from_summary(
            checkin_summary, raw_transcript=content
        )
        self.checkins = [new_checkin, *self.checkins]
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

        checkin_summary = await VlogsAgent.parse_user_checkin(
            content, self.checkin_type
        )
        new_checkin = await self._create_checkin_from_summary(
            checkin_summary, raw_transcript=content
        )
        self.checkins = [new_checkin, *self.checkins]
        self.show_checkin_modal = False
        self._reset_checkin_state()
        await self._reset_voice_state()

    def _reset_checkin_state(self):
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.checkin_text = ""
        self.selected_topics = []
        self.transcription_status = "idle"

    async def _reset_voice_state(self):
        """Reset voice transcription state."""
        voice_state = await self.get_state(VoiceTranscriptionState)
        voice_state.transcript = ""
        voice_state.has_error = False
        voice_state.error_message = ""

    # -------------------------------------------------------------------------
    # Admin Check-in Management
    # -------------------------------------------------------------------------

    def set_active_status_tab(self, tab: str):
        self.active_status_tab = tab

    def set_search_query(self, query: str):
        self.search_query = query

    def open_checkin_detail(self, checkin: CheckInWithTranscript):
        self.selected_checkin = checkin
        self.show_checkin_detail_modal = True

    def close_checkin_detail(self):
        self.show_checkin_detail_modal = False
        self.selected_checkin = {}  # type: ignore[assignment]

    def set_show_checkin_detail_modal(self, value: bool):
        self.show_checkin_detail_modal = value
        if not value:
            self.selected_checkin = {}  # type: ignore[assignment]

    # -------------------------------------------------------------------------
    # Status Update Modal
    # -------------------------------------------------------------------------

    def open_status_update_modal(self, checkin: CheckInWithTranscript):
        self.selected_checkin = checkin
        self.selected_status = checkin.get("status", "pending")
        self.show_status_update_modal = True

    def close_status_update_modal(self):
        self.show_status_update_modal = False
        self.selected_checkin = {}  # type: ignore[assignment]
        self.selected_status = ""

    def set_selected_status(self, status: str):
        self.selected_status = status

    @rx.event
    async def update_checkin_status(self):
        if not self.selected_checkin or not self.selected_status:
            return
        if checkin_id := self.selected_checkin.get("id"):
            self._update_checkin(checkin_id, self.selected_status)
        self.show_status_update_modal = False
        self.selected_checkin = {}  # type: ignore[assignment]
        self.selected_status = ""

    def _update_checkin(self, checkin_id: str, status: str):
        """Update checkin status in both lists."""

        def update(lst: list) -> list:
            return [
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

        self.checkins = update(self.checkins)

    def mark_as_reviewed(self, checkin_id: str):
        self._update_checkin(checkin_id, "reviewed")

    def flag_checkin(self, checkin_id: str):
        self._update_checkin(checkin_id, "flagged")

    # -------------------------------------------------------------------------
    # Transcript Modal
    # -------------------------------------------------------------------------

    def open_transcript_modal(self, checkin: CheckInWithTranscript):
        self.selected_checkin = checkin
        self.show_transcript_modal = True

    def close_transcript_modal(self):
        self.show_transcript_modal = False

    def set_show_transcript_modal(self, value: bool):
        self.show_transcript_modal = value

    # -------------------------------------------------------------------------
    # Call Logs Sync (Admin)
    # -------------------------------------------------------------------------

    @rx.event(background=True)
    async def load_admin_checkins(self):
        """Load admin check-ins from database (all patients)."""
        async with self:
            if self._admin_data_loaded:
                return
            self.is_loading = True

        logger.debug("Loading admin checkins from database")

        try:
            checkins_from_db = await self._load_all_checkins_from_db()
            async with self:
                self.checkins = checkins_from_db
                self.is_loading = False
                self._admin_data_loaded = True
            logger.debug("Loaded %d admin checkins from DB", len(checkins_from_db))
        except Exception as e:
            logger.error("load_admin_checkins failed: %s", e)
            async with self:
                self.is_loading = False

    async def _load_all_checkins_from_db(self) -> List[AdminCheckIn]:
        """Load all check-ins from database for admin view (all patients)."""

        def _query_all_checkins() -> List[AdminCheckIn]:
            with rx.session() as session:
                result = session.exec(
                    select(CheckInDB, CallTranscript.raw_transcript)
                    .outerjoin(
                        CallTranscript,
                        CheckInDB.call_log_id == CallTranscript.call_log_id,
                    )
                    .order_by(CheckInDB.timestamp.desc())
                    .limit(200)
                )
                return [
                    {
                        "id": c.checkin_id,
                        "type": c.checkin_type,
                        "summary": c.summary,
                        "raw_transcript": raw_transcript or "",
                        "timestamp": c.timestamp.isoformat() if c.timestamp else "",
                        "sentiment": "neutral",
                        "key_topics": [],
                        "provider_reviewed": c.provider_reviewed,
                        "patient_name": c.patient_name,
                        "status": c.status,
                    }
                    for c, raw_transcript in result.all()
                ]

        try:
            return await asyncio.to_thread(_query_all_checkins)
        except Exception as e:
            logger.error("_load_all_checkins_from_db failed: %s", e)
            return []

    # -------------------------------------------------------------------------
    # Call Logs Sync (Patient) - CDC Pattern with Database
    # -------------------------------------------------------------------------

    @rx.event(background=True)
    async def refresh_call_logs(self):
        """CDC pipeline: fetch → sync raw → load from DB.

        If reprocess_call_logs_everytime is True, resets processed_to_metrics
        to force reprocessing of all call logs.
        """
        async with self:
            self.call_logs_syncing = True
            self.call_logs_sync_error = ""
            auth_state = await self.get_state(AuthState)
            user_phone = auth_state.user_phone if auth_state.user else ""
            user_name = auth_state.user_full_name if auth_state.user else "Unknown"

        logger.debug(
            "refresh_call_logs: user=%s, phone=%s", user_name, user_phone or "(none)"
        )

        if not user_phone:
            async with self:
                self.call_logs_sync_error = (
                    f"No phone number configured for {user_name}"
                )
                self.call_logs_syncing = False
            return

        try:
            agent = VlogsAgent.from_config()
            phone_clean = re.sub(r"[()\-\s]", "", user_phone)

            # If reprocess flag is set, reset all processed_to_metrics to False
            if current_config.reprocess_call_logs_everytime:
                from ...functions.vlogs.db import reset_all_processed_to_metrics_sync

                reset_count = await asyncio.to_thread(
                    reset_all_processed_to_metrics_sync
                )
                logger.info("Reset %d call logs for reprocessing", reset_count)

            new_raw_count = await agent.fetch_and_sync_raw(phone_number=phone_clean)
            logger.debug("Synced %d raw call logs", new_raw_count)

            # Load checkins based on role
            async with self:
                auth_state = await self.get_state(AuthState)
                is_admin = auth_state.is_admin
            
            if is_admin:
                checkins_from_db = await self._load_all_checkins_from_db()
            else:
                checkins_from_db = await self._load_checkins_from_db()

            async with self:
                if checkins_from_db:
                    self.checkins = checkins_from_db
                self.last_sync_time = datetime.now().strftime("%I:%M %p")
                self.call_logs_syncing = False
            logger.debug("Loaded %d checkins from DB", len(checkins_from_db))

        except Exception as e:
            logger.error("refresh_call_logs failed: %s", e)
            async with self:
                self.call_logs_sync_error = str(e)
                self.call_logs_syncing = False

    async def _load_checkins_from_db(self) -> List[CheckInWithTranscript]:
        """Load check-ins from database with raw_transcript join."""

        def _query_checkins() -> List[CheckInWithTranscript]:
            with rx.session() as session:
                result = session.exec(
                    select(CheckInDB, CallTranscript.raw_transcript)
                    .outerjoin(
                        CallTranscript,
                        CheckInDB.call_log_id == CallTranscript.call_log_id,
                    )
                    .where(CheckInDB.checkin_type == "call")
                    .order_by(CheckInDB.timestamp.desc())
                    .limit(100)
                )
                return [
                    {
                        "id": c.checkin_id,
                        "type": c.checkin_type,
                        "summary": c.summary,
                        "raw_transcript": raw_transcript or "",
                        "timestamp": c.timestamp.isoformat() if c.timestamp else "",
                        "sentiment": "neutral",
                        "key_topics": [],
                        "provider_reviewed": c.provider_reviewed,
                        "patient_name": c.patient_name,
                        "status": c.status,
                    }
                    for c, raw_transcript in result.all()
                ]

        try:
            return await asyncio.to_thread(_query_checkins)
        except Exception as e:
            logger.error("_load_checkins_from_db failed: %s", e)
            return []

    @rx.event(background=True)
    async def start_background_processing(self):
        """Start periodic background processing (on_mount)."""
        async with self:
            if self.is_processing_background:
                return
            self.is_processing_background = True

        logger.debug("Background processing loop started")

        while True:
            async with self:
                if not self.is_processing_background:
                    break

            try:
                agent = VlogsAgent.from_config()
                count = await agent.process_unprocessed_logs()

                if count > 0:
                    logger.debug("Background processed %d logs", count)
                    # Reload based on current user role
                    async with self:
                        auth_state = await self.get_state(AuthState)
                        is_admin = auth_state.is_admin
                    
                    if is_admin:
                        checkins_from_db = await self._load_all_checkins_from_db()
                    else:
                        checkins_from_db = await self._load_checkins_from_db()
                    async with self:
                        if checkins_from_db:
                            self.checkins = checkins_from_db
            except Exception as e:
                logger.error("Background processing error: %s", e)

            await asyncio.sleep(30)

        logger.debug("Background processing loop stopped")

    @rx.event
    def stop_background_processing(self):
        self.is_processing_background = False
