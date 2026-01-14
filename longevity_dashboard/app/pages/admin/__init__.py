"""Admin pages module."""

from .chat import admin_chat_page
from .checkins import admin_checkins_page, admin_checkins_view
from .page import admin_dashboard
from .patient_health import patient_health_page
from .treatments import treatments_page

__all__ = [
    "admin_chat_page",
    "admin_checkins_page",
    "admin_checkins_view",
    "admin_dashboard",
    "patient_health_page",
    "treatments_page",
]
