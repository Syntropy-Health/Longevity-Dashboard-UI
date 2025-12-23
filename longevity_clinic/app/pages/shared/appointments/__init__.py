"""Appointments page module.

This module provides the appointment scheduling interface with:
- Appointment cards and listings
- Calendar date selection
- Time slot selection
- Booking modal
- Appointment details modal
"""

from .components import (
    appointment_card,
    mini_calendar,
    status_badge,
    time_slots_grid,
)
from .modals import (
    booking_modal,
    details_modal,
)
from .page import appointments_page
from .sections import (
    appointments_for_date_section,
    calendar_sidebar,
    past_appointments_section,
    upcoming_appointments_list,
)

__all__ = [
    "appointment_card",
    "appointments_for_date_section",
    "appointments_page",
    # Modals
    "booking_modal",
    # Sections
    "calendar_sidebar",
    "details_modal",
    "mini_calendar",
    "past_appointments_section",
    # Components
    "status_badge",
    "time_slots_grid",
    "upcoming_appointments_list",
]
