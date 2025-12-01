"""Patient dashboard state management."""

import reflex as rx
from typing import List, Dict, Any, TypedDict


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


class DataSource(TypedDict):
    """Data source type."""
    id: str
    name: str
    type: str
    status: str
    icon: str
    last_sync: str


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
    
    # Other modal states
    show_medication_modal: bool = False
    show_condition_modal: bool = False
    show_symptom_modal: bool = False
    show_connect_modal: bool = False
    
    # Selected items for modals
    selected_medication: Dict[str, Any] = {}
    selected_condition: Dict[str, Any] = {}
    selected_symptom: Dict[str, Any] = {}
    
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
    
    data_sources: List[DataSource] = [
        {
            "id": "1",
            "name": "Apple Watch Series 9",
            "type": "wearable",
            "status": "connected",
            "icon": "watch",
            "last_sync": "5 min ago",
        },
        {
            "id": "2",
            "name": "Withings Body+",
            "type": "scale",
            "status": "connected",
            "icon": "weight",
            "last_sync": "2 hours ago",
        },
        {
            "id": "3",
            "name": "Oura Ring Gen 3",
            "type": "wearable",
            "status": "connected",
            "icon": "circle",
            "last_sync": "1 hour ago",
        },
        {
            "id": "4",
            "name": "Dexcom G7",
            "type": "cgm",
            "status": "connected",
            "icon": "activity",
            "last_sync": "Real-time",
        },
        {
            "id": "5",
            "name": "MyFitnessPal",
            "type": "app",
            "status": "connected",
            "icon": "smartphone",
            "last_sync": "30 min ago",
        },
        {
            "id": "6",
            "name": "Epic MyChart",
            "type": "ehr",
            "status": "connected",
            "icon": "stethoscope",
            "last_sync": "1 day ago",
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
        return len([s for s in self.data_sources if s["status"] == "connected"])
    
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
    
    def set_checkin_type(self, checkin_type: str):
        """Set check-in type."""
        self.checkin_type = checkin_type
    
    def open_checkin_modal(self):
        """Open check-in modal."""
        self.show_checkin_modal = True
    
    def close_checkin_modal(self):
        """Close check-in modal."""
        self.show_checkin_modal = False
    
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
    
    def save_checkin(self):
        """Save a new check-in."""
        # In a real app, this would save to database
        self.show_checkin_modal = False
    
    def save_symptom_log(self):
        """Save a symptom log entry."""
        # In a real app, this would save to database
        self.show_symptom_modal = False
    
    def load_dashboard_data(self):
        """Load dashboard data on mount."""
        # In a real app, this would fetch from database
        pass
