"""Notifications page module.

This module provides the notifications interface with:
- Role-based views (admin vs patient)
- Notification cards and listings
- Filter tabs
- Detail modal
"""

from .components import (
    empty_state,
    filter_tabs,
    notification_card,
    notification_icon,
    notification_type_badge,
)
from .modals import notification_detail_modal
from .page import notifications_page
from .views import (
    admin_notifications_view,
    notifications_content,
    patient_notifications_view,
)

__all__ = [
    # Views
    "admin_notifications_view",
    "empty_state",
    "filter_tabs",
    "notification_card",
    # Modals
    "notification_detail_modal",
    # Components
    "notification_icon",
    "notification_type_badge",
    "notifications_content",
    "notifications_page",
    "patient_notifications_view",
]
