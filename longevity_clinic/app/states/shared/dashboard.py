"""Shared dashboard state management.

This module provides consolidated dashboard state for both admin and patient views.
- HealthDashboardState: Manages health data (food, medications, conditions, symptoms)
- AdminDashboardState: Manages admin-specific state including patient selection
"""

import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import reflex as rx

from ...config import get_logger
from ...data.state_schemas import (
    Condition,
    DataSource,
    FoodEntry,
    MedicationEntry,
    Patient,
    Symptom,
    SymptomEntry,
    SymptomTrend,
)
from ...functions.db_utils import (
    get_food_entries_sync,
    get_medications_sync,
    get_primary_demo_user_id,
    get_symptoms_sync,
    get_user_by_external_id_sync,
)
from ...functions.patients.dashboard import load_all_dashboard_data
from ...functions.patients.patients import load_all_patient_data

logger = get_logger("longevity_clinic.dashboard")

# Default nutrition goals
_DEFAULT_NUTRITION = {
    "total_calories": 0,
    "total_protein": 0,
    "total_carbs": 0,
    "total_fat": 0,
    "calorie_goal": 2000,
    "protein_goal": 150,
    "carbs_goal": 250,
    "fat_goal": 65,
}


def _calculate_nutrition(food_entries: List[FoodEntry]) -> Dict[str, Any]:
    """Calculate nutrition summary from food entries."""
    if not food_entries:
        return _DEFAULT_NUTRITION.copy()
    return {
        "total_calories": sum(f.calories for f in food_entries),
        "total_protein": sum(f.protein for f in food_entries),
        "total_carbs": sum(f.carbs for f in food_entries),
        "total_fat": sum(f.fat for f in food_entries),
        **{k: v for k, v in _DEFAULT_NUTRITION.items() if k.endswith("_goal")},
    }


