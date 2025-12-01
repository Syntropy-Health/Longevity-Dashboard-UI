"""Notifications page main entry point.

This module contains the main page function for the notifications page.
"""

import reflex as rx

from ...components.layout import authenticated_layout
from ...states.notification_state import NotificationState
from ...states.auth_state import AuthState
from .views import notifications_content


@rx.page(
    route="/notifications",
    title="Notifications - Longevity Clinic",
    on_load=[
        AuthState.check_auth,
        rx.cond(
            AuthState.is_admin,
            NotificationState.load_admin_notifications,
            NotificationState.load_patient_notifications
        )
    ]
)
def notifications_page() -> rx.Component:
    """Notifications page component.
    
    Returns:
        The complete notifications page with authenticated layout
    """
    return authenticated_layout(
        rx.box(
            notifications_content(),
            class_name="p-6 max-w-4xl mx-auto"
        )
    )
