#!/usr/bin/env python
"""Reset the latest call log for the demo user to unprocessed state.

This marks the most recent call log (by started_at) for the demo user's phone
as processed_to_metrics=False so it can be reprocessed by the CDC pipeline.

Usage:
    uv run python scripts/reset_latest_call_log.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import current_config
from longevity_clinic.app.data.schemas.db import CallLog


def reset_latest_call_log() -> bool:
    """Reset the latest call log for demo user to unprocessed.

    Returns:
        True if a call log was reset, False otherwise.
    """
    demo_phone = current_config.demo_user.phone
    print(f"Looking for latest call log for phone: {demo_phone}")

    with rx.session() as session:
        # Find the latest call log for demo user by started_at
        latest_log = session.exec(
            select(CallLog)
            .where(CallLog.phone_number == demo_phone)
            .order_by(CallLog.started_at.desc())
        ).first()

        if not latest_log:
            print(f"No call logs found for {demo_phone}")
            return False

        print("\nFound latest call log:")
        print(f"  ID: {latest_log.id}")
        print(f"  Call ID: {latest_log.call_id}")
        print(f"  Started: {latest_log.started_at}")
        print(f"  Duration: {latest_log.duration_seconds}s")
        print(f"  Currently processed: {latest_log.processed_to_metrics}")

        if not latest_log.processed_to_metrics:
            print("\n⚠️  Already unprocessed - no change needed")
            return False

        # Reset to unprocessed
        latest_log.processed_to_metrics = False
        session.add(latest_log)
        session.commit()

        print(f"\n✅ Reset call log {latest_log.call_id} to processed_to_metrics=False")
        return True


if __name__ == "__main__":
    success = reset_latest_call_log()
    sys.exit(0 if success else 1)
