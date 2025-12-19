"""Biomarker utilities that hydrate demo data into UI-friendly structures."""

import random
from enum import StrEnum
from typing import Final, TypedDict


def _enum_values(enum_cls: type[StrEnum]) -> list[str]:
    """Return the string values of a StrEnum for compatibility exports."""

    return [member.value for member in enum_cls]


class BiomarkerCategoryEnum(StrEnum):
    CBC = "Complete Blood Count (CBC)"
    METABOLIC_PANEL = "Metabolic Panel"
    LIPID_PANEL = "Lipid Panel"
    HORMONES = "Hormones"
    VITAMINS_MINERALS = "Vitamins & Minerals"
    INFLAMMATION = "Inflammation"


class BiomarkerSimpleCategoryEnum(StrEnum):
    METABOLIC = "Metabolic"
    INFLAMMATION = "Inflammation"
    HORMONES = "Hormones"


class MeasurementUnit(StrEnum):
    MILLIONS_PER_MICROLITER = "M/uL"
    THOUSANDS_PER_MICROLITER = "K/uL"
    GRAMS_PER_DECILITER = "g/dL"
    PERCENT = "%"
    MILLIGRAMS_PER_DECILITER = "mg/dL"
    MICROINTERNATIONAL_UNITS_PER_ML = "uIU/mL"
    MICROGRAMS_PER_DECILITER = "mcg/dL"
    MILLIINTERNATIONAL_UNITS_PER_L = "mIU/L"
    NANOGRAMS_PER_ML = "ng/mL"
    PICOGRAMS_PER_ML = "pg/mL"
    MILLIGRAMS_PER_LITER = "mg/L"
    MICROMOLES_PER_LITER = "umol/L"


class BiomarkerMetricName(StrEnum):
    RED_BLOOD_CELLS = "Red Blood Cells"
    WHITE_BLOOD_CELLS = "White Blood Cells"
    HEMOGLOBIN = "Hemoglobin"
    HEMATOCRIT = "Hematocrit"
    PLATELETS = "Platelets"
    GLUCOSE_FASTING = "Glucose (Fasting)"
    HBA1C = "HbA1c"
    INSULIN = "Insulin"
    CREATININE = "Creatinine"
    TOTAL_CHOLESTEROL = "Total Cholesterol"
    LDL_CHOLESTEROL = "LDL Cholesterol"
    HDL_CHOLESTEROL = "HDL Cholesterol"
    TRIGLYCERIDES = "Triglycerides"
    TESTOSTERONE_TOTAL = "Testosterone (Total)"
    ESTRADIOL = "Estradiol"
    CORTISOL_AM = "Cortisol (AM)"
    TSH = "TSH"
    VITAMIN_D = "Vitamin D"
    VITAMIN_B12 = "Vitamin B12"
    FERRITIN = "Ferritin"
    MAGNESIUM = "Magnesium"
    HS_CRP = "hs-CRP"
    HOMOCYSTEINE = "Homocysteine"


class BiomarkerStatus(StrEnum):
    OPTIMAL = "Optimal"
    WARNING = "Warning"
    CRITICAL = "Critical"


class BiomarkerTrend(StrEnum):
    UP = "up"
    DOWN = "down"
    STABLE = "stable"


BIOMARKER_CATEGORIES: Final[list[str]] = _enum_values(BiomarkerCategoryEnum)
BIOMARKER_SIMPLE_CATEGORIES: Final[list[str]] = _enum_values(
    BiomarkerSimpleCategoryEnum
)
BIOMARKER_STATUSES: Final[list[str]] = _enum_values(BiomarkerStatus)
BIOMARKER_TRENDS: Final[list[str]] = _enum_values(BiomarkerTrend)


class BiomarkerMetricSeed(TypedDict):
    """Seed data used to build biomarker metrics with generated history."""

    metric: BiomarkerMetricName
    value: float
    unit: MeasurementUnit
    status: BiomarkerStatus
    reference_range: str
    history_seed: tuple[float, float]


class BiomarkerMetric(TypedDict):
    """Type definition for a single biomarker metric."""

    name: str
    value: float
    unit: str
    status: str
    reference_range: str
    history: list[dict]


class BiomarkerCategory(TypedDict):
    """Type definition for a biomarker category panel."""

    category: str
    metrics: list[BiomarkerMetric]


def generate_history(base_val: float, volatility: float) -> list[dict]:
    """
    Generate historical biomarker data with random variations.

    Args:
        base_val: Starting value for the biomarker
        volatility: Maximum variation (+/-) for each data point

    Returns:
        List of dictionaries with date and value for the last 6 months
    """
    data = []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    current = base_val
    for m in months:
        current += random.uniform(-volatility, volatility)
        data.append({"date": m, "value": round(current, 1)})
    return data


def get_biomarker_panels(user_id: int | None = None) -> list[BiomarkerCategory]:
    """Get biomarker panels for display.

    In demo mode, returns demo data from seed.
    Otherwise, fetches from database.

    Args:
        user_id: Optional user ID for patient-specific readings.

    Returns:
        List of biomarker panels grouped by category.
    """
    from longevity_clinic.app.config import current_config

    if current_config.is_demo:
        # Use demo data from seed
        from .seed import BIOMARKER_METRIC_SEED_DATA

        panels = []
        for category in BiomarkerCategoryEnum:
            metrics = BIOMARKER_METRIC_SEED_DATA.get(category, [])
            panel_metrics = []
            for metric in metrics:
                base, volatility = metric["history_seed"]
                panel_metrics.append(
                    {
                        "name": metric["metric"].value,
                        "value": metric["value"],
                        "unit": metric["unit"].value,
                        "status": metric["status"].value,
                        "reference_range": metric["reference_range"],
                        "history": generate_history(base, volatility),
                    }
                )
            panels.append(
                {
                    "category": category.value,
                    "metrics": panel_metrics,
                }
            )
        return panels

    # Fetch from database
    from longevity_clinic.app.functions.db_utils import get_biomarker_panels_sync

    return get_biomarker_panels_sync(user_id=user_id)
