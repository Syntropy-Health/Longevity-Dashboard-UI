"""Patient analytics page module.

This module provides the biomarker analytics interface with:
- Biomarker metric cards with trend charts
- Category sections for organizing metrics
- Status badges and indicators
"""

from .page import analytics_page
from .components import (
    trend_chart,
    status_badge,
    status_dot,
    metric_card,
    category_section,
)

__all__ = [
    "analytics_page",
    # Components
    "trend_chart",
    "status_badge",
    "status_dot",
    "metric_card",
    "category_section",
]
