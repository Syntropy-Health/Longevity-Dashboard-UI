"""Database seeding module for Longevity Clinic.

Modular seed data loading organized by domain:
- users: User accounts (patients, admin)
- checkins: Patient check-ins
- notifications: Admin and patient notifications
- appointments: Patient appointments
- call_logs: Sample call log data
- treatments: Treatment catalog and protocols
- biomarkers: Biomarker definitions and readings
- health: Health entries (medications, food, symptoms)
- clinic_metrics: Clinic operational metrics

Usage:
    from scripts.seeding import load_all_seed_data
    load_all_seed_data(reset=False)

Or use the CLI:
    python scripts/load_seed_data.py --reset
"""

from .base import get_engine, create_tables, drop_tables, SeedResult
from .users import load_users
from .checkins import load_checkins
from .notifications import load_notifications
from .appointments import load_appointments
from .call_logs import load_call_logs
from .treatments import load_treatments, load_treatment_protocol_metrics
from .biomarkers import (
    load_biomarker_definitions,
    load_biomarker_readings,
    load_biomarker_aggregates,
)
from .health import load_health_entries
from .clinic_metrics import (
    load_patient_visits,
    load_daily_metrics,
    load_provider_metrics,
)


def load_all_seed_data(reset: bool = False) -> dict[str, SeedResult]:
    """Load all seed data into the database.

    Args:
        reset: If True, drop all tables before loading.

    Returns:
        Dict mapping loader name to SeedResult with counts.
    """
    from sqlmodel import Session

    results = {}
    engine = get_engine()

    if reset:
        drop_tables(engine)

    create_tables(engine)

    with Session(engine) as session:
        # Core data (order matters - users first)
        results["users"] = load_users(session)
        user_id_map = results["users"].id_map

        results["checkins"] = load_checkins(session, user_id_map)
        results["notifications"] = load_notifications(session, user_id_map)
        results["appointments"] = load_appointments(engine, user_id_map)
        results["call_logs"] = load_call_logs(session, user_id_map)

        # Treatments
        results["treatments"] = load_treatments(session)
        results["treatment_protocols"] = load_treatment_protocol_metrics(session)

        # Health entries for primary user
        results["health"] = load_health_entries(session, user_id_map)

        # Biomarkers
        results["biomarker_definitions"] = load_biomarker_definitions(session)
        biomarker_id_map = results["biomarker_definitions"].id_map
        results["biomarker_readings"] = load_biomarker_readings(
            session, user_id_map, biomarker_id_map
        )
        results["biomarker_aggregates"] = load_biomarker_aggregates(session)

        # Clinic metrics
        results["patient_visits"] = load_patient_visits(session)
        results["daily_metrics"] = load_daily_metrics(session)
        results["provider_metrics"] = load_provider_metrics(session)

    return results


__all__ = [
    # Base utilities
    "get_engine",
    "create_tables",
    "drop_tables",
    "SeedResult",
    # Individual loaders
    "load_users",
    "load_checkins",
    "load_notifications",
    "load_call_logs",
    "load_treatments",
    "load_treatment_protocol_metrics",
    "load_biomarker_definitions",
    "load_biomarker_readings",
    "load_biomarker_aggregates",
    "load_health_entries",
    "load_patient_visits",
    "load_daily_metrics",
    "load_provider_metrics",
    "load_appointments",
    # Convenience function
    "load_all_seed_data",
]
