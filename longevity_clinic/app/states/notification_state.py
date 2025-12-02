"""Notification state management for admin and patient views."""

from typing import TypedDict
from datetime import datetime
import reflex as rx

from ..data.demo import ADMIN_NOTIFICATIONS_DEMO, PATIENT_NOTIFICATIONS_DEMO


class Notification(TypedDict):
    """Structure for a notification."""
    id: str
    title: str
    message: str
    type: str  # "info", "warning", "success", "error", "appointment", "treatment", "lab"
    is_read: bool
    created_at: str
    recipient_role: str  # "admin", "patient", "all"
    patient_id: str | None


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
        # Import here to avoid circular imports
        from .auth_state import AuthState
        auth_state = await self.get_state(AuthState)
        if auth_state.is_admin:
            self.notifications = list(ADMIN_NOTIFICATIONS_DEMO)
        else:
            self.notifications = list(PATIENT_NOTIFICATIONS_DEMO)
    
    def load_admin_notifications(self):
        """Load notifications for admin users."""
        self.notifications = list(ADMIN_NOTIFICATIONS_DEMO)
    
    def load_patient_notifications(self):
        """Load notifications for patient users."""
        self.notifications = list(PATIENT_NOTIFICATIONS_DEMO)
    
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
        self.notifications = [
            {**n, "is_read": True} for n in self.notifications
        ]
    
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
    
    def get_icon_for_type(self, notification_type: str) -> str:
        """Get the appropriate icon name for a notification type."""
        icons = {
            "info": "info",
            "warning": "alert-triangle",
            "success": "circle-check",
            "error": "circle-x",
            "appointment": "calendar",
            "treatment": "activity",
            "lab": "flask-conical"
        }
        return icons.get(notification_type, "bell")
    
    @rx.var
    def has_selected_notification(self) -> bool:
        """Check if a notification is currently selected."""
        return bool(self.selected_notification and self.selected_notification.get("id"))
    
    def get_color_for_type(self, notification_type: str) -> str:
        """Get the appropriate color class for a notification type."""
        colors = {
            "info": "text-blue-500",
            "warning": "text-amber-500",
            "success": "text-emerald-500",
            "error": "text-rose-500",
            "appointment": "text-teal-500",
            "treatment": "text-purple-500",
            "lab": "text-cyan-500"
        }
        return colors.get(notification_type, "text-gray-500")
