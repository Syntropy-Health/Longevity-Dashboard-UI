"""Notification model for system notifications and medication reminders."""

from datetime import datetime

import reflex as rx
from sqlmodel import Field

from .base import utc_now


class Notification(rx.Model, table=True):
    """System notification for users.

    Unified model for notifications AND medication reminders.
    notification_type='medication' indicates a medication reminder.
    """

    __tablename__ = "notifications"

    id: int | None = Field(default=None, primary_key=True)
    notification_id: str = Field(index=True, unique=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    recipient_role: str = Field(default="patient")  # "patient" | "admin"

    title: str
    message: str
    notification_type: str = Field(
        default="info"
    )  # "info" | "lab" | "treatment" | "appointment" | "warning" | "success" | "medication"

    is_read: bool = Field(default=False)
    patient_id: str | None = None  # Reference to patient external_id

    # Medication reminder fields (when notification_type='medication')
    time: str | None = None  # Display time like "8:00 AM"
    completed: bool = Field(default=False)
    due_at: datetime | None = None
    recurring: bool = Field(default=False)
    recurrence_pattern: str | None = None  # daily | weekly | monthly
    completed_at: datetime | None = None

    created_at: datetime = Field(default_factory=utc_now)
