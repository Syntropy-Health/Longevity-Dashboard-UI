"""Patient data fetching functions.

Functions for fetching patient management data including patients list,
trend data, treatment data, and biomarker data.
When is_demo=True, returns demo data. Otherwise calls the API.
"""

from typing import List, Dict, Any, Optional

from longevity_clinic.app.config import get_logger, current_config
from longevity_clinic.app.data.demo import (
    DEMO_PATIENTS_STATE,
    DEMO_TREND_DATA,
    DEMO_TREATMENT_DATA,
    DEMO_BIOMARKER_DATA,
)

logger = get_logger("longevity_clinic.patients_functions")


async def fetch_patients(
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch all patients.

    Args:
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of patient records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info("Fetching patients (demo=%s)", is_demo)

    if is_demo:
        logger.debug("fetch_patients: Returning demo data")
        return DEMO_PATIENTS_STATE

    # TODO: Implement API call
    logger.warning("fetch_patients: API not implemented, returning empty list")
    return []


async def fetch_trend_data(
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch trend data for analytics.

    Args:
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of trend data points
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info("Fetching trend data (demo=%s)", is_demo)

    if is_demo:
        logger.debug("fetch_trend_data: Returning demo data")
        return DEMO_TREND_DATA

    # TODO: Implement API call
    logger.warning("fetch_trend_data: API not implemented, returning empty list")
    return []


async def fetch_treatment_data(
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch treatment data for analytics.

    Args:
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of treatment data records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info("Fetching treatment data (demo=%s)", is_demo)

    if is_demo:
        logger.debug("fetch_treatment_data: Returning demo data")
        return DEMO_TREATMENT_DATA

    # TODO: Implement API call
    logger.warning("fetch_treatment_data: API not implemented, returning empty list")
    return []


async def fetch_biomarker_analytics_data(
    is_demo: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """Fetch biomarker data for analytics.

    Args:
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        List of biomarker analytics records
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info("Fetching biomarker analytics data (demo=%s)", is_demo)

    if is_demo:
        logger.debug("fetch_biomarker_analytics_data: Returning demo data")
        return DEMO_BIOMARKER_DATA

    # TODO: Implement API call
    logger.warning(
        "fetch_biomarker_analytics_data: API not implemented, returning empty list"
    )
    return []


async def load_all_patient_data(
    is_demo: Optional[bool] = None,
) -> Dict[str, Any]:
    """Load all patient management data.

    This is a convenience function that fetches all patient-related
    data in one call.

    Args:
        is_demo: If True, return demo data. Defaults to config.is_demo.

    Returns:
        Dict with keys: 'patients', 'trend_data', 'treatment_data', 'biomarker_data'
    """
    if is_demo is None:
        is_demo = current_config.is_demo

    logger.info("Loading all patient data (demo=%s)", is_demo)

    # Fetch all data with the same is_demo setting
    patients = await fetch_patients(is_demo=is_demo)
    trend_data = await fetch_trend_data(is_demo=is_demo)
    treatment_data = await fetch_treatment_data(is_demo=is_demo)
    biomarker_data = await fetch_biomarker_analytics_data(is_demo=is_demo)

    return {
        "patients": patients,
        "trend_data": trend_data,
        "treatment_data": treatment_data,
        "biomarker_data": biomarker_data,
    }
