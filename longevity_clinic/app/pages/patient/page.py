"""Patient portal main page."""

import reflex as rx
from ...states.auth_state import AuthState
from ...states.patient_biomarker_state import PatientBiomarkerState
from ...states.patient_dashboard_state import PatientDashboardState
from ...styles.constants import GlassStyles
from .components import dashboard_tabs
from .tabs import (
    overview_tab,
    food_tracker_tab,
    medications_tab,
    conditions_tab,
    symptoms_tab,
    data_sources_tab,
    checkins_tab,
    settings_tab,
)
from .modals import (
    checkin_modal,
    medication_modal,
    condition_modal,
    symptom_modal,
    connect_source_modal,
)


def patient_portal() -> rx.Component:
    """Patient dashboard page with comprehensive health tracking."""
    return rx.el.div(
        rx.el.div(
            # Header
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "My Health Dashboard",
                        class_name="text-2xl md:text-3xl font-bold text-white",
                    ),
                    rx.el.p(
                        rx.el.span("Welcome back, "),
                        rx.el.span(
                            AuthState.user_first_name,
                            class_name="text-teal-400 font-semibold",
                        ),
                        class_name="text-slate-400 text-sm mt-1",
                    ),
                    class_name="mb-6",
                ),
                # Quick action button
                rx.el.button(
                    rx.icon("mic", class_name="w-5 h-5 mr-2"),
                    "Quick Check-in",
                    on_click=PatientDashboardState.open_checkin_modal,
                    class_name=GlassStyles.BUTTON_PRIMARY,
                ),
                class_name="flex flex-col md:flex-row md:items-center md:justify-between mb-8",
            ),
            # Tab Navigation
            dashboard_tabs(),
            # Tab Content
            rx.cond(
                PatientDashboardState.active_tab == "overview",
                overview_tab(),
                rx.cond(
                    PatientDashboardState.active_tab == "food",
                    food_tracker_tab(),
                    rx.cond(
                        PatientDashboardState.active_tab == "medications",
                        medications_tab(),
                        rx.cond(
                            PatientDashboardState.active_tab == "conditions",
                            conditions_tab(),
                            rx.cond(
                                PatientDashboardState.active_tab == "symptoms",
                                symptoms_tab(),
                                rx.cond(
                                    PatientDashboardState.active_tab == "data_sources",
                                    data_sources_tab(),
                                    rx.cond(
                                        PatientDashboardState.active_tab == "checkins",
                                        checkins_tab(),
                                        rx.cond(
                                            PatientDashboardState.active_tab == "settings",
                                            settings_tab(),
                                            overview_tab(),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            # Modals
            checkin_modal(),
            medication_modal(),
            condition_modal(),
            symptom_modal(),
            connect_source_modal(),
            class_name="p-4 md:p-6 lg:p-8",
        ),
        class_name=f"flex-1 overflow-y-auto {GlassStyles.PAGE_BG}",
        on_mount=[
            PatientBiomarkerState.load_biomarkers,
            PatientDashboardState.load_dashboard_data,
        ],
    )
