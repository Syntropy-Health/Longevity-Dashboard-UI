"""Appointment state management with calendar integration."""

import calendar as cal
from datetime import date, datetime

import reflex as rx

from ...config import get_logger
from ...data.seed import (
    APPOINTMENTS_SEED,
    DEMO_PATIENTS,
    PROVIDERS,
)
from ...functions.db_utils import (
    create_appointment_sync,
    get_appointments_for_user_sync,
    get_appointments_sync,
    update_appointment_status_sync,
)
from ..auth import AuthState

logger = get_logger("longevity_clinic.appointment")


class AppointmentState(rx.State):
    """Manages appointment scheduling with calendar integration."""

    appointments: list[dict] = []
    selected_date: str = ""

    # Loading state
    is_loading: bool = False
    _data_loaded: bool = False
    selected_time: str = ""
    selected_appointment: dict = {}

    # Calendar navigation
    current_year: int = 2025
    current_month: int = 1

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

    # Pagination for upcoming appointments
    upcoming_page: int = 1
    upcoming_page_size: int = 3

    @rx.var
    def providers(self) -> list[str]:
        """Available providers."""
        return PROVIDERS

    @rx.var
    def demo_patients(self) -> list[dict]:
        """Demo patients for admin booking."""
        return DEMO_PATIENTS

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
    def portal_appointments(self) -> list[dict]:
        """Get upcoming appointments in PortalAppointment format for overview tab.

        Transforms full appointment data to simplified portal format:
        - id, title, date, time, type, provider
        """
        return [
            {
                "id": apt.get("id", ""),
                "title": apt.get("title", apt.get("treatment_type", "Appointment")),
                "date": self._format_date_display(apt.get("date", "")),
                "time": self._format_time_display(apt.get("time", "")),
                "type": apt.get("treatment_type", "Consultation"),
                "provider": apt.get("provider", "Dr. Staff"),
            }
            for apt in self.upcoming_appointments[:5]  # Limit to 5 for overview
        ]

    def _format_date_display(self, iso_date: str) -> str:
        """Format ISO date string for display (e.g., 'Jan 16')."""
        if not iso_date:
            return ""
        try:
            d = datetime.strptime(iso_date, "%Y-%m-%d")
            return d.strftime("%b %d")
        except Exception:
            return iso_date

    def _format_time_display(self, time_str: str) -> str:
        """Format time string for display (e.g., '09:00' -> '9:00 AM')."""
        if not time_str:
            return ""
        try:
            t = datetime.strptime(time_str, "%H:%M")
            return t.strftime("%-I:%M %p")
        except Exception:
            return time_str

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

    # ==========================================================================
    # Pagination computed vars for upcoming appointments
    # ==========================================================================

    @rx.var
    def upcoming_total_pages(self) -> int:
        """Total pages for upcoming appointments."""
        total = len(self.upcoming_appointments)
        return max(1, (total + self.upcoming_page_size - 1) // self.upcoming_page_size)

    @rx.var
    def upcoming_paginated(self) -> list[dict]:
        """Paginated slice of upcoming appointments."""
        start = (self.upcoming_page - 1) * self.upcoming_page_size
        end = start + self.upcoming_page_size
        return self.upcoming_appointments[start:end]

    @rx.var
    def upcoming_has_previous(self) -> bool:
        """Whether there's a previous page of upcoming appointments."""
        return self.upcoming_page > 1

    @rx.var
    def upcoming_has_next(self) -> bool:
        """Whether there's a next page of upcoming appointments."""
        return self.upcoming_page < self.upcoming_total_pages

    @rx.var
    def upcoming_page_info(self) -> str:
        """Page info string for upcoming appointments."""
        return f"Page {self.upcoming_page} of {self.upcoming_total_pages}"

    @rx.var
    def upcoming_showing_info(self) -> str:
        """Showing info string for upcoming appointments."""
        total = len(self.upcoming_appointments)
        if total == 0:
            return "No appointments"
        start = (self.upcoming_page - 1) * self.upcoming_page_size + 1
        end = min(self.upcoming_page * self.upcoming_page_size, total)
        return f"Showing {start}-{end} of {total}"

    def upcoming_previous_page(self):
        """Go to previous page of upcoming appointments."""
        if self.upcoming_page > 1:
            self.upcoming_page -= 1

    def upcoming_next_page(self):
        """Go to next page of upcoming appointments."""
        if self.upcoming_page < self.upcoming_total_pages:
            self.upcoming_page += 1

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

    @rx.event(background=True)
    async def load_appointments(self):
        """Load appointments for current authenticated user from DB.

        Falls back to seed data if no appointments found.
        Note: Requires seeded database. Run: python scripts/load_seed_data.py
        """
        # Prevent duplicate loads
        async with self:
            if self._data_loaded:
                logger.debug("load_appointments: Data already loaded, skipping")
                return
            self.is_loading = True

            # Get user_id and role from auth state
            auth_state = await self.get_state(AuthState)
            is_admin = auth_state.is_admin
            user_id = auth_state.user_id

        logger.info(
            "load_appointments: Starting for user_id=%s, is_admin=%s",
            user_id or "none",
            is_admin,
        )

        try:
            # Admins see all appointments, patients see only their own
            if is_admin:
                db_appointments = get_appointments_sync(limit=100)
            elif user_id:
                db_appointments = get_appointments_for_user_sync(
                    user_id=user_id, limit=100
                )
            else:
                logger.warning("load_appointments: No authenticated user")
                db_appointments = []

            # Fall back to seed data if no DB results
            if not db_appointments:
                logger.info("load_appointments: No DB data, using seed data")
                db_appointments = list(APPOINTMENTS_SEED)

            async with self:
                self.appointments = db_appointments
                self.selected_date = date.today().isoformat()
                # Initialize calendar to current month
                today = date.today()
                self.current_year = today.year
                self.current_month = today.month
                self.is_loading = False
                self._data_loaded = True

            logger.info(
                "load_appointments: Complete (%d appointments)", len(db_appointments)
            )
        except Exception as e:
            logger.error("load_appointments: Failed - %s", e)
            async with self:
                self.is_loading = False

    def select_date(self, selected_date: str):
        """Handle date selection from calendar."""
        self.selected_date = selected_date
        self.selected_time = ""

    def select_time(self, time_slot: str):
        """Select a time slot for booking."""
        self.selected_time = time_slot

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

    def close_details_modal(self):
        """Close appointment details modal."""
        self.show_details_modal = False
        self.selected_appointment = {}

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

    @rx.event(background=True)
    async def book_appointment(self):
        """Create a new appointment from booking form for authenticated user."""
        async with self:
            if not self.booking_date or not self.booking_time:
                return

            # Get user info from auth state
            auth_state = await self.get_state(AuthState)
            user = auth_state.user if auth_state.user else {}
            user_id = int(user.get("id")) if user.get("id") else None
            user_name = user.get("name", "Current User")
            user_external_id = user.get("external_id", "current")

            # For admin booking another patient
            patient_name = user_name
            patient_id = user_external_id

            if self.booking_patient and self.booking_patient != "current":
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

        # Persist to DB with user_id
        create_appointment_sync(new_appointment, user_id=user_id)

        async with self:
            self.appointments = [*self.appointments, new_appointment]
            self.show_booking_modal = False
            # Reset form
            self.booking_type = ""
            self.booking_doctor = ""
            self.booking_patient = ""
            self.booking_date = ""
            self.booking_time = ""
            self.booking_notes = ""

        logger.info("book_appointment: Created %s for user %s", new_id, user_id)

    def cancel_appointment(self, appointment_id: str):
        """Cancel an appointment."""
        for i, apt in enumerate(self.appointments):
            if apt.get("id") == appointment_id:
                self.appointments[i] = {**apt, "status": "cancelled"}
                # Sync to DB
                update_appointment_status_sync(appointment_id, "cancelled")
                break
        self.close_details_modal()
