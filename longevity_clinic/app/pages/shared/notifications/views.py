"""Notifications page views.

This module contains the role-based view components:
- Admin notifications view
- Patient notifications view
- Main notifications content (role-based switcher)
"""

import reflex as rx

from ....styles.constants import GlassStyles
from ....states import NotificationState
from ....states import AuthState
from .components import notification_card, filter_tabs, empty_state
from .modals import notification_detail_modal


def admin_notifications_view() -> rx.Component:
    """Render admin-specific notifications view.

    Returns:
        The admin notifications view component
    """
    return rx.box(
        # Header
        rx.flex(
            rx.box(
                rx.text(
                    "Notifications", class_name=f"text-2xl {GlassStyles.HEADING_LIGHT}"
                ),
                rx.text(
                    "Manage clinic alerts, patient updates, and system notifications",
                    class_name=GlassStyles.SUBHEADING_LIGHT,
                ),
            ),
            rx.flex(
                rx.button(
                    rx.icon("check-check", class_name="w-4 h-4 mr-2"),
                    "Mark all read",
                    on_click=NotificationState.mark_all_as_read,
                    class_name=GlassStyles.BUTTON_SECONDARY_LIGHT,
                ),
                class_name="flex gap-3",
            ),
            class_name="flex items-start justify-between mb-6",
        ),
        # Filter tabs
        rx.box(filter_tabs(), class_name="mb-6"),
        # Notifications list
        rx.cond(
            NotificationState.filtered_notifications.length() > 0,
            rx.box(
                rx.foreach(NotificationState.filtered_notifications, notification_card),
                class_name="space-y-3",
            ),
            empty_state(),
        ),
        # Detail modal
        notification_detail_modal(),
    )


def patient_notifications_view() -> rx.Component:
    """Render patient-specific notifications view.

    Returns:
        The patient notifications view component
    """
    return rx.box(
        # Header
        rx.flex(
            rx.box(
                rx.text(
                    "My Notifications",
                    class_name=f"text-2xl {GlassStyles.HEADING_LIGHT}",
                ),
                rx.text(
                    "Stay updated on your appointments, lab results, and treatment progress",
                    class_name=GlassStyles.SUBHEADING_LIGHT,
                ),
            ),
            rx.button(
                rx.icon("check-check", class_name="w-4 h-4 mr-2"),
                "Mark all read",
                on_click=NotificationState.mark_all_as_read,
                class_name=GlassStyles.BUTTON_SECONDARY_LIGHT,
            ),
            class_name="flex items-start justify-between mb-6",
        ),
        # Filter tabs
        rx.box(filter_tabs(), class_name="mb-6"),
        # Notifications list
        rx.cond(
            NotificationState.filtered_notifications.length() > 0,
            rx.box(
                rx.foreach(NotificationState.filtered_notifications, notification_card),
                class_name="space-y-3",
            ),
            empty_state(),
        ),
        # Detail modal
        notification_detail_modal(),
    )


def notifications_content() -> rx.Component:
    """Main notifications content with role-based views.

    Returns:
        The appropriate view based on user role
    """
    return rx.cond(
        AuthState.is_admin, admin_notifications_view(), patient_notifications_view()
    )
