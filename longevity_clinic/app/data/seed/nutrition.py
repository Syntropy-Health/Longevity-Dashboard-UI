"""Nutrition, medication, and symptom seed data for the Longevity Clinic.

Contains:
- Nutrition summary and food entries
- Medication data
- Condition data
- Symptom tracking data
- Reminders and data sources
"""

from __future__ import annotations

# Import types from state_schemas
from ..state_schemas import (
    Condition,
    DataSource,
    FoodEntry,
    MedicationEntry,
    NutritionSummary,
    Reminder,
    Symptom,
    SymptomEntry,
    SymptomTrend,
)

# =============================================================================
# Nutrition Seed Data
# =============================================================================

NUTRITION_SUMMARY_SEED: NutritionSummary = {
    "total_calories": 1850,
    "goal_calories": 2200,
    "total_protein": 95.5,
    "total_carbs": 180.0,
    "total_fat": 65.0,
    "water_intake": 2.4,
}

FOOD_ENTRIES_SEED: list[FoodEntry] = [
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


# =============================================================================
# Medication Seed Data
# =============================================================================

MEDICATIONS_SEED: list[MedicationEntry] = [
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


# =============================================================================
# Condition Seed Data
# =============================================================================

CONDITIONS_SEED: list[Condition] = [
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


# =============================================================================
# Symptom Seed Data
# =============================================================================

SYMPTOMS_SEED: list[Symptom] = [
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

SYMPTOM_LOGS_SEED: list[SymptomEntry] = [
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

SYMPTOM_TRENDS_SEED: list[SymptomTrend] = [
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


# =============================================================================
# Reminder Seed Data
# =============================================================================

REMINDERS_SEED: list[Reminder] = [
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


# =============================================================================
# Data Sources Seed Data (connected devices/apps)
# =============================================================================

DATA_SOURCES_SEED: list[DataSource] = [
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


__all__ = [
    "CONDITIONS_SEED",
    "DATA_SOURCES_SEED",
    "FOOD_ENTRIES_SEED",
    "MEDICATIONS_SEED",
    "NUTRITION_SUMMARY_SEED",
    "REMINDERS_SEED",
    "SYMPTOMS_SEED",
    "SYMPTOM_LOGS_SEED",
    "SYMPTOM_TRENDS_SEED",
]
