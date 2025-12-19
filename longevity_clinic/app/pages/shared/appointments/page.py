"""Appointments page main entry point.

This module contains the main page function for the appointments page.
Uses shared AppointmentState from states/shared/appointment.py.
"""

import reflex as rx

from ....styles.constants import GlassStyles
from ....components.layout import authenticated_layout
from ....states import AppointmentState
from .sections import appointments_sidebar, appointments_content
from .modals import details_modal


def appointments_page() -> rx.Component:
    """Appointments page with calendar and booking functionality.

    Returns:
        The complete appointments page component
    """
    return authenticated_layout(
        rx.el.div(
            # Page header
            rx.el.div(
                rx.el.h1(
                    "Appointments",
                    class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-2",
                ),
                rx.el.p(
                    "Manage your appointments and schedule visits",
                    class_name="text-slate-400 text-sm",
                ),
                class_name="mb-6",
            ),
            # Main layout with calendar sidebar and content
            rx.el.div(
                # Left sidebar with calendar
                appointments_sidebar(AppointmentState),
                # Main content area
                appointments_content(AppointmentState),
                class_name="flex flex-col lg:flex-row gap-6",
            ),
            # Details modal
            details_modal(AppointmentState),
        )
    )
