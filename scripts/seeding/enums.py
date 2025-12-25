"""Enum/choice table seed data loading.

Populates reference tables (treatment_categories, treatment_statuses, etc.)
from domain_enums.py StrEnum values. These tables provide:
1. Database-level referential integrity
2. Single source of truth for valid values
3. UI-friendly metadata (colors, icons, descriptions)

Run FIRST before other seed data as other tables may reference these.
"""

from __future__ import annotations

from sqlmodel import Session, select

from longevity_clinic.app.data.schemas.db import (
    # Enum tables (rx.Model)
    BiomarkerCategory,
    # Domain enums (StrEnum) - source of truth
    BiomarkerSimpleCategoryEnum,
    CheckInType,
    TreatmentCategory,
    TreatmentCategoryEnum,
    TreatmentStatus,
    TreatmentStatusEnum,
    UrgencyLevel,
)

from .base import SeedResult, print_section

# =============================================================================
# Treatment Categories Seed Data
# =============================================================================

TREATMENT_CATEGORY_SEED: list[dict] = [
    {
        "code": "IV_THERAPY",
        "name": TreatmentCategoryEnum.IV_THERAPY.value,
        "description": "Intravenous infusion therapies for direct nutrient delivery",
        "color": "#3B82F6",  # blue-500
        "icon": "droplet",
        "sort_order": 1,
    },
    {
        "code": "CRYOTHERAPY",
        "name": TreatmentCategoryEnum.CRYOTHERAPY.value,
        "description": "Cold therapy treatments for recovery and inflammation",
        "color": "#06B6D4",  # cyan-500
        "icon": "snowflake",
        "sort_order": 2,
    },
    {
        "code": "SUPPLEMENTS",
        "name": TreatmentCategoryEnum.SUPPLEMENTS.value,
        "description": "Nutritional supplement protocols and regimens",
        "color": "#10B981",  # emerald-500
        "icon": "pill",
        "sort_order": 3,
    },
    {
        "code": "HORMONE_THERAPY",
        "name": TreatmentCategoryEnum.HORMONE_THERAPY.value,
        "description": "Bio-identical hormone replacement and optimization",
        "color": "#8B5CF6",  # violet-500
        "icon": "activity",
        "sort_order": 4,
    },
    {
        "code": "PHYSICAL_THERAPY",
        "name": TreatmentCategoryEnum.PHYSICAL_THERAPY.value,
        "description": "Physical rehabilitation and therapeutic exercise",
        "color": "#F97316",  # orange-500
        "icon": "dumbbell",
        "sort_order": 5,
    },
    {
        "code": "SPA_SERVICES",
        "name": TreatmentCategoryEnum.SPA_SERVICES.value,
        "description": "Wellness spa treatments and relaxation therapies",
        "color": "#EC4899",  # pink-500
        "icon": "sparkles",
        "sort_order": 6,
    },
    {
        "code": "MEDICATIONS",
        "name": TreatmentCategoryEnum.MEDICATIONS.value,
        "description": "Prescribed medications and pharmaceutical treatments",
        "color": "#EF4444",  # red-500
        "icon": "pill",
        "sort_order": 7,
    },
]


# =============================================================================
# Treatment Statuses Seed Data
# =============================================================================

TREATMENT_STATUS_SEED: list[dict] = [
    {
        "code": "ACTIVE",
        "name": TreatmentStatusEnum.ACTIVE.value,
        "description": "Treatment is currently active and available",
        "color": "#10B981",  # green-500
        "sort_order": 1,
    },
    {
        "code": "ARCHIVED",
        "name": TreatmentStatusEnum.ARCHIVED.value,
        "description": "Treatment is archived and no longer offered",
        "color": "#6B7280",  # gray-500
        "sort_order": 2,
    },
    {
        "code": "DRAFT",
        "name": TreatmentStatusEnum.DRAFT.value,
        "description": "Treatment is in draft mode, not yet published",
        "color": "#F59E0B",  # amber-500
        "sort_order": 3,
    },
]


# =============================================================================
# Biomarker Categories Seed Data
# =============================================================================

BIOMARKER_CATEGORY_SEED: list[dict] = [
    {
        "code": "METABOLIC",
        "name": BiomarkerSimpleCategoryEnum.METABOLIC.value,
        "description": "Blood sugar, lipids, and metabolic panel markers",
        "color": "#3B82F6",  # blue-500
        "icon": "activity",
        "sort_order": 1,
    },
    {
        "code": "INFLAMMATION",
        "name": BiomarkerSimpleCategoryEnum.INFLAMMATION.value,
        "description": "Inflammation markers like CRP and homocysteine",
        "color": "#EF4444",  # red-500
        "icon": "flame",
        "sort_order": 2,
    },
    {
        "code": "HORMONES",
        "name": BiomarkerSimpleCategoryEnum.HORMONES.value,
        "description": "Hormone levels including testosterone, cortisol, thyroid",
        "color": "#8B5CF6",  # violet-500
        "icon": "zap",
        "sort_order": 3,
    },
]


# =============================================================================
# Check-in Types Seed Data
# =============================================================================

CHECKIN_TYPE_SEED: list[dict] = [
    {
        "code": "MANUAL",
        "name": "Manual Check-in",
        "description": "Text-based check-in entered by patient",
        "icon": "edit",
        "sort_order": 1,
    },
    {
        "code": "VOICE",
        "name": "Voice Check-in",
        "description": "Voice recording transcribed to check-in",
        "icon": "mic",
        "sort_order": 2,
    },
    {
        "code": "CALL",
        "name": "Phone Call",
        "description": "Check-in extracted from phone call transcript",
        "icon": "phone",
        "sort_order": 3,
    },
]


