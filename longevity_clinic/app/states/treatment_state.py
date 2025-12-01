import logging
import random
from typing import Optional, TypedDict

import reflex as rx

from .patient_state import PatientState
from ..data import TREATMENT_CATEGORIES, TREATMENT_FREQUENCIES, TREATMENT_STATUSES


class TreatmentProtocol(TypedDict):
    id: str
    name: str
    category: str
    description: str
    duration: str
    frequency: str
    cost: float
    status: str


class TreatmentState(rx.State):
    protocols: list[TreatmentProtocol] = [
        {
            "id": "T001",
            "name": "Vitamin C IV Mega-Dose",
            "category": "IV Therapy",
            "description": "High-dose Vitamin C infusion to boost immune system and antioxidant levels.",
            "duration": "60 mins",
            "frequency": "Weekly",
            "cost": 150.0,
            "status": "Active",
        },
        {
            "id": "T002",
            "name": "Whole Body Cryotherapy",
            "category": "Cryotherapy",
            "description": "Exposure to ultra-low temperatures to reduce inflammation and improve recovery.",
            "duration": "3 mins",
            "frequency": "Daily",
            "cost": 45.0,
            "status": "Active",
        },
        {
            "id": "T003",
            "name": "Nad+ Optimization",
            "category": "Supplements",
            "description": "Supplement protocol to enhance cellular energy and DNA repair.",
            "duration": "N/A",
            "frequency": "Daily",
            "cost": 120.0,
            "status": "Active",
        },
        {
            "id": "T004",
            "name": "Testosterone Replacement",
            "category": "Hormone Therapy",
            "description": "Bio-identical hormone replacement for optimal levels.",
            "duration": "15 mins",
            "frequency": "Monthly",
            "cost": 200.0,
            "status": "Active",
        },
        {
            "id": "T005",
            "name": "Deep Tissue Massage",
            "category": "Spa Services",
            "description": "Therapeutic massage focusing on realigning deeper layers of muscles.",
            "duration": "60 mins",
            "frequency": "As-needed",
            "cost": 90.0,
            "status": "Active",
        },
    ]
    search_query: str = ""
    category_filter: str = "All"
    is_editor_open: bool = False
    editing_protocol: Optional[TreatmentProtocol] = None
    form_name: str = ""
    form_category: str = ""
    form_description: str = ""
    form_duration: str = ""
    form_frequency: str = ""
    form_cost: str = ""
    form_status: str = "Active"
    is_assign_open: bool = False
    protocol_to_assign: Optional[TreatmentProtocol] = None
    selected_patient_id_for_assignment: str = ""

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
    def close_editor(self):
        self.is_editor_open = False

    @rx.event
    def handle_editor_open_change(self, is_open: bool):
        """Handler for radix dialog open state changes."""
        if not is_open:
            self.is_editor_open = False

    @rx.event
    def save_protocol(self):
        cost_val = 0.0
        try:
            cost_val = float(self.form_cost)
        except ValueError as e:
            logging.exception(f"Error: {e}")
        if self.editing_protocol:
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
            new_id = f"T{random.randint(1000, 9999)}"
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