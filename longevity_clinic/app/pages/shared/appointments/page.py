"""Appointments page main entry point.

This module contains the main page function for the appointments page.
Uses shared AppointmentState from states/shared/appointment.py.
"""

import reflex as rx

from ....components.layout import authenticated_layout
from ....states import AppointmentState
from ....styles.constants import GlassStyles
from .modals import details_modal
from .sections import (
    appointments_for_date_section,
    calendar_sidebar,
    past_appointments_section,
    upcoming_appointments_list,
)


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
            # Top row: Calendar sidebar + Today's appointments
            rx.el.div(
                # Left: Calendar and stats
                rx.el.div(
                    calendar_sidebar(AppointmentState),
                    class_name="w-full lg:w-80 flex-shrink-0",
                ),
                # Right: Today's/Selected date appointments
                rx.el.div(
                    appointments_for_date_section(AppointmentState),
                    class_name="flex-1 min-w-0",
                ),
                class_name="flex flex-col lg:flex-row gap-6 items-start",
            ),
            # Bottom row: Upcoming and Past appointments side by side (full width)
            rx.el.div(
                # Upcoming appointments
                rx.el.div(
                    upcoming_appointments_list(AppointmentState),
                    class_name="flex-1 min-w-0",
                ),
                # Past appointments
                rx.el.div(
                    past_appointments_section(AppointmentState),
                    class_name="flex-1 min-w-0",
                ),
                class_name="flex flex-col lg:flex-row gap-6 mt-6",
            ),
            # Details modal
            details_modal(AppointmentState),
            class_name="max-w-7xl mx-auto",
        )
    )
