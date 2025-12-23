"""Notification state management for admin and patient views.

All notifications are loaded from the database.
Seed data with: python scripts/load_seed_data.py
"""

import reflex as rx

from ...config import get_logger
from ...functions.db_utils import (
    get_notifications_for_role_sync,
)
from ..auth.base import AuthState

logger = get_logger("longevity_clinic.notifications")


class NotificationState(rx.State):
    """Manages notifications for both admin and patient users."""

    notifications: list[dict] = []
    selected_notification: dict = {}
    filter_type: str = "all"  # "all", "unread", "read"

    @rx.var
    def unread_count(self) -> int:
        """Count of unread notifications."""
        return sum(1 for n in self.notifications if not n.get("is_read", False))

    @rx.var
    def filtered_notifications(self) -> list[dict]:
        """Filter notifications based on current filter."""
        if self.filter_type == "unread":
            return [n for n in self.notifications if not n.get("is_read", False)]
        elif self.filter_type == "read":
            return [n for n in self.notifications if n.get("is_read", False)]
        return self.notifications

    async def load_notifications_for_role(self):
        """Load notifications based on user role from AuthState."""
        auth_state = await self.get_state(AuthState)
        role = "admin" if auth_state.is_admin else "patient"

        db_notifications = get_notifications_for_role_sync(role)
        if db_notifications:
            self.notifications = db_notifications
            logger.info(
                "Loaded %d notifications from DB for %s",
                len(db_notifications),
                role,
            )
        else:
            logger.warning(
                "No notifications in DB for %s. "
                "Run 'python scripts/load_seed_data.py' to seed data.",
                role,
            )
            self.notifications = []

    def set_filter(self, filter_type: str):
        """Set the notification filter type."""
        self.filter_type = filter_type

    def mark_as_read(self, notification_id: str):
        """Mark a specific notification as read."""
        for i, notification in enumerate(self.notifications):
            if notification.get("id") == notification_id:
                self.notifications[i] = {**notification, "is_read": True}
                break

    def mark_all_as_read(self):
        """Mark all notifications as read."""
        self.notifications = [{**n, "is_read": True} for n in self.notifications]

    def select_notification(self, notification: dict):
        """Select a notification for detailed view."""
        self.selected_notification = notification
        self.mark_as_read(notification.get("id", ""))

    def clear_selection(self):
        """Clear the selected notification."""
        self.selected_notification = {}

    def delete_notification(self, notification_id: str):
        """Delete a notification."""
        self.notifications = [
            n for n in self.notifications if n.get("id") != notification_id
        ]
        if self.selected_notification.get("id") == notification_id:
            self.selected_notification = {}

    @rx.var
    def has_selected_notification(self) -> bool:
        """Check if a notification is currently selected."""
        return bool(self.selected_notification and self.selected_notification.get("id"))
