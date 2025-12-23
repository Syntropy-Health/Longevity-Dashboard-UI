"""Check-in seed data loading."""

from __future__ import annotations

import json
from datetime import UTC, datetime

from sqlmodel import Session, select

from longevity_clinic.app.data.model import CheckIn
from longevity_clinic.app.data.seed import CHECKIN_SEED_DATA

from .base import SeedResult, print_section


def load_checkins(session: Session, user_id_map: dict[str, int]) -> SeedResult:
    """Load seed check-ins.

    Args:
        session: Database session
        user_id_map: Mapping of external_id to database user id

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading check-ins")
    result = SeedResult(name="checkins")

    for checkin_data in CHECKIN_SEED_DATA:
        checkin_id = checkin_data.get("id", f"CHK-{result.total:03d}")

        # Check if exists
        existing = session.exec(
            select(CheckIn).where(CheckIn.checkin_id == checkin_id)
        ).first()

        if existing:
            print(f"  ○ Skipped (exists): {checkin_id}")
            result.skipped += 1
            continue

        # Parse timestamp
        timestamp_str = checkin_data.get("timestamp", "")
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            timestamp = datetime.now(UTC)

        # Get user_id from patient_name
        user_id = None
        patient_name = checkin_data.get("patient_name", "Unknown")
        for ext_id, db_id in user_id_map.items():
            # Simple name matching
            if ext_id in checkin_data.get("patient_id", ""):
                user_id = db_id
                break

        checkin = CheckIn(
            checkin_id=checkin_id,
            user_id=user_id,
            patient_name=patient_name,
            checkin_type=checkin_data.get("type", "manual"),
            summary=checkin_data.get("summary", ""),
            raw_content=checkin_data.get("content", checkin_data.get("transcript", "")),
            health_topics=json.dumps(
                checkin_data.get("health_topics", checkin_data.get("key_topics", []))
            ),
            mood=checkin_data.get("mood"),
            energy_level=checkin_data.get("energy_level"),
            status=checkin_data.get("status", "pending"),
            provider_reviewed=checkin_data.get("provider_reviewed", False),
            reviewed_by=checkin_data.get("reviewed_by"),
            timestamp=timestamp,
        )
        session.add(checkin)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} check-ins")
    return result
