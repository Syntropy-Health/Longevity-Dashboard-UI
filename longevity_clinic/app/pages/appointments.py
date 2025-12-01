"""Appointments page with calendar view for scheduling."""

import reflex as rx

from ..components.layout import authenticated_layout
from ..states.appointment_state import AppointmentState
from ..states.auth_state import AuthState
from ..styles.constants import GlassStyles


def status_badge(status: str) -> rx.Component:
    """Render appointment status badge."""
    color_map = {
        "scheduled": "bg-amber-100 text-amber-700 border-amber-200",
        "confirmed": "bg-teal-100 text-teal-700 border-teal-200",
        "completed": "bg-gray-100 text-gray-600 border-gray-200",
        "cancelled": "bg-rose-100 text-rose-600 border-rose-200"
    }
    
    return rx.box(
        status.capitalize(),
        class_name=f"px-2.5 py-1 rounded-lg text-xs font-medium border {color_map.get(status, 'bg-gray-100 text-gray-600 border-gray-200')}"
    )


def time_slot_button(slot: dict) -> rx.Component:
    """Render a time slot button."""
    is_available = slot.get("is_available", False)
    is_selected = AppointmentState.selected_time == slot.get("time", "")
    
    return rx.button(
        slot.get("time", ""),
        on_click=lambda: AppointmentState.select_time(slot.get("time", "")),
        disabled=~is_available,
        class_name=f"""
            px-4 py-2 rounded-xl text-sm font-medium transition-all
            {rx.cond(
                is_selected,
                "bg-gradient-to-r from-teal-500 to-emerald-500 text-white shadow-lg",
                rx.cond(
                    is_available,
                    "bg-white/60 border border-teal-200/50 text-teal-700 hover:bg-teal-100/50",
                    "bg-gray-100 text-gray-400 cursor-not-allowed"
                )
            )}
        """
    )


def appointment_card(appointment: dict) -> rx.Component:
    """Render an appointment card."""
    return rx.box(
        rx.flex(
            # Time column
            rx.box(
                rx.text(
                    appointment.get("time", ""),
                    class_name="text-lg font-bold text-teal-600"
                ),
                rx.text(
                    f"{appointment.get('duration_minutes', 60)} min",
                    class_name="text-xs text-gray-400"
                ),
                class_name="text-center min-w-[70px]"
            ),
            
            # Divider
            rx.box(class_name="w-px h-16 bg-teal-200/50 mx-4"),
            
            # Content
            rx.box(
                rx.flex(
                    rx.text(
                        appointment.get("title", "Appointment"),
                        class_name="font-semibold text-gray-900"
                    ),
                    status_badge(appointment.get("status", "scheduled")),
                    class_name="flex items-center gap-3"
                ),
                rx.text(
                    appointment.get("description", ""),
                    class_name="text-sm text-gray-600 mt-1 line-clamp-1"
                ),
                rx.flex(
                    rx.flex(
                        rx.icon("user", class_name="w-3.5 h-3.5 text-gray-400"),
                        rx.text(
                            appointment.get("patient_name", ""),
                            class_name="text-sm text-gray-500"
                        ),
                        class_name="flex items-center gap-1.5"
                    ),
                    rx.flex(
                        rx.icon("stethoscope", class_name="w-3.5 h-3.5 text-gray-400"),
                        rx.text(
                            appointment.get("provider", ""),
                            class_name="text-sm text-gray-500"
                        ),
                        class_name="flex items-center gap-1.5"
                    ),
                    class_name="flex items-center gap-4 mt-2"
                ),
                class_name="flex-1"
            ),
            
            # Actions
            rx.button(
                rx.icon("chevron-right", class_name="w-5 h-5 text-gray-400"),
                on_click=lambda: AppointmentState.open_details_modal(appointment),
                class_name="p-2 rounded-lg hover:bg-teal-100/50 transition-colors"
            ),
            class_name="flex items-center"
        ),
        class_name=f"{GlassStyles.PANEL_LIGHT} p-4 hover:shadow-md transition-all cursor-pointer",
        on_click=lambda: AppointmentState.open_details_modal(appointment)
    )


