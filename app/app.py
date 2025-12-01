import reflex as rx
from app.states.global_state import GlobalState
from app.components.navbar import navbar
from app.components.role_selector import role_selector
from app.styles.glass_styles import GlassStyles
from app.components.patient.dashboard_tabs import patient_dashboard_container


def dashboard_content() -> rx.Component:
    """
    Render either the new patient dashboard or the simple placeholder for admin/guest.
    Refactoring to support the new tabbed interface for patients.
    """
    return rx.cond(
        GlobalState.is_patient,
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    f"Welcome back, {GlobalState.user_name}",
                    class_name="text-3xl md:text-4xl font-bold text-white mb-2 tracking-tight",
                ),
                rx.el.p(
                    "Your cellular health optimization dashboard is ready.",
                    class_name="text-lg text-slate-400 mb-8",
                ),
            ),
            patient_dashboard_container(),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    f"Welcome back, {GlobalState.user_name}",
                    class_name="text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight",
                ),
                rx.el.p(
                    "Your cellular health optimization dashboard is ready.",
                    class_name="text-xl text-slate-400 max-w-2xl",
                ),
                class_name="mb-12",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("heart-pulse", class_name="w-6 h-6 text-teal-400 mb-4"),
                        rx.el.h3(
                            "Biological Age",
                            class_name="text-lg font-semibold text-white mb-1",
                        ),
                        rx.el.p(
                            "34.2 Years",
                            class_name="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-teal-200 to-teal-500",
                        ),
                        rx.el.p(
                            "-2.4 years vs Chronological",
                            class_name="text-sm text-teal-400/80 mt-2",
                        ),
                        class_name="flex flex-col h-full justify-between",
                    ),
                    class_name=f"{GlassStyles.PANEL} p-6 h-48",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-6xl",
            ),
            class_name="flex flex-col items-center justify-center pt-32 px-6",
        ),
    )


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="fixed top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top_left,_var(--tw-gradient-stops))] from-teal-900/20 via-slate-900/0 to-slate-900/0 pointer-events-none"
        ),
        rx.el.div(
            class_name="fixed bottom-0 right-0 w-[500px] h-[500px] bg-teal-500/10 rounded-full blur-[100px] pointer-events-none"
        ),
        navbar(),
        rx.cond(
            GlobalState.current_role != "guest",
            dashboard_content(),
            rx.el.div(
                rx.el.h1(
                    "Aether Longevity",
                    class_name=f"text-6xl font-bold {GlassStyles.HEADING} mb-6",
                ),
                rx.el.p(
                    "Advanced biological optimization.",
                    class_name="text-slate-400 text-xl",
                ),
                rx.el.button(
                    "Enter Portal",
                    on_click=GlobalState.open_role_selector,
                    class_name=f"{GlassStyles.BUTTON_PRIMARY} mt-8",
                ),
                class_name="h-screen flex flex-col items-center justify-center",
            ),
        ),
        role_selector(),
        class_name=GlassStyles.PAGE_BG,
    )


from app.patient_intake import patient_intake_page
from app.admin_protocols import admin_protocols_page
from app.patient_protocols import patient_protocols_page
from app.admin_analytics import admin_analytics_page
from app.patient_analytics import patient_analytics_page
from app.admin_cohort import admin_cohort_page
from app.login import login_page
from app.components.layout import dashboard_layout


def protected_page(page_component: rx.Component) -> rx.Component:
    return dashboard_layout(page_component)


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
)
app.add_page(login_page, route="/login")
app.add_page(lambda: protected_page(index()), route="/", on_load=GlobalState.check_auth)
app.add_page(
    lambda: protected_page(patient_intake_page()),
    route="/intake",
    on_load=GlobalState.check_auth,
)
app.add_page(
    lambda: protected_page(admin_protocols_page()),
    route="/admin/protocols",
    on_load=GlobalState.check_auth,
)
app.add_page(
    lambda: protected_page(patient_protocols_page()),
    route="/patient/protocols",
    on_load=GlobalState.check_auth,
)
app.add_page(
    lambda: protected_page(admin_analytics_page()),
    route="/admin/analytics",
    on_load=GlobalState.check_auth,
)
app.add_page(
    lambda: protected_page(admin_cohort_page()),
    route="/admin/cohort",
    on_load=GlobalState.check_auth,
)
app.add_page(
    lambda: protected_page(patient_analytics_page()),
    route="/patient/analytics",
    on_load=GlobalState.check_auth,
)