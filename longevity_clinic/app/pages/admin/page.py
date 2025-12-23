"""Admin dashboard main page."""

import reflex as rx

from ...components.layout import authenticated_layout
from ...states import AdminMetricsState, PatientState
from ...styles import GlassStyles
from .components import dashboard_tabs
from .modals import add_patient_modal, view_patient_modal
from .sections import patient_management_section
from .state import AdminDashboardState
from .tabs import efficiency_tab, overview_tab, patient_health_tab


def admin_dashboard() -> rx.Component:
    """Admin dashboard page with overview, patient management, patient health, and efficiency tabs."""
    return authenticated_layout(
        rx.el.div(
            rx.el.h1(
                "Dashboard", class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-6"
            ),
            # Tab navigation
            dashboard_tabs(),
            # Tab content
            rx.match(
                AdminDashboardState.active_tab,
                ("overview", overview_tab()),
                (
                    "patients",
                    rx.el.div(
                        patient_management_section(),
                        add_patient_modal(),
                        view_patient_modal(),
                    ),
                ),
                ("efficiency", efficiency_tab()),
                ("health", patient_health_tab()),
                overview_tab(),  # Default
            ),
            on_mount=[
                AdminMetricsState.load_metrics,
                PatientState.load_patients,
                PatientState.load_recently_active_patients,
            ],
        )
    )
