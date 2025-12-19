"""Treatment seed data loading."""

from __future__ import annotations

from sqlmodel import Session, select

from longevity_clinic.app.data.model import Treatment, TreatmentProtocolMetric
from longevity_clinic.app.data.seed import (
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
