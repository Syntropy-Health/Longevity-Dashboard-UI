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
    health_metrics_dashboard,
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
    "health_metrics_dashboard",
]
