"""Condition, SymptomTrend, and DataSource seed data loading.

Loads health conditions, symptom trends, and connected device/app data sources
for the primary demo user.
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlmodel import Session, select

from longevity_clinic.app.data.schemas.db import (
    Condition,
    DataSource,
    SymptomTrend,
)
from longevity_clinic.app.data.seed.nutrition import (
    CONDITIONS_SEED,
    DATA_SOURCES_SEED,
    SYMPTOM_TRENDS_SEED,
)

from .base import SeedResult, print_section


def load_conditions(session: Session, user_id_map: dict[str, int]) -> SeedResult:
    """Load health conditions for the primary demo user.

    Args:
        session: Database session
        user_id_map: Mapping of external_id to database user id

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading conditions")
    result = SeedResult(name="conditions")

    # Get primary user ID (Sarah Chen = P001)
    primary_user_id = user_id_map.get("P001")
    if not primary_user_id:
        print("  ⚠ Primary user not found, skipping conditions")
        return result

    for cond_data in CONDITIONS_SEED:
        # Check for existing condition by name for this user
        existing = session.exec(
            select(Condition).where(
                Condition.user_id == primary_user_id,
                Condition.name == cond_data["name"],
            )
        ).first()

        if existing:
            result.skipped += 1
            continue

        condition = Condition(
            user_id=primary_user_id,
            name=cond_data["name"],
            icd_code=cond_data.get("icd_code", ""),
            diagnosed_date=cond_data.get("diagnosed_date", ""),
            status=cond_data.get("status", "active"),
            severity=cond_data.get("severity", "mild"),
            treatments=cond_data.get("treatments", ""),
            source="seed",
        )
        session.add(condition)
        result.loaded += 1

        # Store mapping from seed id to db id
        if cond_data.get("id"):
            # We'll get the ID after commit, but track the name mapping
            result.id_map[cond_data["id"]] = condition.name  # type: ignore

    session.commit()
    print(f"  ✓ Loaded {result.loaded} conditions, skipped {result.skipped}")
    return result


def load_symptom_trends(session: Session, user_id_map: dict[str, int]) -> SeedResult:
    """Load symptom trends for the primary demo user.

    Args:
        session: Database session
        user_id_map: Mapping of external_id to database user id

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading symptom trends")
    result = SeedResult(name="symptom_trends")

    # Get primary user ID (Sarah Chen = P001)
    primary_user_id = user_id_map.get("P001")
    if not primary_user_id:
        print("  ⚠ Primary user not found, skipping symptom trends")
        return result

    for trend_data in SYMPTOM_TRENDS_SEED:
        # Check for existing trend by symptom_name for this user
        existing = session.exec(
            select(SymptomTrend).where(
                SymptomTrend.user_id == primary_user_id,
                SymptomTrend.symptom_name == trend_data["symptom_name"],
            )
        ).first()

        if existing:
            result.skipped += 1
            continue

        trend = SymptomTrend(
            user_id=primary_user_id,
            symptom_name=trend_data["symptom_name"],
            current_severity=int(trend_data.get("current_severity", 0)),
            previous_severity=int(trend_data.get("previous_severity", 0)),
            trend=trend_data.get("trend", "stable"),
            change_percent=float(trend_data.get("change_percent", 0.0)),
            period=trend_data.get("period", "Last 7 days"),
            calculated_at=datetime.now(UTC),
        )
        session.add(trend)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} symptom trends, skipped {result.skipped}")
    return result


def load_data_sources(session: Session, user_id_map: dict[str, int]) -> SeedResult:
    """Load connected device/app data sources for the primary demo user.

    Args:
        session: Database session
        user_id_map: Mapping of external_id to database user id

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading data sources")
    result = SeedResult(name="data_sources")

    # Get primary user ID (Sarah Chen = P001)
    primary_user_id = user_id_map.get("P001")
    if not primary_user_id:
        print("  ⚠ Primary user not found, skipping data sources")
        return result

    for source_data in DATA_SOURCES_SEED:
        # Check for existing data source by name for this user
        existing = session.exec(
            select(DataSource).where(
                DataSource.user_id == primary_user_id,
                DataSource.name == source_data["name"],
            )
        ).first()

        if existing:
            result.skipped += 1
            continue

        data_source = DataSource(
            user_id=primary_user_id,
            name=source_data["name"],
            source_type=source_data.get("type", "wearable"),
            status=source_data.get("status", "disconnected"),
            icon=source_data.get("icon", ""),
            image=source_data.get("image", ""),
            connected=source_data.get("connected", False),
            last_sync=source_data.get("last_sync", "Never"),
            connected_at=datetime.now(UTC) if source_data.get("connected") else None,
        )
        session.add(data_source)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} data sources, skipped {result.skipped}")
    return result
