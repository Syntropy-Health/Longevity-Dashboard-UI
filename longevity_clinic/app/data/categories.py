"""Shared data categories and reusable enums for the Longevity Clinic app."""

from enum import StrEnum
from typing import Final


def _enum_values(enum_cls: type[StrEnum]) -> list[str]:
    """Helper that returns the list of values for backwards compatibility."""

    return [member.value for member in enum_cls]


# ============================================================================
# TREATMENT CATEGORIES
# ============================================================================
class TreatmentCategory(StrEnum):
    IV_THERAPY = "IV Therapy"
    CRYOTHERAPY = "Cryotherapy"
    SUPPLEMENTS = "Supplements"
    HORMONE_THERAPY = "Hormone Therapy"
    PHYSICAL_THERAPY = "Physical Therapy"
    SPA_SERVICES = "Spa Services"


TREATMENT_CATEGORIES: Final[list[str]] = _enum_values(TreatmentCategory)

TREATMENT_CATEGORY_COLORS = {
    TreatmentCategory.IV_THERAPY.value: {"bg": "bg-blue-100", "text": "text-blue-800"},
    TreatmentCategory.CRYOTHERAPY.value: {"bg": "bg-cyan-100", "text": "text-cyan-800"},
    TreatmentCategory.SUPPLEMENTS.value: {
        "bg": "bg-green-100",
        "text": "text-green-800",
    },
    TreatmentCategory.HORMONE_THERAPY.value: {
        "bg": "bg-purple-100",
        "text": "text-purple-800",
    },
    TreatmentCategory.PHYSICAL_THERAPY.value: {
        "bg": "bg-orange-100",
        "text": "text-orange-800",
    },
    TreatmentCategory.SPA_SERVICES.value: {
        "bg": "bg-pink-100",
        "text": "text-pink-800",
    },
}


# ============================================================================
# FREQUENCY OPTIONS
# ============================================================================
class TreatmentFrequency(StrEnum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    BI_WEEKLY = "Bi-Weekly"
    MONTHLY = "Monthly"
    AS_NEEDED = "As-needed"


TREATMENT_FREQUENCIES: Final[list[str]] = _enum_values(TreatmentFrequency)


# ============================================================================
# STATUS OPTIONS
# ============================================================================
class TreatmentStatus(StrEnum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"
    DRAFT = "Draft"


class PatientStatus(StrEnum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ONBOARDING = "Onboarding"


TREATMENT_STATUSES: Final[list[str]] = _enum_values(TreatmentStatus)
PATIENT_STATUSES: Final[list[str]] = _enum_values(PatientStatus)


# ============================================================================
# HEALTH KEYWORDS (for topic extraction)
# ============================================================================
class HealthKeyword(StrEnum):
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


HEALTH_KEYWORDS: Final[list[str]] = _enum_values(HealthKeyword)


__all__ = [
    "HEALTH_KEYWORDS",
    "PATIENT_STATUSES",
    "TREATMENT_CATEGORIES",
    "TREATMENT_CATEGORY_COLORS",
    "TREATMENT_FREQUENCIES",
    "TREATMENT_STATUSES",
    "HealthKeyword",
    "PatientStatus",
    "TreatmentCategory",
    "TreatmentFrequency",
    "TreatmentStatus",
]
