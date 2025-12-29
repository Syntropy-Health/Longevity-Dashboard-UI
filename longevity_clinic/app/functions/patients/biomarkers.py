"""Biomarker data fetching and processing functions.

This module contains functions for fetching and processing biomarker data.
All data is loaded from the database.
Seed data with: python scripts/load_seed_data.py
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.state import Biomarker, BiomarkerDataPoint
from longevity_clinic.app.functions.db_utils import (
    get_appointments_for_patient_sync,
    get_patient_biomarkers_sync,
    get_patient_treatments_sync,
)
from longevity_clinic.app.functions.db_utils.users import get_user_by_external_id_sync

logger = get_logger("longevity_clinic.biomarkers")


# =============================================================================
# Biomarker Fetching Functions
# =============================================================================


async def fetch_biomarkers(
    patient_id: str | None = None,
) -> list[Biomarker]:
    """Fetch biomarker data for a patient from database.

    Args:
        patient_id: Patient external ID (e.g., 'P001') or None for current

    Returns:
        List of biomarker records

    Note: Requires seeded database. Run: python scripts/load_seed_data.py
    """
    logger.info(
        "Fetching biomarkers for patient: %s",
        patient_id or "current",
    )

    # Fetch from database
    external_id = patient_id or "P001"  # Default to primary demo user
    biomarkers = get_patient_biomarkers_sync(external_id=external_id)

    if biomarkers:
        logger.info("fetch_biomarkers: Loaded %d biomarkers from DB", len(biomarkers))
        return biomarkers

    logger.warning(
        "No biomarker data found in database. "
        "Run 'python scripts/load_seed_data.py' to seed data."
    )
    return []


async def fetch_biomarker_history(
    biomarker_id: str,
    patient_id: str | None = None,
    days: int = 365,
) -> list[BiomarkerDataPoint]:
    """Fetch historical data points for a specific biomarker from database.

    Args:
        biomarker_id: The biomarker to fetch history for
        patient_id: Patient ID (None = current patient)
        days: Number of days of history to fetch

    Returns:
        List of biomarker data points with dates and values

    Note: Requires seeded database. Run: python scripts/load_seed_data.py
    """
    logger.info(
        "Fetching biomarker history: %s for patient %s (%d days)",
        biomarker_id,
        patient_id or "current",
        days,
    )

    # Fetch all biomarkers and find the specific one
    biomarkers = await fetch_biomarkers(patient_id)
    for biomarker in biomarkers:
        if biomarker.get("id") == biomarker_id or biomarker.get("name") == biomarker_id:
            return biomarker.get("history", [])

    logger.warning("Biomarker %s not found", biomarker_id)
    return []


async def fetch_treatments(
    patient_id: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch treatments assigned to a patient from database.

    Args:
        patient_id: Patient external ID (e.g., 'P001') or None for default

    Returns:
        List of treatment records from database (empty if no data)
    """
    logger.info(
        "Fetching treatments for patient: %s",
        patient_id or "current",
    )

    external_id = patient_id or "P001"
    user = get_user_by_external_id_sync(external_id)
    if not user:
        logger.warning("fetch_treatments: User %s not found", external_id)
        return []

    treatments = get_patient_treatments_sync(user.id)
    if treatments:
        logger.info("fetch_treatments: Loaded %d treatments from DB", len(treatments))
        return [
            {
                "id": t["treatment_id"],
                "name": t["treatment_name"],
                "start_date": (t["start_date"].isoformat() if t["start_date"] else ""),
                "status": t["status"],
                "progress": t["progress"],
            }
            for t in treatments
        ]

    logger.warning(
        "No treatment data found in database for user %s. "
        "Run 'python scripts/load_seed_data.py' to seed data.",
        external_id,
    )
    return []


async def fetch_appointments(
    patient_id: str | None = None,
    upcoming_only: bool = True,
) -> list[dict[str, Any]]:
    """Fetch appointments for a patient from database.

    Args:
        patient_id: Patient external ID (e.g., 'P001') or None for default
        upcoming_only: If True, only return future appointments

    Returns:
        List of appointment records from database (empty if no data)
    """
    logger.info(
        "Fetching appointments for patient: %s (upcoming=%s)",
        patient_id or "current",
        upcoming_only,
    )

    external_id = patient_id or "P001"
    appointments = get_appointments_for_patient_sync(external_id)

    if not appointments:
        logger.warning(
            "No appointment data found in database for patient %s. "
            "Run 'python scripts/load_seed_data.py' to seed data.",
            external_id,
        )
        return []

    if upcoming_only:
        today = datetime.now().date()
        appointments = [
            a
            for a in appointments
            if (isinstance(a.get("date"), str) and a["date"] >= today.isoformat())
            or (isinstance(a.get("date"), datetime) and a["date"].date() >= today)
        ]

    logger.info("fetch_appointments: Loaded %d appointments from DB", len(appointments))
    return appointments


async def load_all_biomarker_data(
    patient_id: str | None = None,
) -> dict[str, Any]:
    """Load all biomarker-related data for a patient dashboard.

    This is a convenience function that fetches biomarkers, treatments,
    and appointments in one call.

    Args:
        patient_id: Patient ID (None = current patient)

    Returns:
        Dict with keys: 'biomarkers', 'treatments', 'appointments'

    Note: Requires seeded database. Run: python scripts/load_seed_data.py
    """
    logger.info(
        "Loading all biomarker data for patient: %s",
        patient_id or "current",
    )

    # Fetch all data
    biomarkers = await fetch_biomarkers(patient_id)
    treatments = await fetch_treatments(patient_id)
    appointments = await fetch_appointments(patient_id)

    return {
        "biomarkers": biomarkers,
        "treatments": treatments,
        "appointments": appointments,
    }
