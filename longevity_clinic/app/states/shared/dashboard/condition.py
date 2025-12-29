"""Condition state for health condition tracking.

Handles conditions (diagnoses), filtering, and related pagination.
"""

import asyncio
from typing import Any

import reflex as rx

from ....config import current_config, get_logger
from ....data.schemas.llm import Condition
from ....functions.db_utils import get_conditions_sync
from ...auth.base import AuthState

logger = get_logger(__name__)


class ConditionState(rx.State):
    """State for health condition tracking."""

    # Data
    conditions: list[Condition] = []

    # Filter
    conditions_filter: str = "all"  # all | active | managed | resolved

    # Modal state
    show_condition_modal: bool = False
    selected_condition: dict[str, Any] = {}

    # Pagination - page size from config
    _CONDITIONS_PAGE_SIZE: int = current_config.condition_page_size
    conditions_page: int = 1

    # Loading
    is_loading: bool = False
    _data_loaded: bool = False

    # =========================================================================
    # Computed Variables - Data Loading Config
    # =========================================================================

    @rx.var
    def data_limit(self) -> int:
        """Preemptive data limit based on page_size * preload_pages."""
        return self._CONDITIONS_PAGE_SIZE * current_config.preload_pages

    # =========================================================================
    # Computed Variables - Counts
    # =========================================================================

    @rx.var
    def active_conditions_count(self) -> int:
        return len([c for c in self.conditions if c.status == "active"])

    @rx.var
    def managed_conditions_count(self) -> int:
        return len([c for c in self.conditions if c.status == "managed"])

    @rx.var
    def resolved_conditions_count(self) -> int:
        return len([c for c in self.conditions if c.status == "resolved"])

    @rx.var
    def filtered_conditions(self) -> list[Condition]:
        if self.conditions_filter == "all":
            return self.conditions
        return [c for c in self.conditions if c.status == self.conditions_filter]

    # =========================================================================
    # Computed Variables - Pagination
    # =========================================================================

    @rx.var
    def conditions_paginated(self) -> list[Condition]:
        """Paginated slice of filtered conditions."""
        start = (self.conditions_page - 1) * self._CONDITIONS_PAGE_SIZE
        end = start + self._CONDITIONS_PAGE_SIZE
        return self.filtered_conditions[start:end]

    @rx.var
    def conditions_total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_conditions) + self._CONDITIONS_PAGE_SIZE - 1)
            // self._CONDITIONS_PAGE_SIZE,
        )

    @rx.var
    def conditions_has_previous(self) -> bool:
        return self.conditions_page > 1

    @rx.var
    def conditions_has_next(self) -> bool:
        return self.conditions_page < self.conditions_total_pages

    @rx.var
    def conditions_page_info(self) -> str:
        return f"Page {self.conditions_page} of {self.conditions_total_pages}"

    @rx.var
    def conditions_showing_info(self) -> str:
        total = len(self.filtered_conditions)
        if total == 0:
            return "No conditions"
        start = (self.conditions_page - 1) * self._CONDITIONS_PAGE_SIZE + 1
        end = min(self.conditions_page * self._CONDITIONS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Data Loading
    # =========================================================================

    @rx.event(background=True)
    async def load_condition_data(self):
        """Load condition data from database."""
        user_id = 0
        # Calculate limit from config: page_size * preload_pages
        limit = self._CONDITIONS_PAGE_SIZE * current_config.preload_pages
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
            conditions = await asyncio.to_thread(
                get_conditions_sync, user_id, limit=limit
            )
            logger.info("Loaded %d conditions for user_id=%s", len(conditions), user_id)
            async with self:
                self.conditions = conditions
                self.is_loading = False
                self._data_loaded = True
        except Exception as e:
            logger.error("Failed to load condition data: %s", e)
            async with self:
                self.is_loading = False

    async def load_condition_data_for_patient(self, user_id: int, limit: int = 100):
        """Load condition data for a specific patient (admin view)."""
        try:
            conditions = await asyncio.to_thread(
                get_conditions_sync, user_id, limit=limit
            )
            logger.info(
                "Loaded %d conditions for patient user_id=%s", len(conditions), user_id
            )
            self.conditions = conditions
            self._data_loaded = True
        except Exception as e:
            logger.error("Failed to load condition data for patient: %s", e)

    # =========================================================================
    # Filter & Pagination Handlers
    # =========================================================================

    def set_conditions_filter_with_reset(self, value: str):
        """Set conditions filter and reset page to 1."""
        self.conditions_filter = value
        self.conditions_page = 1

    def conditions_previous_page(self):
        if self.conditions_page > 1:
            self.conditions_page -= 1

    def conditions_next_page(self):
        if self.conditions_page < self.conditions_total_pages:
            self.conditions_page += 1

    # =========================================================================
    # Modal Handlers
    # =========================================================================

    def open_condition_modal(self, condition: dict[str, Any]):
        self.selected_condition = condition
        self.show_condition_modal = True

    def set_show_condition_modal(self, value: bool):
        self.show_condition_modal = value

    def clear_data(self):
        """Clear all condition data."""
        self.conditions = []
        self._data_loaded = False
        self.conditions_filter = "all"
        self.conditions_page = 1
