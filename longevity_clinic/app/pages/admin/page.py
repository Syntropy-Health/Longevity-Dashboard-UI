"""Admin dashboard main page."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...styles import GlassStyles
from .state import AdminDashboardState
from .components import dashboard_tabs
from .tabs import overview_tab, efficiency_tab
from .sections import patient_management_section
from .modals import add_patient_modal, view_patient_modal


def admin_dashboard() -> rx.Component:
    """Admin dashboard page with overview, patient management, and efficiency tabs."""
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
                ("patients", rx.el.div(
                    patient_management_section(),
                    add_patient_modal(),
                    view_patient_modal(),
                )),
                ("efficiency", efficiency_tab()),
                overview_tab(),  # Default
            ),
        )
    )
