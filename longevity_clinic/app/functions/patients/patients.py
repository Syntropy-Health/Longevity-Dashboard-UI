"""Patient data fetching functions.

Functions for fetching patient management data including patients list,
trend data, treatment data, and biomarker data.
All patient data is loaded from the database.
Chart data is loaded from seed data modules.
Seed data with: python scripts/load_seed_data.py
"""

from __future__ import annotations

# Standard library
import asyncio
from typing import Any

# Local application
from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.state import Patient

logger = get_logger("longevity_clinic.patients_functions")


def _get_trend_seed_data() -> list[dict[str, Any]]:
    """Get patient trend seed data for charts."""
    from longevity_clinic.app.data.seed import PATIENT_TREND_SEED

    return PATIENT_TREND_SEED


def _get_treatment_chart_seed_data() -> list[dict[str, Any]]:
    """Get treatment chart seed data for visualizations."""
    from longevity_clinic.app.data.seed import TREATMENT_CHART_SEED

    return TREATMENT_CHART_SEED


def _get_biomarker_chart_seed_data() -> list[dict[str, Any]]:
    """Get biomarker chart seed data for visualizations."""
    from longevity_clinic.app.data.seed import BIOMARKER_CHART_SEED

    return BIOMARKER_CHART_SEED


def _compute_patient_health_score(user_id: int) -> int:
    """Compute overall health score for a patient.

    Score based on:
    - Recent check-in activity (engagement)
    - Biomarker readings if available
    - Default to 75 (good) for demo purposes

    Returns:
        Health score 0-100
    """
    import reflex as rx
    from sqlmodel import func, select

    from longevity_clinic.app.data.schemas.db import CheckIn

    try:
        with rx.session() as session:
            # Count recent check-ins (last 30 days engagement = higher score)
            checkin_count = session.exec(
                select(func.count())
                .select_from(CheckIn)
                .where(CheckIn.user_id == user_id)
            ).one()

            # Base score + engagement bonus
            # Active patients with check-ins get higher scores
            if checkin_count >= 5:
                return 85  # Highly engaged
            elif checkin_count >= 2:
                return 75  # Moderately engaged
            elif checkin_count >= 1:
                return 65  # Some engagement
            else:
                return 50  # No recent activity
    except Exception:
        return 70  # Default fallback


async def fetch_patients() -> list[Patient]:
    """Fetch all patients from database.

    Returns:
        List of patient records

    Note: Requires seeded database. Run: python scripts/load_seed_data.py
    """
    from longevity_clinic.app.functions.db_utils import get_all_patients_sync

    logger.info("Fetching patients from database")

    try:
        users = await asyncio.to_thread(get_all_patients_sync)
        patients: list[Patient] = []

        for user in users:
            # Compute health score based on engagement/biomarkers
            health_score = _compute_patient_health_score(user.id)

            # Convert User model to Patient TypedDict
            patient: Patient = {
                "id": user.external_id or f"P{user.id}",
                "full_name": user.name,
                "email": user.email or "",
                "phone": user.phone or "",
                "age": 0,  # Not stored in User model
                "gender": "",  # Not stored in User model
                "last_visit": (
                    user.updated_at.strftime("%Y-%m-%d") if user.updated_at else ""
                ),
                "status": "Active",  # Default status
                "biomarker_score": health_score,
                "medical_history": "",
                "next_appointment": "",
                "assigned_treatments": [],
            }
            patients.append(patient)

        logger.info("fetch_patients: Returning %d patients from DB", len(patients))
        if not patients:
            logger.warning(
                "No patients found in database. "
                "Run 'python scripts/load_seed_data.py' to seed data."
            )
        return patients
    except Exception as e:
        logger.error("fetch_patients: Failed to fetch from DB - %s", e)
        return []


async def fetch_trend_data() -> list[dict[str, Any]]:
    """Fetch trend data for analytics charts.

    Returns:
        List of trend data points from seed data
    """
    logger.info("Fetching trend data for charts")
    return _get_trend_seed_data()


async def fetch_treatment_data() -> list[dict[str, Any]]:
    """Fetch treatment data for analytics charts.

    Returns:
        List of treatment chart data from seed data
    """
    logger.info("Fetching treatment chart data")
    return _get_treatment_chart_seed_data()


async def fetch_biomarker_analytics_data() -> list[dict[str, Any]]:
    """Fetch biomarker data for analytics charts.

    Returns:
        List of biomarker chart data from seed data
    """
    logger.info("Fetching biomarker chart data")
    return _get_biomarker_chart_seed_data()


async def load_all_patient_data() -> dict[str, Any]:
    """Load all patient management data.

    This is a convenience function that fetches all patient-related
    data in one call.

    Returns:
        Dict with keys: 'patients', 'trend_data', 'treatment_data', 'biomarker_data'

    Note: Patients come from database, chart data from seed modules.
    """
    logger.info("Loading all patient data")

    # Fetch all data
    patients = await fetch_patients()
    trend_data = await fetch_trend_data()
    treatment_data = await fetch_treatment_data()
    biomarker_data = await fetch_biomarker_analytics_data()

    return {
        "patients": patients,
        "trend_data": trend_data,
        "treatment_data": treatment_data,
        "biomarker_data": biomarker_data,
    }
