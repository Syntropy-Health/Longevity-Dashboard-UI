import reflex as rx
from .pages.auth import auth_page
from .pages.admin import admin_dashboard
from .pages.patient import patient_portal, checkins_page, settings_page
from .pages.treatments import treatments_page
from .pages.patient_analytics import analytics_page
from .pages.patient_treatment_search import treatment_search_page
from .pages.notifications import notifications_page
from .pages.appointments import appointments_page

app = rx.App(
    theme=rx.theme(appearance="dark", accent_color="teal"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap",
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
app.add_page(notifications_page, route="/notifications")
app.add_page(appointments_page, route="/appointments")