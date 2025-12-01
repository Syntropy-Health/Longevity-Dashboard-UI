import reflex as rx
from typing import TypedDict, Optional
import random
from datetime import datetime, timedelta

from ..data import BIOMARKER_SIMPLE_CATEGORIES, BIOMARKER_STATUSES, BIOMARKER_TRENDS


class BiomarkerDataPoint(TypedDict):
    date: str
    value: float


class Biomarker(TypedDict):
    id: str
    name: str
    category: str
    unit: str
    description: str
    optimal_min: float
    optimal_max: float
    critical_min: float
    critical_max: float
    current_value: float
    status: str
    trend: str
    history: list[BiomarkerDataPoint]


class PortalAppointment(TypedDict):
    id: str
    title: str
    date: str
    time: str
    type: str
    provider: str


class PortalTreatment(TypedDict):
    id: str
    name: str
    frequency: str
    duration: str
    category: str
    status: str


class PatientBiomarkerState(rx.State):
    biomarkers: list[Biomarker] = [
        {
            "id": "bio_1",
            "name": "Vitamin D (25-OH)",
            "category": "Metabolic",
            "unit": "ng/mL",
            "description": "Crucial for bone health, immune function, and mood regulation.",
            "optimal_min": 40.0,
            "optimal_max": 80.0,
            "critical_min": 20.0,
            "critical_max": 100.0,
            "current_value": 45.2,
            "status": "Optimal",
            "trend": "up",
            "history": [
                {"date": "Jan", "value": 28.5},
                {"date": "Mar", "value": 32.1},
                {"date": "May", "value": 38.4},
                {"date": "Jul", "value": 42.0},
                {"date": "Sep", "value": 45.2},
            ],
        },
        {
            "id": "bio_2",
            "name": "hs-CRP",
            "category": "Inflammation",
            "unit": "mg/L",
            "description": "High-sensitivity C-reactive protein, a marker of systemic inflammation.",
            "optimal_min": 0.0,
            "optimal_max": 1.0,
            "critical_min": 0.0,
            "critical_max": 3.0,
            "current_value": 0.8,
            "status": "Optimal",
            "trend": "down",
            "history": [
                {"date": "Jan", "value": 2.4},
                {"date": "Mar", "value": 1.8},
                {"date": "May", "value": 1.2},
                {"date": "Jul", "value": 0.9},
                {"date": "Sep", "value": 0.8},
            ],
        },
        {
            "id": "bio_3",
            "name": "Total Testosterone",
            "category": "Hormones",
            "unit": "ng/dL",
            "description": "Primary male sex hormone, vital for muscle mass, density, and libido.",
            "optimal_min": 600.0,
            "optimal_max": 900.0,
            "critical_min": 300.0,
            "critical_max": 1200.0,
            "current_value": 550.0,
            "status": "Warning",
            "trend": "stable",
            "history": [
                {"date": "Jan", "value": 480.0},
                {"date": "Mar", "value": 510.0},
                {"date": "May", "value": 530.0},
                {"date": "Jul", "value": 545.0},
                {"date": "Sep", "value": 550.0},
            ],
        },
        {
            "id": "bio_4",
            "name": "HbA1c",
            "category": "Metabolic",
            "unit": "%",
            "description": "Average blood sugar (glucose) levels over the past two to three months.",
            "optimal_min": 4.0,
            "optimal_max": 5.6,
            "critical_min": 3.0,
            "critical_max": 6.5,
            "current_value": 5.2,
            "status": "Optimal",
            "trend": "stable",
            "history": [
                {"date": "Jan", "value": 5.4},
                {"date": "Mar", "value": 5.3},
                {"date": "May", "value": 5.3},
                {"date": "Jul", "value": 5.2},
                {"date": "Sep", "value": 5.2},
            ],
        },
        {
            "id": "bio_5",
            "name": "Cortisol (AM)",
            "category": "Hormones",
            "unit": "mcg/dL",
            "description": "Stress hormone. High levels can indicate chronic stress or adrenal issues.",
            "optimal_min": 10.0,
            "optimal_max": 20.0,
            "critical_min": 5.0,
            "critical_max": 25.0,
            "current_value": 22.5,
            "status": "Critical",
            "trend": "up",
            "history": [
                {"date": "Jan", "value": 16.0},
                {"date": "Mar", "value": 18.5},
                {"date": "May", "value": 19.0},
                {"date": "Jul", "value": 21.2},
                {"date": "Sep", "value": 22.5},
            ],
        },
    ]
    selected_biomarker: Optional[Biomarker] = None
    my_treatments: list[PortalTreatment] = [
        {
            "id": "t1",
            "name": "Vitamin C IV Drip",
            "frequency": "Weekly",
            "duration": "45 mins",
            "category": "IV Therapy",
            "status": "Active",
        },
        {
            "id": "t2",
            "name": "Cryotherapy Session",
            "frequency": "Bi-Weekly",
            "duration": "10 mins",
            "category": "Recovery",
            "status": "Active",
        },
        {
            "id": "t3",
            "name": "Magnesium Supplementation",
            "frequency": "Daily",
            "duration": "Ongoing",
            "category": "Supplements",
            "status": "Active",
        },
    ]
    upcoming_appointments: list[PortalAppointment] = [
        {
            "id": "a1",
            "title": "IV Therapy Session",
            "date": "Today",
            "time": "2:00 PM",
            "type": "Treatment",
            "provider": "Nurse Jackie",
        },
        {
            "id": "a2",
            "title": "Physician Consultation",
            "date": "Oct 24",
            "time": "10:30 AM",
            "type": "Consultation",
            "provider": "Dr. Administrator",
        },
        {
            "id": "a3",
            "title": "Blood Panel Draw",
            "date": "Nov 01",
            "time": "8:15 AM",
            "type": "Lab Work",
            "provider": "Lab Tech",
        },
    ]

    @rx.event
    def select_biomarker(self, biomarker: Biomarker):
        self.selected_biomarker = biomarker

    @rx.event
    def clear_selected_biomarker(self):
        self.selected_biomarker = None

    @rx.var
    def selected_biomarker_history(self) -> list[BiomarkerDataPoint]:
        if self.selected_biomarker:
            return self.selected_biomarker["history"]
        return []

    @rx.var
    def selected_biomarker_name(self) -> str:
        return self.selected_biomarker["name"] if self.selected_biomarker else ""

    @rx.var
    def selected_biomarker_optimal_range(self) -> dict:
        if self.selected_biomarker:
            return {
                "min": self.selected_biomarker["optimal_min"],
                "max": self.selected_biomarker["optimal_max"],
            }
        return {"min": 0, "max": 0}