def mini_calendar() -> rx.Component:
    """Render a simple date selection interface."""
    # Note: This is a simplified calendar. For full calendar functionality,
    # the reflex-calendar component would be integrated here.
    return rx.box(
        rx.flex(
            rx.text(
                "Select Date",
                class_name="font-semibold text-gray-900"
            ),
            rx.text(
                AppointmentState.selected_date_display,
                class_name="text-teal-600 font-medium"
            ),
            class_name="flex items-center justify-between mb-4"
        ),
        rx.el.input(
            type="date",
            value=AppointmentState.selected_date,
            on_change=lambda e: AppointmentState.select_date(e.target.value),
            min=AppointmentState.today_str,
            class_name=f"{GlassStyles.MODAL_INPUT} cursor-pointer"
        ),
        class_name=f"{GlassStyles.PANEL_LIGHT} p-4"
    )


def time_slots_grid() -> rx.Component:
    """Render time slots for selected date."""
    return rx.box(
        rx.text(
            "Available Times",
            class_name="font-semibold text-gray-900 mb-4"
        ),
        rx.cond(
            AppointmentState.selected_date != "",
            rx.box(
                rx.foreach(
                    AppointmentState.available_time_slots,
                    lambda slot: rx.button(
                        slot["time"],
                        on_click=lambda: AppointmentState.select_time(slot["time"]),
                        disabled=~slot["is_available"],
                        class_name=rx.cond(
                            AppointmentState.selected_time == slot["time"],
                            "px-4 py-2 rounded-xl text-sm font-medium bg-gradient-to-r from-teal-500 to-emerald-500 text-white shadow-lg",
                            rx.cond(
                                slot["is_available"],
                                "px-4 py-2 rounded-xl text-sm font-medium bg-white/60 border border-teal-200/50 text-teal-700 hover:bg-teal-100/50 transition-all",
                                "px-4 py-2 rounded-xl text-sm font-medium bg-gray-100 text-gray-400 cursor-not-allowed"
                            )
                        )
                    )
                ),
                class_name="grid grid-cols-3 gap-2"
            ),
            rx.text(
                "Select a date to see available times",
                class_name="text-gray-400 text-center py-8"
            )
        ),
        class_name=f"{GlassStyles.PANEL_LIGHT} p-4"
    )


