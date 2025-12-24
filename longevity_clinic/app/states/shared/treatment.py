"""Treatment states for admin and patient views.

TreatmentState - Admin protocol management (CRUD operations)
TreatmentSearchState - Patient treatment search and requests

Note: All treatment data is loaded from the database.
Seed data with: python scripts/load_seed_data.py
"""

from __future__ import annotations

import asyncio
import logging
import random

import reflex as rx

from ...data.schemas.state import TreatmentCategoryGroup, TreatmentProtocol
from ...functions.db_utils import (
    create_treatment_sync,
    get_treatments_as_protocols_sync,
    update_treatment_sync,
)

logger = logging.getLogger("longevity_clinic.states.treatment")


class TreatmentState(rx.State):
    """Admin state for managing treatment protocols."""

    protocols: list[TreatmentProtocol] = []
    _loaded: bool = False
    search_query: str = ""
    category_filter: str = "All"
    is_editor_open: bool = False
    editing_protocol: TreatmentProtocol | None = None
    form_name: str = ""
    form_category: str = ""
    form_description: str = ""
    form_duration: str = ""
    form_frequency: str = ""
    form_cost: str = ""
    form_status: str = "Active"
    is_assign_open: bool = False
    protocol_to_assign: TreatmentProtocol | None = None
    selected_patient_id_for_assignment: str = ""

    @rx.event
    async def load_protocols(self):
        """Load treatment protocols from database.

        Note: Requires seeded database. Run: python scripts/load_seed_data.py
        """
        if self._loaded:
            return
        try:
            db_protocols = await asyncio.to_thread(get_treatments_as_protocols_sync)
            self.protocols = db_protocols or []
            if not self.protocols:
                logger.warning(
                    "No treatments found in database. "
                    "Run 'python scripts/load_seed_data.py' to seed data."
                )
            self._loaded = True
        except Exception as e:
            logger.error("Error loading protocols from DB: %s", e)
            self.protocols = []
            self._loaded = True

    @rx.var
    def filtered_protocols(self) -> list[TreatmentProtocol]:
        items = self.protocols
        if self.category_filter != "All":
            items = [p for p in items if p["category"] == self.category_filter]
        if self.search_query:
            q = self.search_query.lower()
            items = [
                p
                for p in items
                if q in p["name"].lower() or q in p["description"].lower()
            ]
        return items

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_category_filter(self, category: str):
        self.category_filter = category

    @rx.event
    def open_add_modal(self):
        self.editing_protocol = None
        self.form_name = ""
        self.form_category = "IV Therapy"
        self.form_description = ""
        self.form_duration = ""
        self.form_frequency = "Weekly"
        self.form_cost = ""
        self.form_status = "Active"
        self.is_editor_open = True

    @rx.event
    def open_edit_modal(self, protocol: TreatmentProtocol):
        self.editing_protocol = protocol
        self.form_name = protocol["name"]
        self.form_category = protocol["category"]
        self.form_description = protocol["description"]
        self.form_duration = protocol["duration"]
        self.form_frequency = protocol["frequency"]
        self.form_cost = str(protocol["cost"])
        self.form_status = protocol["status"]
        self.is_editor_open = True

    @rx.event
    def handle_editor_open_change(self, is_open: bool):
        """Handler for radix dialog open state changes."""
        if not is_open:
            self.is_editor_open = False

    @rx.event
    async def save_protocol(self):
        """Save protocol to database."""
        cost_val = 0.0
        try:
            cost_val = float(self.form_cost)
        except ValueError as e:
            logger.exception("Invalid cost value: %s", e)

        if self.editing_protocol:
            # Update existing protocol in DB
            await asyncio.to_thread(
                update_treatment_sync,
                self.editing_protocol["id"],
                name=self.form_name,
                category=self.form_category,
                description=self.form_description,
                duration=self.form_duration,
                frequency=self.form_frequency,
                cost=cost_val,
                status=self.form_status,
            )
            # Update local state
            for p in self.protocols:
                if p["id"] == self.editing_protocol["id"]:
                    p.update(
                        {
                            "name": self.form_name,
                            "category": self.form_category,
                            "description": self.form_description,
                            "duration": self.form_duration,
                            "frequency": self.form_frequency,
                            "cost": cost_val,
                            "status": self.form_status,
                        }
                    )
                    break
        else:
            # Create new protocol in DB
            new_id = f"T{random.randint(1000, 9999)}"
            await asyncio.to_thread(
                create_treatment_sync,
                treatment_id=new_id,
                name=self.form_name,
                category=self.form_category,
                description=self.form_description,
                duration=self.form_duration,
                frequency=self.form_frequency,
                cost=cost_val,
                status=self.form_status,
            )
            new_protocol: TreatmentProtocol = {
                "id": new_id,
                "name": self.form_name,
                "category": self.form_category,
                "description": self.form_description,
                "duration": self.form_duration,
                "frequency": self.form_frequency,
                "cost": cost_val,
                "status": self.form_status,
            }
            self.protocols.append(new_protocol)

        self.is_editor_open = False

    @rx.event
    def open_assign_modal(self, protocol: TreatmentProtocol):
        self.protocol_to_assign = protocol
        self.selected_patient_id_for_assignment = ""
        self.is_assign_open = True

    @rx.event
    def close_assign_modal(self):
        self.is_assign_open = False
        self.protocol_to_assign = None

    @rx.event
    def handle_assign_open_change(self, is_open: bool):
        """Handler for radix dialog open state changes."""
        if not is_open:
            self.is_assign_open = False
            self.protocol_to_assign = None

    @rx.event
    async def confirm_assignment(self):
        """Assign treatment to a patient."""
        from ..patient.state import PatientState

        if self.protocol_to_assign and self.selected_patient_id_for_assignment:
            patient_state = await self.get_state(PatientState)
            patient_state.assign_treatment_to_patient(
                self.selected_patient_id_for_assignment, self.protocol_to_assign
            )
        self.close_assign_modal()

    @rx.event
    def set_form_name(self, val: str):
        self.form_name = val

    @rx.event
    def set_form_category(self, val: str):
        self.form_category = val

    @rx.event
    def set_form_description(self, val: str):
        self.form_description = val

    @rx.event
    def set_form_duration(self, val: str):
        self.form_duration = val

    @rx.event
    def set_form_frequency(self, val: str):
        self.form_frequency = val

    @rx.event
    def set_form_cost(self, val: float):
        self.form_cost = val

    @rx.event
    def set_form_status(self, val: str):
        self.form_status = val

    @rx.event
    def set_selected_patient_id_for_assignment(self, val: str):
        self.selected_patient_id_for_assignment = val


