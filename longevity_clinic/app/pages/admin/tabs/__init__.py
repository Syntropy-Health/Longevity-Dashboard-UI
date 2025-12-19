"""Admin dashboard tabs submodule.

Organizes admin dashboard content into separate tab components with
their own charts and data loading.
"""

from .overview import overview_tab
from .efficiency import efficiency_tab
from .patient_health import patient_health_tab

__all__ = [
    "overview_tab",
    "efficiency_tab",
    "patient_health_tab",
]
