"""Admin dashboard page module.

This module provides the admin dashboard interface with:
- Overview with key metrics and charts
- Patient management
- Clinical efficiency tracking
- Check-ins management
"""

from .page import admin_dashboard
from .state import AdminDashboardState
from .components import (
    stat_card,
    efficiency_stat_card,
    chart_card,
    patient_table_row,
    dashboard_tabs,
)
from .tabs import (
    overview_tab,
    efficiency_tab,
)
from .sections import (
    patient_management_section,
)
from .modals import (
    add_patient_modal,
    view_patient_modal,
)
from .checkins_page import admin_checkins_page

__all__ = [
    "admin_dashboard",
    "AdminDashboardState",
    # Components
    "stat_card",
    "efficiency_stat_card",
    "chart_card",
    "patient_table_row",
    "dashboard_tabs",
    # Tabs
    "overview_tab",
    "efficiency_tab",
    # Sections
    "patient_management_section",
    # Modals
    "add_patient_modal",
    "view_patient_modal",
    # Check-ins page
    "admin_checkins_page",
]
