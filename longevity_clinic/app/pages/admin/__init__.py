"""Admin pages module."""

from .page import admin_dashboard
from .patient_health import patient_health_page
from .treatments import treatments_page
from .checkins import admin_checkins_page, admin_checkins_view

__all__ = [
    "admin_dashboard",
    "patient_health_page",
    "treatments_page",
    "admin_checkins_page",
    "admin_checkins_view",
]
