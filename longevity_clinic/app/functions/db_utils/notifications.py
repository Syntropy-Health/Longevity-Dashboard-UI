"""Notification database operations."""

from __future__ import annotations

from typing import Any

import reflex as rx
from sqlmodel import select

from longevity_clinic.app.config import get_logger
from longevity_clinic.app.data.schemas.db import Notification

logger = get_logger("longevity_clinic.db_utils.notifications")


def get_notifications_for_role_sync(
    role: str,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Get notifications for a specific role (admin or patient).

    Args:
        role: "admin" or "patient"
        limit: Maximum number of notifications to return

    Returns:
        List of notification dicts
    """
    try:
        with rx.session() as session:
            notifications = session.exec(
                select(Notification)
                .where(Notification.recipient_role == role)
                .order_by(Notification.created_at.desc())
                .limit(limit)
            ).all()

            return [
                {
                    "id": n.notification_id,
                    "title": n.title,
                    "message": n.message,
                    "type": n.notification_type,
                    "is_read": n.is_read,
                    "patient_id": n.patient_id,
                    "recipient_role": n.recipient_role,
                    "created_at": n.created_at.isoformat() if n.created_at else "",
                }
                for n in notifications
            ]
    except Exception as e:
        logger.error("Failed to get notifications for role %s: %s", role, e)
        return []


def get_notifications_for_user_sync(
    user_id: int,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Get notifications for a specific user.

    Args:
        user_id: Database user ID
        limit: Maximum number to return

    Returns:
        List of notification dicts
    """
    try:
        with rx.session() as session:
            notifications = session.exec(
                select(Notification)
                .where(Notification.user_id == user_id)
                .order_by(Notification.created_at.desc())
                .limit(limit)
            ).all()

            return [
                {
                    "id": n.notification_id,
                    "title": n.title,
                    "message": n.message,
                    "type": n.notification_type,
                    "is_read": n.is_read,
                    "patient_id": n.patient_id,
                    "recipient_role": n.recipient_role,
                    "created_at": n.created_at.isoformat() if n.created_at else "",
                }
                for n in notifications
            ]
    except Exception as e:
        logger.error("Failed to get notifications for user %s: %s", user_id, e)
        return []


def mark_notification_read_sync(notification_id: str) -> bool:
    """Mark a notification as read.

    Args:
        notification_id: The notification_id to mark as read

    Returns:
        True if successful, False otherwise
    """
    try:
        with rx.session() as session:
            notification = session.exec(
                select(Notification).where(
                    Notification.notification_id == notification_id
                )
            ).first()

            if not notification:
                logger.warning("Notification not found: %s", notification_id)
                return False

            notification.is_read = True
            session.add(notification)
            session.commit()
            return True
    except Exception as e:
        logger.error("Failed to mark notification as read: %s", e)
        return False


def delete_notification_sync(notification_id: str) -> bool:
    """Delete a notification.

    Args:
        notification_id: The notification_id to delete

    Returns:
        True if successful, False otherwise
    """
    try:
        with rx.session() as session:
            notification = session.exec(
                select(Notification).where(
                    Notification.notification_id == notification_id
                )
            ).first()

            if not notification:
                logger.warning("Notification not found: %s", notification_id)
                return False

            session.delete(notification)
            session.commit()
            return True
    except Exception as e:
        logger.error("Failed to delete notification: %s", e)
        return False
