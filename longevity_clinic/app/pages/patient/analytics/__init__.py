"""Patient analytics page module.

This module provides the biomarker analytics interface with:
- Biomarker metric cards with trend charts
- Category sections for organizing metrics (collapsible)
- Status badges and indicators

Note: Components are now defined in components/shared/biomarker_components.py
and re-exported here for backward compatibility.
"""

from .components import (
    category_section,
    collapsible_category_section,
    collapsible_panels_container,
    metric_card,
    status_badge,
    status_dot,
    trend_chart,
)
from .page import analytics_page

__all__ = [
    "analytics_page",
    "category_section",
    "collapsible_category_section",
    "collapsible_panels_container",
    "metric_card",
    "status_badge",
    "status_dot",
    # Components (re-exported from shared)
    "trend_chart",
]
