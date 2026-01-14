"""Patient portal page module."""

from .analytics import analytics_page
from .chat import ai_chat_page
from .checkins import checkins_page, checkins_page_wrapper
from .page import patient_portal
from .settings_page import settings_page
from .treatment import treatment_search_page

__all__ = [
    "ai_chat_page",
    "analytics_page",
    "checkins_page",
    "checkins_page_wrapper",
    "patient_portal",
    "settings_page",
    "treatment_search_page",
]
