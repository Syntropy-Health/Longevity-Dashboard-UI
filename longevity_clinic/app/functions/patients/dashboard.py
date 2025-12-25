"""Dashboard data fetching functions.

Functions for fetching static dashboard-related data including
conditions, data sources, and reminders.

NOTE: Medications, food entries, and symptoms are now sourced from
the database via CDC pipeline (call log extraction). These functions
provide only static/default data for things not yet in the DB.
"""

from __future__ import annotations

# Standard library
from typing import Any

# Local application
from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.llm import (
    Condition,
    DataSource,
    SymptomEntryModel as SymptomEntry,
    SymptomTrend,
)
from longevity_clinic.app.data.seed import (
    CONDITIONS_SEED,
    DATA_SOURCES_SEED,
    REMINDERS_SEED,
    SYMPTOM_LOGS_SEED,
    SYMPTOM_TRENDS_SEED,
)

logger = get_logger("longevity_clinic.dashboard_functions")


# NOTE: fetch_nutrition_summary, fetch_medications, and fetch_food_entries
# have been removed. This data now comes from the database via CDC pipeline
# (call log extraction). See dashboard._load_health_entries_from_db()


async def fetch_conditions(
    patient_id: str | None = None,
) -> list[Condition]:
    """Fetch medical conditions for a patient.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        List of Condition objects (static demo data for now)
    """
    logger.info(
        "Fetching conditions for patient_id=%s (returning %d static conditions)",
        patient_id or "(current_user)",
        len(CONDITIONS_SEED),
    )

    # Return static conditions - these don't come from call logs yet
    return [
        Condition(**cond) if isinstance(cond, dict) else cond
        for cond in CONDITIONS_SEED
    ]


async def fetch_symptoms(
    patient_id: str | None = None,
    days: int = 30,
) -> dict[str, Any]:
    """Fetch symptom data for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        days: Number of days of history

    Returns:
        Dict with 'symptom_logs' and 'symptom_trends' keys.
        NOTE: Actual symptoms come from DB via CDC pipeline.
    """
    symptom_logs = [
        SymptomEntry(**sl) if isinstance(sl, dict) else sl for sl in SYMPTOM_LOGS_SEED
    ]
    symptom_trends = [
        SymptomTrend(**st) if isinstance(st, dict) else st for st in SYMPTOM_TRENDS_SEED
    ]

    logger.info(
        "Fetching symptom data for patient_id=%s (days=%d): %d logs, %d trends",
        patient_id or "(current_user)",
        days,
        len(symptom_logs),
        len(symptom_trends),
    )

    # Return static symptom logs and trends (symptoms come from DB)
    return {
        "symptom_logs": symptom_logs,
        "symptom_trends": symptom_trends,
    }


async def fetch_data_sources(
    patient_id: str | None = None,
) -> list[DataSource]:
    """Fetch connected data sources for a patient.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        List of DataSource objects (static demo data for now)
    """
    data_sources = [
        DataSource(**ds) if isinstance(ds, dict) else ds for ds in DATA_SOURCES_SEED
    ]

    logger.info(
        "Fetching data sources for patient_id=%s: %d sources",
        patient_id or "(current_user)",
        len(data_sources),
    )

    # Return static data sources
    return data_sources


def calculate_medication_adherence(
    medications: list[dict[str, Any]],
) -> float:
    """Calculate overall medication adherence percentage.

    Args:
        medications: List of medication records with adherence data

    Returns:
        Adherence percentage (0-100)
    """
    if not medications:
        return 0.0

    total_adherence = sum(m.get("adherence", 0) for m in medications)
    return total_adherence / len(medications)


# NOTE: fetch_food_entries has been removed.
# Food entries now come from the database via CDC pipeline.


async def fetch_reminders(
    patient_id: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch reminders for a patient.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        List of reminder records (static demo data for now)
    """
    reminders = REMINDERS_SEED

    logger.info(
        "Fetching reminders for patient_id=%s: %d reminders",
        patient_id or "(current_user)",
        len(reminders),
    )

    # Return static reminders
    return reminders


async def load_all_dashboard_data(
    patient_id: str | None = None,
) -> dict[str, Any]:
    """Load static dashboard data for a patient.

    NOTE: Medications, food entries, and symptoms are now loaded from
    the database (via CDC pipeline). This function only provides:
    - conditions (static)
    - symptom_logs (static)
    - symptom_trends (static)
    - reminders (static)
    - data_sources (static)

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        Dict with keys: 'conditions', 'symptom_logs', 'symptom_trends',
        'reminders', 'data_sources'
    """
    logger.info(
        "Loading static dashboard data for patient: %s",
        patient_id or "current",
    )

    # Fetch only static data (medications, food, symptoms come from DB)
    conditions = await fetch_conditions(patient_id)
    symptoms_data = await fetch_symptoms(patient_id)
    reminders = await fetch_reminders(patient_id)
    data_sources = await fetch_data_sources(patient_id)

    return {
        "conditions": conditions,
        "symptom_logs": symptoms_data.get("symptom_logs", []),
        "symptom_trends": symptoms_data.get("symptom_trends", []),
        "reminders": reminders,
        "data_sources": data_sources,
    }
