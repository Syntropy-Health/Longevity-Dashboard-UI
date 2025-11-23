import reflex as rx
from typing import Optional
from .treatment_state import TreatmentState, TreatmentProtocol


class TreatmentSearchState(rx.State):
    search_query: str = ""
    category_filter: str = "All"
    selected_protocol: Optional[TreatmentProtocol] = None
    is_details_open: bool = False
    request_note: str = ""

    @rx.var
    def available_treatments(self) -> list[TreatmentProtocol]:
        return [
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
    def close_details(self):
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