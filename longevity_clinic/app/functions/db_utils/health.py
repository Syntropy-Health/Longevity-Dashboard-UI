"""Health data database operations for food, medications, symptoms, conditions."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.model import (
    FoodLogEntry as FoodLogEntryDB,
    MedicationEntry as MedicationEntryDB,
    SymptomEntry as SymptomEntryDB,
)
from longevity_clinic.app.data.state_schemas import (
    FoodEntry,
    MedicationEntry,
    Symptom,
)

logger = get_logger("longevity_clinic.db_utils.health")


# ============================================================================
# MEDICATIONS
# ============================================================================


def get_medications_sync(
    user_id: int,
    limit: int = 100,
) -> List[MedicationEntry]:
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
) -> Optional[MedicationEntry]:
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


def update_medication_sync(
    medication_id: int,
    **updates: Any,
) -> Optional[MedicationEntry]:
    """Update a medication entry."""
    try:
        with rx.session() as session:
            medication = session.get(MedicationEntryDB, medication_id)
            if not medication:
                logger.warning("Medication not found: %s", medication_id)
                return None

            for key, value in updates.items():
                if hasattr(medication, key):
                    setattr(medication, key, value)

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
        logger.error("Failed to update medication %s: %s", medication_id, e)
        return None


def delete_medication_sync(medication_id: int) -> bool:
    """Delete a medication entry."""
    try:
        with rx.session() as session:
            medication = session.get(MedicationEntryDB, medication_id)
            if not medication:
                return False

            session.delete(medication)
            session.commit()
            return True
    except Exception as e:
        logger.error("Failed to delete medication %s: %s", medication_id, e)
        return False


# ============================================================================
# FOOD LOG ENTRIES
# ============================================================================


def get_food_entries_sync(
    user_id: int,
    limit: int = 100,
) -> List[FoodEntry]:
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
    consumed_at: Optional[str] = None,
) -> Optional[FoodEntry]:
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


def delete_food_entry_sync(entry_id: int) -> bool:
    """Delete a food log entry."""
    try:
        with rx.session() as session:
            entry = session.get(FoodLogEntryDB, entry_id)
            if not entry:
                return False

            session.delete(entry)
            session.commit()
            return True
    except Exception as e:
        logger.error("Failed to delete food entry %s: %s", entry_id, e)
        return False


# ============================================================================
# SYMPTOMS
# ============================================================================


def get_symptoms_sync(
    user_id: int,
    limit: int = 100,
) -> List[Symptom]:
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
) -> Optional[Symptom]:
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


def delete_symptom_sync(symptom_id: int) -> bool:
    """Delete a symptom entry."""
    try:
        with rx.session() as session:
            symptom = session.get(SymptomEntryDB, symptom_id)
            if not symptom:
                return False

            session.delete(symptom)
            session.commit()
            return True
    except Exception as e:
        logger.error("Failed to delete symptom %s: %s", symptom_id, e)
        return False


# ============================================================================
# CONDITIONS (stored in User model as JSON)
# ============================================================================


def get_conditions_sync(user_id: int) -> List[Dict[str, Any]]:
    """Get conditions for a user from database.

    Conditions are stored in the User.conditions JSON field.
    """
    from longevity_clinic.app.data.model import User

    try:
        with rx.session() as session:
            user = session.get(User, user_id)
            if not user or not user.conditions:
                return []

            # Parse JSON conditions
            import json

            if isinstance(user.conditions, str):
                conditions = json.loads(user.conditions)
            else:
                conditions = user.conditions

            return conditions if isinstance(conditions, list) else []
    except Exception as e:
        logger.error("Failed to get conditions for user %s: %s", user_id, e)
        return []


def update_conditions_sync(
    user_id: int,
    conditions: List[Dict[str, Any]],
) -> bool:
    """Update conditions for a user in database."""
    from longevity_clinic.app.data.model import User
    import json

    try:
        with rx.session() as session:
            user = session.get(User, user_id)
            if not user:
                logger.warning("User not found: %s", user_id)
                return False

            user.conditions = json.dumps(conditions)
            user.updated_at = datetime.now(timezone.utc)
            session.add(user)
            session.commit()
            return True
    except Exception as e:
        logger.error("Failed to update conditions for user %s: %s", user_id, e)
        return False
