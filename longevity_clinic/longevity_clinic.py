import reflex as rx

# Pages - Admin
from .app.pages.admin import admin_dashboard, patient_health_page, treatments_page

# Pages - Patient
from .app.pages.patient import (
    analytics_page,
    checkins_page,
    checkins_page_wrapper,
    patient_portal,
    settings_page,
    treatment_search_page,
)

# Pages - Shared
from .app.pages.shared import appointments_page, auth_page, notifications_page

# States
from .app.states import (
    AppointmentState,
    BiomarkerState,
    CheckinState,
    HealthDashboardState,
    TreatmentSearchState,
    TreatmentState,
)

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap",
            rel="stylesheet",
        ),
    ],
    # stylesheets=[
    #     "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    #     "https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap",
    # ],
)
app.add_page(auth_page, route="/")
app.add_page(auth_page, route="/login")

# Admin
app.add_page(admin_dashboard, route="/admin/dashboard")
app.add_page(patient_health_page, route="/admin/patient-health")
app.add_page(
    checkins_page,
    route="/admin/checkins",
    on_load=[CheckinState.load_admin_checkins],
)
app.add_page(
    treatments_page,
    route="/admin/treatments",
    on_load=[TreatmentState.load_protocols],
)

# Patient
app.add_page(
    patient_portal,
    route="/patient/portal",
    on_load=[
        BiomarkerState.load_biomarkers,
        HealthDashboardState.load_dashboard_data,
        AppointmentState.load_appointments,
    ],
)
app.add_page(
    checkins_page_wrapper,
    route="/patient/checkins",
    on_load=[
        BiomarkerState.load_biomarkers,
        HealthDashboardState.load_dashboard_data,
        HealthDashboardState.load_health_data_from_db,
        CheckinState.start_periodic_call_logs_refresh,
    ],
)
app.add_page(settings_page, route="/patient/settings")
app.add_page(analytics_page, route="/patient/analytics")
app.add_page(
    treatment_search_page,
    route="/patient/treatment-search",
    on_load=[TreatmentSearchState.load_treatments],
)

# Shared
app.add_page(
    notifications_page, route="/notifications", title="Notifications - Longevity Clinic"
)
app.add_page(
    appointments_page,
    route="/appointments",
    title="Appointments | Longevity Clinic",
    on_load=[AppointmentState.load_appointments],
)
