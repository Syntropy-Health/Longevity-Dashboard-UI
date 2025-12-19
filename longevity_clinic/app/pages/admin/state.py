"""Admin dashboard state management.

This module re-exports AdminDashboardState from the shared states module.
All admin dashboard state is now managed in:
    longevity_clinic.app.states.shared.dashboard
"""

from ...states.shared.dashboard import AdminDashboardState

__all__ = ["AdminDashboardState"]
