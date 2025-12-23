"""Appointments page sections.

This module contains larger section components for the appointments page:
- Calendar sidebar with stats and booking button
- Appointments for selected date
- Upcoming appointments list (paginated)
- Past appointments section
"""

import reflex as rx

from ....components.paginated_view import paginated_list
from ....components.shared import empty_state
from ....styles.constants import GlassStyles
from .components import appointment_card, mini_calendar
from .modals import booking_modal


def calendar_sidebar(state) -> rx.Component:
    """Sidebar with calendar, booking button, and stats.

    Args:
        state: The AppointmentState

    Returns:
        A sidebar component with calendar and booking button
    """
    return rx.vstack(
        # Book appointment button
        booking_modal(state),
        # Mini calendar
        mini_calendar(state),
        # Quick stats card
        rx.box(
            rx.vstack(
                rx.text(
                    "This Month",
                    class_name="text-slate-400 text-xs font-medium mb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.text(
                            state.total_appointments_this_month,
                            class_name="text-2xl font-bold text-white",
                        ),
                        rx.text("Total", class_name="text-slate-400 text-xs"),
                        class_name="flex flex-col items-center",
                    ),
                    rx.el.div(
                        rx.text(
                            state.upcoming_count,
                            class_name="text-2xl font-bold text-teal-400",
                        ),
                        rx.text("Upcoming", class_name="text-slate-400 text-xs"),
                        class_name="flex flex-col items-center",
                    ),
                    rx.el.div(
                        rx.text(
                            state.completed_count,
                            class_name="text-2xl font-bold text-emerald-400",
                        ),
                        rx.text("Completed", class_name="text-slate-400 text-xs"),
                        class_name="flex flex-col items-center",
                    ),
                    class_name="grid grid-cols-3 gap-2",
                ),
                spacing="2",
            ),
            class_name=GlassStyles.card + " p-4",
        ),
        spacing="4",
        width="100%",
    )


def upcoming_appointments_list(state) -> rx.Component:
    """List of upcoming appointments with pagination.

    Args:
        state: The AppointmentState containing appointments data

    Returns:
        A paginated list component showing upcoming appointments
    """

    def render_appointment(apt: dict) -> rx.Component:
        """Render a single appointment card with click handler."""
        return appointment_card(
            apt,
            on_click=lambda a=apt: state.view_appointment_details(a),
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.el.div(
                    rx.icon("calendar-clock", class_name="w-5 h-5 text-teal-400 mr-2"),
                    rx.text(
                        "Upcoming Appointments", class_name="text-white font-semibold"
                    ),
                    class_name="flex items-center",
                ),
                rx.spacer(),
                rx.text(
                    f"{state.upcoming_count} scheduled",
                    class_name="text-slate-400 text-sm",
                ),
                width="100%",
                align_items="center",
            ),
            paginated_list(
                items=state.upcoming_paginated,
                item_renderer=render_appointment,
                has_previous=state.upcoming_has_previous,
                has_next=state.upcoming_has_next,
                page_info=state.upcoming_page_info,
                showing_info=state.upcoming_showing_info,
                on_previous=state.upcoming_previous_page,
                on_next=state.upcoming_next_page,
                empty_icon="calendar-x",
                empty_message="No upcoming appointments",
                empty_subtitle="Book your next visit",
                list_class="space-y-3",
            ),
            spacing="4",
            width="100%",
        ),
        class_name=GlassStyles.card + " p-4 h-full",
    )


def appointments_for_date_section(state) -> rx.Component:
    """Section showing appointments for the selected date.

    Args:
        state: The AppointmentState

    Returns:
        A section component showing appointments for selected date
    """
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.el.div(
                    rx.icon("calendar-days", class_name="w-5 h-5 text-teal-400 mr-2"),
                    rx.text(
                        state.formatted_selected_date,
                        class_name="text-white font-semibold",
                    ),
                    class_name="flex items-center",
                ),
                rx.spacer(),
                rx.text(
                    f"{state.appointments_for_date.length()} appointment(s)",
                    class_name="text-slate-400 text-sm",
                ),
                width="100%",
                align_items="center",
            ),
            rx.cond(
                state.appointments_for_date.length() > 0,
                rx.vstack(
                    rx.foreach(
                        state.appointments_for_date,
                        lambda apt: appointment_card(
                            apt,
                            on_click=lambda a=apt: state.view_appointment_details(a),
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                # Centered empty state
                empty_state(
                    icon="calendar-check",
                    message="No appointments on this date",
                    subtitle="Select a date from the calendar",
                    icon_size="w-10 h-10",
                    center_full=True,
                ),
            ),
            spacing="4",
            width="100%",
            height="100%",
        ),
        class_name=GlassStyles.card + " p-4 h-full flex flex-col",
    )


def past_appointments_section(state) -> rx.Component:
    """Section showing past appointments.

    Args:
        state: The AppointmentState

    Returns:
        A section component showing past appointments
    """
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.el.div(
                    rx.icon("history", class_name="w-5 h-5 text-slate-400 mr-2"),
                    rx.text(
                        "Past Appointments",
                        class_name="text-white font-semibold",
                    ),
                    class_name="flex items-center",
                ),
                rx.spacer(),
                rx.text(
                    f"{state.past_appointments.length()} total",
                    class_name="text-slate-400 text-sm",
                ),
                width="100%",
                align_items="center",
            ),
            rx.cond(
                state.past_appointments.length() > 0,
                rx.vstack(
                    rx.foreach(
                        state.past_appointments_limited,
                        lambda apt: appointment_card(
                            apt,
                            on_click=lambda a=apt: state.view_appointment_details(a),
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                # Centered empty state
                empty_state(
                    icon="calendar-x",
                    message="No past appointments",
                    icon_size="w-10 h-10",
                    center_full=True,
                ),
            ),
            spacing="4",
            width="100%",
            height="100%",
        ),
        class_name=GlassStyles.card + " p-4 h-full flex flex-col",
    )
