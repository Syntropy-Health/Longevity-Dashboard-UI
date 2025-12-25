"""Components module - exports all reusable UI components.

Structure:
- Layout components (authenticated_layout, sidebar, header)
- Shared UI components (search_input, loading_spinner, etc.)
- Modals (transcript_modal, status_update_modal)
- Charts (biomarker charts, tooltip configs)
- Paginated views (paginated_list, paginated_list_with_filters)
- Indicators (severity_bar, trend_badge)
- Tab components (cards, items for patient portal tabs)
"""

# Layout components
# Charts - biomarker visualization
from .charts import (
    TOOLTIP_PROPS,
    biomarker_history_chart,
    generic_area_chart,
    generic_bar_chart,
    generic_line_chart,
)

# Collapsible section components
from .collapsible import (
    collapsible_container,
    collapsible_grid,
    collapsible_section,
)
from .header import header, notification_badge

# Indicator components
from .indicators import (
    severity_badge,
    severity_bar,
    trend_badge,
    trend_text,
)
from .layout import authenticated_layout

# Modals - truly reusable, state-agnostic
from .modals import checkin_detail_modal, status_update_modal, transcript_modal

# Page-level shared components
from .page import page_header, section_header

# Paginated view components
from .paginated_view import (
    empty_state_box,
    paginated_list,
    paginated_list_with_filters,
)

# Shared UI components
from .shared import (
    empty_state,
    health_metrics_dashboard,
    loading_spinner,
    nutrition_summary_cards,
    patient_select_item,
    search_input,
    stat_metric_card,
)
from .sidebar import mobile_menu, sidebar, sidebar_item

# Tab components - cards and items for patient portal
from .tabs import (
    condition_card,
    data_source_card,
    food_entry_card,
    import_drop_zone,
    medication_log_card,
    medication_subscription_card,
    reminder_item,
    symptom_card,
    symptom_log_item,
    symptom_trend_item,
)

__all__ = [
    "TOOLTIP_PROPS",
    # Layout
    "authenticated_layout",
    # Charts
    "biomarker_history_chart",
    "checkin_detail_modal",
    "collapsible_container",
    "collapsible_grid",
    # Collapsible
    "collapsible_section",
    # Tab cards
    "condition_card",
    "data_source_card",
    "empty_state",
    "empty_state_box",
    "food_entry_card",
    "generic_area_chart",
    "generic_bar_chart",
    "generic_line_chart",
    "header",
    "health_metrics_dashboard",
    "import_drop_zone",
    "loading_spinner",
    "medication_log_card",
    "medication_subscription_card",
    "mobile_menu",
    "notification_badge",
    "nutrition_summary_cards",
    # Page components
    "page_header",
    # Paginated views
    "paginated_list",
    "paginated_list_with_filters",
    "patient_select_item",
    # Tab items
    "reminder_item",
    # Shared UI
    "search_input",
    "section_header",
    "severity_badge",
    # Indicators
    "severity_bar",
    "sidebar",
    "sidebar_item",
    "stat_metric_card",
    "status_update_modal",
    "symptom_card",
    "symptom_log_item",
    "symptom_trend_item",
    # Modals
    "transcript_modal",
    "trend_badge",
    "trend_text",
]
