import reflex as rx
from typing import Optional
from app.models import CohortPatient
from app.enums import PatientStatus
import random


class CohortState(rx.State):
    """
    State for the Admin Patient Cohort management page.
    """

    search_query: str = ""
    status_filter: str = "All"
    selected_patient: Optional[CohortPatient] = None
    is_detail_open: bool = False
    patients: list[CohortPatient] = [
        CohortPatient(
            id="pat_001",
            name="Elena Fisher",
            email="elena.fisher@example.com",
            phone="+1 (555) 123-4567",
            status=PatientStatus.ACTIVE,
            age=36,
            biological_age=34.2,
            active_protocols=["NAD+ Loading Phase", "Cryotherapy"],
            last_visit="2024-02-15",
            longevity_score=92,
            joined_date="2023-08-10",
            biomarkers={"NAD+": 38.2, "hs-CRP": 0.3, "Vitamin D": 65.0},
        ),
        CohortPatient(
            id="pat_002",
            name="Marcus Chen",
            email="marcus.c@example.com",
            phone="+1 (555) 987-6543",
            status=PatientStatus.ONBOARDING,
            age=42,
            biological_age=43.5,
            active_protocols=[],
            last_visit="2024-02-18",
            longevity_score=78,
            joined_date="2024-02-01",
            biomarkers={"NAD+": 22.0, "hs-CRP": 1.5, "Vitamin D": 32.0},
        ),
        CohortPatient(
            id="pat_003",
            name="Sarah Miller",
            email="sarah.m@example.com",
            phone="+1 (555) 456-7890",
            status=PatientStatus.ACTIVE,
            age=29,
            biological_age=26.8,
            active_protocols=["Peptide Therapy"],
            last_visit="2024-02-10",
            longevity_score=95,
            joined_date="2023-05-20",
            biomarkers={"NAD+": 45.0, "hs-CRP": 0.1, "Vitamin D": 55.0},
        ),
        CohortPatient(
            id="pat_004",
            name="James Wilson",
            email="j.wilson@example.com",
            phone="+1 (555) 234-5678",
            status=PatientStatus.INACTIVE,
            age=55,
            biological_age=58.1,
            active_protocols=[],
            last_visit="2023-11-05",
            longevity_score=65,
            joined_date="2023-01-15",
            biomarkers={"NAD+": 18.5, "hs-CRP": 2.8, "Vitamin D": 25.0},
        ),
        CohortPatient(
            id="pat_005",
            name="Olivia Zhang",
            email="olivia.z@example.com",
            phone="+1 (555) 876-5432",
            status=PatientStatus.ACTIVE,
            age=48,
            biological_age=44.2,
            active_protocols=["Hormone Therapy", "Sauna"],
            last_visit="2024-02-14",
            longevity_score=88,
            joined_date="2023-09-01",
            biomarkers={"NAD+": 35.0, "hs-CRP": 0.5, "Vitamin D": 58.0},
        ),
        CohortPatient(
            id="pat_006",
            name="Robert Taylor",
            email="bob.taylor@example.com",
            phone="+1 (555) 345-6789",
            status=PatientStatus.ACTIVE,
            age=62,
            biological_age=55.4,
            active_protocols=["Hyperbaric Oxygen", "IV Therapy"],
            last_visit="2024-02-19",
            longevity_score=91,
            joined_date="2023-03-12",
            biomarkers={"NAD+": 41.0, "hs-CRP": 0.4, "Vitamin D": 62.0},
        ),
    ]

    @rx.var
    def filtered_patients(self) -> list[CohortPatient]:
        filtered = self.patients
        if self.status_filter != "All":
            filtered = [
                p for p in filtered if p.status.lower() == self.status_filter.lower()
            ]
        if self.search_query:
            query = self.search_query.lower()
            filtered = [
                p
                for p in filtered
                if query in p.name.lower() or query in p.email.lower()
            ]
        return filtered

    @rx.var
    def total_patients(self) -> int:
        return len(self.patients)

    @rx.var
    def active_patients_count(self) -> int:
        return len([p for p in self.patients if p.status == PatientStatus.ACTIVE])

    @rx.var
    def avg_longevity_score(self) -> float:
        if not self.patients:
            return 0.0
        total = sum((p.longevity_score for p in self.patients))
        return round(total / len(self.patients), 1)

    @rx.var
    def patients_this_month(self) -> int:
        return 2

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_status_filter(self, status: str):
        self.status_filter = status

    @rx.event
    def open_detail_modal(self, patient: CohortPatient):
        self.selected_patient = patient
        self.is_detail_open = True

    @rx.event
    def close_detail_modal(self):
        self.is_detail_open = False
        self.selected_patient = None

    @rx.event
    def handle_detail_modal_open_change(self, is_open: bool):
        if not is_open:
            self.close_detail_modal()

    @rx.event
    def send_message(self):
        return rx.toast("Message sent to patient.")

    @rx.event
    def edit_patient(self):
        return rx.toast("Edit patient feature coming soon.")