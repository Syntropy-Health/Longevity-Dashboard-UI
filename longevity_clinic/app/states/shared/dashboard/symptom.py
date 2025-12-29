"""Symptom state for symptom tracking.

Handles symptoms, symptom logs, symptom trends, and related pagination.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Any

import reflex as rx

from ....config import current_config, get_logger
from ....data.schemas.llm import (
    Symptom,
    SymptomEntryModel as SymptomEntry,
    SymptomTrend,
)
from ....functions.db_utils import (
    get_symptom_logs_sync,
    get_symptom_trends_sync,
    get_symptoms_sync,
)
from ...auth.base import AuthState

logger = get_logger("longevity_clinic.dashboard.symptom")


class SymptomState(rx.State):
    """State for symptom tracking.

    Tracks:
    - symptoms: Current symptom status
    - symptom_logs: Individual symptom entries/logs
    - symptom_trends: Symptom changes over time
    """

    # Data
    symptoms: list[Symptom] = []
    symptom_logs: list[SymptomEntry] = []
    symptom_trends: list[SymptomTrend] = []

    # Filter
    symptoms_filter: str = "timeline"

    # Symptom detail modal
    show_symptom_modal: bool = False
    selected_symptom: dict[str, Any] = {}

    # Symptom log detail modal
    show_symptom_log_modal: bool = False
    selected_symptom_log: dict[str, Any] = {}

    # Pagination - page sizes from config
    _SYMPTOMS_PAGE_SIZE: int = current_config.symptom_page_size
    _SYMPTOM_LOGS_PAGE_SIZE: int = 8
    _TRENDS_PAGE_SIZE: int = 5
    symptoms_page: int = 1
    symptom_logs_page: int = 1
    symptom_trends_page: int = 1

    # Loading
    is_loading: bool = False
    _data_loaded: bool = False

    # =========================================================================
    # Computed Variables - Data Loading Config
    # =========================================================================

    @rx.var
    def data_limit(self) -> int:
        """Preemptive data limit based on page_size * preload_pages."""
        return self._SYMPTOMS_PAGE_SIZE * current_config.preload_pages

    @rx.var
    def trends_limit(self) -> int:
        """Preemptive trends limit based on page_size * preload_pages."""
        return self._TRENDS_PAGE_SIZE * current_config.preload_pages

    # =========================================================================
    # Computed Variables - Selected Symptom
    # =========================================================================

    @rx.var
    def selected_symptom_name(self) -> str:
        """Name of selected symptom."""
        return self.selected_symptom.get("name", "")

    @rx.var
    def selected_symptom_severity(self) -> str:
        """Severity of selected symptom."""
        return str(self.selected_symptom.get("severity", "unknown")).capitalize()

    @rx.var
    def selected_symptom_frequency(self) -> str:
        """Frequency of selected symptom."""
        return self.selected_symptom.get("frequency", "Unknown")

    @rx.var
    def selected_symptom_trend(self) -> str:
        """Trend of selected symptom."""
        return str(self.selected_symptom.get("trend", "stable")).capitalize()

    # =========================================================================
    # Computed Variables - Selected Symptom Log
    # =========================================================================

    @rx.var
    def selected_log_symptom_name(self) -> str:
        """Symptom name of selected log."""
        return self.selected_symptom_log.get("symptom_name", "")

    @rx.var
    def selected_log_severity(self) -> int:
        """Severity rating of selected log."""
        return int(self.selected_symptom_log.get("severity", 0))

    @rx.var
    def selected_log_notes(self) -> str:
        """Notes of selected log."""
        return self.selected_symptom_log.get("notes", "")

    @rx.var
    def selected_log_timestamp(self) -> str:
        """Timestamp of selected log."""
        return self.selected_symptom_log.get("timestamp", "")

    # =========================================================================
    # Computed Variables - Symptoms Pagination
    # =========================================================================

    @rx.var
    def symptoms_paginated(self) -> list[Symptom]:
        """Paginated slice of symptoms."""
        start = (self.symptoms_page - 1) * self._SYMPTOMS_PAGE_SIZE
        end = start + self._SYMPTOMS_PAGE_SIZE
        return self.symptoms[start:end]

    @rx.var
    def symptoms_total_pages(self) -> int:
        return max(
            1,
            (len(self.symptoms) + self._SYMPTOMS_PAGE_SIZE - 1)
            // self._SYMPTOMS_PAGE_SIZE,
        )

    @rx.var
    def symptoms_has_previous(self) -> bool:
        return self.symptoms_page > 1

    @rx.var
    def symptoms_has_next(self) -> bool:
        return self.symptoms_page < self.symptoms_total_pages

    @rx.var
    def symptoms_page_info(self) -> str:
        return f"Page {self.symptoms_page} of {self.symptoms_total_pages}"

    @rx.var
    def symptoms_showing_info(self) -> str:
        total = len(self.symptoms)
        if total == 0:
            return "No symptoms"
        start = (self.symptoms_page - 1) * self._SYMPTOMS_PAGE_SIZE + 1
        end = min(self.symptoms_page * self._SYMPTOMS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Computed Variables - Symptom Logs Pagination
    # =========================================================================

    @rx.var
    def symptom_logs_paginated(self) -> list[SymptomEntry]:
        """Paginated slice of symptom logs."""
        start = (self.symptom_logs_page - 1) * self._SYMPTOM_LOGS_PAGE_SIZE
        end = start + self._SYMPTOM_LOGS_PAGE_SIZE
        return self.symptom_logs[start:end]

    @rx.var
    def symptom_logs_total_pages(self) -> int:
        return max(
            1,
            (len(self.symptom_logs) + self._SYMPTOM_LOGS_PAGE_SIZE - 1)
            // self._SYMPTOM_LOGS_PAGE_SIZE,
        )

    @rx.var
    def symptom_logs_has_previous(self) -> bool:
        return self.symptom_logs_page > 1

    @rx.var
    def symptom_logs_has_next(self) -> bool:
        return self.symptom_logs_page < self.symptom_logs_total_pages

    @rx.var
    def symptom_logs_page_info(self) -> str:
        return f"Page {self.symptom_logs_page} of {self.symptom_logs_total_pages}"

    @rx.var
    def symptom_logs_showing_info(self) -> str:
        total = len(self.symptom_logs)
        if total == 0:
            return "No symptom logs"
        start = (self.symptom_logs_page - 1) * self._SYMPTOM_LOGS_PAGE_SIZE + 1
        end = min(self.symptom_logs_page * self._SYMPTOM_LOGS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Computed Variables - Symptom Trends Pagination
    # =========================================================================

    @rx.var
    def symptom_trends_paginated(self) -> list[SymptomTrend]:
        """Paginated slice of symptom trends."""
        start = (self.symptom_trends_page - 1) * self._TRENDS_PAGE_SIZE
        end = start + self._TRENDS_PAGE_SIZE
        return self.symptom_trends[start:end]

    @rx.var
    def symptom_trends_total_pages(self) -> int:
        return max(
            1,
            (len(self.symptom_trends) + self._TRENDS_PAGE_SIZE - 1)
            // self._TRENDS_PAGE_SIZE,
        )

    @rx.var
    def symptom_trends_has_previous(self) -> bool:
        return self.symptom_trends_page > 1

    @rx.var
    def symptom_trends_has_next(self) -> bool:
        return self.symptom_trends_page < self.symptom_trends_total_pages

    @rx.var
    def symptom_trends_page_info(self) -> str:
        return f"Page {self.symptom_trends_page} of {self.symptom_trends_total_pages}"

    @rx.var
    def symptom_trends_showing_info(self) -> str:
        total = len(self.symptom_trends)
        if total == 0:
            return "No symptom trends"
        start = (self.symptom_trends_page - 1) * self._TRENDS_PAGE_SIZE + 1
        end = min(self.symptom_trends_page * self._TRENDS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Data Loading
    # =========================================================================

    @rx.event(background=True)
    async def load_symptom_data(self):
        """Load symptom data from database."""
        user_id = 0
        # Calculate limits from config: page_size * preload_pages
        limit = self._SYMPTOMS_PAGE_SIZE * current_config.preload_pages
        trends_limit = self._TRENDS_PAGE_SIZE * current_config.preload_pages
        async with self:
            if self._data_loaded:
                return
            self.is_loading = True
            auth_state = await self.get_state(AuthState)
            user_id = auth_state.user_id

        if not user_id:
            async with self:
                self.is_loading = False
            return

        try:
            symptoms, logs, trends = await asyncio.gather(
                asyncio.to_thread(get_symptoms_sync, user_id, limit=limit),
                asyncio.to_thread(get_symptom_logs_sync, user_id, limit=limit),
                asyncio.to_thread(get_symptom_trends_sync, user_id, limit=trends_limit),
            )
            logger.info(
                "Loaded %d symptoms, %d logs, %d trends for user_id=%s",
                len(symptoms),
                len(logs),
                len(trends),
                user_id,
            )
            async with self:
                self.symptoms = symptoms
                self.symptom_logs = logs
                self.symptom_trends = trends
                self.is_loading = False
                self._data_loaded = True
        except Exception as e:
            logger.error("Failed to load symptom data: %s", e)
            async with self:
                self.is_loading = False

    async def load_symptom_data_for_patient(
        self, user_id: int, limit: int = 100, trends_limit: int = 50
    ):
        """Load symptom data for a specific patient (admin view)."""
        try:
            symptoms, logs, trends = await asyncio.gather(
                asyncio.to_thread(get_symptoms_sync, user_id, limit=limit),
                asyncio.to_thread(get_symptom_logs_sync, user_id, limit=limit),
                asyncio.to_thread(get_symptom_trends_sync, user_id, limit=trends_limit),
            )
            logger.info(
                "Loaded %d symptoms, %d logs, %d trends for patient user_id=%s",
                len(symptoms),
                len(logs),
                len(trends),
                user_id,
            )
            self.symptoms = symptoms
            self.symptom_logs = logs
            self.symptom_trends = trends
            self._data_loaded = True
        except Exception as e:
            logger.error("Failed to load symptom data for patient: %s", e)

    # =========================================================================
    # Filter & Pagination Handlers
    # =========================================================================

    def set_symptoms_filter(self, value: str):
        self.symptoms_filter = value

    def symptoms_previous_page(self):
        if self.symptoms_page > 1:
            self.symptoms_page -= 1

    def symptoms_next_page(self):
        if self.symptoms_page < self.symptoms_total_pages:
            self.symptoms_page += 1

    def symptom_logs_previous_page(self):
        if self.symptom_logs_page > 1:
            self.symptom_logs_page -= 1

    def symptom_logs_next_page(self):
        if self.symptom_logs_page < self.symptom_logs_total_pages:
            self.symptom_logs_page += 1

    def symptom_trends_previous_page(self):
        if self.symptom_trends_page > 1:
            self.symptom_trends_page -= 1

    def symptom_trends_next_page(self):
        if self.symptom_trends_page < self.symptom_trends_total_pages:
            self.symptom_trends_page += 1

    # =========================================================================
    # Modal Handlers
    # =========================================================================

    def open_symptom_modal(self, symptom: dict[str, Any]):
        """Open symptom detail modal."""
        self.selected_symptom = symptom
        self.show_symptom_modal = True

    def close_symptom_modal(self, _value: bool = False):
        """Close symptom detail modal."""
        self.show_symptom_modal = False

    def set_show_symptom_modal(self, value: bool):
        self.show_symptom_modal = value

    def open_symptom_log_modal(self, log: dict[str, Any]):
        """Open symptom log detail modal."""
        self.selected_symptom_log = log
        self.show_symptom_log_modal = True

    def close_symptom_log_modal(self, _value: bool = False):
        """Close symptom log detail modal."""
        self.show_symptom_log_modal = False

    @rx.event
    async def save_symptom_log(self):
        if self.selected_symptom:
            new_log = SymptomEntry(
                id=f"sym_{uuid.uuid4().hex[:8]}",
                symptom_name=self.selected_symptom.get("name", "UNKNOWN"),
                severity=5,
                notes="",
                timestamp=datetime.now().strftime("Today, %I:%M %p"),
            )
            self.symptom_logs = [new_log, *self.symptom_logs]
        self.show_symptom_modal = False

    def clear_data(self):
        """Clear all symptom data."""
        self.symptoms = []
        self.symptom_logs = []
        self.symptom_trends = []
        self._data_loaded = False
        self.symptoms_page = 1
        self.symptom_logs_page = 1
        self.symptom_trends_page = 1
