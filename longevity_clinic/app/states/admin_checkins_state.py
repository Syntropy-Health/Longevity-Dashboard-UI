"""Admin check-ins state management."""

import reflex as rx
from typing import List
import asyncio

from ..data.state_schemas import AdminCheckIn
from ..data.demo import DEMO_ADMIN_CHECKINS

from .patient_state import PatientState
from ..config import get_logger

logger = get_logger("longevity_clinic.admin_state")

# Health keywords for topic extraction
_HEALTH_KEYWORDS = [
    "fatigue",
    "tired",
    "energy",
    "sleep",
    "pain",
    "joint",
    "headache",
    "anxiety",
    "stress",
    "blood pressure",
    "heart",
    "blood sugar",
    "diet",
    "medication",
    "exercise",
    "breathing",
]

# Phone to patient name mapping
_PHONE_TO_PATIENT = {
    "+12126804645": "Demo Patient (Sarah Chen)",
    "(555) 123-4567": "John Doe",
    "(555) 987-6543": "Jane Smith",
    "(555) 456-7890": "Robert Johnson",
    "(555) 222-3333": "Emily Davis",
    "(555) 444-5555": "Michael Wilson",
}


class AdminCheckinsState(rx.State):
    """State management for admin check-ins view."""

    active_status_tab: str = "pending"
    search_query: str = ""
    all_checkins: List[AdminCheckIn] = DEMO_ADMIN_CHECKINS
    call_log_checkins: List[AdminCheckIn] = []
    selected_checkin: AdminCheckIn = {}
    show_checkin_detail_modal: bool = False

    @rx.var
    def combined_checkins(self) -> List[AdminCheckIn]:
        return self.all_checkins + self.call_log_checkins

    @rx.var
    def filtered_checkins(self) -> List[AdminCheckIn]:
        results = self.combined_checkins
        if self.active_status_tab != "all":
            results = [c for c in results if c["status"] == self.active_status_tab]
        if self.search_query.strip():
            q = self.search_query.lower()
            results = [
                c
                for c in results
                if q in c["patient_name"].lower()
                or q in c["summary"].lower()
                or any(q in t.lower() for t in c["key_topics"])
            ]
        return sorted(results, key=lambda x: x["submitted_at"], reverse=True)

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

    @rx.event(background=True)
    async def sync_call_logs_to_admin(self):
        """Sync call logs from PatientState to admin view."""
        print("[DEBUG] sync_call_logs_to_admin ENTERED", flush=True)
        from ..config import get_logger

        logger = get_logger("longevity_clinic.admin_state")
        logger.info("sync_call_logs_to_admin: Starting sync (background)")

        # Small delay to allow UI to render and other tasks to start
        await asyncio.sleep(1)

        patient_state = await self.get_state(PatientState)

        # Access state vars inside async with self if needed, but reading is usually fine?
        # Better to be safe with background tasks reading state
        async with self:
            existing_ids = {c["id"] for c in self.call_log_checkins}

        new_checkins = []
        # patient_state is from get_state, so it's a snapshot or proxy.
        # Iterating it should be safe if we don't hold lock on it?
        # But patient_state might change.
        # We should probably lock patient_state if we want consistent read?
        # But get_state usually gives us the state.

        for call_id, summary in patient_state.transcript_summaries.items():
            if f"call_{call_id}" in existing_ids:
                continue
            phone = summary.get("patient_phone", "")
            normalized = (
                phone.replace(" ", "")
                .replace("-", "")
                .replace("(", "")
                .replace(")", "")
            )
            name = next(
                (
                    n
                    for k, n in _PHONE_TO_PATIENT.items()
                    if k.replace(" ", "")
                    .replace("-", "")
                    .replace("(", "")
                    .replace(")", "")
                    == normalized
                ),
                f"Patient ({phone})",
            )
            ai_summary = summary.get("ai_summary", "") or summary.get("summary", "")
            topics = [kw for kw in _HEALTH_KEYWORDS if kw in ai_summary.lower()][
                :5
            ] or ["voice call"]
            new_checkins.append(
                {
                    "id": f"call_{call_id}",
                    "patient_id": "demo",
                    "patient_name": name,
                    "type": "call",
                    "summary": ai_summary,
                    "timestamp": summary.get("timestamp", ""),
                    "submitted_at": summary.get("call_date", ""),
                    "sentiment": "neutral",
                    "key_topics": topics,
                    "status": "pending",
                    "provider_reviewed": False,
                    "reviewed_by": "",
                    "reviewed_at": "",
                }
            )

        if new_checkins:
            async with self:
                self.call_log_checkins = self.call_log_checkins + new_checkins
            logger.info(
                f"sync_call_logs_to_admin: Added {len(new_checkins)} new checkins"
            )
        else:
            logger.info("sync_call_logs_to_admin: No new checkins to sync")

    def set_active_status_tab(self, tab: str):
        self.active_status_tab = tab

    def set_search_query(self, query: str):
        self.search_query = query

    def open_checkin_detail(self, checkin: AdminCheckIn):
        self.selected_checkin = checkin
        self.show_checkin_detail_modal = True

    def close_checkin_detail(self):
        self.show_checkin_detail_modal = False
        self.selected_checkin = {}

    def set_show_checkin_detail_modal(self, value: bool):
        self.show_checkin_detail_modal = value
        if not value:
            self.selected_checkin = {}

    def _update_checkin(self, checkin_id: str, status: str):
        """Update checkin status in both lists."""
        update = lambda lst: [
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
        self.all_checkins = update(self.all_checkins)
        self.call_log_checkins = update(self.call_log_checkins)
        self.show_checkin_detail_modal = False

    def mark_as_reviewed(self, checkin_id: str):
        self._update_checkin(checkin_id, "reviewed")

    def flag_checkin(self, checkin_id: str):
        self._update_checkin(checkin_id, "flagged")
