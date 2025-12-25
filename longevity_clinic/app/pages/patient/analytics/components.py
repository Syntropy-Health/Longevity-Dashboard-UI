"""Patient analytics reusable components.

Re-exports biomarker components from shared module for backward compatibility.
All components are now defined in components/shared/biomarker_components.py
"""

# Re-export all biomarker components from shared module
from ....components.shared.biomarker import (
    biomarker_status_badge as status_badge,  # Alias for backward compatibility
    category_section,
    collapsible_category_section,
    collapsible_panels_container,
    metric_card,
    status_dot,
    trend_chart,
)

__all__ = [
    "category_section",
    "collapsible_category_section",
    "collapsible_panels_container",
    "metric_card",
    "status_badge",
    "status_dot",
    "trend_chart",
]
