"""Appointments page main entry point.

This module contains the main page function for the appointments page.
"""

import reflex as rx

from ...styles.constants import GlassStyles
from ...states.auth_state import AuthState
from ...components.sidebar import sidebar
from ...components.header import header
from .sections import appointments_sidebar, appointments_content
from .modals import details_modal


# Import AppointmentState - create if doesn't exist
try:
    from ...states.appointment_state import AppointmentState
except ImportError:
    # Fallback state if appointment_state.py doesn't exist yet
    class AppointmentState(rx.State):
        """Appointment scheduling state."""
        
        # Calendar state
        selected_date: int = 15
        current_month: int = 1
        current_year: int = 2025
        calendar_weeks: list[list[int]] = [
            [0, 0, 0, 1, 2, 3, 4],
            [5, 6, 7, 8, 9, 10, 11],
            [12, 13, 14, 15, 16, 17, 18],
            [19, 20, 21, 22, 23, 24, 25],
            [26, 27, 28, 29, 30, 31, 0],
        ]
        
        # Booking form state
        show_booking_modal: bool = False
        booking_type: str = ""
        booking_doctor: str = ""
        booking_date: str = ""
        booking_time: str = ""
        booking_notes: str = ""
        
        # Details modal state
        show_details_modal: bool = False
        selected_appointment_type: str = ""
        selected_appointment_date: str = ""
        selected_appointment_time: str = ""
        selected_appointment_doctor: str = ""
        selected_appointment_status: str = ""
        selected_appointment_notes: str = ""
        
        # Time selection
        selected_time: str = ""
        
        # Appointments data
        appointments: list[dict] = [
            {"id": 1, "type": "Consultation", "date": "Jan 18, 2025", "time": "10:00 AM", "doctor": "Chen", "status": "confirmed", "notes": ""},
            {"id": 2, "type": "Follow-up", "date": "Jan 22, 2025", "time": "2:00 PM", "doctor": "Roberts", "status": "pending", "notes": "Discuss lab results"},
            {"id": 3, "type": "Check-up", "date": "Jan 10, 2025", "time": "9:00 AM", "doctor": "Wong", "status": "completed", "notes": ""},
        ]
        
        @rx.var
        def current_month_year(self) -> str:
            months = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
            return f"{months[self.current_month - 1]} {self.current_year}"
        
        @rx.var
        def formatted_selected_date(self) -> str:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            return f"{months[self.current_month - 1]} {self.selected_date}, {self.current_year}"
        
        @rx.var
        def upcoming_appointments(self) -> list[dict]:
            return [a for a in self.appointments if a.get("status") in ["confirmed", "pending"]]
        
        @rx.var
        def past_appointments(self) -> list[dict]:
            return [a for a in self.appointments if a.get("status") == "completed"]
        
        @rx.var
        def appointments_for_date(self) -> list[dict]:
            # Simple filter - in production would match actual dates
            return self.upcoming_appointments[:1] if self.selected_date == 18 else []
        
        @rx.var
        def total_appointments_this_month(self) -> int:
            return len(self.appointments)
        
        @rx.var
        def upcoming_count(self) -> int:
            return len(self.upcoming_appointments)
        
        @rx.var
        def completed_count(self) -> int:
            return len(self.past_appointments)
        
        def select_date(self, day: int):
            self.selected_date = day
        
        def select_time(self, time: str):
            self.selected_time = time
        
        def prev_month(self):
            if self.current_month == 1:
                self.current_month = 12
                self.current_year -= 1
            else:
                self.current_month -= 1
        
        def next_month(self):
            if self.current_month == 12:
                self.current_month = 1
                self.current_year += 1
            else:
                self.current_month += 1
        
        def view_appointment_details(self, appointment: dict):
            self.selected_appointment_type = appointment.get("type", "")
            self.selected_appointment_date = appointment.get("date", "")
            self.selected_appointment_time = appointment.get("time", "")
            self.selected_appointment_doctor = appointment.get("doctor", "")
            self.selected_appointment_status = appointment.get("status", "")
            self.selected_appointment_notes = appointment.get("notes", "")
            self.show_details_modal = True
        
        def book_appointment(self):
            # Add new appointment
            new_apt = {
                "id": len(self.appointments) + 1,
                "type": self.booking_type or "Consultation",
                "date": self.booking_date or "Jan 25, 2025",
                "time": self.booking_time or "10:00 AM",
                "doctor": self.booking_doctor or "Chen",
                "status": "pending",
                "notes": self.booking_notes,
            }
            self.appointments = self.appointments + [new_apt]
            # Reset form
            self.booking_type = ""
            self.booking_doctor = ""
            self.booking_date = ""
            self.booking_time = ""
            self.booking_notes = ""
            self.show_booking_modal = False
        
        def cancel_selected_appointment(self):
            # In production, would update the appointment status
            self.show_details_modal = False


@rx.page(route="/appointments", title="Appointments | Longevity Clinic")
def appointments_page() -> rx.Component:
    """Appointments page with calendar and booking functionality.
    
    Returns:
        The complete appointments page component
    """
    return rx.box(
        rx.hstack(
            # Sidebar
            sidebar(),
            # Main content
            rx.box(
                rx.vstack(
                    # Header
                    header(),
                    # Page title
                    rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text("Appointments", class_name="text-2xl font-bold text-white"),
                                rx.text(
                                    "Manage your appointments and schedule visits",
                                    class_name="text-slate-400 text-sm",
                                ),
                                align_items="start",
                                spacing="1",
                            ),
                            rx.spacer(),
                            width="100%",
                        ),
                        class_name="px-6 py-4",
                    ),
                    # Main layout with sidebar and content
                    rx.box(
                        rx.hstack(
                            # Left sidebar with calendar
                            appointments_sidebar(AppointmentState),
                            # Main content area
                            appointments_content(AppointmentState),
                            spacing="6",
                            align_items="start",
                            width="100%",
                        ),
                        class_name="px-6 pb-6 flex-1 overflow-auto",
                    ),
                    spacing="0",
                    width="100%",
                    height="100vh",
                ),
                class_name="flex-1 bg-slate-900 overflow-hidden",
            ),
            spacing="0",
            width="100%",
        ),
        # Details modal
        details_modal(AppointmentState),
        class_name="min-h-screen bg-slate-900",
    )
