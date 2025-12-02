"""Patient portal page module.

This module provides the patient portal interface with:
- Dashboard overview
- Biomarker tracking
- Treatment plans
- Nutrition logging
- Health history
"""

from .page import patient_portal
from .components import patient_sidebar_tabs, dashboard_tabs

__all__ = [
    "patient_portal",
    "patient_sidebar_tabs",
    "dashboard_tabs",
]
