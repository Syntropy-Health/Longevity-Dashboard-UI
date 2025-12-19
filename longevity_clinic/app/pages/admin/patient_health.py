"""Admin patient health page - view patient health metrics."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...styles import GlassStyles
from .state import AdminDashboardState
from .tabs import patient_health_tab


def patient_health_page() -> rx.Component:
    """Admin patient health page for viewing patient health metrics."""
    return authenticated_layout(
        rx.el.div(
            rx.el.h1(
                "Patient Health",
                class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-6",
            ),
            patient_health_tab(),
        )
    )
