"""Appointments page components.

This module contains reusable UI components for the appointments page:
- Status badge for appointment status
- Time slot button for time selection
- Appointment card for displaying appointments
- Mini calendar for date selection
- Time slots grid for time selection
"""

import reflex as rx

from ....styles.constants import GlassStyles


def status_badge(status: str) -> rx.Component:
    """Status badge with appropriate color.

    Args:
        status: The appointment status (confirmed, pending, completed, cancelled)

    Returns:
        A styled badge component showing the status
    """
    status_colors = {
        "confirmed": ("bg-emerald-500/20", "text-emerald-300", "border-emerald-500/30"),
        "pending": ("bg-amber-500/20", "text-amber-300", "border-amber-500/30"),
        "completed": ("bg-blue-500/20", "text-blue-300", "border-blue-500/30"),
        "cancelled": ("bg-red-500/20", "text-red-300", "border-red-500/30"),
    }
    colors = status_colors.get(
        status.lower() if isinstance(status, str) else "pending",
        status_colors["pending"],
    )

    return rx.badge(
        status.capitalize() if isinstance(status, str) else status,
        class_name=f"{colors[0]} {colors[1]} border {colors[2]} px-2 py-1 rounded-lg text-xs font-medium",
    )


def time_slot_button(
    time: str, available: bool, selected: bool, on_click
) -> rx.Component:
    """Time slot selection button.

    Args:
        time: The time string to display
        available: Whether the slot is available
        selected: Whether the slot is currently selected
        on_click: Click handler

    Returns:
        A styled button component for time slot selection
    """
    if not available:
        return rx.box(
            rx.text(time, class_name="text-slate-500 text-sm"),
            class_name="px-3 py-2 rounded-lg bg-slate-800/50 border border-slate-700/30 cursor-not-allowed opacity-50",
        )

    return rx.box(
        rx.text(
            time, class_name=f"text-sm {'text-white' if selected else 'text-slate-300'}"
        ),
        class_name=f"px-3 py-2 rounded-lg cursor-pointer transition-all duration-200 border "
        f"{'bg-teal-500/30 border-teal-400/50 shadow-lg shadow-teal-500/20' if selected else 'bg-slate-700/50 border-slate-600/30 hover:bg-slate-700 hover:border-teal-500/30'}",
        on_click=on_click,
    )


def appointment_card(appointment: dict, on_click=None) -> rx.Component:
    """Appointment card component.

    Args:
        appointment: Dictionary containing appointment data
        on_click: Optional click handler

    Returns:
        A styled card component displaying appointment details
    """
    return rx.box(
        rx.hstack(
            # Date/time column
            rx.box(
                rx.el.div(
                    rx.text(
                        appointment.get("date", "N/A"),
                        class_name="text-xs font-bold text-teal-400 uppercase tracking-wide",
                    ),
                    rx.text(
                        appointment.get("time", "N/A"),
                        class_name="text-xs text-slate-400",
                    ),
                    class_name="text-center",
                ),
                class_name="w-20 shrink-0 bg-teal-500/10 rounded-lg py-2 px-2 border border-teal-500/20",
            ),
            # Appointment details
            rx.vstack(
                rx.text(
                    appointment.get(
                        "title", appointment.get("treatment_type", "Appointment")
                    ),
                    class_name="text-white font-medium text-sm",
                ),
                rx.text(
                    f"{appointment.get('treatment_type', 'Consultation')} with {appointment.get('provider', 'Dr. Staff')}",
                    class_name="text-slate-400 text-xs",
                ),
                spacing="1",
                align_items="start",
            ),
            rx.spacer(),
            status_badge(appointment.get("status", "pending")),
            width="100%",
            align_items="center",
            spacing="3",
        ),
        class_name=GlassStyles.CARD_INTERACTIVE
        + " cursor-pointer hover:bg-slate-700/60 transition-all duration-200",
        on_click=on_click,
    )


def mini_calendar(state) -> rx.Component:
    """Mini calendar for date selection.

    Args:
        state: The AppointmentState containing calendar data

    Returns:
        A styled calendar component for selecting dates
    """
    weekdays = ["S", "M", "T", "W", "T", "F", "S"]

    return rx.box(
        rx.vstack(
            # Month navigation
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevron-left", class_name="w-4 h-4"),
                    class_name="bg-transparent hover:bg-slate-700 rounded-lg p-1",
                    on_click=state.prev_month,
                ),
                rx.text(
                    state.current_month_year,
                    class_name="text-white font-semibold text-sm flex-1 text-center",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", class_name="w-4 h-4"),
                    class_name="bg-transparent hover:bg-slate-700 rounded-lg p-1",
                    on_click=state.next_month,
                ),
                width="100%",
                justify="between",
                align_items="center",
                class_name="mb-3",
            ),
            # Weekday headers
            rx.hstack(
                rx.foreach(
                    weekdays,
                    lambda day: rx.box(
                        rx.text(day, class_name="text-slate-400 text-xs font-medium"),
                        class_name="w-8 h-8 flex items-center justify-center",
                    ),
                ),
                spacing="1",
                justify="center",
            ),
            # Calendar grid
            rx.box(
                rx.foreach(
                    state.calendar_weeks,
                    lambda week: rx.hstack(
                        rx.foreach(
                            week,
                            lambda day: rx.cond(
                                day > 0,
                                rx.box(
                                    rx.text(
                                        day,
                                        class_name=rx.cond(
                                            state.selected_date == day,
                                            "text-white font-medium",
                                            "text-slate-300",
                                        ),
                                    ),
                                    class_name=rx.cond(
                                        state.selected_date == day,
                                        "w-8 h-8 rounded-lg bg-teal-500/30 border border-teal-400/50 flex items-center justify-center cursor-pointer",
                                        "w-8 h-8 rounded-lg hover:bg-slate-700 flex items-center justify-center cursor-pointer transition-colors",
                                    ),
                                    on_click=lambda d=day: state.select_date(d),
                                ),
                                rx.box(class_name="w-8 h-8"),
                            ),
                        ),
                        spacing="1",
                        justify="center",
                    ),
                ),
                class_name="space-y-1",
            ),
            spacing="2",
        ),
        class_name=GlassStyles.card + " p-4",
    )


def time_slots_grid(state) -> rx.Component:
    """Time slots selection grid.

    Args:
        state: The AppointmentState containing time slot data

    Returns:
        A styled grid component for selecting appointment times
    """
    morning_slots = ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM"]
    afternoon_slots = ["12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"]

    return rx.box(
        rx.vstack(
            rx.text("Morning", class_name="text-slate-400 text-xs font-medium mb-2"),
            rx.hstack(
                rx.foreach(
                    morning_slots,
                    lambda t: time_slot_button(
                        t,
                        True,
                        state.selected_time == t,
                        lambda time=t: state.select_time(time),
                    ),
                ),
                spacing="2",
                wrap="wrap",
            ),
            rx.text(
                "Afternoon", class_name="text-slate-400 text-xs font-medium mb-2 mt-4"
            ),
            rx.hstack(
                rx.foreach(
                    afternoon_slots,
                    lambda t: time_slot_button(
                        t,
                        True,
                        state.selected_time == t,
                        lambda time=t: state.select_time(time),
                    ),
                ),
                spacing="2",
                wrap="wrap",
            ),
            align_items="start",
        ),
        class_name=GlassStyles.card + " p-4",
    )
