"""Appointments page modals.

This module contains modal dialogs for the appointments page:
- Booking modal for scheduling new appointments
- Details modal for viewing appointment information
"""

import reflex as rx

from ...styles.constants import GlassStyles
from ...data.demo import DEMO_PATIENTS


def booking_modal(state) -> rx.Component:
    """Modal for booking a new appointment.
    
    Args:
        state: The AppointmentState containing booking form data
        
    Returns:
        A modal dialog component for scheduling appointments
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.box(
                rx.hstack(
                    rx.icon("plus", class_name="w-4 h-4"),
                    rx.text("Book Appointment", class_name="font-medium"),
                    spacing="2",
                    align_items="center",
                ),
                class_name=GlassStyles.BUTTON_PRIMARY + " w-full justify-center",
            ),
        ),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.radix.primitives.dialog.title(
                                rx.text("Book Appointment", class_name="text-xl font-semibold text-white"),
                            ),
                            rx.radix.primitives.dialog.description(
                                rx.text("Schedule your next visit", class_name="text-slate-400 text-sm"),
                            ),
                            align_items="start",
                            spacing="1",
                        ),
                        rx.spacer(),
                        rx.radix.primitives.dialog.close(
                            rx.icon_button(
                                rx.icon("x", class_name="w-4 h-4"),
                                class_name="bg-slate-700 hover:bg-slate-600 rounded-lg p-2",
                            ),
                        ),
                        width="100%",
                        align_items="start",
                    ),
                    # Form content
                    rx.box(
                        rx.vstack(
                            # Patient selection
                            rx.vstack(
                                rx.text("Patient", class_name="text-slate-300 text-sm font-medium"),
                                rx.select.root(
                                    rx.select.trigger(
                                        placeholder="Select patient",
                                        class_name="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg text-white",
                                    ),
                                    rx.select.content(
                                        *[
                                            rx.select.item(patient["name"], value=patient["id"])
                                            for patient in DEMO_PATIENTS
                                        ],
                                        class_name="bg-slate-800 border border-slate-700",
                                    ),
                                    value=state.booking_patient,
                                    on_change=state.set_booking_patient,
                                ),
                                width="100%",
                                align_items="start",
                                spacing="2",
                            ),
                            # Appointment type
                            rx.vstack(
                                rx.text("Appointment Type", class_name="text-slate-300 text-sm font-medium"),
                                rx.select.root(
                                    rx.select.trigger(
                                        placeholder="Select type",
                                        class_name="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg text-white",
                                    ),
                                    rx.select.content(
                                        rx.select.item("Consultation", value="consultation"),
                                        rx.select.item("Follow-up", value="follow-up"),
                                        rx.select.item("Check-up", value="checkup"),
                                        rx.select.item("Lab Review", value="lab-review"),
                                        class_name="bg-slate-800 border border-slate-700",
                                    ),
                                    value=state.booking_type,
                                    on_change=state.set_booking_type,
                                ),
                                width="100%",
                                align_items="start",
                                spacing="2",
                            ),
                            # Doctor selection
                            rx.vstack(
                                rx.text("Doctor", class_name="text-slate-300 text-sm font-medium"),
                                rx.select.root(
                                    rx.select.trigger(
                                        placeholder="Select doctor",
                                        class_name="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg text-white",
                                    ),
                                    rx.select.content(
                                        rx.select.item("Dr. Sarah Chen", value="chen"),
                                        rx.select.item("Dr. Michael Roberts", value="roberts"),
                                        rx.select.item("Dr. Emily Wong", value="wong"),
                                        rx.select.item("Dr. James Miller", value="miller"),
                                        class_name="bg-slate-800 border border-slate-700",
                                    ),
                                    value=state.booking_doctor,
                                    on_change=state.set_booking_doctor,
                                ),
                                width="100%",
                                align_items="start",
                                spacing="2",
                            ),
                            # Date selection
                            rx.vstack(
                                rx.text("Preferred Date", class_name="text-slate-300 text-sm font-medium"),
                                rx.input(
                                    type="date",
                                    value=state.booking_date,
                                    on_change=state.set_booking_date,
                                    class_name="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg px-3 py-2 text-white",
                                ),
                                width="100%",
                                align_items="start",
                                spacing="2",
                            ),
                            # Time selection
                            rx.vstack(
                                rx.text("Preferred Time", class_name="text-slate-300 text-sm font-medium"),
                                rx.select.root(
                                    rx.select.trigger(
                                        placeholder="Select time",
                                        class_name="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg text-white",
                                    ),
                                    rx.select.content(
                                        rx.select.item("9:00 AM", value="9:00 AM"),
                                        rx.select.item("10:00 AM", value="10:00 AM"),
                                        rx.select.item("11:00 AM", value="11:00 AM"),
                                        rx.select.item("2:00 PM", value="2:00 PM"),
                                        rx.select.item("3:00 PM", value="3:00 PM"),
                                        rx.select.item("4:00 PM", value="4:00 PM"),
                                        class_name="bg-slate-800 border border-slate-700",
                                    ),
                                    value=state.booking_time,
                                    on_change=state.set_booking_time,
                                ),
                                width="100%",
                                align_items="start",
                                spacing="2",
                            ),
                            # Notes
                            rx.vstack(
                                rx.text("Notes (optional)", class_name="text-slate-300 text-sm font-medium"),
                                rx.text_area(
                                    placeholder="Any specific concerns or notes...",
                                    value=state.booking_notes,
                                    on_change=state.set_booking_notes,
                                    class_name="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg px-3 py-2 text-white min-h-[80px]",
                                ),
                                width="100%",
                                align_items="start",
                                spacing="2",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        class_name="mt-4 max-h-[400px] overflow-y-auto",
                    ),
                    # Actions
                    rx.hstack(
                        rx.radix.primitives.dialog.close(
                            rx.button(
                                "Cancel",
                                class_name="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg",
                            ),
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.button(
                                "Book Appointment",
                                class_name=GlassStyles.BUTTON_PRIMARY,
                                on_click=state.book_appointment,
                            ),
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                        class_name="mt-6",
                    ),
                    spacing="4",
                    width="100%",
                ),
                class_name=GlassStyles.modal + " fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[450px] max-w-[90vw]",
            ),
        ),
        open=state.show_booking_modal,
        on_open_change=state.set_show_booking_modal,
    )


def details_modal(state) -> rx.Component:
    """Modal for viewing appointment details.
    
    Args:
        state: The AppointmentState containing selected appointment data
        
    Returns:
        A modal dialog component for viewing appointment details
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.vstack(
                            rx.radix.primitives.dialog.title(
                                rx.text("Appointment Details", class_name="text-xl font-semibold text-white"),
                            ),
                            rx.radix.primitives.dialog.description(
                                rx.text(state.selected_appointment_type, class_name="text-teal-400 text-sm"),
                            ),
                            align_items="start",
                            spacing="1",
                        ),
                        rx.spacer(),
                        rx.radix.primitives.dialog.close(
                            rx.icon_button(
                                rx.icon("x", class_name="w-4 h-4"),
                                class_name="bg-slate-700 hover:bg-slate-600 rounded-lg p-2",
                            ),
                        ),
                        width="100%",
                        align_items="start",
                    ),
                    # Details content
                    rx.box(
                        rx.vstack(
                            # Date & Time
                            rx.hstack(
                                rx.box(
                                    rx.icon("calendar", class_name="text-teal-400 w-5 h-5"),
                                    class_name="w-10 h-10 rounded-xl bg-teal-500/20 flex items-center justify-center",
                                ),
                                rx.vstack(
                                    rx.text("Date & Time", class_name="text-slate-400 text-xs"),
                                    rx.text(
                                        f"{state.selected_appointment_date} at {state.selected_appointment_time}",
                                        class_name="text-white font-medium",
                                    ),
                                    align_items="start",
                                    spacing="1",
                                ),
                                spacing="3",
                                align_items="center",
                            ),
                            # Doctor
                            rx.hstack(
                                rx.box(
                                    rx.icon("user", class_name="text-blue-400 w-5 h-5"),
                                    class_name="w-10 h-10 rounded-xl bg-blue-500/20 flex items-center justify-center",
                                ),
                                rx.vstack(
                                    rx.text("Doctor", class_name="text-slate-400 text-xs"),
                                    rx.text(
                                        f"Dr. {state.selected_appointment_doctor}",
                                        class_name="text-white font-medium",
                                    ),
                                    align_items="start",
                                    spacing="1",
                                ),
                                spacing="3",
                                align_items="center",
                            ),
                            # Status
                            rx.hstack(
                                rx.box(
                                    rx.icon("circle-check", class_name="text-emerald-400 w-5 h-5"),
                                    class_name="w-10 h-10 rounded-xl bg-emerald-500/20 flex items-center justify-center",
                                ),
                                rx.vstack(
                                    rx.text("Status", class_name="text-slate-400 text-xs"),
                                    rx.text(
                                        state.selected_appointment_status,
                                        class_name="text-white font-medium capitalize",
                                    ),
                                    align_items="start",
                                    spacing="1",
                                ),
                                spacing="3",
                                align_items="center",
                            ),
                            # Notes
                            rx.cond(
                                state.selected_appointment_notes != "",
                                rx.vstack(
                                    rx.text("Notes", class_name="text-slate-400 text-xs font-medium"),
                                    rx.box(
                                        rx.text(
                                            state.selected_appointment_notes,
                                            class_name="text-slate-300 text-sm",
                                        ),
                                        class_name="bg-slate-800/50 rounded-lg p-3 w-full",
                                    ),
                                    width="100%",
                                    align_items="start",
                                    spacing="2",
                                    class_name="mt-2",
                                ),
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        class_name="mt-4",
                    ),
                    # Actions
                    rx.hstack(
                        rx.radix.primitives.dialog.close(
                            rx.button(
                                rx.hstack(
                                    rx.icon("x", class_name="w-4 h-4"),
                                    rx.text("Cancel Appointment"),
                                    spacing="2",
                                ),
                                class_name="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 px-4 py-2 rounded-lg",
                                on_click=state.cancel_selected_appointment,
                            ),
                        ),
                        rx.spacer(),
                        rx.radix.primitives.dialog.close(
                            rx.button(
                                "Close",
                                class_name="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg",
                            ),
                        ),
                        spacing="3",
                        width="100%",
                        class_name="mt-6",
                    ),
                    spacing="4",
                    width="100%",
                ),
                class_name=GlassStyles.modal + " fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[450px] max-w-[90vw]",
            ),
        ),
        open=state.show_details_modal,
        on_open_change=state.set_show_details_modal,
    )
