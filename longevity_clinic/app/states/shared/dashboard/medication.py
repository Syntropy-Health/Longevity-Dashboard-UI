"""Medication state for medication tracking.

Handles medication entries (logs), medication prescriptions (prescriptions),
and related pagination.
"""

import asyncio
from typing import Any

import reflex as rx

from ....config import current_config, get_logger
from ....data.schemas.state import (
    MedicationLogEntry,
    MedicationLogEntryStateModel,
    Prescription,
    PrescriptionStateModel,
)
from ....functions.db_utils import (
    get_medication_entries_sync,
    get_prescriptions_sync,
)
from ...auth.base import AuthState

logger = get_logger("longevity_clinic.dashboard.medication")


class MedicationState(rx.State):
    """State for medication tracking.

    Tracks both:
    - medication_entries: What the patient actually took (logs)
    - prescriptions: What's prescribed (via PatientTreatment)
    """

    # Data - TypedDicts for Reflex foreach compatibility
    medication_entries: list[MedicationLogEntry] = []
    prescriptions: list[Prescription] = []

    # Medication entry (log) detail modal
    show_medication_entry_modal: bool = False
    selected_medication_entry: dict[str, Any] = {}

    # Prescription detail modal
    show_prescription_modal: bool = False
    selected_prescription: dict[str, Any] = {}

    # Legacy modal state (for backward compatibility)
    show_medication_modal: bool = False
    selected_medication: dict[str, Any] = {}
    selected_medication_subscription: dict[str, Any] = {}

    # Pagination - page sizes from config
    _MED_LOGS_PAGE_SIZE: int = current_config.medication_page_size
    _MED_SUBS_PAGE_SIZE: int = current_config.medication_page_size
    medication_entries_page: int = 1
    prescriptions_page: int = 1

    # Loading
    is_loading: bool = False
    _data_loaded: bool = False

    # =========================================================================
    # Computed Variables - Data Loading Config
    # =========================================================================

    @rx.var
    def data_limit(self) -> int:
        """Preemptive data limit based on page_size * preload_pages."""
        return self._MED_LOGS_PAGE_SIZE * current_config.preload_pages

    # =========================================================================
    # Computed Variables - Selected Medication Entry
    # =========================================================================

    @rx.var
    def selected_entry_name(self) -> str:
        """Name of selected medication entry."""
        return self.selected_medication_entry.get("name", "")

    @rx.var
    def selected_entry_dosage(self) -> str:
        """Dosage of selected medication entry."""
        return self.selected_medication_entry.get("dosage", "")

    @rx.var
    def selected_entry_taken_at(self) -> str:
        """Taken at timestamp of selected medication entry."""
        return self.selected_medication_entry.get("taken_at", "")

    @rx.var
    def selected_entry_notes(self) -> str:
        """Notes of selected medication entry."""
        return self.selected_medication_entry.get("notes", "")

    # =========================================================================
    # Computed Variables - Selected Prescription
    # =========================================================================

    @rx.var
    def selected_rx_name(self) -> str:
        """Name of selected prescription."""
        return self.selected_prescription.get("name", "")

    @rx.var
    def selected_rx_dosage(self) -> str:
        """Dosage of selected prescription."""
        return self.selected_prescription.get("dosage", "")

    @rx.var
    def selected_rx_frequency(self) -> str:
        """Frequency of selected prescription."""
        return self.selected_prescription.get("frequency", "")

    @rx.var
    def selected_rx_instructions(self) -> str:
        """Instructions of selected prescription."""
        return self.selected_prescription.get("instructions", "")

    @rx.var
    def selected_rx_status(self) -> str:
        """Status of selected prescription."""
        return self.selected_prescription.get("status", "active").capitalize()

    @rx.var
    def selected_rx_adherence(self) -> float:
        """Adherence rate of selected prescription."""
        return float(self.selected_prescription.get("adherence_rate", 0.0))

    @rx.var
    def selected_rx_assigned_by(self) -> str:
        """Assigned by of selected prescription."""
        return self.selected_prescription.get("assigned_by", "Unknown")

    # =========================================================================
    # Computed Variables - General
    # =========================================================================

    @rx.var
    def total_medication_adherence(self) -> float:
        """Calculate overall medication adherence from prescriptions."""
        if not self.prescriptions:
            return 0.0
        return sum(m.get("adherence_rate", 0.0) for m in self.prescriptions) / len(
            self.prescriptions
        )

    @rx.var
    def active_prescriptions_count(self) -> int:
        """Count of active medication prescriptions."""
        return len([s for s in self.prescriptions if s.get("status") == "active"])

    @rx.var
    def medication_entries_count(self) -> int:
        """Count of Medication Entries."""
        return len(self.medication_entries)

    # =========================================================================
    # Computed Variables - Medication Entries Pagination
    # =========================================================================

    @rx.var
    def medication_entries_paginated(self) -> list[MedicationLogEntryStateModel]:
        """Paginated slice of Medication Entries."""
        start = (self.medication_entries_page - 1) * self._MED_LOGS_PAGE_SIZE
        end = start + self._MED_LOGS_PAGE_SIZE
        return [
            MedicationLogEntryStateModel(**entry)
            for entry in self.medication_entries[start:end]
        ]

    @rx.var
    def medication_entries_total_pages(self) -> int:
        return max(
            1,
            (len(self.medication_entries) + self._MED_LOGS_PAGE_SIZE - 1)
            // self._MED_LOGS_PAGE_SIZE,
        )

    @rx.var
    def medication_entries_has_previous(self) -> bool:
        return self.medication_entries_page > 1

    @rx.var
    def medication_entries_has_next(self) -> bool:
        return self.medication_entries_page < self.medication_entries_total_pages

    @rx.var
    def medication_entries_page_info(self) -> str:
        return f"Page {self.medication_entries_page} of {self.medication_entries_total_pages}"

    @rx.var
    def medication_entries_showing_info(self) -> str:
        total = len(self.medication_entries)
        if total == 0:
            return "No Medication Entries"
        start = (self.medication_entries_page - 1) * self._MED_LOGS_PAGE_SIZE + 1
        end = min(self.medication_entries_page * self._MED_LOGS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Computed Variables - Medication Prescriptions Pagination
    # =========================================================================

    @rx.var
    def prescriptions_paginated(self) -> list[PrescriptionStateModel]:
        """Paginated slice of medication prescriptions."""
        start = (self.prescriptions_page - 1) * self._MED_SUBS_PAGE_SIZE
        end = start + self._MED_SUBS_PAGE_SIZE
        return [PrescriptionStateModel(**p) for p in self.prescriptions[start:end]]

    @rx.var
    def prescriptions_total_pages(self) -> int:
        return max(
            1,
            (len(self.prescriptions) + self._MED_SUBS_PAGE_SIZE - 1)
            // self._MED_SUBS_PAGE_SIZE,
        )

    @rx.var
    def prescriptions_has_previous(self) -> bool:
        return self.prescriptions_page > 1

    @rx.var
    def prescriptions_has_next(self) -> bool:
        return self.prescriptions_page < self.prescriptions_total_pages

    @rx.var
    def prescriptions_page_info(self) -> str:
        return f"Page {self.prescriptions_page} of {self.prescriptions_total_pages}"

    @rx.var
    def prescriptions_showing_info(self) -> str:
        total = len(self.prescriptions)
        if total == 0:
            return "No prescriptions"
        start = (self.prescriptions_page - 1) * self._MED_SUBS_PAGE_SIZE + 1
        end = min(self.prescriptions_page * self._MED_SUBS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Data Loading
    # =========================================================================

    @rx.event(background=True)
    async def load_medication_data(self):
        """Load medication data from database."""
        # Calculate limit from config: page_size * preload_pages
        user_id = 0
        limit = self._MED_LOGS_PAGE_SIZE * current_config.preload_pages
        async with self:
            auth_state = await self.get_state(AuthState)
            # Access user dict directly instead of computed var
            user = auth_state.user
            if not user:
                logger.warning("No user logged in, cannot load medication data")
                self.is_loading = False
                return

            try:
                user_id = int(user.get("id", "0"))
            except (ValueError, TypeError):
                user_id = 0

            if not user_id:
                logger.warning("Invalid user_id=0, cannot load medication data")
                self.is_loading = False
                return

            # Check if already loaded for THIS user
            if self._data_loaded:
                logger.debug("Medication data already loaded for user_id=%s", user_id)
                return

            self.is_loading = True
            logger.info("Loading medication data for user_id=%s", user_id)

        # Now load data outside the async context (user_id and limit are captured)
        try:
            entries, prescriptions = await asyncio.gather(
                asyncio.to_thread(get_medication_entries_sync, user_id, limit=limit),
                asyncio.to_thread(get_prescriptions_sync, user_id, limit=limit),
            )
            logger.info(
                "Loaded %d medication entries and %d prescriptions for user_id=%s",
                len(entries),
                len(prescriptions),
                user_id,
            )
            async with self:
                self.medication_entries = entries
                self.prescriptions = prescriptions
                self.is_loading = False
                self._data_loaded = True
        except Exception as e:
            logger.error("Failed to load medication data: %s", e)
            async with self:
                self.is_loading = False

    async def load_medication_data_for_patient(self, user_id: int, limit: int = 100):
        """Load medication data for a specific patient (admin view)."""
        try:
            entries, prescriptions = await asyncio.gather(
                asyncio.to_thread(get_medication_entries_sync, user_id, limit=limit),
                asyncio.to_thread(get_prescriptions_sync, user_id, limit=limit),
            )
            logger.info(
                "Loaded %d medication entries and %d prescriptions for patient user_id=%s",
                len(entries),
                len(prescriptions),
                user_id,
            )
            self.medication_entries = entries
            self.prescriptions = prescriptions
            self._data_loaded = True
        except Exception as e:
            logger.error("Failed to load medication data for patient: %s", e)

    # =========================================================================
    # Pagination
    # =========================================================================

    def medication_entries_previous_page(self):
        if self.medication_entries_page > 1:
            self.medication_entries_page -= 1

    def medication_entries_next_page(self):
        if self.medication_entries_page < self.medication_entries_total_pages:
            self.medication_entries_page += 1

    def prescriptions_previous_page(self):
        if self.prescriptions_page > 1:
            self.prescriptions_page -= 1

    def prescriptions_next_page(self):
        if self.prescriptions_page < self.prescriptions_total_pages:
            self.prescriptions_page += 1

    # =========================================================================
    # Modal Handlers
    # =========================================================================

    def select_medication_entry(self, entry: dict[str, Any]):
        """Select a medication entry (log) for viewing details."""
        self.selected_medication_entry = entry
        self.show_medication_entry_modal = True

    def close_medication_entry_modal(self, _value: bool = False):
        """Close the medication entry detail modal."""
        self.show_medication_entry_modal = False

    def open_prescription_modal(self, prescription: dict[str, Any]):
        """Open prescription detail modal."""
        self.selected_prescription = prescription
        self.show_prescription_modal = True

    def close_prescription_modal(self, _value: bool = False):
        """Close the prescription detail modal."""
        self.show_prescription_modal = False

    # Legacy handlers for backward compatibility
    def open_medication_modal(self, medication: dict[str, Any]):
        """Legacy: Opens prescription modal."""
        self.open_prescription_modal(medication)

    def set_show_medication_modal(self, value: bool):
        self.show_medication_modal = value

    @rx.event
    async def log_dose(self):
        """Log dose for a medication."""
        self.show_prescription_modal = False
        self.show_medication_modal = False

    def reset_data_loaded(self):
        """Reset data loaded flag to allow reload on next load call.

        Unlike clear_data(), this preserves existing data to prevent UI flicker
        while new data is being fetched.
        """
        self._data_loaded = False

    def clear_data(self):
        """Clear all medication data."""
        self.medication_entries = []
        self.prescriptions = []
        self._data_loaded = False
        self.medication_entries_page = 1
        self.prescriptions_page = 1
