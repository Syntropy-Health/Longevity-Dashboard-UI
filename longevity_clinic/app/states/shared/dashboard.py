"""Shared dashboard state management.

This module provides consolidated dashboard state for both admin and patient views.
- HealthDashboardState: Manages health data (food, medications, conditions, symptoms)
- AdminDashboardState: Manages admin-specific state including patient selection
"""

import asyncio
import uuid
from datetime import datetime
from typing import Any

import reflex as rx

from ...config import get_logger
from ...data.schemas.llm import (
    Condition,
    DataSource,
    FoodEntryModel as FoodEntry,
    MedicationEntryModel as MedicationEntry,
    PatientTreatmentModel as MedicationSubscription,  # Alias for backwards compat
    Symptom,
    SymptomEntryModel as SymptomEntry,
    SymptomTrend,
)
from ...functions.db_utils import (
    get_food_entries_sync,
    get_medication_entries_sync,
    get_medication_subscriptions_sync,
    get_symptoms_sync,
    get_user_by_external_id_sync,
)
from ...functions.patients.dashboard import load_all_dashboard_data
from ..auth.base import AuthState

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


def _calculate_nutrition(food_entries: list[FoodEntry]) -> dict[str, Any]:
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

    Data Source:
    ============
    Health entries (medications, food, symptoms) are fetched from database tables
    populated by CheckinState via two pathways:

    1. Patient Check-ins (voice/text):
       save_checkin_and_log_health() → save_health_entries_sync()
       → MedicationEntry, FoodLogEntry, SymptomEntry tables

    2. Call Log CDC Pipeline:
       start_calls_to_checkin_sync_loop() → update_call_log_metrics()
       → MedicationEntry, FoodLogEntry, SymptomEntry tables

    Data Fetch (via load_dashboard_data):
    - get_medications_sync(user_id) → self.medications (list[MedicationEntry])
    - get_food_entries_sync(user_id) → self.food_entries (list[FoodEntry])
    - get_symptoms_sync(user_id) → self.symptoms (list[Symptom])

    Refresh:
    - load_health_data_from_db() can be called to refresh from database
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
    selected_medication: dict[str, Any] = {}
    selected_medication_subscription: dict[str, Any] = {}
    selected_condition: dict[str, Any] = {}
    selected_symptom: dict[str, Any] = {}

    # Settings
    email_notifications: bool = True
    push_notifications: bool = True

    # Data (loaded via load_dashboard_data)
    nutrition_summary: dict[str, Any] = {}
    food_entries: list[FoodEntry] = []
    medication_entries: list[MedicationEntry] = []  # What patient actually took
    medication_subscriptions: list[MedicationSubscription] = []  # Prescribed meds
    conditions: list[Condition] = []
    symptoms: list[Symptom] = []
    symptom_logs: list[SymptomEntry] = []
    symptom_trends: list[SymptomTrend] = []
    reminders: list[dict[str, Any]] = []
    data_sources: list[DataSource] = []

    # Loading state
    is_loading: bool = False
    _data_loaded: bool = False
    _viewing_patient_id: str | None = None
    _current_user_id: int | None = None  # Cached from AuthState

    # =========================================================================
    # Pagination State
    # =========================================================================
    # Page size constants
    _MED_LOGS_PAGE_SIZE: int = 5
    _MED_SUBS_PAGE_SIZE: int = 5
    _FOOD_PAGE_SIZE: int = 6
    _CONDITIONS_PAGE_SIZE: int = 5
    _SYMPTOMS_PAGE_SIZE: int = 5
    _SYMPTOM_LOGS_PAGE_SIZE: int = 8
    _REMINDERS_PAGE_SIZE: int = 6
    _TRENDS_PAGE_SIZE: int = 5
    _DATA_SOURCES_PAGE_SIZE: int = 6

    # Current page numbers (1-indexed)
    medication_entries_page: int = 1
    medication_subscriptions_page: int = 1
    food_entries_page: int = 1
    conditions_page: int = 1
    symptoms_page: int = 1
    symptom_logs_page: int = 1
    reminders_page: int = 1
    symptom_trends_page: int = 1
    data_sources_page: int = 1

    # =========================================================================
    # Computed Variables
    # =========================================================================

    @rx.var
    def total_medication_adherence(self) -> float:
        """Calculate overall medication adherence from subscriptions."""
        if not self.medication_subscriptions:
            return 0.0
        return sum(m.adherence_rate for m in self.medication_subscriptions) / len(
            self.medication_subscriptions
        )

    @rx.var
    def active_subscriptions_count(self) -> int:
        """Count of active medication subscriptions."""
        return len([s for s in self.medication_subscriptions if s.status == "active"])

    @rx.var
    def medication_entries_count(self) -> int:
        """Count of Medication Entries."""
        return len(self.medication_entries)

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

    @rx.var
    def connected_sources_count(self) -> int:
        return len([s for s in self.data_sources if s.connected])

    @rx.var
    def filtered_data_sources(self) -> list[DataSource]:
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
    # Pagination Computed Variables - Medication Entries (What was taken)
    # =========================================================================

    @rx.var
    def medication_entries_paginated(self) -> list[MedicationEntry]:
        """Paginated slice of Medication Entries."""
        start = (self.medication_entries_page - 1) * self._MED_LOGS_PAGE_SIZE
        end = start + self._MED_LOGS_PAGE_SIZE
        return self.medication_entries[start:end]

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
    # Pagination Computed Variables - Medication Subscriptions (Prescriptions)
    # =========================================================================

    @rx.var
    def medication_subscriptions_paginated(self) -> list[MedicationSubscription]:
        """Paginated slice of medication subscriptions."""
        start = (self.medication_subscriptions_page - 1) * self._MED_SUBS_PAGE_SIZE
        end = start + self._MED_SUBS_PAGE_SIZE
        return self.medication_subscriptions[start:end]

    @rx.var
    def medication_subscriptions_total_pages(self) -> int:
        return max(
            1,
            (len(self.medication_subscriptions) + self._MED_SUBS_PAGE_SIZE - 1)
            // self._MED_SUBS_PAGE_SIZE,
        )

    @rx.var
    def medication_subscriptions_has_previous(self) -> bool:
        return self.medication_subscriptions_page > 1

    @rx.var
    def medication_subscriptions_has_next(self) -> bool:
        return (
            self.medication_subscriptions_page
            < self.medication_subscriptions_total_pages
        )

    @rx.var
    def medication_subscriptions_page_info(self) -> str:
        return f"Page {self.medication_subscriptions_page} of {self.medication_subscriptions_total_pages}"

    @rx.var
    def medication_subscriptions_showing_info(self) -> str:
        total = len(self.medication_subscriptions)
        if total == 0:
            return "No prescriptions"
        start = (self.medication_subscriptions_page - 1) * self._MED_SUBS_PAGE_SIZE + 1
        end = min(self.medication_subscriptions_page * self._MED_SUBS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Pagination Computed Variables - Food Entries
    # =========================================================================

    @rx.var
    def food_entries_paginated(self) -> list[FoodEntry]:
        """Paginated slice of food entries."""
        start = (self.food_entries_page - 1) * self._FOOD_PAGE_SIZE
        end = start + self._FOOD_PAGE_SIZE
        return self.food_entries[start:end]

    @rx.var
    def food_entries_total_pages(self) -> int:
        return max(
            1,
            (len(self.food_entries) + self._FOOD_PAGE_SIZE - 1) // self._FOOD_PAGE_SIZE,
        )

    @rx.var
    def food_entries_has_previous(self) -> bool:
        return self.food_entries_page > 1

    @rx.var
    def food_entries_has_next(self) -> bool:
        return self.food_entries_page < self.food_entries_total_pages

    @rx.var
    def food_entries_page_info(self) -> str:
        return f"Page {self.food_entries_page} of {self.food_entries_total_pages}"

    @rx.var
    def food_entries_showing_info(self) -> str:
        total = len(self.food_entries)
        if total == 0:
            return "No food entries"
        start = (self.food_entries_page - 1) * self._FOOD_PAGE_SIZE + 1
        end = min(self.food_entries_page * self._FOOD_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Pagination Computed Variables - Conditions
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
    # Pagination Computed Variables - Symptoms
    # =========================================================================

    @rx.var
    def symptoms_paginated(self) -> list[Symptom]:
        """Paginated slice of symptoms."""
        start = (self.symptoms_page - 1) * self._SYMPTOMS_PAGE_SIZE
        end = start + self._SYMPTOMS_PAGE_SIZE
        return self.symptoms[start:end]

    @rx.var
    def symptoms_total_pages(self) -> int:
        return max(
            1,
            (len(self.symptoms) + self._SYMPTOMS_PAGE_SIZE - 1)
            // self._SYMPTOMS_PAGE_SIZE,
        )

    @rx.var
    def symptoms_has_previous(self) -> bool:
        return self.symptoms_page > 1

    @rx.var
    def symptoms_has_next(self) -> bool:
        return self.symptoms_page < self.symptoms_total_pages

    @rx.var
    def symptoms_page_info(self) -> str:
        return f"Page {self.symptoms_page} of {self.symptoms_total_pages}"

    @rx.var
    def symptoms_showing_info(self) -> str:
        total = len(self.symptoms)
        if total == 0:
            return "No symptoms"
        start = (self.symptoms_page - 1) * self._SYMPTOMS_PAGE_SIZE + 1
        end = min(self.symptoms_page * self._SYMPTOMS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Pagination Computed Variables - Symptom Logs
    # =========================================================================

    @rx.var
    def symptom_logs_paginated(self) -> list[SymptomEntry]:
        """Paginated slice of symptom logs."""
        start = (self.symptom_logs_page - 1) * self._SYMPTOM_LOGS_PAGE_SIZE
        end = start + self._SYMPTOM_LOGS_PAGE_SIZE
        return self.symptom_logs[start:end]

    @rx.var
    def symptom_logs_total_pages(self) -> int:
        return max(
            1,
            (len(self.symptom_logs) + self._SYMPTOM_LOGS_PAGE_SIZE - 1)
            // self._SYMPTOM_LOGS_PAGE_SIZE,
        )

    @rx.var
    def symptom_logs_has_previous(self) -> bool:
        return self.symptom_logs_page > 1

    @rx.var
    def symptom_logs_has_next(self) -> bool:
        return self.symptom_logs_page < self.symptom_logs_total_pages

    @rx.var
    def symptom_logs_page_info(self) -> str:
        return f"Page {self.symptom_logs_page} of {self.symptom_logs_total_pages}"

    @rx.var
    def symptom_logs_showing_info(self) -> str:
        total = len(self.symptom_logs)
        if total == 0:
            return "No symptom logs"
        start = (self.symptom_logs_page - 1) * self._SYMPTOM_LOGS_PAGE_SIZE + 1
        end = min(self.symptom_logs_page * self._SYMPTOM_LOGS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Pagination Computed Variables - Reminders
    # =========================================================================

    @rx.var
    def reminders_paginated(self) -> list[dict[str, Any]]:
        """Paginated slice of reminders."""
        start = (self.reminders_page - 1) * self._REMINDERS_PAGE_SIZE
        end = start + self._REMINDERS_PAGE_SIZE
        return self.reminders[start:end]

    @rx.var
    def reminders_total_pages(self) -> int:
        return max(
            1,
            (len(self.reminders) + self._REMINDERS_PAGE_SIZE - 1)
            // self._REMINDERS_PAGE_SIZE,
        )

    @rx.var
    def reminders_has_previous(self) -> bool:
        return self.reminders_page > 1

    @rx.var
    def reminders_has_next(self) -> bool:
        return self.reminders_page < self.reminders_total_pages

    @rx.var
    def reminders_page_info(self) -> str:
        return f"Page {self.reminders_page} of {self.reminders_total_pages}"

    @rx.var
    def reminders_showing_info(self) -> str:
        total = len(self.reminders)
        if total == 0:
            return "No reminders"
        start = (self.reminders_page - 1) * self._REMINDERS_PAGE_SIZE + 1
        end = min(self.reminders_page * self._REMINDERS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Pagination Computed Variables - Symptom Trends
    # =========================================================================

    @rx.var
    def symptom_trends_paginated(self) -> list[SymptomTrend]:
        """Paginated slice of symptom trends."""
        start = (self.symptom_trends_page - 1) * self._TRENDS_PAGE_SIZE
        end = start + self._TRENDS_PAGE_SIZE
        return self.symptom_trends[start:end]

    @rx.var
    def symptom_trends_total_pages(self) -> int:
        return max(
            1,
            (len(self.symptom_trends) + self._TRENDS_PAGE_SIZE - 1)
            // self._TRENDS_PAGE_SIZE,
        )

    @rx.var
    def symptom_trends_has_previous(self) -> bool:
        return self.symptom_trends_page > 1

    @rx.var
    def symptom_trends_has_next(self) -> bool:
        return self.symptom_trends_page < self.symptom_trends_total_pages

    @rx.var
    def symptom_trends_page_info(self) -> str:
        return f"Page {self.symptom_trends_page} of {self.symptom_trends_total_pages}"

    @rx.var
    def symptom_trends_showing_info(self) -> str:
        total = len(self.symptom_trends)
        if total == 0:
            return "No symptom trends"
        start = (self.symptom_trends_page - 1) * self._TRENDS_PAGE_SIZE + 1
        end = min(self.symptom_trends_page * self._TRENDS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Pagination Computed Variables - Data Sources
    # =========================================================================

    @rx.var
    def data_sources_paginated(self) -> list[DataSource]:
        """Paginated slice of filtered data sources."""
        start = (self.data_sources_page - 1) * self._DATA_SOURCES_PAGE_SIZE
        end = start + self._DATA_SOURCES_PAGE_SIZE
        return self.filtered_data_sources[start:end]

    @rx.var
    def data_sources_total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_data_sources) + self._DATA_SOURCES_PAGE_SIZE - 1)
            // self._DATA_SOURCES_PAGE_SIZE,
        )

    @rx.var
    def data_sources_has_previous(self) -> bool:
        return self.data_sources_page > 1

    @rx.var
    def data_sources_has_next(self) -> bool:
        return self.data_sources_page < self.data_sources_total_pages

    @rx.var
    def data_sources_page_info(self) -> str:
        return f"Page {self.data_sources_page} of {self.data_sources_total_pages}"

    @rx.var
    def data_sources_showing_info(self) -> str:
        total = len(self.filtered_data_sources)
        if total == 0:
            return "No data sources"
        start = (self.data_sources_page - 1) * self._DATA_SOURCES_PAGE_SIZE + 1
        end = min(self.data_sources_page * self._DATA_SOURCES_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

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

            # Get user ID from AuthState (must be inside async with self)
            auth_state = await self.get_state(AuthState)
            user_id = auth_state.user_id
            if not user_id:
                logger.warning("load_dashboard_data: No authenticated user")
                self.is_loading = False
                return

            self._current_user_id = user_id

        logger.info("load_dashboard_data: Starting for user_id=%s", user_id)

        try:
            db_data, static_data = await asyncio.gather(
                self._load_health_entries_from_db(),
                load_all_dashboard_data(patient_id=self._viewing_patient_id),
            )

            async with self:
                self.nutrition_summary = _calculate_nutrition(db_data["food_entries"])
                self.food_entries = db_data["food_entries"]
                self.medication_entries = db_data["medication_entries"]
                self.medication_subscriptions = db_data["medication_subscriptions"]
                self.symptoms = db_data["symptoms"]
                self.conditions = static_data.get("conditions", [])
                self.symptom_logs = static_data.get("symptom_logs", [])
                self.symptom_trends = static_data.get("symptom_trends", [])
                self.reminders = static_data.get("reminders", [])
                self.data_sources = static_data.get("data_sources", [])
                self.is_loading = False
                self._data_loaded = True

            logger.info(
                "load_dashboard_data: Complete (%d med_logs, %d med_subs, %d foods, %d symptoms)",
                len(db_data["medication_entries"]),
                len(db_data["medication_subscriptions"]),
                len(db_data["food_entries"]),
                len(db_data["symptoms"]),
            )
        except Exception as e:
            logger.error("load_dashboard_data: Failed - %s", e)
            async with self:
                self.is_loading = False

    async def _load_health_entries_from_db(self) -> dict[str, Any]:
        """Load health entries from database for the authenticated user."""
        user_id = self._current_user_id
        if not user_id:
            logger.warning("_load_health_entries_from_db: No user ID set")
            return {
                "medication_entries": [],
                "medication_subscriptions": [],
                "food_entries": [],
                "symptoms": [],
            }

        def _query(uid: int):
            return (
                get_medication_entries_sync(uid, limit=50),
                get_medication_subscriptions_sync(uid, limit=50),
                get_food_entries_sync(uid, limit=50),
                get_symptoms_sync(uid, limit=50),
            )

        try:
            med_logs, med_subs, foods, symptoms = await asyncio.to_thread(
                _query, user_id
            )
            return {
                "medication_entries": med_logs,
                "medication_subscriptions": med_subs,
                "food_entries": foods,
                "symptoms": symptoms,
            }
        except Exception as e:
            logger.error("_load_health_entries_from_db: %s", e)
            return {
                "medication_entries": [],
                "medication_subscriptions": [],
                "food_entries": [],
                "symptoms": [],
            }

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
                    return [], [], [], []

                user_id = user.id
                logger.debug(
                    "load_patient_health_data: Resolved external_id=%s to user_id=%d",
                    patient_id,
                    user_id,
                )
                return (
                    get_medication_entries_sync(user_id, limit=50),
                    get_medication_subscriptions_sync(user_id, limit=50),
                    get_food_entries_sync(user_id, limit=50),
                    get_symptoms_sync(user_id, limit=50),
                )

            (
                medication_entries,
                medication_subscriptions,
                food_entries,
                symptoms,
            ) = await asyncio.to_thread(_load_db_health_data)

            # Calculate nutrition summary from food entries
            nutrition_summary = (
                _calculate_nutrition(food_entries) if food_entries else {}
            )

            async with self:
                self.nutrition_summary = nutrition_summary
                self.food_entries = food_entries
                self.medication_entries = medication_entries
                self.medication_subscriptions = medication_subscriptions
                self.conditions = data.get("conditions", [])
                self.symptoms = symptoms
                self.symptom_logs = data.get("symptom_logs", [])
                self.symptom_trends = data.get("symptom_trends", [])
                self.reminders = data.get("reminders", [])
                self.data_sources = data.get("data_sources", [])
                self.is_loading = False
                self._data_loaded = True

            logger.info(
                "load_patient_health_data: Loaded %d med_logs, %d med_subs, %d foods, %d symptoms for %s",
                len(medication_entries),
                len(medication_subscriptions),
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

        # Ensure we have user ID from AuthState (must be inside async with self)
        async with self:
            if not self._current_user_id:
                auth_state = await self.get_state(AuthState)
                user_id = auth_state.user_id
                if not user_id:
                    logger.warning("load_health_data_from_db: No authenticated user")
                    return
                self._current_user_id = user_id

        try:
            db_data = await self._load_health_entries_from_db()
            if not any(db_data.values()):
                logger.info("load_health_data_from_db: No data in DB")
                return

            async with self:
                if db_data["medication_entries"]:
                    self.medication_entries = db_data["medication_entries"]
                if db_data["medication_subscriptions"]:
                    self.medication_subscriptions = db_data["medication_subscriptions"]
                if db_data["food_entries"]:
                    self.food_entries = db_data["food_entries"]
                    self.nutrition_summary = _calculate_nutrition(
                        db_data["food_entries"]
                    )
                if db_data["symptoms"]:
                    self.symptoms = db_data["symptoms"]

            logger.info(
                "load_health_data_from_db: %d med_logs, %d med_subs, %d foods, %d symptoms",
                len(db_data["medication_entries"]),
                len(db_data["medication_subscriptions"]),
                len(db_data["food_entries"]),
                len(db_data["symptoms"]),
            )
        except Exception as e:
            logger.error("load_health_data_from_db: %s", e)

    def clear_patient_health_data(self):
        """Clear patient health data (used when deselecting patient)."""
        self._viewing_patient_id = None
        self._current_user_id = None
        self._data_loaded = False
        self.nutrition_summary = {}
        self.food_entries = []
        self.medication_entries = []
        self.medication_subscriptions = []
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

    def set_symptoms_filter(self, value: str):
        self.symptoms_filter = value

    def set_data_sources_filter(self, value: str):
        self.data_sources_filter = value

    # =========================================================================
    # Pagination Handlers
    # =========================================================================

    def medication_entries_previous_page(self):
        if self.medication_entries_page > 1:
            self.medication_entries_page -= 1

    def medication_entries_next_page(self):
        if self.medication_entries_page < self.medication_entries_total_pages:
            self.medication_entries_page += 1

    def medication_subscriptions_previous_page(self):
        if self.medication_subscriptions_page > 1:
            self.medication_subscriptions_page -= 1

    def medication_subscriptions_next_page(self):
        if (
            self.medication_subscriptions_page
            < self.medication_subscriptions_total_pages
        ):
            self.medication_subscriptions_page += 1

    def food_entries_previous_page(self):
        if self.food_entries_page > 1:
            self.food_entries_page -= 1

    def food_entries_next_page(self):
        if self.food_entries_page < self.food_entries_total_pages:
            self.food_entries_page += 1

    def symptoms_previous_page(self):
        if self.symptoms_page > 1:
            self.symptoms_page -= 1

    def symptoms_next_page(self):
        if self.symptoms_page < self.symptoms_total_pages:
            self.symptoms_page += 1

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

    def open_medication_modal(self, medication: dict[str, Any]):
        self.selected_medication = medication
        self.show_medication_modal = True

    def set_show_medication_modal(self, value: bool):
        self.show_medication_modal = value

    @rx.event
    async def log_dose(self, _medication_id: str):
        """Log dose for a medication. Parameter required for event binding."""
        self.show_medication_modal = False

    def open_condition_modal(self, condition: dict[str, Any]):
        self.selected_condition = condition
        self.show_condition_modal = True

    def set_show_condition_modal(self, value: bool):
        self.show_condition_modal = value

    def open_symptom_modal(self, symptom: dict[str, Any]):
        self.selected_symptom = symptom
        self.show_symptom_modal = True

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

    def set_show_suggest_integration_modal(self, value: bool):
        self.show_suggest_integration_modal = value

    def set_suggested_integration_name(self, value: str):
        self.suggested_integration_name = value

    def set_suggested_integration_description(self, value: str):
        self.suggested_integration_description = value

    def submit_integration_suggestion(self):
        self.integration_suggestion_submitted = True

    # =========================================================================
    # Pagination Handlers
    # =========================================================================

    def medications_next_page(self):
        """Go to next medications page."""
        if self.medications_page < self.medications_total_pages:
            self.medications_page += 1

    def medications_previous_page(self):
        """Go to previous medications page."""
        if self.medications_page > 1:
            self.medications_page -= 1

    def food_entries_next_page(self):
        """Go to next food entries page."""
        if self.food_entries_page < self.food_entries_total_pages:
            self.food_entries_page += 1

    def food_entries_previous_page(self):
        """Go to previous food entries page."""
        if self.food_entries_page > 1:
            self.food_entries_page -= 1

    def conditions_next_page(self):
        """Go to next conditions page."""
        if self.conditions_page < self.conditions_total_pages:
            self.conditions_page += 1

    def conditions_previous_page(self):
        """Go to previous conditions page."""
        if self.conditions_page > 1:
            self.conditions_page -= 1

    def set_conditions_filter_with_reset(self, value: str):
        """Set conditions filter and reset page to 1."""
        self.conditions_filter = value
        self.conditions_page = 1

    def symptoms_next_page(self):
        """Go to next symptoms page."""
        if self.symptoms_page < self.symptoms_total_pages:
            self.symptoms_page += 1

    def symptoms_previous_page(self):
        """Go to previous symptoms page."""
        if self.symptoms_page > 1:
            self.symptoms_page -= 1

    def symptom_logs_next_page(self):
        """Go to next symptom logs page."""
        if self.symptom_logs_page < self.symptom_logs_total_pages:
            self.symptom_logs_page += 1

    def symptom_logs_previous_page(self):
        """Go to previous symptom logs page."""
        if self.symptom_logs_page > 1:
            self.symptom_logs_page -= 1

    def reminders_next_page(self):
        """Go to next reminders page."""
        if self.reminders_page < self.reminders_total_pages:
            self.reminders_page += 1

    def reminders_previous_page(self):
        """Go to previous reminders page."""
        if self.reminders_page > 1:
            self.reminders_page -= 1

    def symptom_trends_next_page(self):
        """Go to next symptom trends page."""
        if self.symptom_trends_page < self.symptom_trends_total_pages:
            self.symptom_trends_page += 1

    def symptom_trends_previous_page(self):
        """Go to previous symptom trends page."""
        if self.symptom_trends_page > 1:
            self.symptom_trends_page -= 1

    def data_sources_next_page(self):
        """Go to next data sources page."""
        if self.data_sources_page < self.data_sources_total_pages:
            self.data_sources_page += 1

    def data_sources_previous_page(self):
        """Go to previous data sources page."""
        if self.data_sources_page > 1:
            self.data_sources_page -= 1

    def set_data_sources_filter_with_reset(self, value: str):
        """Set data sources filter and reset page to 1."""
        self.data_sources_filter = value
        self.data_sources_page = 1


class AdminDashboardState(rx.State):
    """State management for admin dashboard tab navigation.

    Patient data is managed by PatientState - this class only handles UI state.
    """

    active_tab: str = "overview"

    def set_tab(self, tab: str):
        """Set the active dashboard tab."""
        self.active_tab = tab