def booking_modal() -> rx.Component:
    """Render booking modal."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name=GlassStyles.MODAL_OVERLAY
            ),
            rx.radix.primitives.dialog.content(
                rx.box(
                    # Header
                    rx.flex(
                        rx.box(
                            rx.text(
                                "Book Appointment",
                                class_name=GlassStyles.MODAL_TITLE
                            ),
                            rx.text(
                                f"{AppointmentState.selected_date_display} at {AppointmentState.selected_time}",
                                class_name="text-teal-600 font-medium"
                            )
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name=GlassStyles.CLOSE_BUTTON
                            )
                        ),
                        class_name="flex items-start justify-between mb-6"
                    ),
                    
                    # Form
                    rx.box(
                        # Treatment type
                        rx.box(
                            rx.text("Treatment Type", class_name=GlassStyles.LABEL),
                            rx.select.root(
                                rx.select.trigger(
                                    placeholder="Select treatment...",
                                    class_name=GlassStyles.MODAL_SELECT
                                ),
                                rx.select.content(
                                    rx.foreach(
                                        AppointmentState.treatment_types,
                                        lambda t: rx.select.item(t, value=t)
                                    )
                                ),
                                on_change=AppointmentState.set_new_appointment_treatment,
                                value=AppointmentState.new_appointment_treatment
                            ),
                            class_name="mb-4"
                        ),
                        
                        # Title
                        rx.box(
                            rx.text("Appointment Title (optional)", class_name=GlassStyles.LABEL),
                            rx.el.input(
                                placeholder="e.g., Initial NAD+ Session",
                                value=AppointmentState.new_appointment_title,
                                on_change=lambda e: AppointmentState.set_new_appointment_title(e.target.value),
                                class_name=GlassStyles.MODAL_INPUT
                            ),
                            class_name="mb-4"
                        ),
                        
                        # Description
                        rx.box(
                            rx.text("Description", class_name=GlassStyles.LABEL),
                            rx.el.textarea(
                                placeholder="Add any details about your appointment...",
                                value=AppointmentState.new_appointment_description,
                                on_change=lambda e: AppointmentState.set_new_appointment_description(e.target.value),
                                rows=3,
                                class_name=GlassStyles.MODAL_TEXTAREA
                            ),
                            class_name="mb-4"
                        ),
                        
                        # Duration
                        rx.box(
                            rx.text("Duration (minutes)", class_name=GlassStyles.LABEL),
                            rx.select.root(
                                rx.select.trigger(
                                    placeholder="Select duration...",
                                    class_name=GlassStyles.MODAL_SELECT
                                ),
                                rx.select.content(
                                    rx.select.item("30 minutes", value="30"),
                                    rx.select.item("45 minutes", value="45"),
                                    rx.select.item("60 minutes", value="60"),
                                    rx.select.item("90 minutes", value="90"),
                                    rx.select.item("120 minutes", value="120"),
                                    rx.select.item("180 minutes", value="180"),
                                    rx.select.item("240 minutes", value="240"),
                                ),
                                on_change=AppointmentState.set_new_appointment_duration,
                                default_value="60"
                            ),
                            class_name="mb-4"
                        ),
                        
                        # Notes
                        rx.box(
                            rx.text("Additional Notes", class_name=GlassStyles.LABEL),
                            rx.el.textarea(
                                placeholder="Any special requirements or notes for the clinic...",
                                value=AppointmentState.new_appointment_notes,
                                on_change=lambda e: AppointmentState.set_new_appointment_notes(e.target.value),
                                rows=2,
                                class_name=GlassStyles.MODAL_TEXTAREA
                            )
                        )
                    ),
                    
                    # Footer
                    rx.flex(
                        rx.radix.primitives.dialog.close(
                            rx.button(
                                "Cancel",
                                class_name=GlassStyles.BUTTON_CANCEL
                            )
                        ),
                        rx.button(
                            rx.icon("calendar-plus", class_name="w-4 h-4 mr-2"),
                            "Book Appointment",
                            on_click=AppointmentState.create_appointment,
                            class_name=GlassStyles.BUTTON_PRIMARY_LIGHT
                        ),
                        class_name=GlassStyles.MODAL_FOOTER
                    ),
                    class_name=f"{GlassStyles.MODAL_PANEL} {GlassStyles.MODAL_CONTENT_LG}"
                )
            )
        ),
        open=AppointmentState.show_booking_modal,
        on_open_change=AppointmentState.handle_booking_modal_open_change
    )


def details_modal() -> rx.Component:
    """Render appointment details modal."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name=GlassStyles.MODAL_OVERLAY
            ),
            rx.radix.primitives.dialog.content(
                rx.box(
                    # Header
                    rx.flex(
                        rx.box(
                            rx.text(
                                AppointmentState.selected_appointment.get("title", "Appointment"),
                                class_name=GlassStyles.MODAL_TITLE
                            ),
                            status_badge(AppointmentState.selected_appointment.get("status", "scheduled"))
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name=GlassStyles.CLOSE_BUTTON
                            )
                        ),
                        class_name="flex items-start justify-between mb-6"
                    ),
                    
                    # Details
                    rx.box(
                        # Date and time
                        rx.flex(
                            rx.box(
                                rx.icon("calendar", class_name="w-5 h-5 text-teal-500"),
                                class_name="p-2 rounded-lg bg-teal-100/50"
                            ),
                            rx.box(
                                rx.text("Date & Time", class_name="text-xs text-gray-500"),
                                rx.text(
                                    f"{AppointmentState.selected_appointment.get('date', '')} at {AppointmentState.selected_appointment.get('time', '')}",
                                    class_name="font-medium text-gray-900"
                                ),
                                rx.text(
                                    f"{AppointmentState.selected_appointment.get('duration_minutes', 60)} minutes",
                                    class_name="text-sm text-gray-500"
                                )
                            ),
                            class_name="flex items-start gap-3 p-3 rounded-xl bg-gray-50 mb-3"
                        ),
                        
                        # Treatment
                        rx.flex(
                            rx.box(
                                rx.icon("activity", class_name="w-5 h-5 text-purple-500"),
                                class_name="p-2 rounded-lg bg-purple-100/50"
                            ),
                            rx.box(
                                rx.text("Treatment Type", class_name="text-xs text-gray-500"),
                                rx.text(
                                    AppointmentState.selected_appointment.get("treatment_type", ""),
                                    class_name="font-medium text-gray-900"
                                )
                            ),
                            class_name="flex items-start gap-3 p-3 rounded-xl bg-gray-50 mb-3"
                        ),
                        
                        # Provider
                        rx.flex(
                            rx.box(
                                rx.icon("stethoscope", class_name="w-5 h-5 text-blue-500"),
                                class_name="p-2 rounded-lg bg-blue-100/50"
                            ),
                            rx.box(
                                rx.text("Provider", class_name="text-xs text-gray-500"),
                                rx.text(
                                    AppointmentState.selected_appointment.get("provider", ""),
                                    class_name="font-medium text-gray-900"
                                )
                            ),
                            class_name="flex items-start gap-3 p-3 rounded-xl bg-gray-50 mb-3"
                        ),
                        
                        # Description
                        rx.cond(
                            AppointmentState.selected_appointment.get("description", "") != "",
                            rx.box(
                                rx.text("Description", class_name="text-xs text-gray-500 mb-1"),
                                rx.text(
                                    AppointmentState.selected_appointment.get("description", ""),
                                    class_name="text-gray-700"
                                ),
                                class_name="p-3 rounded-xl bg-gray-50 mb-3"
                            ),
                            rx.fragment()
                        ),
                        
                        # Notes
                        rx.cond(
                            AppointmentState.selected_appointment.get("notes", "") != "",
                            rx.box(
                                rx.text("Notes", class_name="text-xs text-gray-500 mb-1"),
                                rx.text(
                                    AppointmentState.selected_appointment.get("notes", ""),
                                    class_name="text-gray-700"
                                ),
                                class_name="p-3 rounded-xl bg-amber-50 border border-amber-200/50"
                            ),
                            rx.fragment()
                        )
                    ),
                    
                    # Footer actions
                    rx.flex(
                        rx.cond(
                            AppointmentState.selected_appointment.get("status", "") != "cancelled",
                            rx.button(
                                rx.icon("x", class_name="w-4 h-4 mr-2"),
                                "Cancel Appointment",
                                on_click=lambda: AppointmentState.cancel_appointment(
                                    AppointmentState.selected_appointment.get("id", "")
                                ),
                                class_name="px-4 py-2 rounded-xl text-rose-600 hover:bg-rose-100/50 transition-colors"
                            ),
                            rx.fragment()
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.button(
                                "Close",
                                class_name=GlassStyles.BUTTON_PRIMARY_LIGHT
                            )
                        ),
                        class_name=GlassStyles.MODAL_FOOTER
                    ),
                    class_name=f"{GlassStyles.MODAL_PANEL} {GlassStyles.MODAL_CONTENT_LG}"
                )
            )
        ),
        open=AppointmentState.show_details_modal,
        on_open_change=AppointmentState.handle_details_modal_open_change
    )


