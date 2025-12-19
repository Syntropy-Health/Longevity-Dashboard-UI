"""Patient data fetching functions.

Functions for fetching patient management data including patients list,
trend data, treatment data, and biomarker data.
When is_demo=True, returns demo data. Otherwise fetches from database.
"""

from __future__ import annotations

# Standard library
import asyncio
from typing import Any, Dict, List, Optional

# Local application
from longevity_clinic.app.config import current_config, get_logger
from longevity_clinic.app.data.state_schemas import Patient

logger = get_logger("longevity_clinic.patients_functions")


def _get_demo_patients_state():
    """Lazy-load demo patients state."""
    from longevity_clinic.app.data.seed import DEMO_PATIENTS_STATE

    return DEMO_PATIENTS_STATE


def _get_demo_trend_data():
    """Lazy-load demo trend data."""
    from longevity_clinic.app.data.seed import PATIENT_TREND_SEED

    return PATIENT_TREND_SEED


def _get_demo_treatment_data():
    """Lazy-load demo treatment data."""
    from longevity_clinic.app.data.seed import TREATMENT_CHART_SEED

    return TREATMENT_CHART_SEED


def _get_demo_biomarker_data():
    """Lazy-load demo biomarker data."""
    from longevity_clinic.app.data.seed import BIOMARKER_CHART_SEED

    return BIOMARKER_CHART_SEED


async def fetch_patients(
    is_demo: Optional[bool] = None,
) -> List[Patient]:
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
        return _get_demo_patients_state()

    # Fetch from database
    from longevity_clinic.app.functions.db_utils import get_all_patients_sync

    try:
        users = await asyncio.to_thread(get_all_patients_sync)
        patients: List[Patient] = []

        for user in users:
            # Convert User model to Patient TypedDict
            patient: Patient = {
                "id": user.external_id or f"P{user.id}",
                "full_name": user.name,
                "email": user.email or "",
                "phone": user.phone or "",
                "age": user.age or 0,
                "gender": user.gender or "",
                "last_visit": (
                    user.updated_at.strftime("%Y-%m-%d") if user.updated_at else ""
                ),
                "status": user.status or "Active",
                "biomarker_score": 0,  # Would need to compute from actual biomarkers
                "medical_history": "",
                "next_appointment": "",
                "assigned_treatments": [],
            }
            patients.append(patient)

        logger.info("fetch_patients: Returning %d patients from DB", len(patients))
        return patients
    except Exception as e:
        logger.error("fetch_patients: Failed to fetch from DB - %s", e)
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
        return _get_demo_trend_data()

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
        return _get_demo_treatment_data()

    # TODO: Implement API call
    logger.warning("fetch_treatment_data: API not implemented, returning empty list")
    return []


async def fetch_biomarker_analytics_data(
    is_demo: Optional[bool] = False,
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
        return _get_demo_biomarker_data()

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
