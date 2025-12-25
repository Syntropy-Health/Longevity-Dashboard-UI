"""Shared components package.

This package contains reusable UI components used across both patient and admin views.
"""

from .biomarker import (
    biomarker_status_badge,
    category_section,
    collapsible_category_section,
    collapsible_panels_container,
    metric_card,
    status_dot,
    trend_chart,
)
from .checkin import (
    admin_checkin_card,
    checkin_card,
    pagination_controls,
    patient_checkin_card,
    stat_card,
    status_badge,
    status_filter_button,
    topics_list,
    type_icon,
)
from .health_metrics import (
    health_metrics_dashboard,
    nutrition_summary_cards,
)
from .tables import (
    TABLE_DATA_CELL,
    TABLE_HEADER_CELL,
    TABLE_ROW_HOVER,
    avatar_circle,
    empty_table_state,
    filter_select,
    health_score_bar,
    search_input_box,
    status_badge as table_status_badge,
    table_header,
    table_loading_skeleton,
)
from .treatment import (
    CATEGORY_COLORS,
    category_badge,
    protocol_filters,
    treatment_card,
    treatment_meta_item,
)
from .ui_components import (
    chart_card,
    dashboard_stat_card,
    efficiency_stat_card,
    empty_state,
    loading_spinner,
    patient_select_item,
    search_input,
    sidebar_item_with_tag,
    stat_metric_card,
    static_metric_card,
)

__all__ = [
    # Treatment Components
    "CATEGORY_COLORS",
    "TABLE_DATA_CELL",
    # Table Components
    "TABLE_HEADER_CELL",
    "TABLE_ROW_HOVER",
    "admin_checkin_card",
    "avatar_circle",
    "biomarker_status_badge",
    "category_badge",
    "category_section",
    "chart_card",
    "checkin_card",
    "collapsible_category_section",
    "collapsible_panels_container",
    "dashboard_stat_card",
    "efficiency_stat_card",
    "empty_state",
    "empty_table_state",
    "filter_select",
    "health_metrics_dashboard",
    "health_score_bar",
    "loading_spinner",
    "metric_card",
    # Health Metrics
    "nutrition_summary_cards",
    "pagination_controls",
    "patient_checkin_card",
    "patient_select_item",
    "protocol_filters",
    # UI Components
    "search_input",
    "search_input_box",
    "sidebar_item_with_tag",
    "stat_card",
    "stat_metric_card",
    "static_metric_card",
    # Check-in Components
    "status_badge",
    "status_dot",
    "status_filter_button",
    "table_header",
    "table_loading_skeleton",
    "table_status_badge",
    "topics_list",
    "treatment_card",
    "treatment_meta_item",
    # Biomarker Components
    "trend_chart",
    "type_icon",
]
