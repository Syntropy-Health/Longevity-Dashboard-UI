"""Appointment state management with calendar integration."""

from typing import TypedDict
from datetime import datetime, date, timedelta
import reflex as rx


class Appointment(TypedDict):
    """Structure for an appointment."""
    id: str
    title: str
    description: str
    date: str  # ISO format YYYY-MM-DD
    time: str  # HH:MM format
    duration_minutes: int
    treatment_type: str
    patient_id: str
    patient_name: str
    provider: str
    status: str  # "scheduled", "confirmed", "completed", "cancelled"
    notes: str


class TimeSlot(TypedDict):
    """Available time slot structure."""
    time: str
    is_available: bool


class AppointmentState(rx.State):
    """Manages appointment scheduling with calendar integration."""
    
    appointments: list[dict] = []
    selected_date: str = ""
    selected_time: str = ""
    selected_appointment: dict = {}
    
    # Form fields for new appointment
    new_appointment_title: str = ""
    new_appointment_description: str = ""
    new_appointment_treatment: str = ""
    new_appointment_duration: int = 60
    new_appointment_notes: str = ""
    
    # Modal state
    show_booking_modal: bool = False
    show_details_modal: bool = False
    
    # View mode for admin
    view_mode: str = "calendar"  # "calendar", "list"
    
    # Demo appointments data
    _demo_appointments: list[dict] = [
        {
            "id": "APT001",
            "title": "NAD+ IV Therapy",
            "description": "Initial NAD+ infusion session - 4 hour treatment",
            "date": "2025-01-16",
            "time": "09:00",
            "duration_minutes": 240,
            "treatment_type": "IV Therapy",
            "patient_id": "P001",
            "patient_name": "Sarah Chen",
            "provider": "Dr. Johnson",
            "status": "confirmed",
            "notes": "First session, monitor for any reactions"
        },
        {
            "id": "APT002",
            "title": "Hyperbaric Oxygen Session",
            "description": "Standard HBOT treatment - 90 minutes at 1.5 ATA",
            "date": "2025-01-16",
            "time": "14:00",
            "duration_minutes": 90,
            "treatment_type": "HBOT",
            "patient_id": "P002",
            "patient_name": "Marcus Williams",
            "provider": "Dr. Chen",
            "status": "scheduled",
            "notes": ""
        },
        {
            "id": "APT003",
            "title": "Biomarker Assessment",
            "description": "Comprehensive longevity panel and consultation",
            "date": "2025-01-17",
            "time": "10:30",
            "duration_minutes": 60,
            "treatment_type": "Assessment",
            "patient_id": "P003",
            "patient_name": "Elena Rodriguez",
            "provider": "Dr. Patel",
            "status": "confirmed",
            "notes": "Follow-up from previous treatment cycle"
        },
        {
            "id": "APT004",
            "title": "Stem Cell Consultation",
            "description": "Initial consultation for stem cell therapy options",
            "date": "2025-01-18",
            "time": "11:00",
            "duration_minutes": 45,
            "treatment_type": "Consultation",
            "patient_id": "P004",
            "patient_name": "James Park",
            "provider": "Dr. Johnson",
            "status": "scheduled",
            "notes": "New patient referral"
        },
        {
            "id": "APT005",
            "title": "Peptide Therapy Follow-up",
            "description": "3-month progress review for BPC-157/TB-500 protocol",
            "date": "2025-01-20",
            "time": "15:30",
            "duration_minutes": 30,
            "treatment_type": "Follow-up",
            "patient_id": "P001",
            "patient_name": "Sarah Chen",
            "provider": "Dr. Chen",
            "status": "scheduled",
            "notes": "Review healing progress"
        }
    ]
    
    # Available treatment types
    treatment_types: list[str] = [
        "NAD+ IV Therapy",
        "Hyperbaric Oxygen (HBOT)",
        "Stem Cell Therapy",
        "Peptide Therapy",
        "Ozone Therapy",
        "Biomarker Assessment",
        "Consultation",
        "Follow-up",
        "Lab Work",
        "Other"
    ]
    
    # Available providers
    providers: list[str] = [
        "Dr. Johnson",
        "Dr. Chen",
        "Dr. Patel",
        "Dr. Williams"
    ]
    
    @rx.var
    def today_str(self) -> str:
        """Today's date as ISO string."""
        return date.today().isoformat()
    
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
            apt for apt in self.appointments
            if apt.get("date") == self.selected_date
        ]
    
    @rx.var
    def upcoming_appointments(self) -> list[dict]:
        """Get all future appointments sorted by date and time."""
        today = date.today().isoformat()
        upcoming = [
            apt for apt in self.appointments
            if apt.get("date", "") >= today and apt.get("status") != "cancelled"
        ]
        return sorted(upcoming, key=lambda x: (x.get("date", ""), x.get("time", "")))
    
    @rx.var
    def available_time_slots(self) -> list[dict]:
        """Get available time slots for the selected date."""
        base_slots = [
            "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
            "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
            "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
            "17:00"
        ]
        
        booked_times = {
            apt.get("time") for apt in self.appointments_for_selected_date
            if apt.get("status") != "cancelled"
        }
        
        return [
            {"time": slot, "is_available": slot not in booked_times}
            for slot in base_slots
        ]
    
    @rx.var
    def dates_with_appointments(self) -> list[str]:
        """Get list of dates that have appointments."""
        return list(set(
            apt.get("date", "") for apt in self.appointments
            if apt.get("status") != "cancelled"
        ))
    
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
    
    def handle_details_modal_open_change(self, is_open: bool):
        """Handle details modal open state change."""
        self.show_details_modal = is_open
        if not is_open:
            self.selected_appointment = {}
    
    def set_view_mode(self, mode: str):
        """Switch between calendar and list view."""
        self.view_mode = mode
    
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
            "notes": self.new_appointment_notes
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
            "cancelled": "bg-rose-100 text-rose-600"
        }
        return colors.get(status, "bg-gray-100 text-gray-600")
