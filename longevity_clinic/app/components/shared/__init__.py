"""Shared components package.

This package contains reusable UI components used across both patient and admin views.
"""

from .ui_components import (
    search_input,
    patient_select_item,
    stat_metric_card,
    loading_spinner,
    empty_state,
)
from .health_metrics import (
    nutrition_summary_cards,
    medications_list,
    conditions_list,
    symptoms_list,
    food_entries_list,
    health_metrics_dashboard,
)
from .checkin_components import (
    status_badge,
    type_icon,
    topics_list,
    checkin_card,
    patient_checkin_card,
    admin_checkin_card,
    status_filter_button,
    stat_card,
)

__all__ = [
    # UI Components
    "search_input",
    "patient_select_item",
    "stat_metric_card",
    "loading_spinner",
    "empty_state",
    # Health Metrics
    "nutrition_summary_cards",
    "medications_list",
    "conditions_list",
    "symptoms_list",
    "food_entries_list",
    "health_metrics_dashboard",
    # Check-in Components
    "status_badge",
    "type_icon",
    "topics_list",
    "checkin_card",
    "patient_checkin_card",
    "admin_checkin_card",
    "status_filter_button",
    "stat_card",
]
