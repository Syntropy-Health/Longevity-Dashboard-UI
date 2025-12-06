"""Patient dashboard state management."""

import reflex as rx
import asyncio
from typing import List, Dict, Any, TYPE_CHECKING

from datetime import datetime
import uuid

# voice transcription check-in
from .voice_transcription_state import VoiceTranscriptionState
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
    CheckIn,
)

# Import extracted functions
from .functions.patients import extract_checkin_from_text
from .functions import fetch_and_process_call_logs
from ..data.demo import (
    DEMO_PHONE_NUMBER,
    DEMO_NUTRITION_SUMMARY,
    DEMO_FOOD_ENTRIES,
    DEMO_MEDICATIONS,
    DEMO_CONDITIONS,
    DEMO_SYMPTOMS,
    DEMO_SYMPTOM_LOGS,
    DEMO_REMINDERS,
    DEMO_SYMPTOM_TRENDS,
    DEMO_DATA_SOURCES,
    DEMO_CHECKINS,
)

if TYPE_CHECKING:
    from .voice_transcription_state import VoiceTranscriptionState


class PatientDashboardState(rx.State):
    """State management for patient dashboard.""" ""

    # Active tab
    active_tab: str = "overview"

    # Filter states
    conditions_filter: str = "all"
    symptoms_filter: str = "timeline"
    data_sources_filter: str = "devices"

    # Check-in modal state
    show_checkin_modal: bool = False
    checkin_type: str = "voice"
    checkin_text: str = ""
    selected_topics: List[str] = []

    # Voice recording state
    is_recording: bool = False
    recording_session_id: str = ""
    recording_duration: float = 0.0
    transcribed_text: str = ""
    transcription_status: str = (
        ""  # 'idle', 'recording', 'transcribing', 'done', 'error'
    )

    # Other modal states
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
    checkins: List[CheckIn] = DEMO_CHECKINS

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

    @rx.var
    def unreviewed_checkins_count(self) -> int:
        """Count unreviewed check-ins."""
        return len([c for c in self.checkins if not c["provider_reviewed"]])

    @rx.var
    def voice_call_checkins_count(self) -> int:
        """Count check-ins created from voice calls."""
        return len([c for c in self.checkins if c.get("type") == "call"])

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

    @rx.event
    async def set_checkin_type(self, checkin_type: str):
        """Set check-in type."""
        self.checkin_type = checkin_type
        # Reset recording state when switching types
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.transcription_status = "idle"

        voice_state = await self.get_state(VoiceTranscriptionState)
        voice_state.transcript = ""
        voice_state.has_error = False
        voice_state.error_message = ""

    def set_checkin_text(self, text: str):
        """Set the check-in text content."""
        self.checkin_text = text

    def toggle_email_notifications(self):
        """Toggle email notifications."""
        self.email_notifications = not self.email_notifications

    def toggle_push_notifications(self):
        """Toggle push notifications."""
        self.push_notifications = not self.push_notifications

    def toggle_topic(self, topic: str):
        """Toggle a topic selection."""
        if topic in self.selected_topics:
            self.selected_topics = [t for t in self.selected_topics if t != topic]
        else:
            self.selected_topics = [*self.selected_topics, topic]

    def is_topic_selected(self, topic: str) -> bool:
        """Check if a topic is selected."""
        return topic in self.selected_topics

    @rx.event
    async def start_recording(self):
        """Start voice recording."""
        self.is_recording = True
        self.transcription_status = "recording"
        self.recording_duration = 0.0
        self.recording_session_id = f"rec_{uuid.uuid4().hex[:8]}"

    @rx.event
    async def stop_recording(self):
        """Stop voice recording - transcript comes from VoiceTranscriptionState."""
        self.is_recording = False
        self.transcription_status = "done"

    @rx.event
    async def toggle_recording(self):
        """Toggle voice recording on/off."""
        if not self.is_recording:
            # Start recording
            yield PatientDashboardState.start_recording
            # Start duration timer in background
            yield PatientDashboardState.increment_recording_duration
        else:
            # Stop recording
            yield PatientDashboardState.stop_recording

    @rx.event(background=True)
    async def increment_recording_duration(self):
        """Increment the recording duration timer."""
        async with self:
            # Check initial state
            if not self.is_recording:
                return

        while True:
            await asyncio.sleep(1)
            async with self:
                # Check if still recording before incrementing
                if not self.is_recording:
                    return
                self.recording_duration += 1.0

    @rx.event
    async def open_checkin_modal(self):
        """Open check-in modal."""
        logger.info("open_checkin_modal called - setting show_checkin_modal=True")
        self.show_checkin_modal = True
        # Reset local state
        self.checkin_type = "voice"
        self.checkin_text = ""
        self.selected_topics = []
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.transcription_status = "idle"

        # Clear voice transcription state directly
        logger.debug("Clearing VoiceTranscriptionState")
        from .voice_transcription_state import VoiceTranscriptionState

        voice_state = await self.get_state(VoiceTranscriptionState)
        voice_state.transcript = ""
        voice_state.has_error = False
        voice_state.error_message = ""
        logger.info("open_checkin_modal completed")

    @rx.event
    async def close_checkin_modal(self):
        """Close check-in modal."""
        self.show_checkin_modal = False
        self.is_recording = False
        self.transcription_status = "idle"

        # Clear voice transcription state directly
        from .voice_transcription_state import VoiceTranscriptionState

        voice_state = await self.get_state(VoiceTranscriptionState)
        voice_state.transcript = ""
        voice_state.has_error = False
        voice_state.error_message = ""

    def open_medication_modal(self, medication: Dict[str, Any]):
        """Open medication modal with selected medication."""
        self.selected_medication = medication
        self.show_medication_modal = True

    def close_medication_modal(self):
        """Close medication modal."""
        self.show_medication_modal = False
        self.selected_medication = {}

    def open_condition_modal(self, condition: Dict[str, Any]):
        """Open condition modal with selected condition."""
        self.selected_condition = condition
        self.show_condition_modal = True

    def close_condition_modal(self):
        """Close condition modal."""
        self.show_condition_modal = False
        self.selected_condition = {}

    def open_symptom_modal(self, symptom: Dict[str, Any]):
        """Open symptom modal with selected symptom."""
        self.selected_symptom = symptom
        self.show_symptom_modal = True

    def close_symptom_modal(self):
        """Close symptom modal."""
        self.show_symptom_modal = False
        self.selected_symptom = {}

    def open_connect_modal(self):
        """Open connect data source modal."""
        self.show_connect_modal = True

    def close_connect_modal(self):
        """Close connect data source modal."""
        self.show_connect_modal = False

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

    def set_show_checkin_modal(self, value: bool):
        """Set show checkin modal state."""
        self.show_checkin_modal = value

    def set_show_medication_modal(self, value: bool):
        """Set show medication modal state."""
        self.show_medication_modal = value

    def set_show_condition_modal(self, value: bool):
        """Set show condition modal state."""
        self.show_condition_modal = value

    def set_show_symptom_modal(self, value: bool):
        """Set show symptom modal state."""
        self.show_symptom_modal = value

    def set_show_connect_modal(self, value: bool):
        """Set show connect modal state."""
        self.show_connect_modal = value

    def set_show_add_food_modal(self, value: bool):
        """Set show add food modal state."""
        self.show_add_food_modal = value

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

    @rx.event
    async def save_checkin(self):
        """Save a new check-in using LLM for structured extraction."""
        content = (
            self.transcribed_text
            if self.checkin_type == "voice"
            else self.checkin_text.strip()
        )

        if len(content) < 10:
            return

        checkin_model = await extract_checkin_from_text(content, self.checkin_type)
        self.checkins = [checkin_model.to_dict(), *self.checkins]

        self.show_checkin_modal = False
        self._reset_checkin_state()

    @rx.event
    async def save_checkin_with_voice(self):
        """Save a new check-in via voice"""

        voice_state = await self.get_state(VoiceTranscriptionState)
        content = (
            voice_state.transcript
            if self.checkin_type == "voice"
            else self.checkin_text.strip()
        )

        if not content.strip():
            return

        checkin_model = await extract_checkin_from_text(content, self.checkin_type)
        self.checkins = [checkin_model.to_dict(), *self.checkins]

        self.show_checkin_modal = False
        self._reset_checkin_state()

        # Clear voice state
        voice_state.transcript = ""
        voice_state.has_error = False
        voice_state.error_message = ""

    def _reset_checkin_state(self):
        """Reset check-in modal state."""
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.checkin_text = ""
        self.selected_topics = []
        self.transcription_status = "idle"

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

    @rx.event
    async def log_dose(self, medication_id: str):
        """Log a medication dose."""
        # In production, this would update adherence tracking
        self.show_medication_modal = False

    @rx.event
    def load_dashboard_data(self):
        """Load dashboard data on mount."""
        print("[DEBUG] load_dashboard_data: CALLED", flush=True)
        logger.info("load_dashboard_data: Called")

    # =========================================================================
    # Call Logs / Check-ins Sync
    # =========================================================================

    call_logs_syncing: bool = False
    call_logs_sync_error: str = ""
    last_sync_time: str = ""
    _processed_call_ids: List[
        str
    ] = []  # Track processed call IDs (List for Reflex compatibility)

    @rx.event(background=True)
    async def refresh_call_logs(self):
        """Fetch call logs and sync to checkins (background task).

        Background task pattern per https://reflex.dev/docs/events/background-events:
        - Minimize time inside `async with self` (state lock)
        - Do heavy I/O outside the lock
        - Use on_load (not on_mount) so task terminates on navigation
        """
        print("[DEBUG] refresh_call_logs: ENTERED", flush=True)
        logger.info("refresh_call_logs: Starting")

        # 1. Quick lock to set syncing flag and copy needed state
        print("[DEBUG] refresh_call_logs: Acquiring lock for setup...", flush=True)
        async with self:
            self.call_logs_syncing = True
            self.call_logs_sync_error = ""
            processed_ids = set(self._processed_call_ids)
            current_checkins = list(self.checkins)  # Copy current checkins
        print("[DEBUG] refresh_call_logs: Lock released, starting fetch...", flush=True)

        try:
            # 2. Heavy I/O OUTSIDE the lock
            print(
                "[DEBUG] refresh_call_logs: Calling fetch_and_process_call_logs...",
                flush=True,
            )
            new_count, new_checkins, new_summaries = await fetch_and_process_call_logs(
                phone_number=DEMO_PHONE_NUMBER,
                processed_ids=processed_ids,
                use_llm_summary=False,
            )
            print(
                f"[DEBUG] refresh_call_logs: Fetch complete, {new_count} new logs",
                flush=True,
            )
            logger.info("refresh_call_logs: Processed %d new logs", new_count)

            # 3. Process results OUTSIDE the lock
            existing_ids = {c["id"] for c in current_checkins}
            to_add = [c for c in new_checkins if c["id"] not in existing_ids]
            if to_add:
                sorted_new = sorted(
                    to_add, key=lambda x: x.get("timestamp", ""), reverse=True
                )
            else:
                sorted_new = []

            # 4. Quick lock to update state
            print(
                "[DEBUG] refresh_call_logs: Acquiring lock to save results...",
                flush=True,
            )
            async with self:
                if sorted_new:
                    self.checkins = sorted_new + list(self.checkins)
                    logger.info("refresh_call_logs: Added %d checkins", len(sorted_new))

                self._processed_call_ids = list(
                    processed_ids | set(new_summaries.keys())
                )
                self.last_sync_time = datetime.now().strftime("%I:%M %p")
                self.call_logs_syncing = False
            print("[DEBUG] refresh_call_logs: COMPLETED successfully", flush=True)

        except Exception as e:
            print(f"[DEBUG] refresh_call_logs: FAILED - {e}", flush=True)
            logger.error("refresh_call_logs: Failed - %s", e)
            async with self:
                self.call_logs_sync_error = str(e)
                self.call_logs_syncing = False