def appointments_sidebar() -> rx.Component:
    """Render appointment scheduling sidebar."""
    return rx.box(
        rx.text(
            "Schedule Appointment",
            class_name=f"text-lg {GlassStyles.HEADING_LIGHT} mb-4"
        ),
        
        # Date picker
        mini_calendar(),
        
        rx.box(class_name="h-4"),
        
        # Time slots
        time_slots_grid(),
        
        rx.box(class_name="h-4"),
        
        # Book button
        rx.cond(
            (AppointmentState.selected_date != "") & (AppointmentState.selected_time != ""),
            rx.button(
                rx.icon("calendar-plus", class_name="w-5 h-5 mr-2"),
                "Book This Time",
                on_click=AppointmentState.open_booking_modal,
                class_name=f"{GlassStyles.BUTTON_PRIMARY_LIGHT} w-full justify-center"
            ),
            rx.button(
                rx.icon("calendar-plus", class_name="w-5 h-5 mr-2"),
                "Select Date & Time",
                disabled=True,
                class_name="w-full justify-center px-6 py-2.5 rounded-xl font-medium bg-gray-200 text-gray-400 cursor-not-allowed"
            )
        ),
        
        class_name="sticky top-24"
    )


def upcoming_appointments_list() -> rx.Component:
    """Render list of upcoming appointments."""
    return rx.box(
        rx.flex(
            rx.text(
                "Upcoming Appointments",
                class_name=f"text-xl {GlassStyles.HEADING_LIGHT}"
            ),
            rx.text(
                f"{AppointmentState.upcoming_appointments.length()} scheduled",
                class_name="text-sm text-gray-500"
            ),
            class_name="flex items-center justify-between mb-4"
        ),
        
        rx.cond(
            AppointmentState.upcoming_appointments.length() > 0,
            rx.box(
                rx.foreach(
                    AppointmentState.upcoming_appointments,
                    appointment_card
                ),
                class_name="space-y-3"
            ),
            rx.box(
                rx.flex(
                    rx.box(
                        rx.icon("calendar-x", class_name="w-12 h-12 text-gray-300"),
                        class_name="p-6 rounded-full bg-gray-100"
                    ),
                    rx.text(
                        "No upcoming appointments",
                        class_name="text-xl font-semibold text-gray-600 mt-4"
                    ),
                    rx.text(
                        "Select a date and time to book your next session",
                        class_name="text-gray-400 text-center mt-2"
                    ),
                    class_name="flex flex-col items-center justify-center py-12"
                ),
                class_name=f"{GlassStyles.PANEL_LIGHT} p-8"
            )
        )
    )


