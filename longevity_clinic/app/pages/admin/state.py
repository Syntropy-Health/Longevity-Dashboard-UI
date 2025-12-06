"""Admin dashboard state management."""

import reflex as rx


class AdminDashboardState(rx.State):
    """State for admin dashboard tab management."""

    active_tab: str = "overview"

    def set_tab(self, tab: str):
        """Set the active tab."""
        self.active_tab = tab
