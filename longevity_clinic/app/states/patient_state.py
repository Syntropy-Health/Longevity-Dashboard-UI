import reflex as rx
from typing import Optional
import random
from datetime import datetime, timedelta

from ..config import get_logger
from ..data.state_schemas import Patient
from .functions.patients.patients import load_all_patient_data

logger = get_logger("longevity_clinic.patient_state")


class PatientState(rx.State):
    """State for patient management (CRUD operations).

    Data is loaded via load_patients() which respects the IS_DEMO
    environment variable.
    """

    patients: list[Patient] = []
    search_query: str = ""
    status_filter: str = "All"
    sort_key: str = "name"
    is_add_patient_open: bool = False
    is_view_patient_open: bool = False
    selected_patient: Optional[Patient] = None
    new_patient_name: str = ""
    new_patient_email: str = ""
    new_patient_phone: str = ""
    new_patient_age: str = ""
    new_patient_gender: str = ""
    new_patient_history: str = ""
    trend_data: list[dict] = []
    treatment_data: list[dict] = []
    biomarker_data: list[dict] = []

    # Loading state
    is_loading: bool = False
    _data_loaded: bool = False

    @rx.var
    def filtered_patients(self) -> list[Patient]:
        patients = self.patients
        if self.status_filter != "All":
            patients = [
                p for p in patients if p["status"].lower() == self.status_filter.lower()
            ]
        if self.search_query:
            query = self.search_query.lower()
            patients = [
                p
                for p in patients
                if query in p["full_name"].lower() or query in p["email"].lower()
            ]
        if self.sort_key == "name":
            patients = sorted(patients, key=lambda x: x["full_name"])
        elif self.sort_key == "recent":
            patients = sorted(patients, key=lambda x: x["last_visit"], reverse=True)
        elif self.sort_key == "score":
            patients = sorted(
                patients, key=lambda x: x["biomarker_score"], reverse=True
            )
        return patients

    @rx.event(background=True)
    async def load_patients(self):
        """Load patient data.

        Respects IS_DEMO env var: when True, returns demo data;
        when False, calls the API.
        """
        # Prevent duplicate loads
        async with self:
            if self._data_loaded:
                logger.debug("load_patients: Data already loaded, skipping")
                return
            self.is_loading = True

        logger.info("load_patients: Starting")

        try:
            # Fetch data using extracted function (respects IS_DEMO config)
            data = await load_all_patient_data()

            async with self:
                self.patients = data["patients"]
                self.trend_data = data["trend_data"]
                self.treatment_data = data["treatment_data"]
                self.biomarker_data = data["biomarker_data"]
                self.is_loading = False
                self._data_loaded = True

            logger.info("load_patients: Complete (%d patients)", len(data["patients"]))
        except Exception as e:
            logger.error("load_patients: Failed - %s", e)
            async with self:
                self.is_loading = False

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_status_filter(self, status: str):
        self.status_filter = status

    @rx.event
    def set_sort_key(self, key: str):
        self.sort_key = key

    @rx.event
    def open_add_patient(self):
        self.is_add_patient_open = True

    @rx.event
    def close_add_patient(self):
        self.is_add_patient_open = False
        self.new_patient_name = ""
        self.new_patient_email = ""
        self.new_patient_phone = ""
        self.new_patient_age = ""
        self.new_patient_gender = ""
        self.new_patient_history = ""

    @rx.event
    def handle_add_patient_open_change(self, is_open: bool):
        """Handler for radix dialog open state changes."""
        if not is_open:
            self.close_add_patient()

    @rx.event
    def open_view_patient(self, patient: Patient):
        self.selected_patient = patient
        self.is_view_patient_open = True

    @rx.event
    def close_view_patient(self):
        self.is_view_patient_open = False
        self.selected_patient = None

    @rx.event
    def handle_view_patient_open_change(self, is_open: bool):
        """Handler for radix dialog open state changes."""
        if not is_open:
            self.is_view_patient_open = False
            self.selected_patient = None

    @rx.event
    def add_patient(self):
        new_id = f"P{random.randint(100, 999)}"
        new_patient: Patient = {
            "id": new_id,
            "full_name": self.new_patient_name,
            "email": self.new_patient_email,
            "phone": self.new_patient_phone,
            "age": int(self.new_patient_age) if self.new_patient_age.isdigit() else 0,
            "gender": self.new_patient_gender,
            "last_visit": datetime.now().strftime("%Y-%m-%d"),
            "status": "Onboarding",
            "biomarker_score": 0,
            "medical_history": self.new_patient_history,
            "next_appointment": (datetime.now() + timedelta(days=7)).strftime(
                "%Y-%m-%d"
            ),
            "assigned_treatments": [],
        }
        self.patients.append(new_patient)
        self.close_add_patient()

    @rx.event
    def set_new_patient_name(self, value: str):
        self.new_patient_name = value

    @rx.event
    def set_new_patient_email(self, value: str):
        self.new_patient_email = value

    @rx.event
    def set_new_patient_phone(self, value: str):
        self.new_patient_phone = value

    @rx.event
    def set_new_patient_age(self, value: float):
        self.new_patient_age = value

    @rx.event
    def set_new_patient_gender(self, value: str):
        self.new_patient_gender = value

    @rx.event
    def set_new_patient_history(self, value: str):
        self.new_patient_history = value

    @rx.event
    def assign_treatment_to_patient(self, patient_id: str, treatment: dict):
        for p in self.patients:
            if p["id"] == patient_id:
                if not any(
                    (
                        t["id"] == treatment["id"]
                        for t in p.get("assigned_treatments", [])
                    )
                ):
                    p.setdefault("assigned_treatments", []).append(treatment)
                break

    @rx.event
    def remove_treatment_from_patient(self, patient_id: str, treatment_id: str):
        for p in self.patients:
            if p["id"] == patient_id:
                p["assigned_treatments"] = [
                    t
                    for t in p.get("assigned_treatments", [])
                    if t["id"] != treatment_id
                ]
                break
