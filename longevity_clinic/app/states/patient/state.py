import asyncio
import random
from datetime import datetime, timedelta

import reflex as rx

from ...config import current_config, get_logger
from ...data.schemas.state import Patient
from ...functions.patients.patients import load_all_patient_data

logger = get_logger("longevity_clinic.patient_state")


class PatientState(rx.State):
    """Unified state for patient management (CRUD + selection + health views).

    Single source of truth for patient data across admin dashboard:
    - Patient Management tab: CRUD, filtering, sorting
    - Patient Health tab: selection, recently active, health data

    All data is loaded from the database.
    Seed data with: python scripts/load_seed_data.py
    """

    # Patient data
    patients: list[Patient] = []
    recently_active_patients: list[Patient] = []

    # Search & filtering (Patient Management)
    search_query: str = ""
    status_filter: str = "All"
    sort_key: str = "name"

    # Selected patient (Patient Health tab)
    selected_patient_id: str | None = None
    selected_patient: Patient | None = None

    # Add/view patient dialogs
    is_add_patient_open: bool = False
    is_view_patient_open: bool = False
    new_patient_name: str = ""
    new_patient_email: str = ""
    new_patient_phone: str = ""
    new_patient_age: str = ""
    new_patient_gender: str = ""
    new_patient_history: str = ""

    # Chart data (for analytics)
    trend_data: list[dict] = []
    treatment_data: list[dict] = []
    biomarker_data: list[dict] = []

    # Loading state - starts True so UI shows loading until data arrives
    is_loading: bool = True
    _data_loaded: bool = False
    _recent_loaded: bool = False

    # --- Computed Variables ---

    @rx.var
    def patient_count(self) -> int:
        """Total number of patients loaded."""
        return len(self.patients)

    @rx.var
    def has_selected_patient(self) -> bool:
        """Check if a patient is selected for health view."""
        return self.selected_patient_id is not None

    @rx.var
    def filtered_patients(self) -> list[Patient]:
        """Get filtered and sorted patients for Patient Management view."""
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

    @rx.var
    def search_filtered_patients(self) -> list[Patient]:
        """Get patients filtered by search query only (for Patient Health dropdown)."""
        if not self.search_query:
            return self.patients[:20]
        query = self.search_query.lower()
        return [
            p
            for p in self.patients
            if query in p["full_name"].lower() or query in p["email"].lower()
        ][:20]

    # --- Data Loading ---

    @rx.event(background=True)
    async def load_patients(self):
        """Load patient data from database.

        Note: Requires seeded database. Run: python scripts/load_seed_data.py
        """
        async with self:
            if self._data_loaded:
                logger.debug("load_patients: Already loaded, skipping")
                return
            self.is_loading = True

        logger.info("load_patients: Starting database fetch")

        try:
            data = await load_all_patient_data()
            patient_count = len(data["patients"])

            async with self:
                self.patients = data["patients"]
                self.trend_data = data["trend_data"]
                self.treatment_data = data["treatment_data"]
                self.biomarker_data = data["biomarker_data"]
                self.is_loading = False
                self._data_loaded = True

            logger.info("load_patients: Loaded %d patients from DB", patient_count)
            if patient_count == 0:
                logger.warning(
                    "No patients found. Run 'python scripts/load_seed_data.py' to seed."
                )
        except Exception as e:
            logger.error("load_patients: Failed - %s", e)
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def load_recently_active_patients(self):
        """Load recently active patients based on check-in activity.

        Used for "Recently Active" quick access in Patient Health tab.
        Falls back to all patients if no recent activity found.
        """
        from ...functions.db_utils import (
            get_all_patients_sync,
            get_recently_active_patients_sync,
        )

        async with self:
            if self._recent_loaded:
                logger.debug("load_recently_active_patients: Already loaded, skipping")
                return

        logger.info("load_recently_active_patients: Fetching from DB")

        try:
            limit = current_config.quick_access_patient_count

            def _query():
                active = get_recently_active_patients_sync(limit=limit)
                if active:
                    logger.info("Found %d recently active patients", len(active))
                    return active
                logger.info("No check-in activity, falling back to all patients")
                return get_all_patients_sync()[:limit]

            users = await asyncio.to_thread(_query)

            recent_patients = []
            for user in users:
                recent_patients.append(
                    {
                        "id": (
                            str(user.external_id) if user.external_id else f"P{user.id}"
                        ),
                        "full_name": user.name,
                        "email": user.email or "",
                        "phone": user.phone or "",
                        "age": 0,
                        "gender": "",
                        "last_visit": (
                            user.updated_at.strftime("%Y-%m-%d")
                            if user.updated_at
                            else ""
                        ),
                        "status": "Active",
                        "biomarker_score": 0,
                        "medical_history": "",
                        "next_appointment": "",
                        "assigned_treatments": [],
                    }
                )

            async with self:
                self.recently_active_patients = recent_patients
                self._recent_loaded = True

            logger.info(
                "load_recently_active_patients: Loaded %d patients",
                len(recent_patients),
            )
        except Exception as e:
            logger.error("load_recently_active_patients: Failed - %s", e)
            async with self:
                self.recently_active_patients = []

    # --- Patient Selection (for Health tab) ---

    @rx.event
    def select_patient_by_id(self, patient_id: str):
        """Select patient by ID for health data viewing."""
        for p in self.patients:
            if p["id"] == patient_id:
                self.selected_patient_id = patient_id
                self.selected_patient = p
                self.search_query = ""  # Clear search on selection
                logger.info("select_patient_by_id: Selected %s", patient_id)
                return
        # Check recently_active if not found in main list
        for p in self.recently_active_patients:
            if p["id"] == patient_id:
                self.selected_patient_id = patient_id
                self.selected_patient = p
                self.search_query = ""
                logger.info(
                    "select_patient_by_id: Selected from recent - %s", patient_id
                )
                return
        logger.warning("select_patient_by_id: Patient %s not found", patient_id)

    @rx.event
    def clear_selected_patient(self):
        """Clear patient selection."""
        self.selected_patient_id = None
        self.selected_patient = None
        logger.info("clear_selected_patient: Cleared selection")

    # --- Search & Filter Handlers ---

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
                    t["id"] == treatment["id"] for t in p.get("assigned_treatments", [])
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
