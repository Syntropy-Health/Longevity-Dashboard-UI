"""Biomarker data fetching and processing functions.

This module contains functions for fetching and processing biomarker data.
Currently uses demo data but provides placeholders for API integration.
"""

from typing import List, Dict, Any, Optional

from ....config import get_logger
from ....data.state_schemas import Biomarker, BiomarkerDataPoint

logger = get_logger("longevity_clinic.biomarkers")


async def fetch_biomarkers(
    patient_id: Optional[str] = None,
) -> List[Biomarker]:
    """Fetch biomarker data for a patient.

    Args:
        patient_id: Patient ID to fetch biomarkers for (None = current patient)

    Returns:
        List of biomarker records

    Note:
        Currently returns demo data. In production, this would call
        the biomarker API endpoint.
    """
    logger.info("Fetching biomarkers for patient: %s", patient_id or "current")

    # TODO: Implement API call to fetch biomarkers
    # Example API call structure:
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(
    #         f"{config.biomarker_api_base}/patients/{patient_id}/biomarkers",
    #         headers={"Authorization": f"Bearer {config.api_token}"},
    #     )
    #     return response.json()["data"]

    # For now, return empty (demo data loaded from state default)
    logger.debug("fetch_biomarkers: Using demo data (API not implemented)")
    return []


async def fetch_biomarker_history(
    biomarker_id: str,
    patient_id: Optional[str] = None,
    days: int = 365,
) -> List[BiomarkerDataPoint]:
    """Fetch historical data points for a specific biomarker.

    Args:
        biomarker_id: The biomarker to fetch history for
        patient_id: Patient ID (None = current patient)
        days: Number of days of history to fetch

    Returns:
        List of biomarker data points with dates and values
    """
    logger.info(
        "Fetching biomarker history: %s for patient %s (%d days)",
        biomarker_id,
        patient_id or "current",
        days,
    )

    # TODO: Implement API call
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(
    #         f"{config.biomarker_api_base}/biomarkers/{biomarker_id}/history",
    #         params={"patient_id": patient_id, "days": days},
    #     )
    #     return response.json()["data"]

    logger.debug("fetch_biomarker_history: Using demo data (API not implemented)")
    return []


async def fetch_treatments(
    patient_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Fetch treatments assigned to a patient.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        List of treatment records
    """
    logger.info("Fetching treatments for patient: %s", patient_id or "current")

    # TODO: Implement API call
    logger.debug("fetch_treatments: Using demo data (API not implemented)")
    return []


async def fetch_appointments(
    patient_id: Optional[str] = None,
    upcoming_only: bool = True,
) -> List[Dict[str, Any]]:
    """Fetch appointments for a patient.

    Args:
        patient_id: Patient ID (None = current patient)
        upcoming_only: If True, only return future appointments

    Returns:
        List of appointment records
    """
    logger.info(
        "Fetching appointments for patient: %s (upcoming=%s)",
        patient_id or "current",
        upcoming_only,
    )

    # TODO: Implement API call
    logger.debug("fetch_appointments: Using demo data (API not implemented)")
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
) -> Dict[str, Any]:
    """Load all biomarker-related data for a patient dashboard.

    This is a convenience function that fetches biomarkers, treatments,
    and appointments in one call.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        Dict with keys: 'biomarkers', 'treatments', 'appointments'
    """
    logger.info("Loading all biomarker data for patient: %s", patient_id or "current")

    # In production, these could be parallelized with asyncio.gather
    # For now, they return empty lists (demo data loaded from state defaults)
    biomarkers = await fetch_biomarkers(patient_id)
    treatments = await fetch_treatments(patient_id)
    appointments = await fetch_appointments(patient_id)

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
