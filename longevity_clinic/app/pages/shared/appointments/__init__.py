"""Appointments page module.

This module provides the appointment scheduling interface with:
- Appointment cards and listings
- Calendar date selection
- Time slot selection
- Booking modal
- Appointment details modal
"""

from .page import appointments_page
from .components import (
    status_badge,
    appointment_card,
    mini_calendar,
    time_slots_grid,
)
from .modals import (
    booking_modal,
    details_modal,
)
from .sections import (
    appointments_sidebar,
    upcoming_appointments_list,
    appointments_for_date_section,
    appointments_content,
)

__all__ = [
    "appointments_page",
    # Components
    "status_badge",
    "appointment_card",
    "mini_calendar",
    "time_slots_grid",
    # Modals
    "booking_modal",
    "details_modal",
    # Sections
    "appointments_sidebar",
    "upcoming_appointments_list",
    "appointments_for_date_section",
    "appointments_content",
]
