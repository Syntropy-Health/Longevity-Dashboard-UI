"""Notifications page module.

This module provides the notifications interface with:
- Role-based views (admin vs patient)
- Notification cards and listings
- Filter tabs
- Detail modal
"""

from .page import notifications_page
from .components import (
    notification_icon,
    notification_type_badge,
    notification_card,
    filter_tabs,
    empty_state,
)
from .modals import notification_detail_modal
from .views import (
    admin_notifications_view,
    patient_notifications_view,
    notifications_content,
)

__all__ = [
    "notifications_page",
    # Components
    "notification_icon",
    "notification_type_badge",
    "notification_card",
    "filter_tabs",
    "empty_state",
    # Modals
    "notification_detail_modal",
    # Views
    "admin_notifications_view",
    "patient_notifications_view",
    "notifications_content",
]