class HealthDashboardState(rx.State):
    """State management for health dashboard.

    Shared between patient and admin views for displaying health metrics,
    medications, conditions, symptoms, and data sources.
    """

    # Tab and filter states
    active_tab: str = "overview"
    conditions_filter: str = "all"
    symptoms_filter: str = "timeline"
    data_sources_filter: str = "devices"

    # Modal states
    show_medication_modal: bool = False
    show_condition_modal: bool = False
    show_symptom_modal: bool = False
    show_connect_modal: bool = False
    show_add_food_modal: bool = False
    show_suggest_integration_modal: bool = False

    # Form state - suggest integration
    suggested_integration_name: str = ""
    suggested_integration_description: str = ""
    integration_suggestion_submitted: bool = False

    # Form state - add food
    new_food_name: str = ""
    new_food_calories: str = ""
    new_food_protein: str = ""
    new_food_carbs: str = ""
    new_food_fat: str = ""
    new_food_meal_type: str = "snack"

    # Selected items for modals
    selected_medication: Dict[str, Any] = {}
    selected_condition: Dict[str, Any] = {}
    selected_symptom: Dict[str, Any] = {}

    # Settings
    email_notifications: bool = True
    push_notifications: bool = True

    # Data (loaded via load_dashboard_data)
    nutrition_summary: Dict[str, Any] = {}
    food_entries: List[FoodEntry] = []
    medications: List[MedicationEntry] = []
    conditions: List[Condition] = []
    symptoms: List[Symptom] = []
    symptom_logs: List[SymptomEntry] = []
    symptom_trends: List[SymptomTrend] = []
    reminders: List[Dict[str, Any]] = []
    data_sources: List[DataSource] = []

    # Loading state
    is_loading: bool = False
    _data_loaded: bool = False
    _viewing_patient_id: Optional[str] = None

    # =========================================================================
    # Computed Variables
    # =========================================================================

    @rx.var
    def total_medication_adherence(self) -> float:
        """Calculate overall medication adherence."""
        if not self.medications:
            return 0.0
        return sum(m.adherence_rate for m in self.medications) / len(self.medications)

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
    def filtered_conditions(self) -> List[Condition]:
        if self.conditions_filter == "all":
            return self.conditions
        return [c for c in self.conditions if c.status == self.conditions_filter]

    @rx.var
    def connected_sources_count(self) -> int:
        return len([s for s in self.data_sources if s.connected])

    @rx.var
    def filtered_data_sources(self) -> List[DataSource]:
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
    # Data Loading
    # =========================================================================

    @rx.event(background=True)
    async def load_dashboard_data(self):
        """Load dashboard data from database (source of truth)."""
        async with self:
            if self._data_loaded:
                return
            self.is_loading = True

        logger.info("load_dashboard_data: Starting")

        try:
            db_data, static_data = await asyncio.gather(
                self._load_health_entries_from_db(),
                load_all_dashboard_data(patient_id=self._viewing_patient_id),
            )

            async with self:
                self.nutrition_summary = _calculate_nutrition(db_data["food_entries"])
                self.food_entries = db_data["food_entries"]
                self.medications = db_data["medications"]
                self.symptoms = db_data["symptoms"]
                self.conditions = static_data.get("conditions", [])
                self.symptom_logs = static_data.get("symptom_logs", [])
                self.symptom_trends = static_data.get("symptom_trends", [])
                self.reminders = static_data.get("reminders", [])
                self.data_sources = static_data.get("data_sources", [])
                self.is_loading = False
                self._data_loaded = True

            logger.info(
                "load_dashboard_data: Complete (%d meds, %d foods, %d symptoms)",
                len(db_data["medications"]),
                len(db_data["food_entries"]),
                len(db_data["symptoms"]),
            )
        except Exception as e:
            logger.error("load_dashboard_data: Failed - %s", e)
            async with self:
                self.is_loading = False

    async def _load_health_entries_from_db(self) -> Dict[str, Any]:
        """Load health entries from database."""

        def _query():
            user_id = get_primary_demo_user_id()
            if not user_id:
                logger.warning("No primary demo user found")
                return [], [], []
            return (
                get_medications_sync(user_id, limit=50),
                get_food_entries_sync(user_id, limit=50),
                get_symptoms_sync(user_id, limit=50),
            )

        try:
            meds, foods, symptoms = await asyncio.to_thread(_query)
            return {"medications": meds, "food_entries": foods, "symptoms": symptoms}
        except Exception as e:
            logger.error("_load_health_entries_from_db: %s", e)
            return {"medications": [], "food_entries": [], "symptoms": []}

    @rx.event(background=True)
    async def load_patient_health_data(self, patient_id: str):
        """Load dashboard data for a specific patient (admin view).

        Args:
            patient_id: The patient's external_id (e.g., "P001" or "P1")
        """
        logger.info("load_patient_health_data: patient=%s", patient_id)

        async with self:
            self._viewing_patient_id = patient_id
            self.is_loading = True
            self._data_loaded = False

        try:
            # Load static data (conditions, symptom_logs, reminders, data_sources)
            data = await load_all_dashboard_data(patient_id=patient_id)

            # Load health entries from database
            def _load_db_health_data():
                # Convert external_id to user_id
                user = get_user_by_external_id_sync(patient_id)
                if not user:
                    logger.warning(
                        "load_patient_health_data: No user found for external_id=%s",
                        patient_id,
                    )
                    return [], [], []

                user_id = user.id
                logger.debug(
                    "load_patient_health_data: Resolved external_id=%s to user_id=%d",
                    patient_id,
                    user_id,
                )
                return (
                    get_medications_sync(user_id, limit=50),
                    get_food_entries_sync(user_id, limit=50),
                    get_symptoms_sync(user_id, limit=50),
                )

            medications, food_entries, symptoms = await asyncio.to_thread(
                _load_db_health_data
            )

            # Calculate nutrition summary from food entries
            nutrition_summary = (
                _calculate_nutrition(food_entries) if food_entries else {}
            )

            async with self:
                self.nutrition_summary = nutrition_summary
                self.food_entries = food_entries
                self.medications = medications
                self.conditions = data.get("conditions", [])
                self.symptoms = symptoms
                self.symptom_logs = data.get("symptom_logs", [])
                self.symptom_trends = data.get("symptom_trends", [])
                self.reminders = data.get("reminders", [])
                self.data_sources = data.get("data_sources", [])
                self.is_loading = False
                self._data_loaded = True

            logger.info(
                "load_patient_health_data: Loaded %d meds, %d foods, %d symptoms for %s",
                len(medications),
                len(food_entries),
                len(symptoms),
                patient_id,
            )
        except Exception as e:
            logger.error("load_patient_health_data: %s", e)
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def load_health_data_from_db(self):
        """Refresh health data from database (CDC-synced data)."""
        logger.info("load_health_data_from_db: Refreshing")

        try:
            db_data = await self._load_health_entries_from_db()
            if not any(db_data.values()):
                logger.info("load_health_data_from_db: No data in DB")
                return

            async with self:
                if db_data["medications"]:
                    self.medications = db_data["medications"]
                if db_data["food_entries"]:
                    self.food_entries = db_data["food_entries"]
                    self.nutrition_summary = _calculate_nutrition(
                        db_data["food_entries"]
                    )
                if db_data["symptoms"]:
                    self.symptoms = db_data["symptoms"]

            logger.info(
                "load_health_data_from_db: %d meds, %d foods, %d symptoms",
                len(db_data["medications"]),
                len(db_data["food_entries"]),
                len(db_data["symptoms"]),
            )
        except Exception as e:
            logger.error("load_health_data_from_db: %s", e)

    def clear_patient_health_data(self):
        """Clear patient health data (used when deselecting patient)."""
        self._viewing_patient_id = None
        self._data_loaded = False
        self.nutrition_summary = {}
        self.food_entries = []
        self.medications = []
        self.conditions = []
        self.symptoms = []
        self.symptom_logs = []
        self.symptom_trends = []
        self.reminders = []
        self.data_sources = []

    # =========================================================================
    # Setters (Tab, Filter, Settings)
    # =========================================================================

    def set_active_tab(self, tab: str):
        self.active_tab = tab

    def set_conditions_filter(self, value: str):
        self.conditions_filter = value

    def set_symptoms_filter(self, value: str):
        self.symptoms_filter = value

    def set_data_sources_filter(self, value: str):
        self.data_sources_filter = value

    def toggle_email_notifications(self):
        self.email_notifications = not self.email_notifications

    def toggle_push_notifications(self):
        self.push_notifications = not self.push_notifications

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
    # Modal Handlers (Medication, Condition, Symptom)
    # =========================================================================

    def open_medication_modal(self, medication: Dict[str, Any]):
        self.selected_medication = medication
        self.show_medication_modal = True

    def close_medication_modal(self):
        self.show_medication_modal = False
        self.selected_medication = {}

    def set_show_medication_modal(self, value: bool):
        self.show_medication_modal = value

    @rx.event
    async def log_dose(self, medication_id: str):
        self.show_medication_modal = False

    def open_condition_modal(self, condition: Dict[str, Any]):
        self.selected_condition = condition
        self.show_condition_modal = True

    def close_condition_modal(self):
        self.show_condition_modal = False
        self.selected_condition = {}

    def set_show_condition_modal(self, value: bool):
        self.show_condition_modal = value

    def open_symptom_modal(self, symptom: Dict[str, Any]):
        self.selected_symptom = symptom
        self.show_symptom_modal = True

    def close_symptom_modal(self):
        self.show_symptom_modal = False
        self.selected_symptom = {}

    def set_show_symptom_modal(self, value: bool):
        self.show_symptom_modal = value

    @rx.event
    async def save_symptom_log(self):
        if self.selected_symptom:
            new_log = SymptomEntry(
                id=f"sym_{uuid.uuid4().hex[:8]}",
                symptom_name=self.selected_symptom.get("name", "Unknown"),
                severity=5,
                notes="",
                timestamp=datetime.now().strftime("Today, %I:%M %p"),
            )
            self.symptom_logs = [new_log, *self.symptom_logs]
        self.show_symptom_modal = False

    # =========================================================================
    # Modal Handlers (Connect, Add Food, Suggest Integration)
    # =========================================================================

    def open_connect_modal(self):
        self.show_connect_modal = True

    def close_connect_modal(self):
        self.show_connect_modal = False

    def set_show_connect_modal(self, value: bool):
        self.show_connect_modal = value

    def open_add_food_modal(self):
        self.show_add_food_modal = True
        self.new_food_name = ""
        self.new_food_calories = ""
        self.new_food_protein = ""
        self.new_food_carbs = ""
        self.new_food_fat = ""
        self.new_food_meal_type = "snack"

    def close_add_food_modal(self):
        self.show_add_food_modal = False

    def set_show_add_food_modal(self, value: bool):
        self.show_add_food_modal = value

    def set_new_food_name(self, value: str):
        self.new_food_name = value

    def set_new_food_calories(self, value: float):
        self.new_food_calories = str(value) if value else ""

    def set_new_food_protein(self, value: float):
        self.new_food_protein = str(value) if value else ""

    def set_new_food_carbs(self, value: float):
        self.new_food_carbs = str(value) if value else ""

    def set_new_food_fat(self, value: float):
        self.new_food_fat = str(value) if value else ""

    def set_new_food_meal_type(self, value: str):
        self.new_food_meal_type = value

    def save_food_entry(self):
        """Save a new food entry."""
        new_entry = FoodEntry(
            id=str(uuid.uuid4())[:8],
            name=self.new_food_name,
            calories=int(self.new_food_calories) if self.new_food_calories else 0,
            protein=float(self.new_food_protein) if self.new_food_protein else 0.0,
            carbs=float(self.new_food_carbs) if self.new_food_carbs else 0.0,
            fat=float(self.new_food_fat) if self.new_food_fat else 0.0,
            time=datetime.now().strftime("%I:%M %p"),
            meal_type=self.new_food_meal_type,
        )
        self.food_entries = [*self.food_entries, new_entry]
        self.nutrition_summary = {
            **self.nutrition_summary,
            "total_calories": self.nutrition_summary.get("total_calories", 0)
            + new_entry.calories,
            "total_protein": self.nutrition_summary.get("total_protein", 0)
            + new_entry.protein,
            "total_carbs": self.nutrition_summary.get("total_carbs", 0)
            + new_entry.carbs,
            "total_fat": self.nutrition_summary.get("total_fat", 0) + new_entry.fat,
        }
        self.show_add_food_modal = False

    def open_suggest_integration_modal(self):
        self.show_suggest_integration_modal = True
        self.suggested_integration_name = ""
        self.suggested_integration_description = ""
        self.integration_suggestion_submitted = False

    def close_suggest_integration_modal(self):
        self.show_suggest_integration_modal = False

    def set_show_suggest_integration_modal(self, value: bool):
        self.show_suggest_integration_modal = value

    def set_suggested_integration_name(self, value: str):
        self.suggested_integration_name = value

    def set_suggested_integration_description(self, value: str):
        self.suggested_integration_description = value

    def submit_integration_suggestion(self):
        self.integration_suggestion_submitted = True


