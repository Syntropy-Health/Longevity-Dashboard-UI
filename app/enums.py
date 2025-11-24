from enum import StrEnum
from typing import Final


def _enum_values(enum_class) -> list[str]:
    return [e.value for e in enum_class]


class TreatmentFrequency(StrEnum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    BI_WEEKLY = "Bi-Weekly"
    MONTHLY = "Monthly"
    AS_NEEDED = "As-needed"


TREATMENT_FREQUENCIES: Final[list[str]] = _enum_values(TreatmentFrequency)


class TreatmentStatus(StrEnum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"
    DRAFT = "Draft"


class PatientStatus(StrEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ONBOARDING = "Onboarding"


class TreatmentCategory(StrEnum):
    IV_THERAPY = "IV Therapy"
    CRYOTHERAPY = "Cryotherapy"
    SUPPLEMENTS = "Supplements"
    HORMONE_THERAPY = "Hormone Therapy"
    PHYSICAL_THERAPY = "Physical Therapy"
    SPA_SERVICES = "Spa Services"
    PEPTIDES = "Peptide Therapy"
    HYPERBARIC = "Hyperbaric Oxygen"


class BiomarkerCategoryEnum(StrEnum):
    CBC = "Complete Blood Count (CBC)"
    METABOLIC_PANEL = "Metabolic Panel"
    LIPID_PANEL = "Lipid Panel"
    HORMONES = "Hormones"
    VITAMINS_MINERALS = "Vitamins & Minerals"
    INFLAMMATION = "Inflammation"


BiomarkerCategory = BiomarkerCategoryEnum


class BiomarkerSimpleCategoryEnum(StrEnum):
    METABOLIC = "Metabolic"
    INFLAMMATION = "Inflammation"
    HORMONES = "Hormones"


BiomarkerSimpleCategory = BiomarkerSimpleCategoryEnum


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
    MICROMOLAR = "µM"


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
    NAD_PLUS = "NAD+"


class BiomarkerStatus(StrEnum):
    OPTIMAL = "Optimal"
    WARNING = "Warning"
    CRITICAL = "Critical"


class BiomarkerTrend(StrEnum):
    UP = "up"
    DOWN = "down"
    STABLE = "stable"