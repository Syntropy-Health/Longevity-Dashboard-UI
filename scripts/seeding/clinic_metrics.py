"""Clinic operational metrics seed data loading."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlmodel import Session, select

from longevity_clinic.app.data.schemas.db import (
    ClinicDailyMetrics,
    PatientVisit,
    ProviderMetrics,
)
from longevity_clinic.app.data.seed import (
    HOURLY_FLOW_SEED,
    PATIENT_VISIT_SEED,
    PROVIDER_METRICS_SEED,
    ROOM_UTILIZATION_SEED,
)

from .base import SeedResult, print_section


def load_patient_visits(session: Session) -> SeedResult:
    """Load seed patient visit trend data for charts.

    Args:
        session: Database session

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading patient visit trends")
    result = SeedResult(name="patient_visits")

    base_date = datetime.now(UTC) - timedelta(days=180)

    for i, data in enumerate(PATIENT_VISIT_SEED):
        # Check if exists
        existing = session.exec(
            select(PatientVisit).where(
                PatientVisit.period == data["period"],
                PatientVisit.period_type == data["period_type"],
            )
        ).first()

        if existing:
            print(f"  ○ Skipped (exists): {data['period']}")
            result.skipped += 1
            continue

        visit = PatientVisit(
            period=data["period"],
            period_type=data["period_type"],
            active_patients=data["active_patients"],
            new_patients=data["new_patients"],
            total_visits=data["total_visits"],
            recorded_at=base_date + timedelta(days=i * 30),
        )
        session.add(visit)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} patient visit records")
    return result


def load_daily_metrics(session: Session) -> SeedResult:
    """Load seed daily clinic metrics for efficiency charts.

    Args:
        session: Database session

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading daily clinic metrics")
    result = SeedResult(name="daily_metrics")

    today = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)

    # Load hourly flow data
    for data in HOURLY_FLOW_SEED:
        existing = session.exec(
            select(ClinicDailyMetrics).where(
                ClinicDailyMetrics.date == today,
                ClinicDailyMetrics.hour == data["hour"],
            )
        ).first()

        if existing:
            result.skipped += 1
            continue

        metric = ClinicDailyMetrics(
            date=today,
            hour=data["hour"],
            scheduled_appointments=data["scheduled_appointments"],
            walkin_appointments=data["walkin_appointments"],
            completed_appointments=data["scheduled_appointments"]
            + data["walkin_appointments"],
            avg_wait_time_minutes=data["avg_wait_time_minutes"],
            patient_throughput=(
                data["scheduled_appointments"] + data["walkin_appointments"]
            )
            / 1.0,
        )
        session.add(metric)
        result.loaded += 1

    # Load room utilization data
    for data in ROOM_UTILIZATION_SEED:
        existing = session.exec(
            select(ClinicDailyMetrics).where(
                ClinicDailyMetrics.date == today,
                ClinicDailyMetrics.room_id == data["room_id"],
            )
        ).first()

        if existing:
            result.skipped += 1
            continue

        metric = ClinicDailyMetrics(
            date=today,
            room_id=data["room_id"],
            room_occupancy_pct=data["room_occupancy_pct"],
            treatments_completed=data["treatments_completed"],
        )
        session.add(metric)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} daily clinic metrics")
    return result


def load_provider_metrics(session: Session) -> SeedResult:
    """Load seed provider performance metrics.

    Args:
        session: Database session

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading provider metrics")
    result = SeedResult(name="provider_metrics")

    current_period = datetime.now(UTC).strftime("%Y-%m")

    for data in PROVIDER_METRICS_SEED:
        existing = session.exec(
            select(ProviderMetrics).where(
                ProviderMetrics.provider_name == data["provider_name"],
                ProviderMetrics.period == current_period,
            )
        ).first()

        if existing:
            print(f"  ○ Skipped (exists): {data['provider_name']}")
            result.skipped += 1
            continue

        metric = ProviderMetrics(
            provider_name=data["provider_name"],
            period=current_period,
            period_type=data["period_type"],
            patient_count=data["patient_count"],
            efficiency_score=data["efficiency_score"],
            on_time_rate=data["on_time_rate"],
            avg_rating=data["avg_rating"],
        )
        session.add(metric)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} provider metrics")
    return result
