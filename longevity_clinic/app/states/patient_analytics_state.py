import reflex as rx
from typing import TypedDict
import random


class BiomarkerMetric(TypedDict):
    name: str
    value: float
    unit: str
    status: str
    reference_range: str
    history: list[dict]


class BiomarkerCategory(TypedDict):
    category: str
    metrics: list[BiomarkerMetric]


class PatientAnalyticsState(rx.State):
    active_tab: str = "Overview"

    def _generate_history(self, base_val, volatility) -> list[dict]:
        data = []
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        current = base_val
        for m in months:
            current += random.uniform(-volatility, volatility)
            data.append({"date": m, "value": round(current, 1)})
        return data

    @rx.var
    def biomarker_panels(self) -> list[BiomarkerCategory]:
        return [
            {
                "category": "Complete Blood Count (CBC)",
                "metrics": [
                    {
                        "name": "Red Blood Cells",
                        "value": 4.8,
                        "unit": "M/uL",
                        "status": "Optimal",
                        "reference_range": "4.5 - 5.9",
                        "history": self._generate_history(4.8, 0.2),
                    },
                    {
                        "name": "White Blood Cells",
                        "value": 6.2,
                        "unit": "K/uL",
                        "status": "Optimal",
                        "reference_range": "4.0 - 11.0",
                        "history": self._generate_history(6.2, 0.5),
                    },
                    {
                        "name": "Hemoglobin",
                        "value": 14.5,
                        "unit": "g/dL",
                        "status": "Optimal",
                        "reference_range": "13.5 - 17.5",
                        "history": self._generate_history(14.5, 0.3),
                    },
                    {
                        "name": "Hematocrit",
                        "value": 42.0,
                        "unit": "%",
                        "status": "Optimal",
                        "reference_range": "37.0 - 50.0",
                        "history": self._generate_history(42.0, 1.5),
                    },
                    {
                        "name": "Platelets",
                        "value": 250.0,
                        "unit": "K/uL",
                        "status": "Optimal",
                        "reference_range": "150 - 450",
                        "history": self._generate_history(250, 20),
                    },
                ],
            },
            {
                "category": "Metabolic Panel",
                "metrics": [
                    {
                        "name": "Glucose (Fasting)",
                        "value": 92.0,
                        "unit": "mg/dL",
                        "status": "Optimal",
                        "reference_range": "65 - 99",
                        "history": self._generate_history(90, 5),
                    },
                    {
                        "name": "HbA1c",
                        "value": 5.7,
                        "unit": "%",
                        "status": "Warning",
                        "reference_range": "< 5.7",
                        "history": self._generate_history(5.6, 0.1),
                    },
                    {
                        "name": "Insulin",
                        "value": 6.5,
                        "unit": "uIU/mL",
                        "status": "Optimal",
                        "reference_range": "2.6 - 24.9",
                        "history": self._generate_history(6.5, 1.2),
                    },
                    {
                        "name": "Creatinine",
                        "value": 0.9,
                        "unit": "mg/dL",
                        "status": "Optimal",
                        "reference_range": "0.7 - 1.3",
                        "history": self._generate_history(0.9, 0.1),
                    },
                ],
            },
            {
                "category": "Lipid Panel",
                "metrics": [
                    {
                        "name": "Total Cholesterol",
                        "value": 185.0,
                        "unit": "mg/dL",
                        "status": "Optimal",
                        "reference_range": "< 200",
                        "history": self._generate_history(180, 10),
                    },
                    {
                        "name": "LDL Cholesterol",
                        "value": 115.0,
                        "unit": "mg/dL",
                        "status": "Warning",
                        "reference_range": "< 100",
                        "history": self._generate_history(110, 5),
                    },
                    {
                        "name": "HDL Cholesterol",
                        "value": 55.0,
                        "unit": "mg/dL",
                        "status": "Optimal",
                        "reference_range": "> 40",
                        "history": self._generate_history(55, 2),
                    },
                    {
                        "name": "Triglycerides",
                        "value": 95.0,
                        "unit": "mg/dL",
                        "status": "Optimal",
                        "reference_range": "< 150",
                        "history": self._generate_history(95, 15),
                    },
                ],
            },
            {
                "category": "Hormones",
                "metrics": [
                    {
                        "name": "Testosterone (Total)",
                        "value": 550.0,
                        "unit": "ng/dL",
                        "status": "Optimal",
                        "reference_range": "300 - 1000",
                        "history": self._generate_history(550, 30),
                    },
                    {
                        "name": "Estradiol",
                        "value": 25.0,
                        "unit": "pg/mL",
                        "status": "Optimal",
                        "reference_range": "10 - 40",
                        "history": self._generate_history(25, 5),
                    },
                    {
                        "name": "Cortisol (AM)",
                        "value": 18.5,
                        "unit": "mcg/dL",
                        "status": "Warning",
                        "reference_range": "10 - 20",
                        "history": self._generate_history(18, 3),
                    },
                    {
                        "name": "TSH",
                        "value": 1.8,
                        "unit": "mIU/L",
                        "status": "Optimal",
                        "reference_range": "0.4 - 4.0",
                        "history": self._generate_history(1.8, 0.2),
                    },
                ],
            },
            {
                "category": "Vitamins & Minerals",
                "metrics": [
                    {
                        "name": "Vitamin D",
                        "value": 28.0,
                        "unit": "ng/mL",
                        "status": "Critical",
                        "reference_range": "30 - 100",
                        "history": self._generate_history(28, 2),
                    },
                    {
                        "name": "Vitamin B12",
                        "value": 450.0,
                        "unit": "pg/mL",
                        "status": "Optimal",
                        "reference_range": "200 - 900",
                        "history": self._generate_history(450, 50),
                    },
                    {
                        "name": "Ferritin",
                        "value": 45.0,
                        "unit": "ng/mL",
                        "status": "Optimal",
                        "reference_range": "30 - 400",
                        "history": self._generate_history(45, 5),
                    },
                    {
                        "name": "Magnesium",
                        "value": 2.1,
                        "unit": "mg/dL",
                        "status": "Optimal",
                        "reference_range": "1.7 - 2.2",
                        "history": self._generate_history(2.1, 0.1),
                    },
                ],
            },
            {
                "category": "Inflammation",
                "metrics": [
                    {
                        "name": "hs-CRP",
                        "value": 0.8,
                        "unit": "mg/L",
                        "status": "Optimal",
                        "reference_range": "< 1.0",
                        "history": self._generate_history(0.8, 0.3),
                    },
                    {
                        "name": "Homocysteine",
                        "value": 8.5,
                        "unit": "umol/L",
                        "status": "Optimal",
                        "reference_range": "< 10.0",
                        "history": self._generate_history(8.5, 1.0),
                    },
                ],
            },
        ]

    @rx.event
    def export_report(self):
        return rx.toast("Analytics report downloaded successfully.", duration=3000)