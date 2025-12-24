"""
Domain enumerations for Longevity Clinic application.

These StrEnum classes define the allowed values for various domain concepts:
- Treatment categories, frequencies, statuses
- Biomarker categories, metrics, statuses, units
- Patient statuses
- Health keywords for topic extraction

Unlike enum tables in enums.py (rx.Model classes for referential integrity),
these are pure Python enumerations for type-safe value constraints.

Usage:
    from longevity_clinic.app.data.schemas.db import (
        TreatmentCategoryEnum, BiomarkerCategoryEnum, HealthKeyword
    )
"""

from enum import StrEnum
from typing import Final


def _enum_values(enum_cls: type[StrEnum]) -> list[str]:
    """Return the string values of a StrEnum for compatibility exports."""
    return [member.value for member in enum_cls]


# =============================================================================
# TREATMENT ENUMS
# =============================================================================


class TreatmentCategoryEnum(StrEnum):
    """Treatment category codes for clinic services."""

    IV_THERAPY = "IV Therapy"
    CRYOTHERAPY = "Cryotherapy"
    SUPPLEMENTS = "Supplements"
    HORMONE_THERAPY = "Hormone Therapy"
    PHYSICAL_THERAPY = "Physical Therapy"
    SPA_SERVICES = "Spa Services"


class TreatmentFrequencyEnum(StrEnum):
    """Treatment frequency options."""

    DAILY = "Daily"
    WEEKLY = "Weekly"
    BI_WEEKLY = "Bi-Weekly"
    MONTHLY = "Monthly"
    AS_NEEDED = "As-needed"


class TreatmentStatusEnum(StrEnum):
    """Treatment lifecycle statuses."""

    ACTIVE = "Active"
    ARCHIVED = "Archived"
    DRAFT = "Draft"


class PatientStatusEnum(StrEnum):
    """Patient enrollment statuses."""

    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ONBOARDING = "Onboarding"


# Legacy list exports for backwards compatibility
TREATMENT_CATEGORIES: Final[list[str]] = _enum_values(TreatmentCategoryEnum)
TREATMENT_FREQUENCIES: Final[list[str]] = _enum_values(TreatmentFrequencyEnum)
TREATMENT_STATUSES: Final[list[str]] = _enum_values(TreatmentStatusEnum)
PATIENT_STATUSES: Final[list[str]] = _enum_values(PatientStatusEnum)


# =============================================================================
# BIOMARKER ENUMS
# =============================================================================


class BiomarkerCategoryEnum(StrEnum):
    """Biomarker panel categories (detailed)."""

    CBC = "Complete Blood Count (CBC)"
    METABOLIC_PANEL = "Metabolic Panel"
    LIPID_PANEL = "Lipid Panel"
    HORMONES = "Hormones"
    VITAMINS_MINERALS = "Vitamins & Minerals"
    INFLAMMATION = "Inflammation"


class BiomarkerSimpleCategoryEnum(StrEnum):
    """Simplified biomarker categories for dashboards."""

    METABOLIC = "Metabolic"
    INFLAMMATION = "Inflammation"
    HORMONES = "Hormones"


class MeasurementUnitEnum(StrEnum):
    """Standard units for biomarker measurements."""

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


class BiomarkerMetricNameEnum(StrEnum):
    """Standard biomarker metric names."""

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


class BiomarkerStatusEnum(StrEnum):
    """Biomarker reading status indicators."""

    OPTIMAL = "Optimal"
    WARNING = "Warning"
    CRITICAL = "Critical"


class BiomarkerTrendEnum(StrEnum):
    """Biomarker trend direction indicators."""

    UP = "up"
    DOWN = "down"
    STABLE = "stable"


# Legacy list exports for backwards compatibility
BIOMARKER_CATEGORIES: Final[list[str]] = _enum_values(BiomarkerCategoryEnum)
BIOMARKER_SIMPLE_CATEGORIES: Final[list[str]] = _enum_values(
    BiomarkerSimpleCategoryEnum
)
BIOMARKER_STATUSES: Final[list[str]] = _enum_values(BiomarkerStatusEnum)
BIOMARKER_TRENDS: Final[list[str]] = _enum_values(BiomarkerTrendEnum)


# =============================================================================
# HEALTH KEYWORDS
# =============================================================================


class HealthKeywordEnum(StrEnum):
    """Health keywords for topic extraction from check-in transcripts."""

    FATIGUE = "fatigue"
    TIRED = "tired"
    ENERGY = "energy"
    SLEEP = "sleep"
    PAIN = "pain"
    JOINT = "joint"
    HEADACHE = "headache"
    ANXIETY = "anxiety"
    STRESS = "stress"
    BLOOD_PRESSURE = "blood pressure"
    HEART = "heart"
    BLOOD_SUGAR = "blood sugar"
    DIET = "diet"
    MEDICATION = "medication"
    EXERCISE = "exercise"
    BREATHING = "breathing"


HEALTH_KEYWORDS: Final[list[str]] = _enum_values(HealthKeywordEnum)


__all__ = [
    # Treatment enums
    "TreatmentCategoryEnum",
    "TreatmentFrequencyEnum",
    "TreatmentStatusEnum",
    "PatientStatusEnum",
    "TREATMENT_CATEGORIES",
    "TREATMENT_FREQUENCIES",
    "TREATMENT_STATUSES",
    "PATIENT_STATUSES",
    # Biomarker enums
    "BiomarkerCategoryEnum",
    "BiomarkerSimpleCategoryEnum",
    "MeasurementUnitEnum",
    "BiomarkerMetricNameEnum",
    "BiomarkerStatusEnum",
    "BiomarkerTrendEnum",
    "BIOMARKER_CATEGORIES",
    "BIOMARKER_SIMPLE_CATEGORIES",
    "BIOMARKER_STATUSES",
    "BIOMARKER_TRENDS",
    # Health keywords
    "HealthKeywordEnum",
    "HEALTH_KEYWORDS",
]
