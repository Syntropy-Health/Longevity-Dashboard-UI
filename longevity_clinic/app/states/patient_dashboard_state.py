"""Patient dashboard state management.

Handles patient dashboard data including nutrition, medications, conditions,
symptoms, and data sources. Check-in functionality has been moved to
PatientCheckinState for better separation of concerns.
"""

import reflex as rx
from typing import List, Dict, Any
from datetime import datetime
import uuid

from ..config import get_logger

logger = get_logger("longevity_clinic.dashboard")

from ..data.state_schemas import (
    NutritionSummary,
    FoodEntry,
    Medication,
    Condition,
    Symptom,
    SymptomLog,
    Reminder,
    SymptomTrend,
    DataSource,
)

from ..data.demo import (
    DEMO_NUTRITION_SUMMARY,
    DEMO_FOOD_ENTRIES,
    DEMO_MEDICATIONS,
    DEMO_CONDITIONS,
    DEMO_SYMPTOMS,
    DEMO_SYMPTOM_LOGS,
    DEMO_REMINDERS,
    DEMO_SYMPTOM_TRENDS,
    DEMO_DATA_SOURCES,
)


class PatientDashboardState(rx.State):
    """State management for patient dashboard.

    Note: Check-in related state has been moved to PatientCheckinState.
    """

    # Active tab
    active_tab: str = "overview"

    # Filter states
    conditions_filter: str = "all"
    symptoms_filter: str = "timeline"
    data_sources_filter: str = "devices"

    # Modal states (non-checkin related)
    show_medication_modal: bool = False
    show_condition_modal: bool = False
    show_symptom_modal: bool = False
    show_connect_modal: bool = False
    show_add_food_modal: bool = False
    show_suggest_integration_modal: bool = False

    # Suggest integration form state
    suggested_integration_name: str = ""
    suggested_integration_description: str = ""
    integration_suggestion_submitted: bool = False

    # Add food form state
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

    # Settings state
    email_notifications: bool = True
    push_notifications: bool = True

    # Data - initialized from demo module
    nutrition_summary: NutritionSummary = DEMO_NUTRITION_SUMMARY
    food_entries: List[FoodEntry] = DEMO_FOOD_ENTRIES
    medications: List[Medication] = DEMO_MEDICATIONS
    conditions: List[Condition] = DEMO_CONDITIONS
    symptoms: List[Symptom] = DEMO_SYMPTOMS
    symptom_logs: List[SymptomLog] = DEMO_SYMPTOM_LOGS
    reminders: List[Reminder] = DEMO_REMINDERS
    symptom_trends: List[SymptomTrend] = DEMO_SYMPTOM_TRENDS
    data_sources: List[DataSource] = DEMO_DATA_SOURCES

    # =========================================================================
    # Computed Variables
    # =========================================================================

    @rx.var
    def total_medication_adherence(self) -> float:
        """Calculate overall medication adherence."""
        if not self.medications:
            return 0.0
        total = sum(med["adherence_rate"] for med in self.medications)
        return total / len(self.medications)

    @rx.var
    def active_conditions_count(self) -> int:
        """Count active conditions."""
        return len([c for c in self.conditions if c["status"] == "active"])

    @rx.var
    def managed_conditions_count(self) -> int:
        """Count managed conditions."""
        return len([c for c in self.conditions if c["status"] == "managed"])

    @rx.var
    def resolved_conditions_count(self) -> int:
        """Count resolved conditions."""
        return len([c for c in self.conditions if c["status"] == "resolved"])

    @rx.var
    def filtered_conditions(self) -> List[Condition]:
        """Get filtered conditions based on filter."""
        if self.conditions_filter == "all":
            return self.conditions
        return [c for c in self.conditions if c["status"] == self.conditions_filter]

    @rx.var
    def connected_sources_count(self) -> int:
        """Count connected data sources."""
        return len([s for s in self.data_sources if s.get("connected", False)])

    @rx.var
    def filtered_data_sources(self) -> List[DataSource]:
        """Get filtered data sources."""
        type_map = {
            "devices": ["wearable", "scale", "cgm"],
            "api_connections": ["app", "ehr"],
            "import_history": [],
        }
        types = type_map.get(self.data_sources_filter, [])
        if not types:
            return self.data_sources
        return [s for s in self.data_sources if s["type"] in types]

    # =========================================================================
    # Tab and Filter Methods
    # =========================================================================

    def set_active_tab(self, tab: str):
        """Set the active tab."""
        self.active_tab = tab

    def set_conditions_filter(self, filter_value: str):
        """Set conditions filter."""
        self.conditions_filter = filter_value

    def set_symptoms_filter(self, filter_value: str):
        """Set symptoms filter."""
        self.symptoms_filter = filter_value

    def set_data_sources_filter(self, filter_value: str):
        """Set data sources filter."""
        self.data_sources_filter = filter_value

    # =========================================================================
    # Data Source Methods
    # =========================================================================

    def toggle_data_source_connection(self, source_id: str):
        """Toggle a data source connection on/off."""
        updated_sources = []
        for source in self.data_sources:
            if source["id"] == source_id:
                new_connected = not source["connected"]
                updated_sources.append(
                    {
                        **source,
                        "connected": new_connected,
                        "status": "connected" if new_connected else "disconnected",
                        "last_sync": "Just now" if new_connected else "Disconnected",
                    }
                )
            else:
                updated_sources.append(source)
        self.data_sources = updated_sources

    # =========================================================================
    # Settings Methods
    # =========================================================================

    def toggle_email_notifications(self):
        """Toggle email notifications."""
        self.email_notifications = not self.email_notifications

    def toggle_push_notifications(self):
        """Toggle push notifications."""
        self.push_notifications = not self.push_notifications

    # =========================================================================
    # Medication Modal
    # =========================================================================

    def open_medication_modal(self, medication: Dict[str, Any]):
        """Open medication modal with selected medication."""
        self.selected_medication = medication
        self.show_medication_modal = True

    def close_medication_modal(self):
        """Close medication modal."""
        self.show_medication_modal = False
        self.selected_medication = {}

    def set_show_medication_modal(self, value: bool):
        """Set show medication modal state."""
        self.show_medication_modal = value

    @rx.event
    async def log_dose(self, medication_id: str):
        """Log a medication dose."""
        # In production, this would update adherence tracking
        self.show_medication_modal = False

    # =========================================================================
    # Condition Modal
    # =========================================================================

    def open_condition_modal(self, condition: Dict[str, Any]):
        """Open condition modal with selected condition."""
        self.selected_condition = condition
        self.show_condition_modal = True

    def close_condition_modal(self):
        """Close condition modal."""
        self.show_condition_modal = False
        self.selected_condition = {}

    def set_show_condition_modal(self, value: bool):
        """Set show condition modal state."""
        self.show_condition_modal = value

    # =========================================================================
    # Symptom Modal
    # =========================================================================

    def open_symptom_modal(self, symptom: Dict[str, Any]):
        """Open symptom modal with selected symptom."""
        self.selected_symptom = symptom
        self.show_symptom_modal = True

    def close_symptom_modal(self):
        """Close symptom modal."""
        self.show_symptom_modal = False
        self.selected_symptom = {}

    def set_show_symptom_modal(self, value: bool):
        """Set show symptom modal state."""
        self.show_symptom_modal = value

    @rx.event
    async def save_symptom_log(self):
        """Save a symptom log entry."""
        if self.selected_symptom:
            new_log: SymptomLog = {
                "id": f"sym_{uuid.uuid4().hex[:8]}",
                "symptom_name": self.selected_symptom.get("name", "Unknown"),
                "severity": 5,
                "notes": "",
                "timestamp": datetime.now().strftime("Today, %I:%M %p"),
            }
            self.symptom_logs = [new_log, *self.symptom_logs]

        self.show_symptom_modal = False

    # =========================================================================
    # Connect Data Source Modal
    # =========================================================================

    def open_connect_modal(self):
        """Open connect data source modal."""
        self.show_connect_modal = True

    def close_connect_modal(self):
        """Close connect data source modal."""
        self.show_connect_modal = False

    def set_show_connect_modal(self, value: bool):
        """Set show connect modal state."""
        self.show_connect_modal = value

    # =========================================================================
    # Add Food Modal
    # =========================================================================

    def open_add_food_modal(self):
        """Open add food modal."""
        self.show_add_food_modal = True
        # Reset form
        self.new_food_name = ""
        self.new_food_calories = ""
        self.new_food_protein = ""
        self.new_food_carbs = ""
        self.new_food_fat = ""
        self.new_food_meal_type = "snack"

    def close_add_food_modal(self):
        """Close add food modal."""
        self.show_add_food_modal = False

    def set_show_add_food_modal(self, value: bool):
        """Set show add food modal state."""
        self.show_add_food_modal = value

    def set_new_food_name(self, value: str):
        """Set new food name."""
        self.new_food_name = value

    def set_new_food_calories(self, value: float):
        """Set new food calories."""
        self.new_food_calories = str(value) if value else ""

    def set_new_food_protein(self, value: float):
        """Set new food protein."""
        self.new_food_protein = str(value) if value else ""

    def set_new_food_carbs(self, value: float):
        """Set new food carbs."""
        self.new_food_carbs = str(value) if value else ""

    def set_new_food_fat(self, value: float):
        """Set new food fat."""
        self.new_food_fat = str(value) if value else ""

    def set_new_food_meal_type(self, value: str):
        """Set new food meal type."""
        self.new_food_meal_type = value

    def save_food_entry(self):
        """Save a new food entry."""
        # Create new food entry
        new_entry = {
            "id": str(uuid.uuid4())[:8],
            "name": self.new_food_name,
            "calories": int(self.new_food_calories) if self.new_food_calories else 0,
            "protein": float(self.new_food_protein) if self.new_food_protein else 0.0,
            "carbs": float(self.new_food_carbs) if self.new_food_carbs else 0.0,
            "fat": float(self.new_food_fat) if self.new_food_fat else 0.0,
            "time": datetime.now().strftime("%I:%M %p"),
            "meal_type": self.new_food_meal_type,
        }

        # Add to list
        self.food_entries = [*self.food_entries, new_entry]

        # Update nutrition summary
        self.nutrition_summary = {
            **self.nutrition_summary,
            "total_calories": self.nutrition_summary["total_calories"]
            + new_entry["calories"],
            "total_protein": self.nutrition_summary["total_protein"]
            + new_entry["protein"],
            "total_carbs": self.nutrition_summary["total_carbs"] + new_entry["carbs"],
            "total_fat": self.nutrition_summary["total_fat"] + new_entry["fat"],
        }

        # Close modal
        self.show_add_food_modal = False

    # =========================================================================
    # Suggest Integration Modal
    # =========================================================================

    def open_suggest_integration_modal(self):
        """Open suggest integration modal."""
        self.show_suggest_integration_modal = True
        self.suggested_integration_name = ""
        self.suggested_integration_description = ""
        self.integration_suggestion_submitted = False

    def close_suggest_integration_modal(self):
        """Close suggest integration modal."""
        self.show_suggest_integration_modal = False

    def set_show_suggest_integration_modal(self, value: bool):
        """Set suggest integration modal visibility."""
        self.show_suggest_integration_modal = value

    def set_suggested_integration_name(self, value: str):
        """Set suggested integration name."""
        self.suggested_integration_name = value

    def set_suggested_integration_description(self, value: str):
        """Set suggested integration description."""
        self.suggested_integration_description = value

    def submit_integration_suggestion(self):
        """Submit integration suggestion."""
        # In a real app, this would send the suggestion to the backend
        self.integration_suggestion_submitted = True

    # =========================================================================
    # Dashboard Load
    # =========================================================================

    @rx.event
    def load_dashboard_data(self):
        """Load dashboard data on mount."""
        print("[DEBUG] load_dashboard_data: CALLED", flush=True)
        logger.info("load_dashboard_data: Called")
