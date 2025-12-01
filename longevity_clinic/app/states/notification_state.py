"""Notification state management for admin and patient views."""

from typing import TypedDict
from datetime import datetime
import reflex as rx


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
    
    # Demo notifications data
    _admin_notifications: list[dict] = [
        {
            "id": "1",
            "title": "New Patient Registration",
            "message": "Sarah Chen has completed registration and requires initial assessment scheduling.",
            "type": "info",
            "is_read": False,
            "created_at": "2025-01-15T09:30:00",
            "recipient_role": "admin",
            "patient_id": "P001"
        },
        {
            "id": "2",
            "title": "Lab Results Ready",
            "message": "Comprehensive metabolic panel results for Marcus Williams are now available for review.",
            "type": "lab",
            "is_read": False,
            "created_at": "2025-01-15T08:45:00",
            "recipient_role": "admin",
            "patient_id": "P002"
        },
        {
            "id": "3",
            "title": "Treatment Protocol Update Required",
            "message": "NMN + Resveratrol protocol needs adjustment based on latest research findings.",
            "type": "treatment",
            "is_read": True,
            "created_at": "2025-01-14T16:20:00",
            "recipient_role": "admin",
            "patient_id": None
        },
        {
            "id": "4",
            "title": "Appointment Rescheduling Request",
            "message": "Elena Rodriguez requested to reschedule tomorrow's hyperbaric oxygen session.",
            "type": "appointment",
            "is_read": False,
            "created_at": "2025-01-15T07:00:00",
            "recipient_role": "admin",
            "patient_id": "P003"
        },
        {
            "id": "5",
            "title": "Critical: Low Inventory Alert",
            "message": "NAD+ IV therapy supplies are running low. Reorder recommended within 48 hours.",
            "type": "warning",
            "is_read": False,
            "created_at": "2025-01-15T06:00:00",
            "recipient_role": "admin",
            "patient_id": None
        },
        {
            "id": "6",
            "title": "Monthly Report Generated",
            "message": "December 2024 clinical efficiency report is ready for download.",
            "type": "success",
            "is_read": True,
            "created_at": "2025-01-01T00:00:00",
            "recipient_role": "admin",
            "patient_id": None
        }
    ]
    
    _patient_notifications: list[dict] = [
        {
            "id": "101",
            "title": "Upcoming Appointment Reminder",
            "message": "Your NAD+ IV Therapy session is scheduled for tomorrow at 10:00 AM.",
            "type": "appointment",
            "is_read": False,
            "created_at": "2025-01-15T09:00:00",
            "recipient_role": "patient",
            "patient_id": "current"
        },
        {
            "id": "102",
            "title": "Lab Results Available",
            "message": "Your comprehensive metabolic panel results are now ready. Click to view detailed analysis.",
            "type": "lab",
            "is_read": False,
            "created_at": "2025-01-14T14:30:00",
            "recipient_role": "patient",
            "patient_id": "current"
        },
        {
            "id": "103",
            "title": "Treatment Plan Updated",
            "message": "Dr. Johnson has updated your longevity protocol. Review the changes in your treatment plan.",
            "type": "treatment",
            "is_read": True,
            "created_at": "2025-01-13T11:00:00",
            "recipient_role": "patient",
            "patient_id": "current"
        },
        {
            "id": "104",
            "title": "Biomarker Improvement",
            "message": "Great news! Your telomere length has improved by 8% since your last assessment.",
            "type": "success",
            "is_read": True,
            "created_at": "2025-01-10T15:45:00",
            "recipient_role": "patient",
            "patient_id": "current"
        },
        {
            "id": "105",
            "title": "Supplement Reminder",
            "message": "Don't forget to take your NMN and Resveratrol supplements with breakfast.",
            "type": "info",
            "is_read": True,
            "created_at": "2025-01-15T07:00:00",
            "recipient_role": "patient",
            "patient_id": "current"
        }
    ]
    
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
    
    def load_admin_notifications(self):
        """Load notifications for admin users."""
        self.notifications = self._admin_notifications.copy()
    
    def load_patient_notifications(self):
        """Load notifications for patient users."""
        self.notifications = self._patient_notifications.copy()
    
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
