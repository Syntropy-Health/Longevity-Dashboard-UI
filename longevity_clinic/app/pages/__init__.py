"""Pages module - exports all page components."""

# Patient portal pages (includes analytics and treatment search)
# Admin pages (dashboard + treatments)
from .admin import admin_dashboard, treatments_page
from .patient import analytics_page, patient_portal, treatment_search_page

# Shared pages (auth, appointments, notifications)
from .shared import appointments_page, auth_page, notifications_page

__all__ = [
    # Admin
    "admin_dashboard",
    "analytics_page",
    "appointments_page",
    # Shared
    "auth_page",
    "notifications_page",
    # Patient
    "patient_portal",
    "treatment_search_page",
    "treatments_page",
]
