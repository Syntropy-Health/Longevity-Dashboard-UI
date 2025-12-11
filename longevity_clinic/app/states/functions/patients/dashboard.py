"""Dashboard data fetching functions.

Functions for fetching static dashboard-related data including
conditions, data sources, and reminders.

NOTE: Medications, food entries, and symptoms are now sourced from
the database via CDC pipeline (call log extraction). These functions
provide only static/default data for things not yet in the DB.
"""

from typing import List, Dict, Any, Optional

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.state_schemas import (
    Condition,
    SymptomEntry,
    SymptomTrend,
    DataSource,
)
from longevity_clinic.app.data.demo import (
    DEMO_CONDITIONS,
    DEMO_SYMPTOM_LOGS,
    DEMO_REMINDERS,
    DEMO_SYMPTOM_TRENDS,
    DEMO_DATA_SOURCES,
)

logger = get_logger("longevity_clinic.dashboard_functions")


# NOTE: fetch_nutrition_summary, fetch_medications, and fetch_food_entries
# have been removed. This data now comes from the database via CDC pipeline
# (call log extraction). See dashboard_state._load_health_entries_from_db()


async def fetch_conditions(
    patient_id: Optional[str] = None,
) -> List[Condition]:
    """Fetch medical conditions for a patient.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        List of Condition objects (static demo data for now)
    """
    logger.info(
        "Fetching conditions for patient: %s",
        patient_id or "current",
    )

    # Return static conditions - these don't come from call logs yet
    return [
        Condition(**cond) if isinstance(cond, dict) else cond
        for cond in DEMO_CONDITIONS
    ]


async def fetch_symptoms(
    patient_id: Optional[str] = None,
    days: int = 30,
) -> Dict[str, Any]:
    """Fetch symptom data for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        days: Number of days of history

    Returns:
        Dict with 'symptom_logs' and 'symptom_trends' keys.
        NOTE: Actual symptoms come from DB via CDC pipeline.
    """
    logger.info(
        "Fetching symptom logs/trends for patient: %s (%d days)",
        patient_id or "current",
        days,
    )

    # Return static symptom logs and trends (symptoms come from DB)
    return {
        "symptom_logs": [
            SymptomEntry(**sl) if isinstance(sl, dict) else sl
            for sl in DEMO_SYMPTOM_LOGS
        ],
        "symptom_trends": [
            SymptomTrend(**st) if isinstance(st, dict) else st
            for st in DEMO_SYMPTOM_TRENDS
        ],
    }


async def fetch_data_sources(
    patient_id: Optional[str] = None,
) -> List[DataSource]:
    """Fetch connected data sources for a patient.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        List of DataSource objects (static demo data for now)
    """
    logger.info(
        "Fetching data sources for patient: %s",
        patient_id or "current",
    )

    # Return static data sources
    return [
        DataSource(**ds) if isinstance(ds, dict) else ds for ds in DEMO_DATA_SOURCES
    ]


async def sync_data_source(
    source_id: str,
    patient_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Trigger sync for a connected data source.

    Args:
        source_id: Data source to sync
        patient_id: Patient ID (None = current patient)

    Returns:
        Sync result with status and any new data
    """
    logger.info(
        "Syncing data source %s for patient: %s", source_id, patient_id or "current"
    )

    # TODO: Implement API call
    logger.debug("sync_data_source: Not implemented")
    return {"status": "pending", "message": "Sync not implemented"}


def calculate_medication_adherence(
    medications: List[Dict[str, Any]],
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


def categorize_conditions(
    conditions: List[Dict[str, Any]],
) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize conditions by status.

    Args:
        conditions: List of condition records

    Returns:
        Dict with 'active', 'managed', 'resolved' lists
    """
    result = {
        "active": [],
        "managed": [],
        "resolved": [],
    }

    for condition in conditions:
        status = condition.get("status", "active").lower()
        if status in result:
            result[status].append(condition)
        else:
            result["active"].append(condition)

    return result


def calculate_symptom_trends(
    symptom_logs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Calculate symptom frequency and severity trends.

    Args:
        symptom_logs: List of symptom log entries

    Returns:
        List of symptom trend summaries
    """
    if not symptom_logs:
        return []

    # Group by symptom
    symptom_counts: Dict[str, List[int]] = {}
    for log in symptom_logs:
        name = log.get("symptom_name", "Unknown")
        severity = log.get("severity", 5)
        if name not in symptom_counts:
            symptom_counts[name] = []
        symptom_counts[name].append(severity)

    # Calculate trends
    trends = []
    for name, severities in symptom_counts.items():
        avg_severity = sum(severities) / len(severities)
        trends.append(
            {
                "symptom": name,
                "occurrences": len(severities),
                "avg_severity": round(avg_severity, 1),
                "max_severity": max(severities),
            }
        )

    return sorted(trends, key=lambda x: x["occurrences"], reverse=True)


# NOTE: fetch_food_entries has been removed.
# Food entries now come from the database via CDC pipeline.


async def fetch_reminders(
    patient_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Fetch reminders for a patient.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        List of reminder records (static demo data for now)
    """
    logger.info(
        "Fetching reminders for patient: %s", patient_id or "current"
    )

    # Return static reminders
    return DEMO_REMINDERS


async def load_all_dashboard_data(
    patient_id: Optional[str] = None,
) -> Dict[str, Any]:
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
