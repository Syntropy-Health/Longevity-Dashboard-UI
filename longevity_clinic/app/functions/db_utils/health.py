"""Health data database operations for food, medications, symptoms, conditions."""

from __future__ import annotations

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.db import (
    FoodLogEntry as FoodLogEntryDB,
    MedicationEntry as MedicationEntryDB,
    SymptomEntry as SymptomEntryDB,
)
from longevity_clinic.app.data.schemas.llm import (
    FoodEntryModel as FoodEntry,
    MedicationEntryModel as MedicationEntry,
    Symptom,
)

logger = get_logger("longevity_clinic.db_utils.health")


# ============================================================================
# MEDICATIONS
# ============================================================================


def get_medications_sync(
    user_id: int,
    limit: int = 100,
) -> list[MedicationEntry]:
    """Get medications for a user from database."""
    try:
        with rx.session() as session:
            medications = session.exec(
                select(MedicationEntryDB)
                .where(MedicationEntryDB.user_id == user_id)
                .order_by(MedicationEntryDB.created_at.desc())
                .limit(limit)
            ).all()

            return [
                MedicationEntry(
                    id=str(med.id),
                    name=med.name,
                    dosage=med.dosage,
                    frequency=med.frequency,
                    status=med.status,
                    adherence_rate=med.adherence_rate,
                )
                for med in medications
            ]
    except Exception as e:
        logger.error("Failed to get medications for user %s: %s", user_id, e)
        return []


def create_medication_sync(
    user_id: int,
    name: str,
    dosage: str,
    frequency: str,
    status: str = "active",
    adherence_rate: float = 1.0,
) -> MedicationEntry | None:
    """Create a medication entry for a user."""
    try:
        with rx.session() as session:
            medication = MedicationEntryDB(
                user_id=user_id,
                name=name,
                dosage=dosage,
                frequency=frequency,
                status=status,
                adherence_rate=adherence_rate,
            )
            session.add(medication)
            session.commit()
            session.refresh(medication)

            return MedicationEntry(
                id=str(medication.id),
                name=medication.name,
                dosage=medication.dosage,
                frequency=medication.frequency,
                status=medication.status,
                adherence_rate=medication.adherence_rate,
            )
    except Exception as e:
        logger.error("Failed to create medication: %s", e)
        return None


# ============================================================================
# FOOD LOG ENTRIES
# ============================================================================


def get_food_entries_sync(
    user_id: int,
    limit: int = 100,
) -> list[FoodEntry]:
    """Get food log entries for a user from database."""
    try:
        with rx.session() as session:
            entries = session.exec(
                select(FoodLogEntryDB)
                .where(FoodLogEntryDB.user_id == user_id)
                .order_by(FoodLogEntryDB.logged_at.desc())
                .limit(limit)
            ).all()

            return [
                FoodEntry(
                    id=str(entry.id),
                    name=entry.name,
                    calories=entry.calories or 0,
                    protein=entry.protein or 0.0,
                    carbs=entry.carbs or 0.0,
                    fat=entry.fat or 0.0,
                    time=entry.consumed_at or "",
                    meal_type=entry.meal_type or "snack",
                )
                for entry in entries
            ]
    except Exception as e:
        logger.error("Failed to get food entries for user %s: %s", user_id, e)
        return []


def create_food_entry_sync(
    user_id: int,
    name: str,
    meal_type: str = "snack",
    calories: int = 0,
    protein: float = 0.0,
    carbs: float = 0.0,
    fat: float = 0.0,
    consumed_at: str | None = None,
) -> FoodEntry | None:
    """Create a food log entry for a user."""
    try:
        with rx.session() as session:
            entry = FoodLogEntryDB(
                user_id=user_id,
                name=name,
                meal_type=meal_type,
                calories=calories,
                protein=protein,
                carbs=carbs,
                fat=fat,
                consumed_at=consumed_at,
            )
            session.add(entry)
            session.commit()
            session.refresh(entry)

            return FoodEntry(
                id=str(entry.id),
                name=entry.name,
                calories=entry.calories or 0,
                protein=entry.protein or 0.0,
                carbs=entry.carbs or 0.0,
                fat=entry.fat or 0.0,
                time=entry.consumed_at or "",
                meal_type=entry.meal_type or "snack",
            )
    except Exception as e:
        logger.error("Failed to create food entry: %s", e)
        return None


# ============================================================================
# SYMPTOMS
# ============================================================================


def get_symptoms_sync(
    user_id: int,
    limit: int = 100,
) -> list[Symptom]:
    """Get symptom entries for a user from database."""
    try:
        with rx.session() as session:
            symptoms = session.exec(
                select(SymptomEntryDB)
                .where(SymptomEntryDB.user_id == user_id)
                .order_by(SymptomEntryDB.reported_at.desc())
                .limit(limit)
            ).all()

            return [
                Symptom(
                    id=str(symptom.id),
                    name=symptom.name,
                    severity=symptom.severity,
                    frequency=symptom.frequency,
                    trend=symptom.trend,
                )
                for symptom in symptoms
            ]
    except Exception as e:
        logger.error("Failed to get symptoms for user %s: %s", user_id, e)
        return []


def create_symptom_sync(
    user_id: int,
    name: str,
    severity: str = "",
    frequency: str = "",
    trend: str = "stable",
) -> Symptom | None:
    """Create a symptom entry for a user."""
    try:
        with rx.session() as session:
            symptom = SymptomEntryDB(
                user_id=user_id,
                name=name,
                severity=severity,
                frequency=frequency,
                trend=trend,
            )
            session.add(symptom)
            session.commit()
            session.refresh(symptom)

            return Symptom(
                id=str(symptom.id),
                name=symptom.name,
                severity=symptom.severity,
                frequency=symptom.frequency,
                trend=symptom.trend,
            )
    except Exception as e:
        logger.error("Failed to create symptom: %s", e)
        return None