class AdminDashboardState(rx.State):
    """State management for admin dashboard patient selection."""

    active_tab: str = "overview"
    patients: List[Patient] = []
    recently_active_patients: List[Patient] = []
    patient_search_query: str = ""
    selected_patient_id: Optional[str] = None
    selected_patient: Optional[Patient] = None
    is_loading: bool = False
    _patients_loaded: bool = False
    _recent_patients_loaded: bool = False

    @rx.var
    def has_selected_patient(self) -> bool:
        return self.selected_patient_id is not None

    @rx.var
    def filtered_patients(self) -> List[Patient]:
        if not self.patient_search_query:
            return self.patients[:20]
        query = self.patient_search_query.lower()
        return [
            p
            for p in self.patients
            if query in p["full_name"].lower() or query in p["email"].lower()
        ][:20]

    @rx.var
    def selected_patient_name(self) -> str:
        return self.selected_patient["full_name"] if self.selected_patient else ""

    def set_tab(self, tab: str):
        self.active_tab = tab

    @rx.event(background=True)
    async def load_patients_for_selection(self):
        """Load patients list for selection dropdown."""
        async with self:
            if self._patients_loaded:
                return
            self.is_loading = True

        try:
            data = await load_all_patient_data()
            async with self:
                self.patients = data["patients"]
                self.is_loading = False
                self._patients_loaded = True
            logger.info(
                "load_patients_for_selection: %d patients", len(data["patients"])
            )
        except Exception as e:
            logger.error("load_patients_for_selection: %s", e)
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def load_recently_active_patients(self):
        """Load recently active patients based on check-in activity.

        Falls back to fetching the first few patients if no recent activity found.
        """
        from ...config import current_config
        from ...functions.db_utils import (
            get_recently_active_patients_sync,
            get_all_patients_sync,
        )

        async with self:
            if self._recent_patients_loaded:
                return

        try:

            def _query():
                # First try to get recently active patients
                active = get_recently_active_patients_sync(
                    limit=current_config.quick_access_patient_count
                )
                if active:
                    return active

                # Fallback: get first few patients from database
                logger.info(
                    "No recently active patients, fetching first %d patients",
                    current_config.quick_access_patient_count,
                )
                return get_all_patients_sync()[
                    : current_config.quick_access_patient_count
                ]

            users = await asyncio.to_thread(_query)

            # Convert User models to Patient TypedDict format
            recent_patients = []
            for user in users:
                recent_patients.append(
                    {
                        "id": str(user.external_id),
                        "full_name": user.name,
                        "email": user.email,
                        "phone": user.phone or "",
                        "age": 0,  # Not stored in User model
                        "gender": "",
                        "last_visit": (
                            user.updated_at.strftime("%Y-%m-%d")
                            if user.updated_at
                            else ""
                        ),
                        "status": "active",
                        "biomarker_score": 0,
                        "medical_history": "",
                        "next_appointment": "",
                        "assigned_treatments": [],
                    }
                )

            async with self:
                self.recently_active_patients = recent_patients
                self._recent_patients_loaded = True

            logger.info("Loaded %d recently active patients", len(recent_patients))
        except Exception as e:
            logger.error("load_recently_active_patients: %s", e)
            async with self:
                self.recently_active_patients = []

    def set_patient_search_query(self, query: str):
        self.patient_search_query = query

    def select_patient(self, patient: Patient):
        self.selected_patient_id = patient["id"]
        self.selected_patient = patient
        self.patient_search_query = ""
        logger.info("select_patient: %s", patient["id"])

    def select_patient_by_id(self, patient_id: str):
        """Select patient by ID (for use with foreach/lambda)."""
        for p in self.patients:
            if p["id"] == patient_id:
                self.selected_patient_id = patient_id
                self.selected_patient = p
                self.patient_search_query = ""
                logger.info("select_patient_by_id: %s", patient_id)
                return
        logger.warning("select_patient_by_id: patient %s not found", patient_id)

    def clear_selected_patient(self):
        self.selected_patient_id = None
        self.selected_patient = None
        logger.info("clear_selected_patient")
