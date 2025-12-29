"""Health entries seed data loading (medications, food, symptoms)."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlmodel import Session, select

from longevity_clinic.app.data.schemas.db import (
    FoodLogEntry,
    MedicationEntry,
    SymptomEntry,
)
from longevity_clinic.app.data.seed import (
    FOOD_ENTRIES_SEED,
    MEDICATIONS_SEED,
    SYMPTOMS_SEED,
)

from .base import SeedResult, print_section


def load_health_entries(session: Session, user_id_map: dict[str, int]) -> SeedResult:
    """Load health entries (medications, food, symptoms) for primary demo user.

    Args:
        session: Database session
        user_id_map: Mapping of external_id to database user id

    Returns:
        SeedResult with load statistics (combined for all health entry types)
    """
    print_section("Loading health entries for Sarah Chen")
    result = SeedResult(name="health_entries")

    # Get primary user ID (Sarah Chen = P001)
    primary_user_id = user_id_map.get("P001")
    if not primary_user_id:
        print("  ⚠ Primary user not found, skipping health entries")
        return result

    med_count = food_count = symptom_count = 0

    # Load medication entries (doses taken logs)
    for med_data in MEDICATIONS_SEED:
        existing = session.exec(
            select(MedicationEntry).where(
                MedicationEntry.user_id == primary_user_id,
                MedicationEntry.name == med_data["name"],
            )
        ).first()

        if existing:
            result.skipped += 1
            continue

        med = MedicationEntry(
            user_id=primary_user_id,
            name=med_data["name"],
            dosage=med_data.get("dosage", ""),
            notes="Seed data entry",
            source="seed",
            taken_at=datetime.now(UTC),
        )
        session.add(med)
        med_count += 1
        result.loaded += 1

    # Load food entries
    for food_data in FOOD_ENTRIES_SEED:
        existing = session.exec(
            select(FoodLogEntry).where(
                FoodLogEntry.user_id == primary_user_id,
                FoodLogEntry.name == food_data["name"],
            )
        ).first()

        if existing:
            result.skipped += 1
            continue

        food = FoodLogEntry(
            user_id=primary_user_id,
            name=food_data["name"],
            calories=food_data.get("calories", 0),
            protein=food_data.get("protein", 0.0),
            carbs=food_data.get("carbs", 0.0),
            fat=food_data.get("fat", 0.0),
            meal_type=food_data.get("meal_type", "snack"),
            consumed_at=food_data.get("time", ""),
            source="seed",
            logged_at=datetime.now(UTC),
        )
        session.add(food)
        food_count += 1
        result.loaded += 1

    # Load symptoms
    for symptom_data in SYMPTOMS_SEED:
        existing = session.exec(
            select(SymptomEntry).where(
                SymptomEntry.user_id == primary_user_id,
                SymptomEntry.name == symptom_data["name"],
            )
        ).first()

        if existing:
            result.skipped += 1
            continue

        symptom = SymptomEntry(
            user_id=primary_user_id,
            name=symptom_data["name"],
            severity=symptom_data.get("severity", ""),
            frequency=symptom_data.get("frequency", ""),
            trend=symptom_data.get("trend", "stable"),
            source="seed",
            reported_at=datetime.now(UTC),
        )
        session.add(symptom)
        symptom_count += 1
        result.loaded += 1

    session.commit()
    print(
        f"  ✓ Loaded {med_count} medications, {food_count} food entries, {symptom_count} symptoms"
    )
    return result


# NOTE: load_prescriptions() removed.
# Medications are now part of Treatment catalog (category=Medications)
# and loaded via load_patient_treatment_assignments() in scripts/seeding/treatments.py
