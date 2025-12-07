"""Dashboard data fetching functions.

Functions for fetching dashboard-related data including nutrition,
medications, conditions, symptoms, and data sources.
When is_demo=True, returns demo data. Otherwise calls the API.
"""

from typing import List, Dict, Any, Optional

from longevity_clinic.app.config import get_logger, current_config
from longevity_clinic.app.data.demo import (
    DEMO_NUTRITION_SUMMARY,
    DEMO_FOOD_ENTRIES,
    DEMO_MEDICATIONS,
    DEMO_CONDITIONS,
    DEMO_SYMPTOMS,
    DEMO_SYMPTOM_LOGS,
    DEMO_REMINDERS,
    DEMO_SYMPTOM_TRENDS,
    DEMO_DATA_SOURCES,
)

logger = get_logger("longevity_clinic.dashboard_functions")


async def fetch_nutrition_summary(
    patient_id: Optional[str] = None,
    date: Optional[str] = None,
    is_demo: Optional[bool] = None,
) -> Dict[str, Any]:
    """Fetch nutrition summary for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        date: Date to fetch summary for (None = today)
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        Nutrition summary dict with calories, protein, carbs, fat
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching nutrition summary for patient: %s, date: %s (demo=%s)",
        patient_id or "current",
        date or "today",
        is_demo,
    )

    if is_demo:
        logger.debug("fetch_nutrition_summary: Returning demo data")
        return DEMO_NUTRITION_SUMMARY

    # TODO: Implement API call
    logger.warning("fetch_nutrition_summary: API not implemented, returning empty dict")
    return {}


async def fetch_medications(
    patient_id: Optional[str] = None,
    active_only: bool = True,
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch medications for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        active_only: Only return active medications
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of medication records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching medications for patient: %s (active_only=%s, demo=%s)",
        patient_id or "current",
        active_only,
        is_demo,
    )

    if is_demo:
        logger.debug("fetch_medications: Returning demo data")
        return DEMO_MEDICATIONS

    # TODO: Implement API call
    logger.warning("fetch_medications: API not implemented, returning empty list")
    return []


async def fetch_conditions(
    patient_id: Optional[str] = None,
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch medical conditions for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of condition records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching conditions for patient: %s (demo=%s)",
        patient_id or "current",
        is_demo,
    )

    if is_demo:
        logger.debug("fetch_conditions: Returning demo data")
        return DEMO_CONDITIONS

    # TODO: Implement API call
    logger.warning("fetch_conditions: API not implemented, returning empty list")
    return []


async def fetch_symptoms(
    patient_id: Optional[str] = None,
    days: int = 30,
    is_demo: Optional[bool] = None,
) -> Dict[str, Any]:
    """Fetch symptom data for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        days: Number of days of history
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        Dict with 'symptoms', 'symptom_logs', 'symptom_trends' keys
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching symptoms for patient: %s (%d days, demo=%s)",
        patient_id or "current",
        days,
        is_demo,
    )

    if is_demo:
        logger.debug("fetch_symptoms: Returning demo data")
        return {
            "symptoms": DEMO_SYMPTOMS,
            "symptom_logs": DEMO_SYMPTOM_LOGS,
            "symptom_trends": DEMO_SYMPTOM_TRENDS,
        }

    # TODO: Implement API call
    logger.warning("fetch_symptoms: API not implemented, returning empty data")
    return {"symptoms": [], "symptom_logs": [], "symptom_trends": []}


async def fetch_data_sources(
    patient_id: Optional[str] = None,
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch connected data sources for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of data source records with connection status
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching data sources for patient: %s (demo=%s)",
        patient_id or "current",
        is_demo,
    )

    if is_demo:
        logger.debug("fetch_data_sources: Returning demo data")
        return DEMO_DATA_SOURCES

    # TODO: Implement API call
    logger.warning("fetch_data_sources: API not implemented, returning empty list")
    return []


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


async def fetch_food_entries(
    patient_id: Optional[str] = None,
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch food entries for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of food entry records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching food entries for patient: %s (demo=%s)",
        patient_id or "current",
        is_demo,
    )

    if is_demo:
        logger.debug("fetch_food_entries: Returning demo data")
        return DEMO_FOOD_ENTRIES

    # TODO: Implement API call
    logger.warning("fetch_food_entries: API not implemented, returning empty list")
    return []


async def fetch_reminders(
    patient_id: Optional[str] = None,
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch reminders for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of reminder records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching reminders for patient: %s (demo=%s)", patient_id or "current", is_demo
    )

    if is_demo:
        logger.debug("fetch_reminders: Returning demo data")
        return DEMO_REMINDERS

    # TODO: Implement API call
    logger.warning("fetch_reminders: API not implemented, returning empty list")
    return []


async def load_all_dashboard_data(
    patient_id: Optional[str] = None,
    is_demo: Optional[bool] = None,
) -> Dict[str, Any]:
    """Load all dashboard data for a patient.

    This is a convenience function that fetches all dashboard-related
    data in one call.

    Args:
        patient_id: Patient ID (None = current patient)
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        Dict with keys: 'nutrition_summary', 'food_entries', 'medications',
        'conditions', 'symptoms', 'symptom_logs', 'symptom_trends',
        'reminders', 'data_sources'
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Loading all dashboard data for patient: %s (demo=%s)",
        patient_id or "current",
        is_demo,
    )

    # Fetch all data with the same is_demo setting
    nutrition_summary = await fetch_nutrition_summary(patient_id, is_demo=is_demo)
    food_entries = await fetch_food_entries(patient_id, is_demo=is_demo)
    medications = await fetch_medications(patient_id, is_demo=is_demo)
    conditions = await fetch_conditions(patient_id, is_demo=is_demo)
    symptoms_data = await fetch_symptoms(patient_id, is_demo=is_demo)
    reminders = await fetch_reminders(patient_id, is_demo=is_demo)
    data_sources = await fetch_data_sources(patient_id, is_demo=is_demo)

    return {
        "nutrition_summary": nutrition_summary,
        "food_entries": food_entries,
        "medications": medications,
        "conditions": conditions,
        "symptoms": symptoms_data.get("symptoms", []),
        "symptom_logs": symptoms_data.get("symptom_logs", []),
        "symptom_trends": symptoms_data.get("symptom_trends", []),
        "reminders": reminders,
        "data_sources": data_sources,
    }
