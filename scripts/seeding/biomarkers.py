"""Biomarker seed data loading."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from longevity_clinic.app.data.model import (
    BiomarkerAggregate,
    BiomarkerDefinition,
    BiomarkerReading,
)
from longevity_clinic.app.data.seed import (
    BIOMARKER_AGGREGATE_SEED,
    PORTAL_BIOMARKERS_SEED,
)

from .base import SeedResult, print_section


def load_biomarker_definitions(session: Session) -> SeedResult:
    """Load biomarker definitions from PORTAL_BIOMARKERS_SEED.

    Args:
        session: Database session

    Returns:
        SeedResult with id_map of biomarker code -> database id
    """
    print_section("Loading biomarker definitions")
    result = SeedResult(name="biomarker_definitions")

    for bio_data in PORTAL_BIOMARKERS_SEED:
        # Create a code from the name
        code = (
            bio_data["name"]
            .upper()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
        )

        existing = session.exec(
            select(BiomarkerDefinition).where(BiomarkerDefinition.code == code)
        ).first()

        if existing:
            result.id_map[code] = existing.id
            print(f"  ○ Skipped (exists): {bio_data['name']}")
            result.skipped += 1
            continue

        definition = BiomarkerDefinition(
            code=code,
            name=bio_data["name"],
            category=bio_data["category"],
            unit=bio_data["unit"],
            description=bio_data.get("description", ""),
            optimal_min=bio_data["optimal_min"],
            optimal_max=bio_data["optimal_max"],
            critical_min=bio_data.get("critical_min", 0.0),
            critical_max=bio_data.get("critical_max", bio_data["optimal_max"] * 2),
        )
        session.add(definition)
        session.flush()
        result.id_map[code] = definition.id
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} biomarker definitions")
    return result


def load_biomarker_readings(
    session: Session,
    user_id_map: dict[str, int],
    biomarker_id_map: dict[str, int],
) -> SeedResult:
    """Load biomarker readings from PORTAL_BIOMARKERS_SEED history.

    Args:
        session: Database session
        user_id_map: Mapping of external_id to database user id
        biomarker_id_map: Mapping of biomarker code to database id

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading biomarker readings")
    result = SeedResult(name="biomarker_readings")

    # Get primary user ID
    primary_user_id = user_id_map.get("P001")
    if not primary_user_id:
        print("  ⚠ Primary user not found, skipping biomarker readings")
        return result

    month_map = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

    for bio_data in PORTAL_BIOMARKERS_SEED:
        code = (
            bio_data["name"]
            .upper()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
        )
        biomarker_db_id = biomarker_id_map.get(code)

        if not biomarker_db_id:
            continue

        history = bio_data.get("history", [])
        for i, point in enumerate(history):
            # Parse month to date (use 2025 and 15th of month)
            month_str = point.get("date", "Jan")
            month_num = month_map.get(month_str, 1)
            measured_at = datetime(2025, month_num, 15, 10, 0, 0, tzinfo=timezone.utc)

            # Check if exists
            existing = session.exec(
                select(BiomarkerReading).where(
                    BiomarkerReading.user_id == primary_user_id,
                    BiomarkerReading.biomarker_id == biomarker_db_id,
                    BiomarkerReading.measured_at == measured_at,
                )
            ).first()

            if existing:
                result.skipped += 1
                continue

            # Determine status based on optimal range
            value = point["value"]
            optimal_min = bio_data["optimal_min"]
            optimal_max = bio_data["optimal_max"]
            if optimal_min <= value <= optimal_max:
                status = "optimal"
            elif value < bio_data.get(
                "critical_min", optimal_min * 0.5
            ) or value > bio_data.get("critical_max", optimal_max * 2):
                status = "critical"
            else:
                status = "warning"

            # Calculate trend from history
            if i == 0:
                trend = "stable"
            else:
                prev_value = history[i - 1]["value"]
                if value > prev_value * 1.05:
                    trend = "up"
                elif value < prev_value * 0.95:
                    trend = "down"
                else:
                    trend = "stable"

            reading = BiomarkerReading(
                user_id=primary_user_id,
                biomarker_id=biomarker_db_id,
                value=value,
                status=status,
                trend=trend,
                source="lab",
                measured_at=measured_at,
            )
            session.add(reading)
            result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} biomarker readings")
    return result


def load_biomarker_aggregates(session: Session) -> SeedResult:
    """Load seed biomarker aggregate data for charts.

    Args:
        session: Database session

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading biomarker aggregates")
    result = SeedResult(name="biomarker_aggregates")

    base_date = datetime.now(timezone.utc) - timedelta(weeks=16)

    for i, data in enumerate(BIOMARKER_AGGREGATE_SEED):
        existing = session.exec(
            select(BiomarkerAggregate).where(
                BiomarkerAggregate.period == data["period"]
            )
        ).first()

        if existing:
            print(f"  ○ Skipped (exists): {data['period']}")
            result.skipped += 1
            continue

        aggregate = BiomarkerAggregate(
            period=data["period"],
            period_type=data["period_type"],
            avg_score=data["avg_score"],
            patient_count=data["patient_count"],
            improvement_pct=data["improvement_pct"],
            recorded_at=base_date + timedelta(weeks=i * 4),
        )
        session.add(aggregate)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} biomarker aggregates")
    return result
