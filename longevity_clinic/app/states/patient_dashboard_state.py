"""Patient dashboard state management."""

import reflex as rx
import asyncio
from typing import List, Dict, Any, TypedDict

from .functions import (
    start_voice_recording,
    stop_voice_recording,
    transcribe_voice_input,
    process_text_checkin,
    extract_health_topics,
    save_checkin,
    log_symptom,
    log_medication_dose,
)


class NutritionSummary(TypedDict):
    """Nutrition summary type."""
    total_calories: int
    goal_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float
    water_intake: float


class FoodEntry(TypedDict):
    """Food entry type."""
    id: str
    name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    time: str
    meal_type: str


class Medication(TypedDict):
    """Medication type."""
    id: str
    name: str
    dosage: str
    frequency: str
    status: str
    adherence_rate: float


class Condition(TypedDict):
    """Health condition type."""
    id: str
    name: str
    icd_code: str
    diagnosed_date: str
    status: str
    severity: str
    treatments: str


class Symptom(TypedDict):
    """Symptom type."""
    id: str
    name: str
    severity: str
    frequency: str
    trend: str


class SymptomLog(TypedDict):
    """Symptom log entry type."""
    id: str
    symptom_name: str
    severity: int
    notes: str
    timestamp: str


class Reminder(TypedDict):
    """Health reminder type."""
    id: str
    title: str
    description: str
    time: str
    type: str  # medication, appointment, checkup, exercise
    completed: bool


class SymptomTrend(TypedDict):
    """Symptom trend data type."""
    id: str
    symptom_name: str
    current_severity: int
    previous_severity: int
    trend: str  # improving, worsening, stable
    change_percent: float
    period: str


class DataSource(TypedDict):
    """Data source type."""
    id: str
    name: str
    type: str
    status: str
    icon: str
    image: str
    last_sync: str
    connected: bool


class CheckIn(TypedDict):
    """Check-in entry type."""
    id: str
    type: str
    summary: str
    timestamp: str
    sentiment: str
    key_topics: List[str]
    provider_reviewed: bool


