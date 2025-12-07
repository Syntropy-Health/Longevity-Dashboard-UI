"""Admin check-ins state management.

Refactored to use functions from functions/admins/checkins.py
"""

import reflex as rx
from typing import List
import asyncio

from ...data.state_schemas import AdminCheckIn
from ...data.demo import DEMO_ADMIN_CHECKINS
from ..patient_state import PatientState
from longevity_clinic.app.config import get_logger
from ..functions.admins import (
    transform_call_log_to_admin_checkin,
    filter_checkins,
    count_checkins_by_status,
)

logger = get_logger("longevity_clinic.admin_state")


class AdminCheckinsState(rx.State):
    """State management for admin check-ins view."""

    active_status_tab: str = "pending"
    search_query: str = ""
    all_checkins: List[AdminCheckIn] = DEMO_ADMIN_CHECKINS
    call_log_checkins: List[AdminCheckIn] = []
    selected_checkin: AdminCheckIn = {}
    show_checkin_detail_modal: bool = False

    # =========================================================================
    # Computed Variables
    # =========================================================================

    @rx.var
    def combined_checkins(self) -> List[AdminCheckIn]:
        """Combine static and call log check-ins."""
        return self.all_checkins + self.call_log_checkins

    @rx.var
    def filtered_checkins(self) -> List[AdminCheckIn]:
        """Filter check-ins by status and search query."""
        return filter_checkins(
            self.combined_checkins,
            status=self.active_status_tab,
            search_query=self.search_query,
        )

    @rx.var
    def pending_count(self) -> int:
        """Count pending check-ins."""
        return count_checkins_by_status(self.combined_checkins)["pending"]

    @rx.var
    def reviewed_count(self) -> int:
        """Count reviewed check-ins."""
        return count_checkins_by_status(self.combined_checkins)["reviewed"]

    @rx.var
    def flagged_count(self) -> int:
        """Count flagged check-ins."""
        return count_checkins_by_status(self.combined_checkins)["flagged"]

    @rx.var
    def total_count(self) -> int:
        """Total check-in count."""
        return len(self.combined_checkins)

    # =========================================================================
    # Sync Call Logs
    # =========================================================================

    @rx.event(background=True)
    async def sync_call_logs_to_admin(self):
        """Sync call logs from PatientState to admin view."""
        print("[DEBUG] sync_call_logs_to_admin ENTERED", flush=True)
        logger.info("sync_call_logs_to_admin: Starting sync (background)")

        # Small delay to allow UI to render
        await asyncio.sleep(1)

        patient_state = await self.get_state(PatientState)

        # Get existing IDs
        async with self:
            existing_ids = {c["id"] for c in self.call_log_checkins}

        # Transform call logs to admin check-ins
        new_checkins = []
        for call_id, summary in patient_state.transcript_summaries.items():
            checkin_id = f"call_{call_id}"
            if checkin_id in existing_ids:
                continue
            new_checkins.append(transform_call_log_to_admin_checkin(call_id, summary))

        if new_checkins:
            async with self:
                self.call_log_checkins = self.call_log_checkins + new_checkins
            logger.info(
                "sync_call_logs_to_admin: Added %d new checkins", len(new_checkins)
            )
        else:
            logger.info("sync_call_logs_to_admin: No new checkins to sync")

    # =========================================================================
    # UI Event Handlers
    # =========================================================================

    def set_active_status_tab(self, tab: str):
        """Set active status filter tab."""
        self.active_status_tab = tab

    def set_search_query(self, query: str):
        """Set search query."""
        self.search_query = query

    def open_checkin_detail(self, checkin: AdminCheckIn):
        """Open check-in detail modal."""
        self.selected_checkin = checkin
        self.show_checkin_detail_modal = True

    def close_checkin_detail(self):
        """Close check-in detail modal."""
        self.show_checkin_detail_modal = False
        self.selected_checkin = {}

    def set_show_checkin_detail_modal(self, value: bool):
        """Set modal visibility."""
        self.show_checkin_detail_modal = value
        if not value:
            self.selected_checkin = {}

    # =========================================================================
    # Status Updates
    # =========================================================================

    def _update_checkin(self, checkin_id: str, status: str):
        """Update check-in status in both lists."""

        def update_list(lst):
            return [
                {
                    **c,
                    "status": status,
                    "provider_reviewed": True,
                    "reviewed_by": "Dr. Admin",
                    "reviewed_at": "Just now",
                }
                if c["id"] == checkin_id
                else c
                for c in lst
            ]

        self.all_checkins = update_list(self.all_checkins)
        self.call_log_checkins = update_list(self.call_log_checkins)
        self.show_checkin_detail_modal = False

    def mark_as_reviewed(self, checkin_id: str):
        """Mark check-in as reviewed."""
        self._update_checkin(checkin_id, "reviewed")

    def flag_checkin(self, checkin_id: str):
        """Flag check-in for follow-up."""
        self._update_checkin(checkin_id, "flagged")
