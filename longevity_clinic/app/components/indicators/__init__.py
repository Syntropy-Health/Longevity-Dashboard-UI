"""Indicator components for visual status display.

This package contains reusable indicator components:
- severity_bar: Progress-style severity indicator (0-10 scale)
- severity_badge: Compact badge-style severity indicator
- severity_comparison: Side-by-side current vs previous comparison
- trend_badge: Improving/stable/worsening badge with icon
- trend_text: Compact inline trend display
"""

from .severity import severity_badge, severity_bar, severity_comparison
from .trend import trend_badge, trend_text

__all__ = [
    "severity_badge",
    "severity_bar",
    "severity_comparison",
    "trend_badge",
    "trend_text",
]
