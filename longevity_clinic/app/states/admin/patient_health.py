"""Admin patient health state for viewing patient data.

This state is used by admin views to load and display health data for
a specific patient. Unlike the patient's own dashboard states which use
AuthState.user_id, this state loads data by patient_id (external_id).
"""

import asyncio
from typing import Any

import reflex as rx

from ...config import get_logger
from ...data.schemas.llm import (
    Condition,
    DataSource,
    FoodEntryModel as FoodEntry,
    MedicationEntryModel as MedicationEntry,
    PatientTreatmentModel as MedicationSubscription,
    Symptom,
    SymptomEntryModel as SymptomEntry,
    SymptomTrend,
)
from ...functions.db_utils import (
    get_food_entries_sync,
    get_medication_entries_sync,
    get_patient_treatments_sync,
    get_symptom_logs_sync,
    get_symptoms_sync,
    get_user_by_external_id_sync,
)
from ...functions.patients.dashboard import load_all_dashboard_data

logger = get_logger("longevity_clinic.admin.patient_health")

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


class AdminPatientHealthState(rx.State):
    """State for admin viewing a specific patient's health data.

    Used by admin/tabs/patient_health.py to display patient health metrics.
    Loads data by patient external_id (e.g., "P001") rather than auth user ID.
    """

    # Tab navigation for admin health view
    active_tab: str = "overview"

    # Loading state
    is_loading: bool = False
    _data_loaded: bool = False
    _viewing_patient_id: str | None = None

    # Health data (loaded via load_patient_health_data)
    nutrition_summary: dict[str, Any] = {}
    food_entries: list[FoodEntry] = []
    medication_entries: list[MedicationEntry] = []
    medication_subscriptions: list[MedicationSubscription] = []
    conditions: list[Condition] = []
    symptoms: list[Symptom] = []
    symptom_logs: list[SymptomEntry] = []
    symptom_trends: list[SymptomTrend] = []
    reminders: list[dict[str, Any]] = []
    data_sources: list[DataSource] = []

    # =========================================================================
    # Tab Navigation
    # =========================================================================

    def set_active_tab(self, tab: str):
        """Set the active tab (overview or analytics)."""
        self.active_tab = tab

    # =========================================================================
    # Data Loading
    # =========================================================================

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
            # Load static data (conditions, symptom_trends, reminders, data_sources)
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
                    return [], [], [], [], []

                user_id = user.id
                logger.debug(
                    "load_patient_health_data: Resolved external_id=%s to user_id=%d",
                    patient_id,
                    user_id,
                )
                return (
                    get_medication_entries_sync(user_id, limit=50),
                    get_patient_treatments_sync(user_id, limit=50),
                    get_food_entries_sync(user_id, limit=50),
                    get_symptoms_sync(user_id, limit=50),
                    get_symptom_logs_sync(user_id, limit=50),
                )

            (
                medication_entries,
                medication_subscriptions,
                food_entries,
                symptoms,
                symptom_logs,
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
                # Symptom logs from DB, fallback to static if empty
                self.symptom_logs = (
                    symptom_logs if symptom_logs else data.get("symptom_logs", [])
                )
                self.symptom_trends = data.get("symptom_trends", [])
                self.reminders = data.get("reminders", [])
                self.data_sources = data.get("data_sources", [])
                self.is_loading = False
                self._data_loaded = True

            logger.info(
                "load_patient_health_data: Loaded %d med_logs, %d med_subs, %d foods, %d symptoms, %d symptom_logs for %s",
                len(medication_entries),
                len(medication_subscriptions),
                len(food_entries),
                len(symptoms),
                len(symptom_logs),
                patient_id,
            )
        except Exception as e:
            logger.error("load_patient_health_data: %s", e)
            async with self:
                self.is_loading = False

    def clear_patient_health_data(self):
        """Clear patient health data (used when deselecting patient)."""
        self._viewing_patient_id = None
        self._data_loaded = False
        self.active_tab = "overview"
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