class PatientDashboardState(rx.State):
    """State management for patient dashboard."""
    
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
    transcription_status: str = ""  # 'idle', 'recording', 'transcribing', 'done', 'error'
    
    # Other modal states
    show_medication_modal: bool = False
    show_condition_modal: bool = False
    show_symptom_modal: bool = False
    show_connect_modal: bool = False
    show_add_food_modal: bool = False
    
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
    
    # Data
    nutrition_summary: NutritionSummary = {
        "total_calories": 1850,
        "goal_calories": 2200,
        "total_protein": 95.5,
        "total_carbs": 180.0,
        "total_fat": 65.0,
        "water_intake": 2.4,
    }
    
    food_entries: List[FoodEntry] = [
        {
            "id": "1",
            "name": "Greek Yogurt with Berries",
            "calories": 320,
            "protein": 18.0,
            "carbs": 28.0,
            "fat": 12.0,
            "time": "8:30 AM",
            "meal_type": "breakfast",
        },
        {
            "id": "2",
            "name": "Grilled Salmon Salad",
            "calories": 520,
            "protein": 42.0,
            "carbs": 18.0,
            "fat": 28.0,
            "time": "12:45 PM",
            "meal_type": "lunch",
        },
        {
            "id": "3",
            "name": "Protein Smoothie",
            "calories": 280,
            "protein": 25.0,
            "carbs": 32.0,
            "fat": 8.0,
            "time": "3:30 PM",
            "meal_type": "snack",
        },
        {
            "id": "4",
            "name": "Chicken Stir-Fry",
            "calories": 730,
            "protein": 45.0,
            "carbs": 62.0,
            "fat": 24.0,
            "time": "7:00 PM",
            "meal_type": "dinner",
        },
    ]
    
    medications: List[Medication] = [
        {
            "id": "1",
            "name": "Metformin",
            "dosage": "500mg",
            "frequency": "Twice daily with meals",
            "status": "active",
            "adherence_rate": 96.0,
        },
        {
            "id": "2",
            "name": "Lisinopril",
            "dosage": "10mg",
            "frequency": "Once daily in morning",
            "status": "active",
            "adherence_rate": 92.0,
        },
        {
            "id": "3",
            "name": "Vitamin D3",
            "dosage": "5000 IU",
            "frequency": "Once daily with food",
            "status": "active",
            "adherence_rate": 88.0,
        },
        {
            "id": "4",
            "name": "Omega-3 Fish Oil",
            "dosage": "1200mg",
            "frequency": "Twice daily",
            "status": "active",
            "adherence_rate": 85.0,
        },
    ]
    
    conditions: List[Condition] = [
        {
            "id": "1",
            "name": "Type 2 Diabetes",
            "icd_code": "E11.9",
            "diagnosed_date": "Jan 2022",
            "status": "managed",
            "severity": "moderate",
            "treatments": "Metformin, Diet management",
        },
        {
            "id": "2",
            "name": "Hypertension",
            "icd_code": "I10",
            "diagnosed_date": "Mar 2021",
            "status": "managed",
            "severity": "mild",
            "treatments": "Lisinopril, Exercise",
        },
        {
            "id": "3",
            "name": "Vitamin D Deficiency",
            "icd_code": "E55.9",
            "diagnosed_date": "Aug 2023",
            "status": "active",
            "severity": "mild",
            "treatments": "Vitamin D3 supplementation",
        },
        {
            "id": "4",
            "name": "Allergic Rhinitis",
            "icd_code": "J30.4",
            "diagnosed_date": "2015",
            "status": "resolved",
            "severity": "mild",
            "treatments": "Environmental management",
        },
    ]
    
    symptoms: List[Symptom] = [
        {
            "id": "1",
            "name": "Fatigue",
            "severity": "moderate",
            "frequency": "2-3 times per week",
            "trend": "improving",
        },
        {
            "id": "2",
            "name": "Headache",
            "severity": "mild",
            "frequency": "1-2 times per week",
            "trend": "stable",
        },
        {
            "id": "3",
            "name": "Joint Stiffness",
            "severity": "mild",
            "frequency": "Morning, daily",
            "trend": "improving",
        },
    ]
    
    symptom_logs: List[SymptomLog] = [
        {
            "id": "1",
            "symptom_name": "Fatigue",
            "severity": 5,
            "notes": "Felt tired after lunch, may be related to heavy meal",
            "timestamp": "Today, 2:30 PM",
        },
        {
            "id": "2",
            "symptom_name": "Headache",
            "severity": 3,
            "notes": "Mild headache in the morning, resolved with water",
            "timestamp": "Yesterday, 9:00 AM",
        },
        {
            "id": "3",
            "symptom_name": "Joint Stiffness",
            "severity": 4,
            "notes": "Morning stiffness lasted about 20 minutes",
            "timestamp": "Yesterday, 7:30 AM",
        },
    ]
    
    reminders: List[Reminder] = [
        {
            "id": "1",
            "title": "Take Metformin",
            "description": "500mg with breakfast",
            "time": "8:00 AM",
            "type": "medication",
            "completed": True,
        },
        {
            "id": "2",
            "title": "Blood Pressure Check",
            "description": "Log your morning reading",
            "time": "9:00 AM",
            "type": "checkup",
            "completed": False,
        },
        {
            "id": "3",
            "title": "Evening Walk",
            "description": "30 minutes moderate pace",
            "time": "6:00 PM",
            "type": "exercise",
            "completed": False,
        },
        {
            "id": "4",
            "title": "Take Lisinopril",
            "description": "10mg in the morning",
            "time": "8:30 AM",
            "type": "medication",
            "completed": True,
        },
        {
            "id": "5",
            "title": "Dr. Chen Appointment",
            "description": "Follow-up consultation",
            "time": "Tomorrow, 2:00 PM",
            "type": "appointment",
            "completed": False,
        },
    ]
    
    symptom_trends: List[SymptomTrend] = [
        {
            "id": "1",
            "symptom_name": "Fatigue",
            "current_severity": 5,
            "previous_severity": 7,
            "trend": "improving",
            "change_percent": 28.6,
            "period": "Last 7 days",
        },
        {
            "id": "2",
            "symptom_name": "Headache",
            "current_severity": 3,
            "previous_severity": 3,
            "trend": "stable",
            "change_percent": 0.0,
            "period": "Last 7 days",
        },
        {
            "id": "3",
            "symptom_name": "Joint Stiffness",
            "current_severity": 4,
            "previous_severity": 6,
            "trend": "improving",
            "change_percent": 33.3,
            "period": "Last 7 days",
        },
    ]
    
    data_sources: List[DataSource] = [
        {
            "id": "1",
            "name": "Apple Watch Series 9",
            "type": "wearable",
            "status": "connected",
            "icon": "watch",
            "image": "/devices/apple_watch.svg",
            "last_sync": "5 min ago",
            "connected": True,
        },
        {
            "id": "2",
            "name": "Withings Body+",
            "type": "scale",
            "status": "connected",
            "icon": "weight",
            "image": "/devices/withings_scale.svg",
            "last_sync": "2 hours ago",
            "connected": True,
        },
        {
            "id": "3",
            "name": "Oura Ring Gen 3",
            "type": "wearable",
            "status": "connected",
            "icon": "circle",
            "image": "/devices/oura_ring.svg",
            "last_sync": "1 hour ago",
            "connected": True,
        },
        {
            "id": "4",
            "name": "Dexcom G7",
            "type": "cgm",
            "status": "connected",
            "icon": "activity",
            "image": "/devices/dexcom_g7.svg",
            "last_sync": "Real-time",
            "connected": True,
        },
        {
            "id": "5",
            "name": "MyFitnessPal",
            "type": "app",
            "status": "connected",
            "icon": "smartphone",
            "image": "/devices/myfitnesspal.svg",
            "last_sync": "30 min ago",
            "connected": True,
        },
        {
            "id": "6",
            "name": "Epic MyChart",
            "type": "ehr",
            "status": "connected",
            "icon": "stethoscope",
            "image": "/devices/epic_mychart.svg",
            "last_sync": "1 day ago",
            "connected": True,
        },
    ]
    
    checkins: List[CheckIn] = [
        {
            "id": "1",
            "type": "voice",
            "summary": "Feeling good today, energy levels are up. Noticed some minor joint stiffness this morning but it went away after stretching.",
            "timestamp": "Today, 10:30 AM",
            "sentiment": "positive",
            "key_topics": ["energy", "joint stiffness", "exercise"],
            "provider_reviewed": False,
        },
        {
            "id": "2",
            "type": "text",
            "summary": "Had a headache yesterday evening. Took some water and rested, felt better after an hour.",
            "timestamp": "Yesterday, 8:15 PM",
            "sentiment": "neutral",
            "key_topics": ["headache", "hydration"],
            "provider_reviewed": True,
        },
        {
            "id": "3",
            "type": "voice",
            "summary": "Blood sugar has been stable this week. Following the new meal plan closely.",
            "timestamp": "2 days ago, 9:00 AM",
            "sentiment": "positive",
            "key_topics": ["blood sugar", "diet", "medication"],
            "provider_reviewed": True,
        },
    ]
    
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
                updated_sources.append({
                    **source,
                    "connected": new_connected,
                    "status": "connected" if new_connected else "disconnected",
                    "last_sync": "Just now" if new_connected else "Disconnected",
                })
            else:
                updated_sources.append(source)
        self.data_sources = updated_sources
    
    def set_checkin_type(self, checkin_type: str):
        """Set check-in type."""
        self.checkin_type = checkin_type
        # Reset recording state when switching types
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.transcription_status = "idle"
    
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
        
        result = await start_voice_recording()
        self.recording_session_id = result["session_id"]
    
    @rx.event
    async def stop_recording(self):
        """Stop voice recording and transcribe."""
        # Stop recording first
        self.is_recording = False
        self.transcription_status = "transcribing"
        
        # Stop and get audio
        await stop_voice_recording(self.recording_session_id)
        
        # Transcribe the audio
        transcription = await transcribe_voice_input(None)
        self.transcribed_text = transcription["text"]
        self.transcription_status = "done"
        
        # Extract topics from transcription
        topics_result = await extract_health_topics(self.transcribed_text)
        self.selected_topics = topics_result["topics"]
    
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
    
    def open_checkin_modal(self):
        """Open check-in modal."""
        self.show_checkin_modal = True
        # Reset state
        self.checkin_type = "voice"
        self.checkin_text = ""
        self.selected_topics = []
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.transcription_status = "idle"
    
    def close_checkin_modal(self):
        """Close check-in modal."""
        self.show_checkin_modal = False
        self.is_recording = False
        self.transcription_status = "idle"
    
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
        from datetime import datetime
        import uuid
        
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
            "total_calories": self.nutrition_summary["total_calories"] + new_entry["calories"],
            "total_protein": self.nutrition_summary["total_protein"] + new_entry["protein"],
            "total_carbs": self.nutrition_summary["total_carbs"] + new_entry["carbs"],
            "total_fat": self.nutrition_summary["total_fat"] + new_entry["fat"],
        }
        
        # Close modal
        self.show_add_food_modal = False
    
    @rx.event
    async def save_checkin(self):
        """Save a new check-in using the processing functions."""
        # Determine content based on type
        content = ""
        if self.checkin_type == "voice":
            content = self.transcribed_text
        else:
            # Process text input
            text_result = await process_text_checkin(self.checkin_text)
            if not text_result["is_valid"]:
                # Handle validation error
                return
            content = text_result["sanitized_text"]
        
        # Extract topics if not already done
        if not self.selected_topics and content:
            topics_result = await extract_health_topics(content)
            self.selected_topics = topics_result["topics"]
        
        # Save the check-in
        result = await save_checkin(
            checkin_type=self.checkin_type,
            content=content,
            topics=self.selected_topics,
        )
        
        if result["status"] == "success":
            # Add to local checkins list for demo
            from datetime import datetime
            new_checkin = {
                "id": result["checkin_id"],
                "type": self.checkin_type,
                "summary": content[:100] + "..." if len(content) > 100 else content,
                "timestamp": datetime.now().strftime("Today, %I:%M %p"),
                "sentiment": "neutral",
                "key_topics": self.selected_topics,
                "provider_reviewed": False,
            }
            self.checkins = [new_checkin, *self.checkins]
        
        self.show_checkin_modal = False
        # Reset state
        self.is_recording = False
        self.recording_duration = 0.0
        self.transcribed_text = ""
        self.checkin_text = ""
        self.selected_topics = []
        self.transcription_status = "idle"
    
    @rx.event
    async def save_symptom_log(self):
        """Save a symptom log entry using the processing functions."""
        if self.selected_symptom:
            result = await log_symptom(
                symptom_name=self.selected_symptom.get("name", "Unknown"),
                severity=5,  # Default - would come from form
                notes="",
            )
            if result["status"] == "success":
                # Add to local logs for demo
                from datetime import datetime
                new_log = {
                    "id": result["log_id"],
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
        result = await log_medication_dose(medication_id=medication_id)
        # Update UI or show confirmation
        self.show_medication_modal = False
    
    def load_dashboard_data(self):
        """Load dashboard data on mount."""
        # In a real app, this would fetch from database
        pass
