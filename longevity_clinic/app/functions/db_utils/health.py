"""Health data database operations for food, medications, symptoms, conditions."""

from __future__ import annotations

from datetime import datetime

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.db import (
    FoodLogEntry as FoodLogEntryDB,
    MedicationEntry as MedicationEntryDB,
    MedicationSubscription as MedicationSubscriptionDB,
    SymptomEntry as SymptomEntryDB,
)
from longevity_clinic.app.data.schemas.llm import (
    FoodEntryModel as FoodEntry,
    MedicationEntryModel as MedicationEntry,
    MedicationSubscriptionModel as MedicationSubscription,
    Symptom,
)

logger = get_logger("longevity_clinic.db_utils.health")


# ============================================================================
# MEDICATION SUBSCRIPTIONS (Prescribed medications)
# ============================================================================


def get_medication_subscriptions_sync(
    user_id: int,
    status: str | None = None,
    limit: int = 100,
) -> list[MedicationSubscription]:
    """Get medication subscriptions (prescriptions) for a user."""
    try:
        with rx.session() as session:
            query = select(MedicationSubscriptionDB).where(
                MedicationSubscriptionDB.user_id == user_id
            )
            if status:
                query = query.where(MedicationSubscriptionDB.status == status)
            query = query.order_by(MedicationSubscriptionDB.created_at.desc()).limit(
                limit
            )
            subscriptions = session.exec(query).all()

            return [
                MedicationSubscription(
                    id=str(sub.id),
                    name=sub.name,
                    dosage=sub.dosage,
                    frequency=sub.frequency,
                    instructions=sub.instructions,
                    status=sub.status,
                    adherence_rate=sub.adherence_rate,
                    prescriber=sub.prescriber,
                )
                for sub in subscriptions
            ]
    except Exception as e:
        logger.error(
            "Failed to get medication subscriptions for user %s: %s", user_id, e
        )
        return []


def create_medication_subscription_sync(
    user_id: int,
    name: str,
    dosage: str,
    frequency: str,
    instructions: str = "",
    prescriber: str = "",
    status: str = "active",
    adherence_rate: float = 100.0,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    source: str = "manual",
) -> MedicationSubscriptionDB | None:
    """Create a medication subscription for a user."""
    try:
        with rx.session() as session:
            subscription = MedicationSubscriptionDB(
                user_id=user_id,
                name=name,
                dosage=dosage,
                frequency=frequency,
                instructions=instructions,
                prescriber=prescriber,
                status=status,
                adherence_rate=adherence_rate,
                start_date=start_date,
                end_date=end_date,
                source=source,
            )
            session.add(subscription)
            session.commit()
            session.refresh(subscription)
            return subscription
    except Exception as e:
        logger.error("Failed to create medication subscription: %s", e)
        return None


# ============================================================================
# MEDICATION LOGS (What patient actually took)
# ============================================================================


def get_medication_logs_sync(
    user_id: int,
    limit: int = 100,
) -> list[MedicationEntry]:
    """Get medication logs (what was taken) for a user."""
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
        logger.error("Failed to get medication logs for user %s: %s", user_id, e)
        return []


def create_medication_log_sync(
    user_id: int,
    name: str,
    dosage: str = "",
    taken_at: datetime | None = None,
    notes: str = "",
    checkin_id: int | None = None,
    subscription_id: int | None = None,
    source: str = "manual",
) -> MedicationEntryDB | None:
    """Create a medication log entry for a user."""
    try:
        with rx.session() as session:
            log = MedicationEntryDB(
                user_id=user_id,
                name=name,
                dosage=dosage,
                taken_at=taken_at or datetime.now(),
                notes=notes,
                checkin_id=checkin_id,
                subscription_id=subscription_id,
                source=source,
            )
            session.add(log)
            session.commit()
            session.refresh(log)
            return log
    except Exception as e:
        logger.error("Failed to create medication log: %s", e)
        return None


# Legacy alias for backward compatibility
def get_medications_sync(
    user_id: int,
    limit: int = 100,
) -> list[MedicationEntry]:
    """Get medication logs for a user (legacy alias for get_medication_logs_sync)."""
    return get_medication_logs_sync(user_id, limit)


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
