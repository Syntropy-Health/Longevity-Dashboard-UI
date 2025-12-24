"""Biomarker data fetching and processing functions.

This module contains functions for fetching and processing biomarker data.
All data is loaded from the database.
Seed data with: python scripts/load_seed_data.py
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.functions.db_utils import (
    get_appointments_for_patient_sync,
    get_patient_biomarkers_sync,
    get_patient_treatments_sync,
)
from longevity_clinic.app.functions.db_utils.users import get_user_by_external_id_sync
from longevity_clinic.app.data.schemas.state import Biomarker, BiomarkerDataPoint

logger = get_logger("longevity_clinic.biomarkers")


# =============================================================================
# Seed data getters for treatments and appointments (chart/display data)
# =============================================================================


def _get_portal_treatments_seed() -> list[dict[str, Any]]:
    """Get portal treatments seed data for patient display."""
    from longevity_clinic.app.data.seed import PORTAL_TREATMENTS_SEED

    return PORTAL_TREATMENTS_SEED


def _get_portal_appointments_seed() -> list[dict[str, Any]]:
    """Get portal appointments seed data for patient display."""
    from longevity_clinic.app.data.seed import PORTAL_APPOINTMENTS_SEED

    return PORTAL_APPOINTMENTS_SEED


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
    """Fetch treatments assigned to a patient.

    Args:
        patient_id: Patient external ID (e.g., 'P001') or None for default

    Returns:
        List of treatment records from database, falling back to seed data
    """
    logger.info(
        "Fetching treatments for patient: %s",
        patient_id or "current",
    )

    # Try DB lookup first
    external_id = patient_id or "P001"
    user = get_user_by_external_id_sync(external_id)
    if user:
        treatments = get_patient_treatments_sync(user.id)
        if treatments:
            logger.info(
                "fetch_treatments: Loaded %d treatments from DB", len(treatments)
            )
            return [
                {
                    "id": t.treatment_id,
                    "name": t.treatment.name if t.treatment else "",
                    "start_date": t.start_date.isoformat() if t.start_date else "",
                    "status": t.status,
                    "progress": t.progress or 0,
                }
                for t in treatments
            ]

    # Fall back to seed data
    logger.debug("fetch_treatments: No DB data, using seed")
    return _get_portal_treatments_seed()


async def fetch_appointments(
    patient_id: str | None = None,
    upcoming_only: bool = True,
) -> list[dict[str, Any]]:
    """Fetch appointments for a patient.

    Args:
        patient_id: Patient external ID (e.g., 'P001') or None for default
        upcoming_only: If True, only return future appointments

    Returns:
        List of appointment records from database, falling back to seed data
    """
    logger.info(
        "Fetching appointments for patient: %s (upcoming=%s)",
        patient_id or "current",
        upcoming_only,
    )

    # Try DB lookup first
    external_id = patient_id or "P001"
    appointments = get_appointments_for_patient_sync(external_id)

    if appointments:
        if upcoming_only:
            today = datetime.now().date()
            appointments = [
                a
                for a in appointments
                if isinstance(a.get("date"), str)
                and a["date"] >= today.isoformat()
                or isinstance(a.get("date"), datetime)
                and a["date"].date() >= today
            ]
        logger.info(
            "fetch_appointments: Loaded %d appointments from DB", len(appointments)
        )
        return appointments

    # Fall back to seed data
    logger.debug("fetch_appointments: No DB data, using seed")
    return _get_portal_appointments_seed()


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
