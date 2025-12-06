import reflex as rx
from .app.pages.auth import auth_page
from .app.pages.admin import admin_dashboard, admin_checkins_page
from .app.pages.patient import patient_portal, checkins_page, settings_page
from .app.pages.treatments import treatments_page
from .app.pages.patient_analytics import analytics_page
from .app.pages.patient_treatment_search import treatment_search_page
from .app.pages.notifications import notifications_page
from .app.pages.appointments import appointments_page
from .app.states.patient_biomarker_state import PatientBiomarkerState
from .app.states.patient_dashboard_state import PatientDashboardState
from .app.states.patient_checkin_state import PatientCheckinState

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
)
app.add_page(auth_page, route="/")
app.add_page(auth_page, route="/login")
app.add_page(admin_dashboard, route="/admin/dashboard")
app.add_page(admin_checkins_page, route="/admin/checkins")
app.add_page(patient_portal, route="/patient/portal")
app.add_page(
    checkins_page,
    route="/patient/checkins",
    on_load=[
        PatientBiomarkerState.load_biomarkers,
        PatientDashboardState.load_dashboard_data,
        # PatientCheckinState.refresh_call_logs,
    ],
)
app.add_page(settings_page, route="/patient/settings")
app.add_page(treatments_page, route="/admin/treatments")
app.add_page(analytics_page, route="/patient/analytics")
app.add_page(treatment_search_page, route="/patient/treatment-search")
app.add_page(notifications_page, route="/notifications")
app.add_page(appointments_page, route="/appointments")