# =============================================================================
# Urgency Levels Seed Data
# =============================================================================

URGENCY_LEVEL_SEED: list[dict] = [
    {
        "code": "ROUTINE",
        "name": "Routine",
        "description": "Standard check-in, no immediate action needed",
        "color": "#10B981",  # green-500
        "priority": 0,
        "sla_hours": None,
    },
    {
        "code": "FOLLOW_UP",
        "name": "Follow-up",
        "description": "Requires follow-up within a few days",
        "color": "#F59E0B",  # amber-500
        "priority": 1,
        "sla_hours": 72,
    },
    {
        "code": "URGENT",
        "name": "Urgent",
        "description": "Requires immediate attention",
        "color": "#EF4444",  # red-500
        "priority": 2,
        "sla_hours": 24,
    },
]


# =============================================================================
# Loader Functions
# =============================================================================


def load_treatment_categories(session: Session) -> SeedResult:
    """Load treatment categories from TREATMENT_CATEGORY_SEED.

    Args:
        session: Database session

    Returns:
        SeedResult with id_map of code -> database id
    """
    print_section("Loading treatment categories")
    result = SeedResult(name="treatment_categories")

    for data in TREATMENT_CATEGORY_SEED:
        code = data["code"]

        existing = session.exec(
            select(TreatmentCategory).where(TreatmentCategory.code == code)
        ).first()

        if existing:
            result.id_map[code] = existing.id
            result.skipped += 1
            continue

        category = TreatmentCategory(**data)
        session.add(category)
        session.flush()
        result.id_map[code] = category.id
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} treatment categories")
    return result


def load_treatment_statuses(session: Session) -> SeedResult:
    """Load treatment statuses from TREATMENT_STATUS_SEED.

    Args:
        session: Database session

    Returns:
        SeedResult with id_map of code -> database id
    """
    print_section("Loading treatment statuses")
    result = SeedResult(name="treatment_statuses")

    for data in TREATMENT_STATUS_SEED:
        code = data["code"]

        existing = session.exec(
            select(TreatmentStatus).where(TreatmentStatus.code == code)
        ).first()

        if existing:
            result.id_map[code] = existing.id
            result.skipped += 1
            continue

        status = TreatmentStatus(**data)
        session.add(status)
        session.flush()
        result.id_map[code] = status.id
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} treatment statuses")
    return result


def load_biomarker_categories(session: Session) -> SeedResult:
    """Load biomarker categories from BIOMARKER_CATEGORY_SEED.

    Args:
        session: Database session

    Returns:
        SeedResult with id_map of code -> database id
    """
    print_section("Loading biomarker categories")
    result = SeedResult(name="biomarker_categories")

    for data in BIOMARKER_CATEGORY_SEED:
        code = data["code"]

        existing = session.exec(
            select(BiomarkerCategory).where(BiomarkerCategory.code == code)
        ).first()

        if existing:
            result.id_map[code] = existing.id
            result.skipped += 1
            continue

        category = BiomarkerCategory(**data)
        session.add(category)
        session.flush()
        result.id_map[code] = category.id
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} biomarker categories")
    return result


def load_checkin_types(session: Session) -> SeedResult:
    """Load check-in types from CHECKIN_TYPE_SEED.

    Args:
        session: Database session

    Returns:
        SeedResult with id_map of code -> database id
    """
    print_section("Loading check-in types")
    result = SeedResult(name="checkin_types")

    for data in CHECKIN_TYPE_SEED:
        code = data["code"]

        existing = session.exec(
            select(CheckInType).where(CheckInType.code == code)
        ).first()

        if existing:
            result.id_map[code] = existing.id
            result.skipped += 1
            continue

        checkin_type = CheckInType(**data)
        session.add(checkin_type)
        session.flush()
        result.id_map[code] = checkin_type.id
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} check-in types")
    return result


def load_urgency_levels(session: Session) -> SeedResult:
    """Load urgency levels from URGENCY_LEVEL_SEED.

    Args:
        session: Database session

    Returns:
        SeedResult with id_map of code -> database id
    """
    print_section("Loading urgency levels")
    result = SeedResult(name="urgency_levels")

    for data in URGENCY_LEVEL_SEED:
        code = data["code"]

        existing = session.exec(
            select(UrgencyLevel).where(UrgencyLevel.code == code)
        ).first()

        if existing:
            result.id_map[code] = existing.id
            result.skipped += 1
            continue

        level = UrgencyLevel(**data)
        session.add(level)
        session.flush()
        result.id_map[code] = level.id
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} urgency levels")
    return result


def load_all_enums(session: Session) -> dict[str, SeedResult]:
    """Load all enum tables in order.

    Args:
        session: Database session

    Returns:
        Dict of table_name -> SeedResult
    """
    return {
        "treatment_categories": load_treatment_categories(session),
        "treatment_statuses": load_treatment_statuses(session),
        "biomarker_categories": load_biomarker_categories(session),
        "checkin_types": load_checkin_types(session),
        "urgency_levels": load_urgency_levels(session),
    }


__all__ = [
    # Seed data
    "BIOMARKER_CATEGORY_SEED",
    "CHECKIN_TYPE_SEED",
    "TREATMENT_CATEGORY_SEED",
    "TREATMENT_STATUS_SEED",
    "URGENCY_LEVEL_SEED",
    # Loader functions
    "load_all_enums",
    "load_biomarker_categories",
    "load_checkin_types",
    "load_treatment_categories",
    "load_treatment_statuses",
    "load_urgency_levels",
]