class TreatmentSearchState(rx.State):
    """Patient state for searching and requesting treatments."""

    search_query: str = ""
    category_filter: str = "All"
    selected_protocol: TreatmentProtocol | None = None
    is_details_open: bool = False
    request_note: str = ""
    _treatments: list[TreatmentProtocol] = []
    _loaded: bool = False

    @rx.event
    async def load_treatments(self):
        """Load available treatments from database.

        Note: Requires seeded database. Run: python scripts/load_seed_data.py
        """
        if self._loaded:
            return
        try:
            db_treatments = await asyncio.to_thread(get_treatments_as_protocols_sync)
            self._treatments = db_treatments or []
            if not self._treatments:
                logger.warning(
                    "No treatments found in database. "
                    "Run 'python scripts/load_seed_data.py' to seed data."
                )
            self._loaded = True
        except Exception as e:
            logger.error("Error loading treatments: %s", e)
            self._treatments = []
            self._loaded = True

    @rx.var
    def available_treatments(self) -> list[TreatmentProtocol]:
        """Get all available treatments from database."""
        return self._treatments

    @rx.var
    def filtered_treatments(self) -> list[TreatmentProtocol]:
        items = self.available_treatments
        if self.category_filter != "All":
            items = [p for p in items if p["category"] == self.category_filter]
        if self.search_query:
            q = self.search_query.lower()
            items = [
                p
                for p in items
                if q in p["name"].lower() or q in p["description"].lower()
            ]
        return items

    @rx.var
    def treatments_by_category(self) -> list[TreatmentCategoryGroup]:
        """Group filtered treatments by category for collapsible display.

        Returns:
            List of TreatmentCategoryGroup dicts
        """
        from collections import OrderedDict

        grouped: OrderedDict[str, list[TreatmentProtocol]] = OrderedDict()
        for treatment in self.filtered_treatments:
            cat = treatment["category"]
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(treatment)

        return [
            TreatmentCategoryGroup(
                category=cat, treatments=treatments, count=len(treatments)
            )
            for cat, treatments in grouped.items()
        ]

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_category_filter(self, category: str):
        self.category_filter = category

    @rx.event
    def open_details(self, protocol: TreatmentProtocol):
        self.selected_protocol = protocol
        self.is_details_open = True
        self.request_note = ""

    @rx.event
    def handle_details_open_change(self, is_open: bool):
        """Handler for radix dialog open state changes."""
        if not is_open:
            self.is_details_open = False
            self.selected_protocol = None

    @rx.event
    def set_request_note(self, note: str):
        self.request_note = note

    @rx.event
    def submit_request(self):
        self.is_details_open = False
        return rx.toast(
            f"Request for {self.selected_protocol['name']} submitted successfully.",
            duration=3000,
        )