def appointments_for_date_section() -> rx.Component:
    """Render appointments for selected date."""
    return rx.cond(
        AppointmentState.selected_date != "",
        rx.box(
            rx.flex(
                rx.text(
                    AppointmentState.selected_date_display,
                    class_name=f"text-lg {GlassStyles.HEADING_LIGHT}"
                ),
                rx.text(
                    f"{AppointmentState.appointments_for_selected_date.length()} appointments",
                    class_name="text-sm text-gray-500"
                ),
                class_name="flex items-center justify-between mb-4"
            ),
            rx.cond(
                AppointmentState.appointments_for_selected_date.length() > 0,
                rx.box(
                    rx.foreach(
                        AppointmentState.appointments_for_selected_date,
                        appointment_card
                    ),
                    class_name="space-y-3"
                ),
                rx.box(
                    rx.text(
                        "No appointments scheduled for this date",
                        class_name="text-gray-500 text-center py-8"
                    ),
                    class_name=f"{GlassStyles.PANEL_LIGHT}"
                )
            ),
            class_name="mb-8"
        ),
        rx.fragment()
    )


def appointments_content() -> rx.Component:
    """Main appointments content."""
    return rx.box(
        # Header
        rx.flex(
            rx.box(
                rx.text(
                    "Appointments",
                    class_name=f"text-2xl {GlassStyles.HEADING_LIGHT}"
                ),
                rx.text(
                    "Schedule and manage your longevity treatment sessions",
                    class_name=GlassStyles.SUBHEADING_LIGHT
                )
            ),
            class_name="mb-6"
        ),
        
        # Main layout
        rx.flex(
            # Main content area
            rx.box(
                appointments_for_date_section(),
                upcoming_appointments_list(),
                class_name="flex-1"
            ),
            
            # Sidebar
            rx.box(
                appointments_sidebar(),
                class_name="w-80 ml-6"
            ),
            class_name="flex"
        ),
        
        # Modals
        booking_modal(),
        details_modal()
    )


@rx.page(
    route="/appointments",
    title="Appointments - Longevity Clinic",
    on_load=[
        AuthState.check_auth,
        AppointmentState.load_appointments
    ]
)
def appointments_page() -> rx.Component:
    """Appointments page component."""
    return authenticated_layout(
        rx.box(
            appointments_content(),
            class_name="p-6 max-w-6xl mx-auto"
        )
    )
