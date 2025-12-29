"""Notification state management for admin and patient views.

All notifications are loaded from the database.
Includes medication reminders (notification_type='medication').
Seed data with: python scripts/load_seed_data.py
"""

import asyncio

import reflex as rx

from ...config import get_logger
from ...functions.db_utils import (
    get_medication_notifications_sync,
    get_notifications_for_role_sync,
    get_notifications_for_user_sync,
    toggle_medication_completed_sync,
)
from ..auth.base import AuthState

logger = get_logger("longevity_clinic.notifications")


class NotificationState(rx.State):
    """Manages notifications for both admin and patient users.

    Includes medication reminders (formerly ReminderState).
    """

    notifications: list[dict] = []
    selected_notification: dict = {}
    filter_type: str = "all"  # "all", "unread", "read"

    # Medication notifications (reminders)
    medication_notifications: list[dict] = []
    _MEDICATIONS_PAGE_SIZE: int = 6
    medications_page: int = 1
    _medications_loaded: bool = False

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

    # =========================================================================
    # Medication Notifications Pagination (formerly reminders)
    # =========================================================================

    @rx.var
    def medication_notifications_paginated(self) -> list[dict]:
        """Paginated slice of medication notifications."""
        start = (self.medications_page - 1) * self._MEDICATIONS_PAGE_SIZE
        end = start + self._MEDICATIONS_PAGE_SIZE
        return self.medication_notifications[start:end]

    @rx.var
    def medications_total_pages(self) -> int:
        return max(
            1,
            (len(self.medication_notifications) + self._MEDICATIONS_PAGE_SIZE - 1)
            // self._MEDICATIONS_PAGE_SIZE,
        )

    @rx.var
    def medications_has_previous(self) -> bool:
        return self.medications_page > 1

    @rx.var
    def medications_has_next(self) -> bool:
        return self.medications_page < self.medications_total_pages

    @rx.var
    def medications_page_info(self) -> str:
        return f"Page {self.medications_page} of {self.medications_total_pages}"

    @rx.var
    def medications_showing_info(self) -> str:
        total = len(self.medication_notifications)
        if total == 0:
            return "No medications"
        start = (self.medications_page - 1) * self._MEDICATIONS_PAGE_SIZE + 1
        end = min(self.medications_page * self._MEDICATIONS_PAGE_SIZE, total)
        return f"Showing {start}-{end} of {total}"

    # =========================================================================
    # Data Loading
    # =========================================================================

    async def load_notifications_for_role(self):
        """Load notifications based on user role and ID from AuthState.

        For patients: loads notifications by user_id for user-specific data
        For admins: loads notifications by role for all admin notifications
        """
        auth_state = await self.get_state(AuthState)
        is_admin = auth_state.is_admin
        user_id = auth_state.user_id

        if is_admin:
            # Admins see all admin-role notifications
            db_notifications = get_notifications_for_role_sync("admin")
            logger.info(
                "Loaded %d notifications from DB for admin role",
                len(db_notifications) if db_notifications else 0,
            )
        else:
            # Patients see only their own notifications
            if not user_id:
                logger.warning("load_notifications_for_role: No authenticated user")
                self.notifications = []
                return

            db_notifications = get_notifications_for_user_sync(user_id)
            logger.info(
                "Loaded %d notifications from DB for user_id=%s",
                len(db_notifications) if db_notifications else 0,
                user_id,
            )

        if db_notifications:
            self.notifications = db_notifications
        else:
            logger.warning(
                "No notifications in DB. "
                "Run 'python scripts/load_seed_data.py' to seed data."
            )
            self.notifications = []

    @rx.event(background=True)
    async def load_medication_notifications(self):
        """Load medication notifications (reminders) from database."""
        async with self:
            if self._medications_loaded:
                return
            auth_state = await self.get_state(AuthState)
            user_id = auth_state.user_id

        if not user_id:
            return

        try:
            meds = await asyncio.to_thread(
                get_medication_notifications_sync, user_id, True, 50
            )
            async with self:
                self.medication_notifications = meds
                self._medications_loaded = True
        except Exception as e:
            logger.error("Failed to load medication notifications: %s", e)

    # =========================================================================
    # Filter & Pagination Handlers
    # =========================================================================

    def set_filter(self, filter_type: str):
        """Set the notification filter type."""
        self.filter_type = filter_type

    def medications_previous_page(self):
        if self.medications_page > 1:
            self.medications_page -= 1

    def medications_next_page(self):
        if self.medications_page < self.medications_total_pages:
            self.medications_page += 1

    # =========================================================================
    # Notification Actions
    # =========================================================================

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

    # =========================================================================
    # Medication (Reminder) Actions
    # =========================================================================

    async def toggle_medication_completed(self, notification_id: str):
        """Toggle a medication notification's completed status."""
        try:
            db_id = int(notification_id)
            success = await asyncio.to_thread(toggle_medication_completed_sync, db_id)
            if success:
                # Update local state
                for i, med in enumerate(self.medication_notifications):
                    if med.get("id") == notification_id:
                        self.medication_notifications[i] = {
                            **med,
                            "completed": not med.get("completed", False),
                        }
                        break
        except Exception as e:
            logger.error("Failed to toggle medication completed: %s", e)

    def clear_medication_data(self):
        """Clear medication notification data."""
        self.medication_notifications = []
        self._medications_loaded = False
        self.medications_page = 1
