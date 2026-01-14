"""Notification type definitions for Syntropy app notifications."""

from enum import Enum
from typing import TypedDict


class NotificationType(str, Enum):
    """Notification type enumeration."""

    TIPS = "TIPS"
    SUGGESTION = "SUGGESTION"
    ALERT = "ALERT"


MAX_NOTIFICATIONS = 99


class SyntropyNotification(TypedDict):
    """TypedDict for Syntropy app notifications (distinct from DB Notification model)."""

    id: int
    notification_type: NotificationType
    title: str
    message: str
    timestamp: str
    read: bool
