"""Admin dashboard tabs submodule.

Organizes admin dashboard content into separate tab components with
their own charts and data loading.
"""

from .efficiency import efficiency_tab
from .overview import overview_tab
from .patient_health import patient_health_tab

__all__ = [
    "efficiency_tab",
    "overview_tab",
    "patient_health_tab",
]
