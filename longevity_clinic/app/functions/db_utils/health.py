"""Health data database operations for food, medications, symptoms, conditions."""

from __future__ import annotations

from datetime import datetime

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.db import (
    FoodLogEntry as FoodLogEntryDB,
    MedicationEntry as MedicationEntryDB,
    PatientTreatment as PatientTreatmentDB,
    SymptomEntry as SymptomEntryDB,
    Treatment as TreatmentDB,
)
from longevity_clinic.app.data.schemas.db.domain_enums import TreatmentCategoryEnum
from longevity_clinic.app.data.schemas.llm import (
    FoodEntryModel as FoodEntry,
    MedicationEntryModel as MedicationEntry,
    PatientTreatmentModel as PatientTreatment,
    Symptom,
)

logger = get_logger("longevity_clinic.db_utils.health")


# ============================================================================
# MEDICATION SUBSCRIPTIONS (via PatientTreatment with category=Medications)
# ============================================================================


def get_medication_subscriptions_sync(
    user_id: int,
    status: str | None = None,
    limit: int = 100,
) -> list[PatientTreatment]:
    """Get medication subscriptions (prescriptions) for a user.

    Now queries PatientTreatment joined with Treatment where category='Medications'.
    Returns PatientTreatmentModel (aliased as MedicationSubscription for compat).
    """
    try:
        with rx.session() as session:
            query = (
                select(PatientTreatmentDB, TreatmentDB)
                .join(TreatmentDB, PatientTreatmentDB.treatment_id == TreatmentDB.id)
                .where(PatientTreatmentDB.user_id == user_id)
                .where(TreatmentDB.category == TreatmentCategoryEnum.MEDICATIONS.value)
            )
            if status:
                query = query.where(PatientTreatmentDB.status == status)
            query = query.order_by(PatientTreatmentDB.start_date.desc()).limit(limit)
            results = session.exec(query).all()

            return [
                PatientTreatment(
                    id=str(pt.id),
                    name=t.name,
                    category=t.category,
                    dosage=pt.dosage or "",
                    frequency=t.frequency or "",
                    instructions=pt.instructions or "",
                    status=pt.status,
                    adherence_rate=pt.adherence_rate or 100.0,
                    assigned_by=pt.assigned_by or "",
                    sessions_completed=pt.sessions_completed or 0,
                    sessions_total=pt.sessions_total,
                )
                for pt, t in results
            ]
    except Exception as e:
        logger.error(
            "Failed to get medication subscriptions for user %s: %s", user_id, e
        )
        return []


# Legacy alias
MedicationSubscription = PatientTreatment


# NOTE: create_medication_subscription_sync removed.
# Use PatientTreatment with Treatment(category=Medications) instead.
# See scripts/seeding/treatments.py for adding medication treatments.


# ============================================================================
# Medication Entries (What patient actually took)
# ============================================================================


def get_medication_entries_sync(
    user_id: int,
    limit: int = 100,
) -> list[MedicationEntry]:
    """Get Medication Entries (what was taken) for a user."""
    try:
        with rx.session() as session:
            logs = session.exec(
                select(MedicationEntryDB)
                .where(MedicationEntryDB.user_id == user_id)
                .order_by(MedicationEntryDB.taken_at.desc())
                .limit(limit)
            ).all()

            return [
                MedicationEntry(
                    id=str(log.id),
                    name=log.name,
                    dosage=log.dosage,
                    taken_at=log.taken_at.isoformat() if log.taken_at else "",
                    notes=log.notes,
                )
                for log in logs
            ]
    except Exception as e:
        logger.error("Failed to get Medication Entries for user %s: %s", user_id, e)
        return []


def create_medication_entry_sync(
    user_id: int,
    name: str,
    dosage: str = "",
    taken_at: datetime | None = None,
    notes: str = "",
    checkin_id: int | None = None,
    patient_treatment_id: int | None = None,
    source: str = "manual",
) -> MedicationEntryDB | None:
    """Create a Medication Entry entry for a user."""
    try:
        with rx.session() as session:
            log = MedicationEntryDB(
                user_id=user_id,
                name=name,
                dosage=dosage,
                taken_at=taken_at or datetime.now(),
                notes=notes,
                checkin_id=checkin_id,
                patient_treatment_id=patient_treatment_id,
                source=source,
            )
            session.add(log)
            session.commit()
            session.refresh(log)
            return log
    except Exception as e:
        logger.error("Failed to create Medication Entry: %s", e)
        return None


# Legacy alias for backward compatibility
def get_medications_sync(
    user_id: int,
    limit: int = 100,
) -> list[MedicationEntry]:
    """Get Medication Entries for a user (legacy alias for get_medication_entries_sync)."""
    return get_medication_entries_sync(user_id, limit)


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
