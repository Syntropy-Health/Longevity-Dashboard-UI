"""Unified check-in state management for both admin and patient views."""

from __future__ import annotations

import asyncio
import json
import re
from datetime import datetime

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import current_config, get_logger, process_config
from longevity_clinic.app.data.schemas.db import CallTranscript, CheckIn as CheckInDB
from longevity_clinic.app.data.schemas.llm import MetricLogsOutput
from longevity_clinic.app.data.schemas.state import (
    AdminCheckIn,
    CheckInWithTranscript,
)
from longevity_clinic.app.functions.db_utils import (
    create_checkin_sync,
    delete_checkin_sync,
    save_health_entries_sync,
    update_checkin_sync,
)
from longevity_clinic.app.states.shared.dashboard import HealthDashboardState

from ...functions import VlogsAgent
from ...functions.admins import filter_checkins
from ...functions.vlogs.db import reset_all_processed_to_metrics_sync
from ..auth.base import AuthState
from .voice_transcription import VoiceTranscriptionState

logger = get_logger("longevity_clinic.checkins")


class CheckinState(rx.State):
    """Unified state for check-ins (patient and admin views).

    Data Flow - Patient Check-ins (voice/text):
    ============================================
    1. save_checkin_and_log_health() → VlogsAgent.parse_checkin_with_health_data()
    2. LLM extracts MetricLogsOutput (checkin summary + medications/food/symptoms)
    3. create_checkin_sync() → CheckIn table (returns db_id for FK linking)
    4. save_health_entries_sync() → MedicationEntry, FoodLogEntry, SymptomEntry tables
       (all entries linked to CheckIn via checkin_id FK and user_id for querying)
    5. Reload checkins from DB to update UI

    Data Flow - Call Log CDC Pipeline:
    ===================================
    1. start_calls_to_checkin_sync_loop() polls in background
    2. VlogsAgent.process_unprocessed_logs() finds unprocessed CallLog records
    3. LLM extracts MetricLogsOutput from transcript
    4. update_call_log_metrics() → CheckIn + health entry tables
    5. Marks CallLog.processed_to_metrics=True
    6. Reload checkins from DB to update UI

    Dashboard Integration:
    ======================
    HealthDashboardState.load_health_data_from_db() is triggered via page on_load
    in longevity_clinic.py to refresh dashboard tabs. Data is fetched from:
    - get_medications_sync(user_id) → MedicationEntry table
    - get_food_entries_sync(user_id) → FoodLogEntry table
    - get_symptoms_sync(user_id) → SymptomEntry table

    Database Relationships:
    =======================
    CheckIn is the central table linking all health data:
    - MedicationEntry.checkin_id → CheckIn.id
    - FoodLogEntry.checkin_id → CheckIn.id
    - SymptomEntry.checkin_id → CheckIn.id
    All health entries also have user_id for direct dashboard queries.
    """

    # Unified check-in data (role-based filtering via computed vars)
    checkins: list[CheckInWithTranscript] = []
    active_status_tab: str = "pending"
    search_query: str = ""

    # Patient modal state
    show_checkin_modal: bool = False
    checkin_type: str = "voice"
    checkin_text: str = ""
    selected_topics: list[str] = []

    # Admin modals state
    show_checkin_detail_modal: bool = False
    selected_checkin: dict = {}  # CheckInWithTranscript dict
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

    # Edit/Delete modal state
    show_edit_modal: bool = False
    edit_checkin_id: str = ""
    edit_checkin_summary: str = ""
    show_delete_confirm: bool = False
    delete_checkin_id: str = ""

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

    # =================================================================
    # Admin Computed Variables
    # =================================================================

    @rx.var
    def combined_checkins(self) -> list[AdminCheckIn]:
        """Return all checkins for admin view."""
        return self.checkins

    @rx.var
    def filtered_checkins(self) -> list[AdminCheckIn]:
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
    def selected_checkin_topics(self) -> list[str]:
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

    # =========================================================================
    # Pagination Computed Variables
    # =========================================================================

    @rx.var
    def per_page(self) -> int:
        """Items per page from config."""
        return current_config.checkins_per_page

    @rx.var
    def total_pages(self) -> int:
        """Total number of pages based on filtered checkins."""
        total = len(self.filtered_checkins)
        per_page = current_config.checkins_per_page
        return max(1, (total + per_page - 1) // per_page)

    @rx.var
    def paginated_checkins(self) -> list[AdminCheckIn]:
        """Return current page of filtered checkins."""
        per_page = current_config.checkins_per_page
        start = (self.current_page - 1) * per_page
        end = start + per_page
        return self.filtered_checkins[start:end]

    @rx.var
    def has_previous_page(self) -> bool:
        """Whether there's a previous page."""
        return self.current_page > 1

    @rx.var
    def has_next_page(self) -> bool:
        """Whether there's a next page."""
        return self.current_page < self.total_pages

    @rx.var
    def page_info(self) -> str:
        """Page info string (e.g., 'Page 1 of 5')."""
        return f"Page {self.current_page} of {self.total_pages}"

    @rx.var
    def showing_info(self) -> str:
        """Showing info string (e.g., 'Showing 1-10 of 25')."""
        per_page = current_config.checkins_per_page
        total = len(self.filtered_checkins)
        start = (self.current_page - 1) * per_page + 1
        end = min(self.current_page * per_page, total)
        if total == 0:
            return "No check-ins"
        return f"Showing {start}-{end} of {total}"

    # -------------------------------------------------------------------------
    # Pagination Event Handlers
    # -------------------------------------------------------------------------

    def next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1

    def previous_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1

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

    def set_show_checkin_modal(self, value: bool):
        self.show_checkin_modal = value

    # -------------------------------------------------------------------------
    # Save Patient Check-in
    # -------------------------------------------------------------------------

    @rx.event(background=True)
    async def save_checkin_and_log_health(self):
        """Save a new check-in via voice/text (background process).

        Data Flow:
        1. Parse content with LLM → MetricLogsOutput (checkin + health entries)
        2. Create CheckIn record → checkins table
        3. Persist health entries → medication_entries, food_log_entries, symptom_entries
        4. Reload checkins from DB to update UI

        Database Tables Updated:
        - checkins: CheckIn record with summary, sentiment, topics
        - medication_entries: Medications mentioned in check-in
        - food_log_entries: Food/nutrition entries
        - symptom_entries: Symptoms reported

        Dashboard Sync:
        After save, HealthDashboardState.load_health_data_from_db() will
        fetch updated entries from these tables for display.
        """
        async with self:
            voice_state = await self.get_state(VoiceTranscriptionState)
            content = (
                voice_state.transcript
                if self.checkin_type == "voice"
                else self.checkin_text.strip()
            )
            if not content.strip():
                logger.warning("No content to save for checkin")
                return
            self.checkin_saving = True
            checkin_type = self.checkin_type

        logger.info(
            "Saving new checkin type=%s, content_len=%d", checkin_type, len(content)
        )

        try:
            # Step 1: Parse content with LLM - get full health data extraction
            parse_result: MetricLogsOutput = (
                await VlogsAgent.parse_checkin_with_health_data(
                    content=content, checkin_type=checkin_type
                )
            )
            checkin_summary = parse_result.checkin

            logger.debug(
                "LLM parsed: summary_len=%d, meds=%d, foods=%d, symptoms=%d, content=%s",
                len(checkin_summary.summary),
                len(parse_result.medications_entries),
                len(parse_result.food_entries),
                len(parse_result.symptom_entries),
                content[:100],
            )

            # Get user info for DB persistence
            async with self:
                auth_state = await self.get_state(AuthState)
                user_id = auth_state.user_id if auth_state.user_id else None
                patient_name = auth_state.user_full_name or "UNKNOWN"

            # Step 2: Persist CheckIn to database
            health_topics_json = (
                json.dumps(checkin_summary.key_topics)
                if checkin_summary.key_topics
                else None
            )

            # Step 2: Persist CheckIn to database (returns db_id to avoid extra query)
            db_result = await asyncio.to_thread(
                create_checkin_sync,
                checkin_id=checkin_summary.id,
                patient_name=patient_name,
                summary=checkin_summary.summary,
                checkin_type=checkin_summary.type,
                user_id=user_id,
                raw_content=content,
                health_topics=health_topics_json,
            )

            if db_result:
                logger.info("Created CheckIn %s in database", checkin_summary.id)

                # Step 3: Use db_id from create result (no extra query needed)
                checkin_db_id = db_result.get("db_id")

                if checkin_db_id:
                    # Determine source based on checkin type
                    source = "voice" if checkin_type == "voice" else "manual"
                    # Persist health entries linked to this checkin
                    health_counts = await asyncio.to_thread(
                        save_health_entries_sync,
                        checkin_db_id,
                        user_id,
                        parse_result,
                        source,
                    )

                    logger.info(
                        "Saved health entries for %s: %d meds, %d foods, %d symptoms",
                        checkin_summary.id,
                        health_counts["medications"],
                        health_counts["foods"],
                        health_counts["symptoms"],
                    )
                else:
                    logger.warning(
                        "db_id not returned for %s - health entries not saved",
                        checkin_summary.id,
                    )
            else:
                logger.warning("Failed to save checkin to database")

            # Step 4: Reload checkins from DB to ensure consistency
            checkins_from_db = await self._load_checkins_from_db()

            async with self:
                self.checkins = checkins_from_db
                self._reset_checkin_state()
                # Reset voice state
                voice_state = await self.get_state(VoiceTranscriptionState)
                voice_state.transcript = ""
                voice_state.has_error = False
                voice_state.error_message = ""
                voice_state.processing = False

        except Exception as e:
            logger.error("save_checkin_and_log_health failed: %s", e)
        finally:
            # Always close modal and reset saving state when done
            async with self:
                self.checkin_saving = False
                self.show_checkin_modal = False

    def _reset_checkin_state(self):
        """Reset patient checkin form state."""
        self.checkin_text = ""
        self.selected_topics = []

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
        self.current_page = 1  # Reset pagination on filter change

    def set_search_query(self, query: str):
        self.search_query = query
        self.current_page = 1  # Reset pagination on search change

    def open_checkin_detail(self, checkin: CheckInWithTranscript):
        self.selected_checkin = checkin
        self.show_checkin_detail_modal = True

    def close_checkin_detail(self):
        """Close the check-in detail modal and clear selection."""
        self.show_checkin_detail_modal = False
        self.selected_checkin = {}

    def set_show_checkin_detail_modal(self, value: bool):
        """Set modal visibility and clear selection when closing."""
        self.show_checkin_detail_modal = value
        if not value:
            self.selected_checkin = {}

    # -------------------------------------------------------------------------
    # Status Update
    # -------------------------------------------------------------------------

    @rx.event
    async def update_checkin_status(self):
        if not self.selected_checkin or not self.selected_status:
            return
        if checkin_id := self.selected_checkin.get("id"):
            self._update_checkin(checkin_id, self.selected_status)
        self.selected_checkin = {}
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
    # Edit/Delete Handlers
    # -------------------------------------------------------------------------

    def open_edit_modal(self, checkin_id: str):
        """Open edit modal for a check-in (closes detail modal if open)."""
        # Close detail modal first to prevent conflicts
        self.show_checkin_detail_modal = False
        self.selected_checkin = {}

        checkin = next((c for c in self.checkins if c["id"] == checkin_id), None)
        if checkin:
            self.edit_checkin_id = checkin_id
            self.edit_checkin_summary = checkin.get("summary", "")
            self.show_edit_modal = True

    def close_edit_modal(self):
        """Close edit modal."""
        self.show_edit_modal = False
        self.edit_checkin_id = ""
        self.edit_checkin_summary = ""

    def set_edit_checkin_summary(self, value: str):
        """Update edit summary text."""
        self.edit_checkin_summary = value

    @rx.event(background=True)
    async def save_edit_checkin(self):
        """Save edited check-in to database."""
        async with self:
            checkin_id = self.edit_checkin_id
            new_summary = self.edit_checkin_summary
            if not checkin_id:
                return

        # Update in database
        success = await asyncio.to_thread(
            update_checkin_sync, checkin_id, summary=new_summary
        )

        if success:
            # Update local state
            async with self:
                self.checkins = [
                    {**c, "summary": new_summary} if c["id"] == checkin_id else c
                    for c in self.checkins
                ]
                self.show_edit_modal = False
                self.edit_checkin_id = ""
                self.edit_checkin_summary = ""
            logger.info("Updated checkin %s", checkin_id)
        else:
            logger.error("Failed to update checkin %s", checkin_id)

    def open_delete_confirm(self, checkin_id: str):
        """Open delete confirmation dialog (closes detail modal if open)."""
        # Close detail modal first to prevent conflicts
        self.show_checkin_detail_modal = False
        self.selected_checkin = {}

        self.delete_checkin_id = checkin_id
        self.show_delete_confirm = True

    def close_delete_confirm(self):
        """Close delete confirmation dialog."""
        self.show_delete_confirm = False
        self.delete_checkin_id = ""

    @rx.event(background=True)
    async def confirm_delete_checkin(self):
        """Delete check-in from database."""
        async with self:
            checkin_id = self.delete_checkin_id
            if not checkin_id:
                return

        # Delete from database
        success = await asyncio.to_thread(delete_checkin_sync, checkin_id)

        if success:
            # Remove from local state
            async with self:
                self.checkins = [c for c in self.checkins if c["id"] != checkin_id]
                self.show_delete_confirm = False
                self.delete_checkin_id = ""
            logger.info("Deleted checkin %s", checkin_id)
        else:
            logger.error("Failed to delete checkin %s", checkin_id)
            async with self:
                self.show_delete_confirm = False
                self.delete_checkin_id = ""

    # -------------------------------------------------------------------------
    # Transcript Modal (DEPRECATED - use open_checkin_detail instead)
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

    async def _load_all_checkins_from_db(self) -> list[AdminCheckIn]:
        """Load all check-ins from database for admin view (all patients)."""

        def _query_all_checkins() -> list[AdminCheckIn]:
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
        """CDC pipeline: fetch → sync raw → process LLM → load from DB.

        Full pipeline:
        1. Fetch and sync raw call logs from API
        2. Process unprocessed logs with LLM (creates CheckIn + health entries)
        3. Reload checkins from DB
        """
        async with self:
            self.call_logs_syncing = True
            self.call_logs_sync_error = ""
            auth_state = await self.get_state(AuthState)
            user_phone = auth_state.user_phone if auth_state.user else ""
            user_name = auth_state.user_full_name if auth_state.user else "UNKNOWN"

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

            # Reset if reprocess flag set
            if process_config.reprocess_all:
                reset_count = await asyncio.to_thread(
                    reset_all_processed_to_metrics_sync
                )
                logger.info("Reset %d call logs for reprocessing", reset_count)

            # Step 1-2: Fetch and sync raw call logs
            new_raw_count = await agent.fetch_and_sync_raw(phone_number=phone_clean)
            logger.debug("Synced %d raw call logs", new_raw_count)

            # Step 3-4: Process unprocessed logs with LLM → creates CheckIn + health entries
            processed_count = await agent.process_unprocessed_logs()
            if processed_count > 0:
                logger.info("Processed %d call logs to health metrics", processed_count)

            # Reload checkins
            async with self:
                auth_state = await self.get_state(AuthState)
                is_admin = auth_state.is_admin

            checkins_from_db = await (
                self._load_all_checkins_from_db()
                if is_admin
                else self._load_checkins_from_db()
            )

            async with self:
                if checkins_from_db:
                    self.checkins = checkins_from_db
                self.last_sync_time = datetime.now().strftime("%I:%M %p")
                self.call_logs_syncing = False

            logger.debug("Loaded %d checkins from DB", len(checkins_from_db))

            # Trigger dashboard refresh so user sees new health entries
            if processed_count > 0:
                yield HealthDashboardState.load_health_data_from_db

        except Exception as e:
            logger.error("refresh_call_logs failed: %s", e)
            async with self:
                self.call_logs_sync_error = str(e)
                self.call_logs_syncing = False

    @rx.event(background=True)
    async def start_periodic_call_logs_refresh(self):
        """Start periodic refresh loop for call logs (uses process_config.refresh_interval)."""
        async with self:
            if self.is_processing_background:
                return
            self.is_processing_background = True

        logger.debug(
            "Periodic refresh started (interval=%ds)", process_config.refresh_interval
        )

        while True:
            async with self:
                if not self.is_processing_background:
                    break

            # Trigger full refresh pipeline
            yield CheckinState.refresh_call_logs
            await asyncio.sleep(process_config.refresh_interval)

        logger.debug("Periodic refresh stopped")

    async def _load_checkins_from_db(self) -> list[CheckInWithTranscript]:
        """Load all check-ins from database for patient view (all types)."""

        def _query_checkins() -> list[CheckInWithTranscript]:
            with rx.session() as session:
                result = session.exec(
                    select(CheckInDB, CallTranscript.raw_transcript)
                    .outerjoin(
                        CallTranscript,
                        CheckInDB.call_log_id == CallTranscript.call_log_id,
                    )
                    .order_by(CheckInDB.timestamp.desc())
                    .limit(100)
                )
                checkins = []
                for c, raw_transcript in result.all():
                    # For non-call types, use raw_content if no transcript
                    transcript_text = raw_transcript or c.raw_content or ""
                    checkins.append(
                        {
                            "id": c.checkin_id,
                            "type": c.checkin_type,
                            "summary": c.summary,
                            "raw_transcript": transcript_text,
                            "timestamp": c.timestamp.isoformat() if c.timestamp else "",
                            "sentiment": "neutral",
                            "key_topics": [],
                            "provider_reviewed": c.provider_reviewed,
                            "patient_name": c.patient_name,
                            "status": c.status,
                        }
                    )
                return checkins

        try:
            return await asyncio.to_thread(_query_checkins)
        except Exception as e:
            logger.error("_load_checkins_from_db failed: %s", e)
            return []

    # -------------------------------------------------------------------------
    # Background Processing Loop (on_mount/on_unmount lifecycle)
    # -------------------------------------------------------------------------

    @rx.event(background=True)
    async def start_calls_to_checkin_sync_loop(self):
        """Background CDC loop: process unprocessed call logs periodically.

        Pipeline per cycle:
        1. Process unprocessed call logs (LLM → CheckIn + health entries)
        2. Reload checkins from DB to update UI
        """
        async with self:
            if self.is_processing_background:
                return
            self.is_processing_background = True

        logger.debug(
            "Checkin sync loop started (poll_interval=%ds)",
            process_config.poll_interval,
        )

        # Initial load
        try:
            async with self:
                auth_state = await self.get_state(AuthState)
                is_admin = auth_state.is_admin

            checkins_from_db = await (
                self._load_all_checkins_from_db()
                if is_admin
                else self._load_checkins_from_db()
            )
            async with self:
                self.checkins = checkins_from_db
            logger.debug("Initial load: %d checkins", len(checkins_from_db))
        except Exception as e:
            logger.error("Initial checkin load failed: %s", e)

        # Polling loop
        while True:
            async with self:
                if not self.is_processing_background:
                    break

            try:
                agent = VlogsAgent.from_config()
                processed_count = await agent.process_unprocessed_logs()

                if processed_count > 0:
                    logger.info("Processed %d call logs", processed_count)
                    async with self:
                        auth_state = await self.get_state(AuthState)
                        is_admin = auth_state.is_admin

                    checkins_from_db = await (
                        self._load_all_checkins_from_db()
                        if is_admin
                        else self._load_checkins_from_db()
                    )
                    async with self:
                        if checkins_from_db:
                            self.checkins = checkins_from_db
            except Exception as e:
                logger.error("Background processing error: %s", e)

            await asyncio.sleep(process_config.poll_interval)

        logger.debug("Checkin sync loop stopped")

    @rx.event
    def stop_checkin_sync_loop(self):
        """Stop the background CDC processing loop."""
        self.is_processing_background = False

    # Legacy aliases
    start_background_processing = start_calls_to_checkin_sync_loop
    stop_background_processing = stop_checkin_sync_loop
