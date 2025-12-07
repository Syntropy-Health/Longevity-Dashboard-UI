"""Dashboard data fetching functions.

Functions for fetching dashboard-related data including nutrition,
medications, conditions, symptoms, and data sources.
"""

from typing import List, Dict, Any, Optional

from longevity_clinic.app.config import get_logger

logger = get_logger("longevity_clinic.dashboard_functions")


async def fetch_nutrition_summary(
    patient_id: Optional[str] = None,
    date: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch nutrition summary for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        date: Date to fetch summary for (None = today)

    Returns:
        Nutrition summary dict with calories, protein, carbs, fat
    """
    logger.info(
        "Fetching nutrition summary for patient: %s, date: %s",
        patient_id or "current",
        date or "today",
    )

    # TODO: Implement API call
    logger.debug("fetch_nutrition_summary: Using demo data (API not implemented)")
    return {}


async def fetch_medications(
    patient_id: Optional[str] = None,
    active_only: bool = True,
) -> List[Dict[str, Any]]:
    """Fetch medications for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        active_only: Only return active medications

    Returns:
        List of medication records
    """
    logger.info(
        "Fetching medications for patient: %s (active_only=%s)",
        patient_id or "current",
        active_only,
    )

    # TODO: Implement API call
    logger.debug("fetch_medications: Using demo data (API not implemented)")
    return []


async def fetch_conditions(
    patient_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Fetch medical conditions for a patient.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        List of condition records
    """
    logger.info("Fetching conditions for patient: %s", patient_id or "current")

    # TODO: Implement API call
    logger.debug("fetch_conditions: Using demo data (API not implemented)")
    return []


async def fetch_symptoms(
    patient_id: Optional[str] = None,
    days: int = 30,
) -> List[Dict[str, Any]]:
    """Fetch symptom logs for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        days: Number of days of history

    Returns:
        List of symptom records
    """
    logger.info(
        "Fetching symptoms for patient: %s (%d days)", patient_id or "current", days
    )

    # TODO: Implement API call
    logger.debug("fetch_symptoms: Using demo data (API not implemented)")
    return []


async def fetch_data_sources(
    patient_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Fetch connected data sources for a patient.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        List of data source records with connection status
    """
    logger.info("Fetching data sources for patient: %s", patient_id or "current")

    # TODO: Implement API call
    logger.debug("fetch_data_sources: Using demo data (API not implemented)")
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
