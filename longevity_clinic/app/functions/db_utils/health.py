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
    TreatmentCategory as TreatmentCategoryDB,
)
from longevity_clinic.app.data.schemas.db.domain_enums import TreatmentCategoryEnum

# Import Pydantic models for internal use (LLM extraction)
from longevity_clinic.app.data.schemas.llm import (
    Symptom,
    SymptomEntryModel as SymptomLog,
)

# Import TypedDicts for return types (used in state)
from longevity_clinic.app.data.schemas.state import (
    FoodEntry,
    MedicationLogEntry,
    Prescription,
)

logger = get_logger("longevity_clinic.db_utils.health")


# ============================================================================
# MEDICATION SUBSCRIPTIONS (via PatientTreatment with category_id=Medications)
# ============================================================================


def get_prescriptions_sync(
    user_id: int,
    status: str | None = None,
    limit: int = 100,
) -> list[Prescription]:
    """Get medication subscriptions (prescriptions) for a user.

    Queries PatientTreatment joined with Treatment and TreatmentCategory
    where category name = 'Medications'.
    Returns Prescription TypedDict for Reflex state compatibility.
    """
    try:
        with rx.session() as session:
            query = (
                select(PatientTreatmentDB, TreatmentDB, TreatmentCategoryDB)
                .join(TreatmentDB, PatientTreatmentDB.treatment_id == TreatmentDB.id)
                .join(
                    TreatmentCategoryDB,
                    TreatmentDB.category_id == TreatmentCategoryDB.id,
                )
                .where(PatientTreatmentDB.user_id == user_id)
                .where(
                    TreatmentCategoryDB.name == TreatmentCategoryEnum.MEDICATIONS.value
                )
            )
            if status:
                query = query.where(PatientTreatmentDB.status == status)
            query = query.order_by(PatientTreatmentDB.start_date.desc()).limit(limit)
            results = session.exec(query).all()

            logger.info(
                "get_prescriptions_sync: user_id=%s, found %d results",
                user_id,
                len(results),
            )

            return [
                Prescription(
                    id=str(pt.id),
                    name=t.name,
                    category=cat.name,  # Get category name from TreatmentCategory
                    dosage=pt.dosage or "",
                    frequency=t.frequency or "",
                    instructions=pt.instructions or "",
                    status=pt.status,
                    adherence_rate=pt.adherence_rate or 100.0,
                    assigned_by=pt.assigned_by or "",
                    sessions_completed=pt.sessions_completed or 0,
                    sessions_total=pt.sessions_total,
                )
                for pt, t, cat in results
            ]
    except Exception as e:
        logger.error(
            "Failed to get medication subscriptions for user %s: %s", user_id, e
        )
        return []


# NOTE:Use PatientTreatment with Treatment(category=Medications) instead.
# See scripts/seeding/treatments.py for adding medication treatments.

# ============================================================================


def get_medication_entries_sync(
    user_id: int,
    limit: int = 100,
) -> list[MedicationLogEntry]:
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
                MedicationLogEntry(
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
) -> list[MedicationLogEntry]:
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
                    logged_at=entry.logged_at.isoformat() if entry.logged_at else None,
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
                logged_at=entry.logged_at.isoformat() if entry.logged_at else None,
            )
    except Exception as e:
        logger.error("Failed to create food entry: %s", e)
        return None


# ============================================================================
# SYMPTOMS
# ============================================================================


def _normalize_enum_value(
    value: str | None, valid_values: set[str], default: str
) -> str:
    """Normalize enum values from DB to match StrEnum expectations.

    Handles case mismatches (e.g., 'unknown' -> 'UNKNOWN') and None values.
    """
    if value is None:
        return default
    # Try exact match first
    if value in valid_values:
        return value
    # Try uppercase for UNKNOWN case
    upper_value = value.upper()
    if upper_value in valid_values:
        return upper_value
    # Return default if no match
    return default


# Valid enum values for normalization
_SEVERITY_VALUES = {"UNKNOWN", "mild", "moderate", "severe"}
_TREND_VALUES = {"UNKNOWN", "improving", "worsening", "stable"}


def get_symptoms_sync(
    user_id: int,
    limit: int = 100,
) -> list[Symptom]:
    """Get symptom entries for a user from database.

    Normalizes enum values from DB to ensure compatibility with Pydantic validation.
    """
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
                    severity=_normalize_enum_value(
                        symptom.severity, _SEVERITY_VALUES, "UNKNOWN"
                    ),
                    frequency=symptom.frequency or "unknown",
                    trend=_normalize_enum_value(
                        symptom.trend, _TREND_VALUES, "UNKNOWN"
                    ),
                )
                for symptom in symptoms
            ]
    except Exception as e:
        logger.error("Failed to get symptoms for user %s: %s", user_id, e)
        return []


def get_symptom_logs_sync(
    user_id: int,
    limit: int = 100,
) -> list[SymptomLog]:
    """Get symptom log entries for timeline display.

    Returns SymptomEntryModel (SymptomLog) with fields formatted for UI:
    - symptom_name (from DB name)
    - severity as int (mapped from enum string: mild=3, moderate=5, severe=8, unknown=0)
    - timestamp (formatted from reported_at)
    - notes
    """
    severity_map = {"mild": 3, "moderate": 5, "severe": 8, "unknown": 0}

    try:
        with rx.session() as session:
            symptoms = session.exec(
                select(SymptomEntryDB)
                .where(SymptomEntryDB.user_id == user_id)
                .order_by(SymptomEntryDB.reported_at.desc())
                .limit(limit)
            ).all()

            return [
                SymptomLog(
                    id=str(symptom.id),
                    symptom_name=symptom.name,
                    severity=severity_map.get(symptom.severity or "unknown", 0),
                    notes=symptom.notes or "",
                    timestamp=(
                        symptom.reported_at.strftime("%b %d, %I:%M %p")
                        if symptom.reported_at
                        else ""
                    ),
                )
                for symptom in symptoms
            ]
    except Exception as e:
        logger.error("Failed to get symptom logs for user %s: %s", user_id, e)
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
