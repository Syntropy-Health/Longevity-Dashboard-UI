"""Patient portal page module."""

from .page import patient_portal
from .checkins import checkins_page, checkins_page_wrapper
from .settings_page import settings_page
from .analytics import analytics_page
from .treatment_search import treatment_search_page

__all__ = [
    "patient_portal",
    "checkins_page",
    "checkins_page_wrapper",
    "settings_page",
    "analytics_page",
    "treatment_search_page",
]
