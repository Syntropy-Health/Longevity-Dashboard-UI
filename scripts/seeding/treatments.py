"""Treatment seed data loading."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlmodel import Session, select

from longevity_clinic.app.data.schemas.db import (
    PatientTreatment,
    Treatment,
    TreatmentProtocolMetric,
)
from longevity_clinic.app.data.seed import (
    PATIENT_TREATMENT_ASSIGNMENTS_SEED,
    TREATMENT_CATALOG_SEED,
    TREATMENT_PROTOCOL_METRICS_SEED,
)

from .base import SeedResult, print_section


def load_treatments(session: Session) -> SeedResult:
    """Load treatment catalog from TREATMENT_CATALOG_SEED.

    Args:
        session: Database session

    Returns:
        SeedResult with id_map of treatment_id -> database id
    """
    print_section("Loading treatments")
    result = SeedResult(name="treatments")

    for treatment_data in TREATMENT_CATALOG_SEED:
        treatment_id = treatment_data["treatment_id"]

        existing = session.exec(
            select(Treatment).where(Treatment.treatment_id == treatment_id)
        ).first()

        if existing:
            result.id_map[treatment_id] = existing.id
            print(f"  ○ Skipped (exists): {treatment_data['name']}")
            result.skipped += 1
            continue

        treatment = Treatment(
            treatment_id=treatment_id,
            name=treatment_data["name"],
            category=treatment_data["category"],
            description=treatment_data["description"],
            duration=treatment_data["duration"],
            frequency=treatment_data["frequency"],
            cost=treatment_data["cost"],
            status=treatment_data["status"],
        )
        session.add(treatment)
        session.flush()
        result.id_map[treatment_id] = treatment.id
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} treatments")
    return result


def load_treatment_protocol_metrics(session: Session) -> SeedResult:
    """Load seed treatment protocol metrics for admin dashboard charts.

    Args:
        session: Database session

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading treatment protocol metrics")
    result = SeedResult(name="treatment_protocols")

    for data in TREATMENT_PROTOCOL_METRICS_SEED:
        existing = session.exec(
            select(TreatmentProtocolMetric).where(
                TreatmentProtocolMetric.name == data["name"]
            )
        ).first()

        if existing:
            print(f"  ○ Skipped (exists): {data['name']}")
            result.skipped += 1
            continue

        protocol = TreatmentProtocolMetric(
            name=data["name"],
            category=data["category"],
            active_count=data["active_count"],
            completed_count=data["completed_count"],
            success_rate=data["success_rate"],
            avg_duration_days=data["avg_duration_days"],
        )
        session.add(protocol)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} treatment protocol metrics")
    return result


def load_patient_treatment_assignments(
    session: Session,
    user_id_map: dict[str, int],
    treatment_id_map: dict[str, int],
) -> SeedResult:
    """Load patient treatment assignments from PATIENT_TREATMENT_ASSIGNMENTS_SEED.

    Args:
        session: Database session
        user_id_map: Mapping of external_id (P001, P002...) to database user id
        treatment_id_map: Mapping of treatment_id (T001, T002...) to database id

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading patient treatment assignments")
    result = SeedResult(name="patient_treatments")

    for assignment in PATIENT_TREATMENT_ASSIGNMENTS_SEED:
        patient_ext_id = assignment["patient_external_id"]
        treatment_ext_id = assignment["treatment_id"]

        # Get database IDs
        user_db_id = user_id_map.get(patient_ext_id)
        treatment_db_id = treatment_id_map.get(treatment_ext_id)

        if not user_db_id:
            print(f"  ⚠ User {patient_ext_id} not found, skipping")
            result.skipped += 1
            continue

        if not treatment_db_id:
            print(f"  ⚠ Treatment {treatment_ext_id} not found, skipping")
            result.skipped += 1
            continue

        # Check if assignment already exists
        existing = session.exec(
            select(PatientTreatment).where(
                PatientTreatment.user_id == user_db_id,
                PatientTreatment.treatment_id == treatment_db_id,
            )
        ).first()

        if existing:
            print(f"  ○ Skipped (exists): {patient_ext_id} -> {treatment_ext_id}")
            result.skipped += 1
            continue

        # Calculate start date based on sessions completed (assume ~1 session/week)
        weeks_ago = assignment.get("sessions_completed", 0)
        start_date = datetime.now(UTC) - timedelta(weeks=weeks_ago)

        patient_treatment = PatientTreatment(
            user_id=user_db_id,
            treatment_id=treatment_db_id,
            assigned_by=assignment.get("assigned_by"),
            start_date=start_date,
            status=assignment.get("status", "active"),
            notes=assignment.get("notes"),
            sessions_completed=assignment.get("sessions_completed", 0),
            sessions_total=assignment.get("sessions_total"),
            last_session_at=datetime.now(UTC) - timedelta(days=3),
        )
        session.add(patient_treatment)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} patient treatment assignments")
    return result
