"""Admin-specific state modules.

Contains state classes used only by admin views.
"""

from .dashboard import AdminDashboardState
from .patient_health import AdminPatientHealthState

__all__ = ["AdminDashboardState", "AdminPatientHealthState"]
