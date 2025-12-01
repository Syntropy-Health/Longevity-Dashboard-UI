"""Pages module.

This module exports all page components from their respective submodules.
Each page has been modularized into its own subdirectory for maintainability.
"""

# Patient portal page
from .patient import patient_portal

# Admin dashboard page
from .admin import admin_dashboard

# Treatments page
from .treatments import treatments_page

# Patient analytics page
from .patient_analytics import analytics_page

# Treatment search page
from .patient_treatment_search import treatment_search_page

# Appointments page
from .appointments import appointments_page

# Notifications page
from .notifications import notifications_page

# Auth page
from .auth import auth_page, login_form

__all__ = [
    # Main page functions
    "patient_portal",
    "admin_dashboard",
    "treatments_page",
    "analytics_page",
    "treatment_search_page",
    "appointments_page",
    "notifications_page",
    "auth_page",
    "login_form",
]
