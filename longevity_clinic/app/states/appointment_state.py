"""Appointment state management with calendar integration."""

from datetime import datetime, date
import calendar as cal
import reflex as rx

from ..data.demo import DEMO_PATIENTS, DEMO_APPOINTMENTS, TREATMENT_TYPES, PROVIDERS


class AppointmentState(rx.State):
    """Manages appointment scheduling with calendar integration."""

    appointments: list[dict] = []
    selected_date: str = ""
    selected_time: str = ""
    selected_appointment: dict = {}

    # Calendar navigation
    current_year: int = 2025
    current_month: int = 1

    # Form fields for new appointment
    new_appointment_title: str = ""
    new_appointment_description: str = ""
    new_appointment_treatment: str = ""
    new_appointment_duration: int = 60
    new_appointment_notes: str = ""

    # Modal state
    show_booking_modal: bool = False
    show_details_modal: bool = False

    # Booking form fields
    booking_type: str = ""
    booking_doctor: str = ""
    booking_patient: str = ""
    booking_date: str = ""
    booking_time: str = ""
    booking_notes: str = ""

    # View mode for admin
    view_mode: str = "calendar"  # "calendar", "list"

    # Demo appointments data
    _demo_appointments: list[dict] = DEMO_APPOINTMENTS

    # Available treatment types and providers
    treatment_types: list[str] = TREATMENT_TYPES
    providers: list[str] = PROVIDERS

    @rx.var
    def today_str(self) -> str:
        """Today's date as ISO string."""
        return date.today().isoformat()

    @rx.var
    def current_month_year(self) -> str:
        """Current month and year for display."""
        month_names = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        return f"{month_names[self.current_month - 1]} {self.current_year}"

    def prev_month(self):
        """Navigate to previous month."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

    def next_month(self):
        """Navigate to next month."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

    @rx.var
    def calendar_weeks(self) -> list[list[int]]:
        """Get calendar weeks for current month (for display)."""
        # Get first day of month (0=Monday, 6=Sunday) and number of days
        first_weekday, num_days = cal.monthrange(self.current_year, self.current_month)

        # Adjust for Sunday start (cal uses Monday=0)
        first_weekday = (first_weekday + 1) % 7

        weeks = []
        current_week = [0] * first_weekday  # Empty days before first

        for day in range(1, num_days + 1):
            current_week.append(day)
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []

        # Pad last week
        if current_week:
            current_week.extend([0] * (7 - len(current_week)))
            weeks.append(current_week)

        return weeks

    @rx.var
    def selected_date_display(self) -> str:
        """Format selected date for display."""
        if not self.selected_date:
            return "Select a date"
        try:
            d = datetime.strptime(self.selected_date, "%Y-%m-%d")
            return d.strftime("%B %d, %Y")
        except Exception:
            return self.selected_date

    @rx.var
    def appointments_for_selected_date(self) -> list[dict]:
        """Get appointments for the selected date."""
        if not self.selected_date:
            return []
        return [
            apt for apt in self.appointments if apt.get("date") == self.selected_date
        ]

    @rx.var
    def upcoming_appointments(self) -> list[dict]:
        """Get all future appointments sorted by date and time."""
        today = date.today().isoformat()
        upcoming = [
            apt
            for apt in self.appointments
            if apt.get("date", "") >= today and apt.get("status") != "cancelled"
        ]
        return sorted(upcoming, key=lambda x: (x.get("date", ""), x.get("time", "")))

    @rx.var
    def available_time_slots(self) -> list[dict]:
        """Get available time slots for the selected date."""
        base_slots = [
            "08:00",
            "08:30",
            "09:00",
            "09:30",
            "10:00",
            "10:30",
            "11:00",
            "11:30",
            "12:00",
            "12:30",
            "13:00",
            "13:30",
            "14:00",
            "14:30",
            "15:00",
            "15:30",
            "16:00",
            "16:30",
            "17:00",
        ]

        booked_times = {
            apt.get("time")
            for apt in self.appointments_for_selected_date
            if apt.get("status") != "cancelled"
        }

        return [
            {"time": slot, "is_available": slot not in booked_times}
            for slot in base_slots
        ]

    @rx.var
    def dates_with_appointments(self) -> list[str]:
        """Get list of dates that have appointments."""
        return list(
            set(
                apt.get("date", "")
                for apt in self.appointments
                if apt.get("status") != "cancelled"
            )
        )

    @rx.var
    def total_appointments_this_month(self) -> int:
        """Get total appointments for current month."""
        month_str = f"{self.current_year}-{self.current_month:02d}"
        return len(
            [
                apt
                for apt in self.appointments
                if apt.get("date", "").startswith(month_str)
            ]
        )

    @rx.var
    def upcoming_count(self) -> int:
        """Count of upcoming appointments."""
        return len(self.upcoming_appointments)

    @rx.var
    def completed_count(self) -> int:
        """Count of completed appointments."""
        return len(
            [apt for apt in self.appointments if apt.get("status") == "completed"]
        )

    @rx.var
    def formatted_selected_date(self) -> str:
        """Format selected date for display."""
        if not self.selected_date:
            return "No date selected"
        try:
            d = datetime.strptime(self.selected_date, "%Y-%m-%d")
            return d.strftime("%B %d, %Y")
        except Exception:
            return self.selected_date

    @rx.var
    def appointments_for_date(self) -> list[dict]:
        """Get appointments for the selected date (alias)."""
        return self.appointments_for_selected_date

    @rx.var
    def past_appointments(self) -> list[dict]:
        """Get past appointments."""
        today = date.today().isoformat()
        past = [apt for apt in self.appointments if apt.get("date", "") < today]
        return sorted(
            past, key=lambda x: (x.get("date", ""), x.get("time", "")), reverse=True
        )

    @rx.var
    def past_appointments_limited(self) -> list[dict]:
        """Get last 3 past appointments."""
        return self.past_appointments[:3]

    @rx.var
    def selected_appointment_type(self) -> str:
        """Get selected appointment type."""
        return self.selected_appointment.get("treatment_type", "")

    @rx.var
    def selected_appointment_date(self) -> str:
        """Get selected appointment date."""
        return self.selected_appointment.get("date", "")

    @rx.var
    def selected_appointment_time(self) -> str:
        """Get selected appointment time."""
        return self.selected_appointment.get("time", "")

    @rx.var
    def selected_appointment_doctor(self) -> str:
        """Get selected appointment doctor."""
        provider = self.selected_appointment.get("provider", "")
        return provider.replace("Dr. ", "") if provider else ""

    @rx.var
    def selected_appointment_status(self) -> str:
        """Get selected appointment status."""
        return self.selected_appointment.get("status", "")

    @rx.var
    def selected_appointment_notes(self) -> str:
        """Get selected appointment notes."""
        return self.selected_appointment.get("notes", "")

    def view_appointment_details(self, appointment: dict):
        """View appointment details in modal."""
        self.selected_appointment = appointment
        self.show_details_modal = True

    def cancel_selected_appointment(self):
        """Cancel the currently selected appointment."""
        apt_id = self.selected_appointment.get("id")
        if apt_id:
            self.cancel_appointment(apt_id)

    def load_appointments(self):
        """Load demo appointments data."""
        self.appointments = self._demo_appointments.copy()
        self.selected_date = date.today().isoformat()

    def select_date(self, selected_date: str):
        """Handle date selection from calendar."""
        self.selected_date = selected_date
        self.selected_time = ""

    def select_time(self, time_slot: str):
        """Select a time slot for booking."""
        self.selected_time = time_slot

    def open_booking_modal(self):
        """Open the booking modal."""
        self.show_booking_modal = True
        self.new_appointment_title = ""
        self.new_appointment_description = ""
        self.new_appointment_treatment = ""
        self.new_appointment_duration = 60
        self.new_appointment_notes = ""

    def close_booking_modal(self):
        """Close the booking modal."""
        self.show_booking_modal = False

    def handle_booking_modal_open_change(self, is_open: bool):
        """Handle booking modal open state change."""
        self.show_booking_modal = is_open

    def open_details_modal(self, appointment: dict):
        """Open appointment details modal."""
        self.selected_appointment = appointment
        self.show_details_modal = True

    def close_details_modal(self):
        """Close appointment details modal."""
        self.show_details_modal = False
        self.selected_appointment = {}

    def set_show_booking_modal(self, is_open: bool):
        """Set booking modal open state."""
        self.show_booking_modal = is_open
        if not is_open:
            # Reset form when closing
            self.booking_type = ""
            self.booking_doctor = ""
            self.booking_patient = ""
            self.booking_date = ""
            self.booking_time = ""
            self.booking_notes = ""

    def set_show_details_modal(self, is_open: bool):
        """Set details modal open state."""
        self.show_details_modal = is_open
        if not is_open:
            self.selected_appointment = {}

    def handle_details_modal_open_change(self, is_open: bool):
        """Handle details modal open state change."""
        self.show_details_modal = is_open
        if not is_open:
            self.selected_appointment = {}

    def set_view_mode(self, mode: str):
        """Switch between calendar and list view."""
        self.view_mode = mode

    def set_booking_type(self, value: str):
        """Set booking type."""
        self.booking_type = value

    def set_booking_doctor(self, value: str):
        """Set booking doctor."""
        self.booking_doctor = value

    def set_booking_patient(self, value: str):
        """Set booking patient."""
        self.booking_patient = value

    def set_booking_date(self, value: str):
        """Set booking date."""
        self.booking_date = value

    def set_booking_time(self, value: str):
        """Set booking time."""
        self.booking_time = value

    def set_booking_notes(self, value: str):
        """Set booking notes."""
        self.booking_notes = value

    def book_appointment(self):
        """Create a new appointment from booking form."""
        if not self.booking_date or not self.booking_time:
            return

        # Find patient name if patient selected
        patient_name = "Current User"
        patient_id = "current"

        if self.booking_patient:
            patient_id = self.booking_patient
            for p in DEMO_PATIENTS:
                if p["id"] == self.booking_patient:
                    patient_name = p["name"]
                    break

        new_id = f"APT{len(self.appointments) + 100}"
        new_appointment = {
            "id": new_id,
            "title": self.booking_type or "Consultation",
            "description": self.booking_notes,
            "date": self.booking_date,
            "time": self.booking_time,
            "duration_minutes": 60,
            "treatment_type": self.booking_type or "Consultation",
            "patient_id": patient_id,
            "patient_name": patient_name,
            "provider": self.booking_doctor or "Dr. Johnson",
            "status": "scheduled",
            "notes": self.booking_notes,
        }

        self.appointments = [*self.appointments, new_appointment]
        self.show_booking_modal = False
        # Reset form
        self.booking_type = ""
        self.booking_doctor = ""
        self.booking_patient = ""
        self.booking_date = ""
        self.booking_time = ""
        self.booking_notes = ""

    def set_new_appointment_title(self, value: str):
        """Set new appointment title."""
        self.new_appointment_title = value

    def set_new_appointment_description(self, value: str):
        """Set new appointment description."""
        self.new_appointment_description = value

    def set_new_appointment_treatment(self, value: str):
        """Set new appointment treatment type."""
        self.new_appointment_treatment = value

    def set_new_appointment_duration(self, value: str):
        """Set new appointment duration."""
        try:
            self.new_appointment_duration = int(value)
        except ValueError:
            self.new_appointment_duration = 60

    def set_new_appointment_notes(self, value: str):
        """Set new appointment notes."""
        self.new_appointment_notes = value

    def create_appointment(self):
        """Create a new appointment."""
        if not self.selected_date or not self.selected_time:
            return

        new_id = f"APT{len(self.appointments) + 100}"
        new_appointment = {
            "id": new_id,
            "title": self.new_appointment_title or self.new_appointment_treatment,
            "description": self.new_appointment_description,
            "date": self.selected_date,
            "time": self.selected_time,
            "duration_minutes": self.new_appointment_duration,
            "treatment_type": self.new_appointment_treatment,
            "patient_id": "current",  # Would be set based on auth state
            "patient_name": "Current User",
            "provider": "Dr. Johnson",  # Would be selected
            "status": "scheduled",
            "notes": self.new_appointment_notes,
        }

        self.appointments = [*self.appointments, new_appointment]
        self.close_booking_modal()
        self.selected_time = ""

    def cancel_appointment(self, appointment_id: str):
        """Cancel an appointment."""
        for i, apt in enumerate(self.appointments):
            if apt.get("id") == appointment_id:
                self.appointments[i] = {**apt, "status": "cancelled"}
                break
        self.close_details_modal()

    def confirm_appointment(self, appointment_id: str):
        """Confirm an appointment."""
        for i, apt in enumerate(self.appointments):
            if apt.get("id") == appointment_id:
                self.appointments[i] = {**apt, "status": "confirmed"}
                break

    def complete_appointment(self, appointment_id: str):
        """Mark an appointment as completed."""
        for i, apt in enumerate(self.appointments):
            if apt.get("id") == appointment_id:
                self.appointments[i] = {**apt, "status": "completed"}
                break
        self.close_details_modal()

    def get_status_color(self, status: str) -> str:
        """Get color class for appointment status."""
        colors = {
            "scheduled": "bg-amber-100 text-amber-700",
            "confirmed": "bg-teal-100 text-teal-700",
            "completed": "bg-gray-100 text-gray-600",
            "cancelled": "bg-rose-100 text-rose-600",
        }
        return colors.get(status, "bg-gray-100 text-gray-600")
