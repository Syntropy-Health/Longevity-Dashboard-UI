"""Patient portal page module.

This module provides the patient portal interface with:
- Dashboard overview
- Biomarker tracking
- Treatment plans
- Nutrition logging
- Health history
"""

from .page import patient_portal
from .checkins_page import checkins_page
from .settings_page import settings_page
from .components import patient_sidebar_tabs, dashboard_tabs, patient_portal_tabs

__all__ = [
    "patient_portal",
    "checkins_page",
    "settings_page",
    "patient_sidebar_tabs",
    "dashboard_tabs",
    "patient_portal_tabs",
]
