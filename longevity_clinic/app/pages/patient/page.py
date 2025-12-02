"""Patient portal main page."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...states.auth_state import AuthState
from ...states.patient_biomarker_state import PatientBiomarkerState
from ...states.patient_dashboard_state import PatientDashboardState
from ...styles.constants import GlassStyles
from .components import patient_sidebar_tabs
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
    return authenticated_layout(
        rx.el.div(
            # Page Header
            rx.el.div(
                rx.el.h1(
                    "My Health Dashboard",
                    class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-2",
                ),
                rx.el.p(
                    rx.el.span("Welcome back, "),
                    rx.el.span(
                        AuthState.user_first_name,
                        class_name="text-teal-400 font-semibold",
                    ),
                    class_name="text-slate-400 text-sm",
                ),
                class_name="mb-6",
            ),
            
            # Main Layout: Sidebar + Content
            rx.el.div(
                # Tab Navigation (horizontal for now, could be sidebar later)
                patient_sidebar_tabs(),
                
                # Tab Content
                rx.match(
                    PatientDashboardState.active_tab,
                    ("overview", overview_tab()),
                    ("food", food_tracker_tab()),
                    ("medications", medications_tab()),
                    ("conditions", conditions_tab()),
                    ("symptoms", symptoms_tab()),
                    ("checkins", checkins_tab()),
                    ("settings", settings_with_data_sources_tab()),
                    overview_tab(),  # Default
                ),
            ),
            
            # Modals
            checkin_modal(),
            medication_modal(),
            condition_modal(),
            symptom_modal(),
            connect_source_modal(),
            on_mount=[
                PatientBiomarkerState.load_biomarkers,
                PatientDashboardState.load_dashboard_data,
            ],
        )
    )


def settings_with_data_sources_tab() -> rx.Component:
    """Settings tab that includes data sources section."""
    return rx.el.div(
        settings_tab(),
        rx.el.div(
            rx.el.h3("Data Sources", class_name="text-lg font-semibold text-white mb-4 mt-8"),
            data_sources_tab(),
        ),
    )
