"""Data source state for device/app integrations.

Handles data sources (wearables, CGMs, apps, EHRs) and related pagination.
"""

import asyncio
from typing import Any

import reflex as rx

from ....config import current_config, get_logger
from ....data.schemas.llm import DataSource
from ....functions.db_utils import get_data_sources_sync
from ...auth.base import AuthState

logger = get_logger("longevity_clinic.dashboard.data_source")


class DataSourceState(rx.State):
    """State for data source (device/app) management."""

    # Data
    data_sources: list[DataSource] = []

    # Filter
    data_sources_filter: str = "devices"  # devices | api_connections | import_history

    # Modal state
    show_connect_modal: bool = False
    show_suggest_integration_modal: bool = False
    suggested_integration_name: str = ""
    suggested_integration_description: str = ""
    integration_suggestion_submitted: bool = False

    # Pagination - page size from config
    _DATA_SOURCES_PAGE_SIZE: int = current_config.data_source_page_size
    data_sources_page: int = 1

    # Loading
    is_loading: bool = False
    _data_loaded: bool = False

    # =========================================================================
    # Computed Variables - Data Loading Config
    # =========================================================================

    @rx.var
    def data_limit(self) -> int:
        """Preemptive data limit based on page_size * preload_pages."""
        return self._DATA_SOURCES_PAGE_SIZE * current_config.preload_pages

    # =========================================================================
    # Computed Variables
    # =========================================================================

    @rx.var
    def connected_sources_count(self) -> int:
        return len([s for s in self.data_sources if s.connected])

    @rx.var
    def filtered_data_sources(self) -> list[DataSource]:
        type_map = {
            "devices": ["wearable", "scale", "cgm"],
            "api_connections": ["app", "ehr"],
            "import_history": [],
        }
        types = type_map.get(self.data_sources_filter, [])
        return (
            [s for s in self.data_sources if s.type in types]
            if types
            else self.data_sources
        )

    # =========================================================================
    # Computed Variables - Pagination
    # =========================================================================

    @rx.var
    def data_sources_paginated(self) -> list[DataSource]:
        """Paginated slice of filtered data sources."""
        start = (self.data_sources_page - 1) * self._DATA_SOURCES_PAGE_SIZE
        end = start + self._DATA_SOURCES_PAGE_SIZE
        return self.filtered_data_sources[start:end]

    @rx.var
    def data_sources_total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_data_sources) + self._DATA_SOURCES_PAGE_SIZE - 1)
            // self._DATA_SOURCES_PAGE_SIZE,
        )

    @rx.var
    def data_sources_has_previous(self) -> bool:
        return self.data_sources_page > 1

    @rx.var
    def data_sources_has_next(self) -> bool:
        return self.data_sources_page < self.data_sources_total_pages

    @rx.var
    def data_sources_page_info(self) -> str:
        return f"Page {self.data_sources_page} of {self.data_sources_total_pages}"

    @rx.var
    def data_sources_showing_info(self) -> str:
        total = len(self.filtered_data_sources)
        if total == 0:
            return "No data sources"
        start = (self.data_sources_page - 1) * self._DATA_SOURCES_PAGE_SIZE + 1
        end = min(self.data_sources_page * self._DATA_SOURCES_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Data Loading
    # =========================================================================

    @rx.event(background=True)
    async def load_data_source_data(self):
        """Load data source data from database."""
        user_id = 0
        # Calculate limit from config: page_size * preload_pages
        limit = self._DATA_SOURCES_PAGE_SIZE * current_config.preload_pages
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
            sources = await asyncio.to_thread(
                get_data_sources_sync, user_id, limit=limit
            )
            logger.info("Loaded %d data sources for user_id=%s", len(sources), user_id)
            async with self:
                self.data_sources = sources
                self.is_loading = False
                self._data_loaded = True
        except Exception as e:
            logger.error("Failed to load data source data: %s", e)
            async with self:
                self.is_loading = False

    async def load_data_source_data_for_patient(self, user_id: int, limit: int = 50):
        """Load data source data for a specific patient (admin view)."""
        try:
            sources = await asyncio.to_thread(
                get_data_sources_sync, user_id, limit=limit
            )
            logger.info(
                "Loaded %d data sources for patient user_id=%s", len(sources), user_id
            )
            self.data_sources = sources
            self._data_loaded = True
        except Exception as e:
            logger.error("Failed to load data source data for patient: %s", e)

    # =========================================================================
    # Filter & Pagination Handlers
    # =========================================================================

    def set_data_sources_filter(self, value: str):
        self.data_sources_filter = value

    def set_data_sources_filter_with_reset(self, value: str):
        """Set data sources filter and reset page to 1."""
        self.data_sources_filter = value
        self.data_sources_page = 1

    def data_sources_previous_page(self):
        if self.data_sources_page > 1:
            self.data_sources_page -= 1

    def data_sources_next_page(self):
        if self.data_sources_page < self.data_sources_total_pages:
            self.data_sources_page += 1

    # =========================================================================
    # Connection Handlers
    # =========================================================================

    def toggle_data_source_connection(self, source_id: str):
        """Toggle a data source connection on/off."""
        self.data_sources = [
            (
                s.model_copy(
                    update={
                        "connected": not s.connected,
                        "status": "connected" if not s.connected else "disconnected",
                        "last_sync": "Just now" if not s.connected else "Disconnected",
                    }
                )
                if s.id == source_id
                else s
            )
            for s in self.data_sources
        ]

    # =========================================================================
    # Modal Handlers
    # =========================================================================

    def set_show_connect_modal(self, value: bool):
        self.show_connect_modal = value

    def open_suggest_integration_modal(self):
        self.show_suggest_integration_modal = True
        self.suggested_integration_name = ""
        self.suggested_integration_description = ""
        self.integration_suggestion_submitted = False

    def set_show_suggest_integration_modal(self, value: bool):
        self.show_suggest_integration_modal = value

    def set_suggested_integration_name(self, value: str):
        self.suggested_integration_name = value

    def set_suggested_integration_description(self, value: str):
        self.suggested_integration_description = value

    def submit_integration_suggestion(self):
        self.integration_suggestion_submitted = True

    def clear_data(self):
        """Clear all data source data."""
        self.data_sources = []
        self._data_loaded = False
        self.data_sources_filter = "devices"
        self.data_sources_page = 1
