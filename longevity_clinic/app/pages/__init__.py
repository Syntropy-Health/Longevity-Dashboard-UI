"""Pages module - exports all page components."""

# Patient portal pages (includes analytics and treatment search)
from .patient import patient_portal, analytics_page, treatment_search_page

# Admin pages (dashboard + treatments)
from .admin import admin_dashboard, treatments_page

# Shared pages (auth, appointments, notifications)
from .shared import auth_page, appointments_page, notifications_page

__all__ = [
    # Patient
    "patient_portal",
    "analytics_page",
    "treatment_search_page",
    # Admin
    "admin_dashboard",
    "treatments_page",
    # Shared
    "auth_page",
    "appointments_page",
    "notifications_page",
]
