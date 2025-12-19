"""Notification seed data loading."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlmodel import Session, select

from longevity_clinic.app.data.model import Notification
from longevity_clinic.app.data.seed import (
    ADMIN_NOTIFICATIONS_SEED,
    PATIENT_NOTIFICATIONS_SEED,
)

from .base import SeedResult, print_section


def load_notifications(session: Session, user_id_map: dict[str, int]) -> SeedResult:
    """Load seed notifications.

    Args:
        session: Database session
        user_id_map: Mapping of external_id to database user id

    Returns:
        SeedResult with load statistics
    """
    print_section("Loading notifications")
    result = SeedResult(name="notifications")

    all_notifications = ADMIN_NOTIFICATIONS_SEED + PATIENT_NOTIFICATIONS_SEED

    for notif_data in all_notifications:
        notif_id = notif_data.get("id", f"NOTIF-{result.total:03d}")

        # Check if exists
        existing = session.exec(
            select(Notification).where(Notification.notification_id == notif_id)
        ).first()

        if existing:
            print(f"  ○ Skipped (exists): {notif_id}")
            result.skipped += 1
            continue

        # Parse timestamp
        timestamp_str = notif_data.get("created_at", "")
        try:
            created_at = datetime.fromisoformat(timestamp_str)
        except (ValueError, AttributeError):
            created_at = datetime.now(timezone.utc)

        # Map patient_id to user_id
        user_id = None
        patient_id = notif_data.get("patient_id")
        if patient_id and patient_id != "current" and patient_id in user_id_map:
            user_id = user_id_map[patient_id]

        notification = Notification(
            notification_id=notif_id,
            user_id=user_id,
            recipient_role=notif_data.get("recipient_role", "patient"),
            title=notif_data.get("title", ""),
            message=notif_data.get("message", ""),
            notification_type=notif_data.get("type", "info"),
            is_read=notif_data.get("is_read", False),
            patient_id=patient_id,
            created_at=created_at,
        )
        session.add(notification)
        result.loaded += 1

    session.commit()
    print(f"  ✓ Loaded {result.loaded} notifications")
    return result
