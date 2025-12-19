"""Components module - exports all reusable UI components.

Structure:
- Layout components (authenticated_layout, sidebar, header)
- Shared UI components (search_input, loading_spinner, etc.)
- Modals (transcript_modal, status_update_modal)
- Charts (biomarker charts, tooltip configs)
"""

# Layout components
from .layout import authenticated_layout
from .sidebar import sidebar, mobile_menu, sidebar_item
from .header import header, notification_badge

# Page-level shared components
from .page_components import page_header, section_header

# Modals - truly reusable, state-agnostic
from .modals import transcript_modal, status_update_modal, checkin_detail_modal

# Charts - biomarker visualization
from .charts import (
    biomarker_history_chart,
    generic_area_chart,
    generic_bar_chart,
    generic_line_chart,
    TOOLTIP_PROPS,
)

# Shared UI components
from .shared import (
    search_input,
    patient_select_item,
    stat_metric_card,
    loading_spinner,
    empty_state,
    nutrition_summary_cards,
    medications_list,
    conditions_list,
    symptoms_list,
    food_entries_list,
    health_metrics_dashboard,
)

__all__ = [
    # Layout
    "authenticated_layout",
    "sidebar",
    "mobile_menu",
    "sidebar_item",
    "header",
    "notification_badge",
    # Page components
    "page_header",
    "section_header",
    # Modals
    "transcript_modal",
    "status_update_modal",
    "checkin_detail_modal",
    # Charts
    "biomarker_history_chart",
    "generic_area_chart",
    "generic_bar_chart",
    "generic_line_chart",
    "TOOLTIP_PROPS",
    # Shared UI
    "search_input",
    "patient_select_item",
    "stat_metric_card",
    "loading_spinner",
    "empty_state",
    "nutrition_summary_cards",
    "medications_list",
    "conditions_list",
    "symptoms_list",
    "food_entries_list",
    "health_metrics_dashboard",
]
