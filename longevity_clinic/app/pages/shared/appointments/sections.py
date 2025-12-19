"""Appointments page sections.

This module contains larger section components for the appointments page:
- Appointments sidebar with calendar and booking
- Upcoming appointments list
- Appointments for selected date
- Main appointments content area
"""

import reflex as rx

from ....styles.constants import GlassStyles
from .components import appointment_card, mini_calendar
from .modals import booking_modal


def appointments_sidebar(state) -> rx.Component:
    """Sidebar with calendar and booking options.

    Args:
        state: The AppointmentState

    Returns:
        A sidebar component with calendar and booking button
    """
    return rx.box(
        rx.vstack(
            # Book appointment button
            booking_modal(state),
            # Mini calendar
            mini_calendar(state),
            # Quick stats
            rx.box(
                rx.vstack(
                    rx.text(
                        "This Month",
                        class_name="text-slate-400 text-xs font-medium mb-2",
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                state.total_appointments_this_month,
                                class_name="text-2xl font-bold text-white",
                            ),
                            rx.text("Total", class_name="text-slate-400 text-xs"),
                            align_items="center",
                        ),
                        rx.vstack(
                            rx.text(
                                state.upcoming_count,
                                class_name="text-2xl font-bold text-teal-400",
                            ),
                            rx.text("Upcoming", class_name="text-slate-400 text-xs"),
                            align_items="center",
                        ),
                        rx.vstack(
                            rx.text(
                                state.completed_count,
                                class_name="text-2xl font-bold text-emerald-400",
                            ),
                            rx.text("Completed", class_name="text-slate-400 text-xs"),
                            align_items="center",
                        ),
                        spacing="4",
                        justify="between",
                        width="100%",
                    ),
                    spacing="2",
                ),
                class_name=GlassStyles.card + " p-4",
            ),
            spacing="4",
            width="100%",
        ),
        class_name="w-80 flex-shrink-0",
    )


def upcoming_appointments_list(state) -> rx.Component:
    """List of upcoming appointments.

    Args:
        state: The AppointmentState containing appointments data

    Returns:
        A list component showing upcoming appointments
    """
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("Upcoming Appointments", class_name="text-white font-semibold"),
                rx.spacer(),
                rx.text(
                    f"{state.upcoming_count} scheduled",
                    class_name="text-slate-400 text-sm",
                ),
                width="100%",
                align_items="center",
            ),
            rx.cond(
                state.upcoming_appointments.length() > 0,
                rx.vstack(
                    rx.foreach(
                        state.upcoming_appointments,
                        lambda apt: appointment_card(
                            apt,
                            on_click=lambda a=apt: state.view_appointment_details(a),
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.box(
                    rx.vstack(
                        rx.icon("calendar-x", class_name="text-slate-500 w-12 h-12"),
                        rx.text(
                            "No upcoming appointments", class_name="text-slate-400"
                        ),
                        rx.text(
                            "Book your next visit", class_name="text-slate-500 text-sm"
                        ),
                        align_items="center",
                        spacing="2",
                    ),
                    class_name="py-12 text-center",
                ),
            ),
            spacing="4",
            width="100%",
        ),
        class_name=GlassStyles.card + " p-4",
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
                rx.text(
                    f"Appointments on {state.formatted_selected_date}",
                    class_name="text-white font-semibold",
                ),
                rx.spacer(),
                rx.text(
                    f"{state.appointments_for_date.length()} found",
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
                rx.box(
                    rx.vstack(
                        rx.icon(
                            "calendar-check", class_name="text-slate-500 w-10 h-10"
                        ),
                        rx.text(
                            "No appointments on this date",
                            class_name="text-slate-400 text-sm",
                        ),
                        align_items="center",
                        spacing="2",
                    ),
                    class_name="py-8 text-center",
                ),
            ),
            spacing="4",
            width="100%",
        ),
        class_name=GlassStyles.card + " p-4",
    )


def appointments_content(state) -> rx.Component:
    """Main content area for appointments.

    Args:
        state: The AppointmentState

    Returns:
        The main content component with appointments listings
    """
    return rx.box(
        rx.vstack(
            # Upcoming appointments
            upcoming_appointments_list(state),
            # Appointments for selected date
            appointments_for_date_section(state),
            # Past appointments section
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Past Appointments", class_name="text-white font-semibold"
                        ),
                        rx.spacer(),
                        rx.button(
                            "View All",
                            class_name="text-teal-400 hover:text-teal-300 text-sm bg-transparent",
                        ),
                        width="100%",
                        align_items="center",
                    ),
                    rx.cond(
                        state.past_appointments.length() > 0,
                        rx.vstack(
                            rx.foreach(
                                state.past_appointments_limited,  # Show only last 3
                                lambda apt: appointment_card(
                                    apt,
                                    on_click=lambda a=apt: state.view_appointment_details(
                                        a
                                    ),
                                ),
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        rx.box(
                            rx.text(
                                "No past appointments",
                                class_name="text-slate-400 text-sm",
                            ),
                            class_name="py-4 text-center",
                        ),
                    ),
                    spacing="4",
                    width="100%",
                ),
                class_name=GlassStyles.card + " p-4",
            ),
            spacing="4",
            width="100%",
        ),
        class_name="flex-1",
    )
