"""Biomarker seed data for the Longevity Clinic.

Contains:
- Biomarker metric seed data (for biomarker state)
- Biomarker chart data (for dashboard charts)
- Portal biomarkers (patient-facing detailed view)
"""

from __future__ import annotations

from typing import Dict, List

# Import biomarker types
from ..biomarkers import (
    BiomarkerCategoryEnum,
    BiomarkerMetricName,
    BiomarkerMetricSeed,
    BiomarkerStatus,
    MeasurementUnit,
)


# =============================================================================
# Biomarker Metric Seed Data (organized by category)
# =============================================================================

BIOMARKER_METRIC_SEED_DATA: Dict[BiomarkerCategoryEnum, List[BiomarkerMetricSeed]] = {
    BiomarkerCategoryEnum.CBC: [
        {
            "metric": BiomarkerMetricName.RED_BLOOD_CELLS,
            "value": 4.8,
            "unit": MeasurementUnit.MILLIONS_PER_MICROLITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "4.5 - 5.9",
            "history_seed": (4.8, 0.2),
        },
        {
            "metric": BiomarkerMetricName.WHITE_BLOOD_CELLS,
            "value": 6.2,
            "unit": MeasurementUnit.THOUSANDS_PER_MICROLITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "4.0 - 11.0",
            "history_seed": (6.2, 0.5),
        },
        {
            "metric": BiomarkerMetricName.HEMOGLOBIN,
            "value": 14.5,
            "unit": MeasurementUnit.GRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "13.5 - 17.5",
            "history_seed": (14.5, 0.3),
        },
        {
            "metric": BiomarkerMetricName.HEMATOCRIT,
            "value": 42.0,
            "unit": MeasurementUnit.PERCENT,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "37.0 - 50.0",
            "history_seed": (42.0, 1.5),
        },
        {
            "metric": BiomarkerMetricName.PLATELETS,
            "value": 250.0,
            "unit": MeasurementUnit.THOUSANDS_PER_MICROLITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "150 - 450",
            "history_seed": (250.0, 20.0),
        },
    ],
    BiomarkerCategoryEnum.METABOLIC_PANEL: [
        {
            "metric": BiomarkerMetricName.GLUCOSE_FASTING,
            "value": 92.0,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "65 - 99",
            "history_seed": (90.0, 5.0),
        },
        {
            "metric": BiomarkerMetricName.HBA1C,
            "value": 5.7,
            "unit": MeasurementUnit.PERCENT,
            "status": BiomarkerStatus.WARNING,
            "reference_range": "< 5.7",
            "history_seed": (5.6, 0.1),
        },
        {
            "metric": BiomarkerMetricName.INSULIN,
            "value": 6.5,
            "unit": MeasurementUnit.MICROINTERNATIONAL_UNITS_PER_ML,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "2.6 - 24.9",
            "history_seed": (6.5, 1.2),
        },
        {
            "metric": BiomarkerMetricName.CREATININE,
            "value": 0.9,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "0.7 - 1.3",
            "history_seed": (0.9, 0.1),
        },
    ],
    BiomarkerCategoryEnum.LIPID_PANEL: [
        {
            "metric": BiomarkerMetricName.TOTAL_CHOLESTEROL,
            "value": 185.0,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "< 200",
            "history_seed": (180.0, 10.0),
        },
        {
            "metric": BiomarkerMetricName.LDL_CHOLESTEROL,
            "value": 115.0,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.WARNING,
            "reference_range": "< 100",
            "history_seed": (110.0, 5.0),
        },
        {
            "metric": BiomarkerMetricName.HDL_CHOLESTEROL,
            "value": 55.0,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "> 40",
            "history_seed": (55.0, 2.0),
        },
        {
            "metric": BiomarkerMetricName.TRIGLYCERIDES,
            "value": 95.0,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "< 150",
            "history_seed": (95.0, 15.0),
        },
    ],
    BiomarkerCategoryEnum.HORMONES: [
        {
            "metric": BiomarkerMetricName.TESTOSTERONE_TOTAL,
            "value": 550.0,
            "unit": MeasurementUnit.NANOGRAMS_PER_ML,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "300 - 1000",
            "history_seed": (550.0, 30.0),
        },
        {
            "metric": BiomarkerMetricName.ESTRADIOL,
            "value": 25.0,
            "unit": MeasurementUnit.PICOGRAMS_PER_ML,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "10 - 40",
            "history_seed": (25.0, 5.0),
        },
        {
            "metric": BiomarkerMetricName.CORTISOL_AM,
            "value": 18.5,
            "unit": MeasurementUnit.MICROGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.WARNING,
            "reference_range": "10 - 20",
            "history_seed": (18.0, 3.0),
        },
        {
            "metric": BiomarkerMetricName.TSH,
            "value": 1.8,
            "unit": MeasurementUnit.MILLIINTERNATIONAL_UNITS_PER_L,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "0.4 - 4.0",
            "history_seed": (1.8, 0.2),
        },
    ],
    BiomarkerCategoryEnum.VITAMINS_MINERALS: [
        {
            "metric": BiomarkerMetricName.VITAMIN_D,
            "value": 28.0,
            "unit": MeasurementUnit.NANOGRAMS_PER_ML,
            "status": BiomarkerStatus.CRITICAL,
            "reference_range": "30 - 100",
            "history_seed": (28.0, 2.0),
        },
        {
            "metric": BiomarkerMetricName.VITAMIN_B12,
            "value": 450.0,
            "unit": MeasurementUnit.PICOGRAMS_PER_ML,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "200 - 900",
            "history_seed": (450.0, 50.0),
        },
        {
            "metric": BiomarkerMetricName.FERRITIN,
            "value": 45.0,
            "unit": MeasurementUnit.NANOGRAMS_PER_ML,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "30 - 400",
            "history_seed": (45.0, 5.0),
        },
        {
            "metric": BiomarkerMetricName.MAGNESIUM,
            "value": 2.1,
            "unit": MeasurementUnit.MILLIGRAMS_PER_DECILITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "1.7 - 2.2",
            "history_seed": (2.1, 0.1),
        },
    ],
    BiomarkerCategoryEnum.INFLAMMATION: [
        {
            "metric": BiomarkerMetricName.HS_CRP,
            "value": 0.8,
            "unit": MeasurementUnit.MILLIGRAMS_PER_LITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "< 1.0",
            "history_seed": (0.8, 0.3),
        },
        {
            "metric": BiomarkerMetricName.HOMOCYSTEINE,
            "value": 8.5,
            "unit": MeasurementUnit.MICROMOLES_PER_LITER,
            "status": BiomarkerStatus.OPTIMAL,
            "reference_range": "< 10.0",
            "history_seed": (8.5, 1.0),
        },
    ],
}


# =============================================================================
# Biomarker Chart Seed Data (simple score format)
# =============================================================================

BIOMARKER_CHART_SEED: List[dict] = [
    {"name": "Wk 1", "score": 65},
    {"name": "Wk 4", "score": 72},
    {"name": "Wk 8", "score": 78},
    {"name": "Wk 12", "score": 82},
    {"name": "Wk 16", "score": 88},
]


# =============================================================================
# Portal Biomarkers Seed (patient-facing detailed view)
# =============================================================================

PORTAL_BIOMARKERS_SEED: List[dict] = [
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


__all__ = [
    "BIOMARKER_METRIC_SEED_DATA",
    "BIOMARKER_CHART_SEED",
    "PORTAL_BIOMARKERS_SEED",
]
