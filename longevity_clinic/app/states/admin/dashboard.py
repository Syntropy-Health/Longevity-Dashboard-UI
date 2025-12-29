"""Admin dashboard state for tab navigation.

This module provides the AdminDashboardState for admin view tab management.
"""

import reflex as rx

from ...config import get_logger

logger = get_logger("longevity_clinic.admin.dashboard")


class AdminDashboardState(rx.State):
    """State management for admin dashboard tab navigation.

    Patient data is managed by PatientState - this class only handles UI state.
    For viewing patient health data, use AdminPatientHealthState.
    """

    active_tab: str = "overview"

    def set_tab(self, tab: str):
        """Set the active dashboard tab."""
        self.active_tab = tab
        logger.debug("Admin dashboard tab set to: %s", tab)
