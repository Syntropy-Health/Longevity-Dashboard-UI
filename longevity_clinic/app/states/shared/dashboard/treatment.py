"""Treatment state for patient portal.

Handles active treatments/protocols with pagination for the patient view.
Moved from BiomarkerState for better separation of concerns.
"""

import asyncio
from typing import Any

import reflex as rx

from ....config import get_logger
from ....data.schemas.state import PortalTreatment
from ....functions.db_utils import get_patient_treatments_sync
from ....functions.db_utils.users import get_user_by_external_id_sync
from ...auth.base import AuthState

logger = get_logger("longevity_clinic.dashboard.treatment")


class TreatmentPortalState(rx.State):
    """State for patient treatment/protocol management.

    Handles active treatments with pagination for the patient portal.
    """

    # Data
    my_treatments: list[PortalTreatment] = []

    # Pagination
    _TREATMENTS_PAGE_SIZE: int = 4
    treatments_page: int = 1

    # Loading
    is_loading: bool = False
    _data_loaded: bool = False

    # =========================================================================
    # Computed Variables - Pagination
    # =========================================================================

    @rx.var
    def treatments_paginated(self) -> list[PortalTreatment]:
        """Paginated slice of treatments."""
        start = (self.treatments_page - 1) * self._TREATMENTS_PAGE_SIZE
        end = start + self._TREATMENTS_PAGE_SIZE
        return self.my_treatments[start:end]

    @rx.var
    def treatments_total_pages(self) -> int:
        """Total number of treatment pages."""
        return max(
            1,
            (len(self.my_treatments) + self._TREATMENTS_PAGE_SIZE - 1)
            // self._TREATMENTS_PAGE_SIZE,
        )

    @rx.var
    def treatments_has_previous(self) -> bool:
        """Check if there's a previous page."""
        return self.treatments_page > 1

    @rx.var
    def treatments_has_next(self) -> bool:
        """Check if there's a next page."""
        return self.treatments_page < self.treatments_total_pages

    @rx.var
    def treatments_page_info(self) -> str:
        """Page info string."""
        return f"Page {self.treatments_page} of {self.treatments_total_pages}"

    @rx.var
    def treatments_showing_info(self) -> str:
        """Showing info string."""
        total = len(self.my_treatments)
        if total == 0:
            return "No treatments"
        start = (self.treatments_page - 1) * self._TREATMENTS_PAGE_SIZE + 1
        end = min(self.treatments_page * self._TREATMENTS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    @rx.var
    def treatments_count(self) -> int:
        """Total number of treatments."""
        return len(self.my_treatments)

    # =========================================================================
    # Data Loading
    # =========================================================================

    @rx.event(background=True)
    async def load_treatments(self):
        """Load treatment data from database for authenticated user."""
        async with self:
            if self._data_loaded:
                logger.debug("load_treatments: Already loaded, skipping")
                return
            self.is_loading = True
            auth_state = await self.get_state(AuthState)
            user_id = auth_state.user_id

        if not user_id:
            logger.warning("load_treatments: No user_id, skipping")
            async with self:
                self.is_loading = False
            return

        logger.info("load_treatments: Fetching for user_id %s", user_id)

        try:
            treatments = await asyncio.to_thread(
                get_patient_treatments_sync, user_id, 50
            )

            # Transform to PortalTreatment format
            portal_treatments: list[PortalTreatment] = [
                {
                    "id": str(t.get("treatment_id", "")),
                    "name": t.get("treatment_name", "Unknown"),
                    "frequency": t.get("frequency", "As needed"),
                    "duration": t.get("duration", "Ongoing"),
                    "category": t.get("category", "General"),
                    "status": t.get("status", "Active"),
                }
                for t in treatments
            ]

            async with self:
                self.my_treatments = portal_treatments
                self.is_loading = False
                self._data_loaded = True

            logger.info(
                "load_treatments: Loaded %d treatments",
                len(portal_treatments),
            )
        except Exception as e:
            logger.error("load_treatments: Failed - %s", e)
            async with self:
                self.is_loading = False

    async def load_treatments_for_patient(self, external_id: str):
        """Load treatments for a specific patient (admin view).

        Args:
            external_id: Patient external ID (e.g., 'P001')
        """
        logger.info("load_treatments_for_patient: %s", external_id)

        try:
            user = get_user_by_external_id_sync(external_id)
            if not user:
                logger.warning("User not found: %s", external_id)
                return

            treatments = await asyncio.to_thread(
                get_patient_treatments_sync, user.id, 50
            )

            portal_treatments: list[PortalTreatment] = [
                {
                    "id": str(t.get("treatment_id", "")),
                    "name": t.get("treatment_name", "Unknown"),
                    "frequency": t.get("frequency", "As needed"),
                    "duration": t.get("duration", "Ongoing"),
                    "category": t.get("category", "General"),
                    "status": t.get("status", "Active"),
                }
                for t in treatments
            ]

            self.my_treatments = portal_treatments
            self._data_loaded = True
            logger.info("Loaded %d treatments for patient", len(portal_treatments))
        except Exception as e:
            logger.error("Failed to load treatments for patient: %s", e)

    # =========================================================================
    # Pagination Events
    # =========================================================================

    @rx.event
    def treatments_previous_page(self):
        """Go to previous page."""
        if self.treatments_page > 1:
            self.treatments_page -= 1

    @rx.event
    def treatments_next_page(self):
        """Go to next page."""
        if self.treatments_page < self.treatments_total_pages:
            self.treatments_page += 1

    @rx.event
    def reset_treatments_page(self):
        """Reset to first page."""
        self.treatments_page = 1
