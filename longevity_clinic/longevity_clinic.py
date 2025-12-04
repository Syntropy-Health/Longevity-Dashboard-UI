import reflex as rx
from .app.config import current_config
from .app.pages.auth import auth_page
from .app.pages.admin import admin_dashboard
from .app.pages.patient import patient_portal, checkins_page, settings_page
from .app.pages.treatments import treatments_page
from .app.pages.patient_analytics import analytics_page
from .app.pages.patient_treatment_search import treatment_search_page

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
app.add_page(patient_portal, route="/patient/portal")
app.add_page(checkins_page, route="/patient/checkins")
app.add_page(settings_page, route="/patient/settings")
app.add_page(treatments_page, route="/admin/treatments")
app.add_page(analytics_page, route="/patient/analytics")
app.add_page(treatment_search_page, route="/patient/treatment-search")