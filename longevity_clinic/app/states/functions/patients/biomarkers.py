"""Biomarker data fetching and processing functions.

This module contains functions for fetching and processing biomarker data.
When is_demo=True, returns demo data. Otherwise calls the API.
"""

from typing import List, Dict, Any, Optional

from ....config import get_logger, current_config
from ....data.state_schemas import Biomarker, BiomarkerDataPoint
from ....data.demo import (
    DEMO_PORTAL_BIOMARKERS,
    DEMO_PORTAL_TREATMENTS,
    DEMO_PORTAL_APPOINTMENTS,
)

logger = get_logger("longevity_clinic.biomarkers")


async def fetch_biomarkers(
    patient_id: Optional[str] = None,
    is_demo: Optional[bool] = None,
) -> List[Biomarker]:
    """Fetch biomarker data for a patient.

    Args:
        patient_id: Patient ID to fetch biomarkers for (None = current patient)
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of biomarker records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching biomarkers for patient: %s (demo=%s)",
        patient_id or "current",
        is_demo,
    )

    if is_demo:
        logger.debug("fetch_biomarkers: Returning demo data")
        return DEMO_PORTAL_BIOMARKERS

    # TODO: Implement API call to fetch biomarkers
    # Example API call structure:
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(
    #         f"{config.biomarker_api_base}/patients/{patient_id}/biomarkers",
    #         headers={"Authorization": f"Bearer {config.api_token}"},
    #     )
    #     return response.json()["data"]

    logger.warning("fetch_biomarkers: API not implemented, returning empty list")
    return []


async def fetch_biomarker_history(
    biomarker_id: str,
    patient_id: Optional[str] = None,
    days: int = 365,
    is_demo: Optional[bool] = None,
) -> List[BiomarkerDataPoint]:
    """Fetch historical data points for a specific biomarker.

    Args:
        biomarker_id: The biomarker to fetch history for
        patient_id: Patient ID (None = current patient)
        days: Number of days of history to fetch
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of biomarker data points with dates and values
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching biomarker history: %s for patient %s (%d days, demo=%s)",
        biomarker_id,
        patient_id or "current",
        days,
        is_demo,
    )

    if is_demo:
        # Find the biomarker in demo data and return its history
        for biomarker in DEMO_PORTAL_BIOMARKERS:
            if (
                biomarker.get("id") == biomarker_id
                or biomarker.get("name") == biomarker_id
            ):
                return biomarker.get("history", [])
        return []

    # TODO: Implement API call
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(
    #         f"{config.biomarker_api_base}/biomarkers/{biomarker_id}/history",
    #         params={"patient_id": patient_id, "days": days},
    #     )
    #     return response.json()["data"]

    logger.warning("fetch_biomarker_history: API not implemented, returning empty list")
    return []


async def fetch_treatments(
    patient_id: Optional[str] = None,
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch treatments assigned to a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of treatment records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching treatments for patient: %s (demo=%s)",
        patient_id or "current",
        is_demo,
    )

    if is_demo:
        logger.debug("fetch_treatments: Returning demo data")
        return DEMO_PORTAL_TREATMENTS

    # TODO: Implement API call
    logger.warning("fetch_treatments: API not implemented, returning empty list")
    return []


async def fetch_appointments(
    patient_id: Optional[str] = None,
    upcoming_only: bool = True,
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch appointments for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        upcoming_only: If True, only return future appointments
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of appointment records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Fetching appointments for patient: %s (upcoming=%s, demo=%s)",
        patient_id or "current",
        upcoming_only,
        is_demo,
    )

    if is_demo:
        logger.debug("fetch_appointments: Returning demo data")
        return DEMO_PORTAL_APPOINTMENTS

    # TODO: Implement API call
    logger.warning("fetch_appointments: API not implemented, returning empty list")
    return []


def calculate_biomarker_status(
    value: float,
    optimal_min: float,
    optimal_max: float,
) -> str:
    """Calculate biomarker status based on value and optimal range.

    Args:
        value: Current biomarker value
        optimal_min: Lower bound of optimal range
        optimal_max: Upper bound of optimal range

    Returns:
        Status string: 'optimal', 'low', 'high', or 'critical'
    """
    if optimal_min <= value <= optimal_max:
        return "optimal"

    # Calculate how far outside range
    if value < optimal_min:
        deviation = (optimal_min - value) / optimal_min
        return "critical" if deviation > 0.3 else "low"
    else:
        deviation = (value - optimal_max) / optimal_max
        return "critical" if deviation > 0.3 else "high"


def calculate_biomarker_trend(
    history: List[BiomarkerDataPoint],
    lookback_points: int = 5,
) -> str:
    """Calculate trend direction from biomarker history.

    Args:
        history: List of historical data points (newest first)
        lookback_points: Number of points to consider

    Returns:
        Trend string: 'improving', 'stable', 'declining'
    """
    if len(history) < 2:
        return "stable"

    recent = history[:lookback_points]
    if len(recent) < 2:
        return "stable"

    # Simple linear trend: compare first and last
    first_value = recent[-1].get("value", 0)
    last_value = recent[0].get("value", 0)

    change_pct = (last_value - first_value) / first_value if first_value else 0

    if abs(change_pct) < 0.05:
        return "stable"
    elif change_pct > 0:
        return "improving"
    else:
        return "declining"


def format_biomarker_value(
    value: float,
    unit: str,
    precision: int = 1,
) -> str:
    """Format biomarker value with unit.

    Args:
        value: The biomarker value
        unit: Unit of measurement
        precision: Decimal places

    Returns:
        Formatted string like "125.5 mg/dL"
    """
    return f"{value:.{precision}f} {unit}"


async def load_all_biomarker_data(
    patient_id: Optional[str] = None,
    is_demo: Optional[bool] = None,
) -> Dict[str, Any]:
    """Load all biomarker-related data for a patient dashboard.

    This is a convenience function that fetches biomarkers, treatments,
    and appointments in one call.

    Args:
        patient_id: Patient ID (None = current patient)
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        Dict with keys: 'biomarkers', 'treatments', 'appointments'
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info(
        "Loading all biomarker data for patient: %s (demo=%s)",
        patient_id or "current",
        is_demo,
    )

    # Fetch all data with the same is_demo setting
    biomarkers = await fetch_biomarkers(patient_id, is_demo=is_demo)
    treatments = await fetch_treatments(patient_id, is_demo=is_demo)
    appointments = await fetch_appointments(patient_id, is_demo=is_demo)

    return {
        "biomarkers": biomarkers,
        "treatments": treatments,
        "appointments": appointments,
    }


def get_biomarker_by_name(
    biomarkers: List[Biomarker],
    name: str,
) -> Optional[Biomarker]:
    """Find a biomarker by name.

    Args:
        biomarkers: List of biomarker records
        name: Biomarker name to find

    Returns:
        Biomarker dict or None if not found
    """
    for biomarker in biomarkers:
        if biomarker.get("name", "").lower() == name.lower():
            return biomarker
    return None


def get_biomarker_optimal_range(biomarker: Biomarker) -> Dict[str, float]:
    """Extract optimal range from biomarker.

    Args:
        biomarker: Biomarker dict

    Returns:
        Dict with 'min' and 'max' keys
    """
    return {
        "min": biomarker.get("optimal_min", 0),
        "max": biomarker.get("optimal_max", 0),
    }
