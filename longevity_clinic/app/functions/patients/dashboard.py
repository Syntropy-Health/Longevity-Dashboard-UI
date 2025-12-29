"""Dashboard data fetching functions.

Functions for fetching dashboard-related data including
conditions, data sources, symptoms, and reminders.

All data is loaded from the database.
Run `python scripts/load_seed_data.py` to seed data.
"""

from __future__ import annotations

# Standard library
from typing import Any

# Local application
from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.llm import (
    Condition,
    DataSource,
)
from longevity_clinic.app.functions.db_utils import (
    get_conditions_sync,
    get_data_sources_sync,
    get_medication_notifications_sync,
    get_symptom_logs_sync,
    get_symptom_trends_sync,
)

logger = get_logger("longevity_clinic.dashboard_functions")


# NOTE: fetch_nutrition_summary, fetch_medications, and fetch_food_entries
# have been removed. This data now comes from the database via CDC pipeline
# (call log extraction). See dashboard._load_health_entries_from_db()


async def fetch_conditions(
    user_id: int | None = None,
) -> list[Condition]:
    """Fetch medical conditions for a patient from database.

    Args:
        user_id: Database user ID (None for empty list)

    Returns:
        List of Condition objects from database
    """
    if not user_id:
        logger.warning("fetch_conditions: No user_id provided")
        return []

    conditions = get_conditions_sync(user_id)
    logger.info(
        "fetch_conditions: Loaded %d conditions for user_id=%s",
        len(conditions),
        user_id,
    )
    return conditions


async def fetch_symptoms(
    user_id: int | None = None,
    days: int = 30,
) -> dict[str, Any]:
    """Fetch symptom data for a patient from database.

    Args:
        user_id: Database user ID (None for empty data)
        days: Number of days of history (unused, returns all)

    Returns:
        Dict with 'symptom_logs' and 'symptom_trends' keys.
    """
    if not user_id:
        logger.warning("fetch_symptoms: No user_id provided")
        return {"symptom_logs": [], "symptom_trends": []}

    symptom_logs = get_symptom_logs_sync(user_id)
    symptom_trends = get_symptom_trends_sync(user_id)

    logger.info(
        "fetch_symptoms: Loaded %d logs, %d trends for user_id=%s (days=%d)",
        len(symptom_logs),
        len(symptom_trends),
        user_id,
        days,
    )

    return {
        "symptom_logs": symptom_logs,
        "symptom_trends": symptom_trends,
    }


async def fetch_data_sources(
    user_id: int | None = None,
) -> list[DataSource]:
    """Fetch connected data sources for a patient from database.

    Args:
        user_id: Database user ID (None for empty list)

    Returns:
        List of DataSource objects from database
    """
    if not user_id:
        logger.warning("fetch_data_sources: No user_id provided")
        return []

    data_sources = get_data_sources_sync(user_id)
    logger.info(
        "fetch_data_sources: Loaded %d sources for user_id=%s",
        len(data_sources),
        user_id,
    )
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
    user_id: int | None = None,
) -> list[dict[str, Any]]:
    """Fetch reminders (medication notifications) for a patient from database.

    Args:
        user_id: Database user ID (None for empty list)

    Returns:
        List of reminder/notification records from database
    """
    if not user_id:
        logger.warning("fetch_reminders: No user_id provided")
        return []

    reminders = get_medication_notifications_sync(user_id)
    logger.info(
        "fetch_reminders: Loaded %d reminders for user_id=%s",
        len(reminders),
        user_id,
    )
    return reminders


async def load_all_dashboard_data(
    user_id: int | None = None,
) -> dict[str, Any]:
    """Load dashboard data for a patient from database.

    Args:
        user_id: Database user ID (None for empty data)

    Returns:
        Dict with keys: 'conditions', 'symptom_logs', 'symptom_trends',
        'reminders', 'data_sources'
    """
    logger.info(
        "Loading dashboard data for user_id: %s",
        user_id or "(none)",
    )

    if not user_id:
        logger.warning("load_all_dashboard_data: No user_id provided")
        return {
            "conditions": [],
            "symptom_logs": [],
            "symptom_trends": [],
            "reminders": [],
            "data_sources": [],
        }

    # Fetch all data from database
    conditions = await fetch_conditions(user_id)
    symptoms_data = await fetch_symptoms(user_id)
    reminders = await fetch_reminders(user_id)
    data_sources = await fetch_data_sources(user_id)

    return {
        "conditions": conditions,
        "symptom_logs": symptoms_data.get("symptom_logs", []),
        "symptom_trends": symptoms_data.get("symptom_trends", []),
        "reminders": reminders,
        "data_sources": data_sources,
    }
