"""Biomarker analytics components for patient and admin views.

This module provides reusable UI components for displaying biomarker data:
- trend_chart: Mini area chart for biomarker trends
- biomarker_status_badge: Status indicator (Optimal/Warning/Critical)
- status_dot: Small status indicator dot
- metric_card: Biomarker metric card with trend chart
- category_section: Non-collapsible category section
- collapsible_category_section: Accordion-style collapsible section
- collapsible_panels_container: Container for multiple collapsible panels

Usage:
    from longevity_clinic.app.components.shared import (
        metric_card,
        collapsible_panels_container,
    )

    # Display collapsible biomarker panels
    collapsible_panels_container(BiomarkerState.biomarker_panels)
"""

import reflex as rx

from ...data import BiomarkerCategory, BiomarkerMetric
from ...styles.constants import GlassStyles
from ..charts import TOOLTIP_PROPS
from ..collapsible import collapsible_grid, collapsible_section

# =============================================================================
# Chart Components
# =============================================================================


def trend_chart(data: list[dict], color: str) -> rx.Component:
    """Mini area chart for biomarker trends.

    Args:
        data: List of dicts with 'date' and 'value' keys
        color: Hex color for the chart line/fill

    Returns:
        Area chart component
    """
    return rx.recharts.area_chart(
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.area(
            data_key="value",
            stroke=color,
            fill=color,
            type_="monotone",
            stroke_width=2,
            fill_opacity=0.2,
        ),
        rx.recharts.x_axis(data_key="date", hide=True),
        rx.recharts.y_axis(hide=True, domain=["auto", "auto"]),
        data=data,
        height=70,
        width="100%",
        margin={"top": 5, "right": 0, "bottom": 0, "left": 0},
    )


# =============================================================================
# Status Indicators
# =============================================================================


def biomarker_status_badge(status: str) -> rx.Component:
    """Render a biomarker status badge with appropriate styling.

    Args:
        status: One of 'Optimal', 'Warning', 'Critical'

    Returns:
        Styled status badge component
    """
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            ("Optimal", GlassStyles.STATUS_OPTIMAL),
            ("Warning", GlassStyles.STATUS_WARNING),
            ("Critical", GlassStyles.STATUS_CRITICAL),
            GlassStyles.STATUS_DEFAULT,
        ),
    )


def status_dot(status: str) -> rx.Component:
    """Render a small status indicator dot.

    Args:
        status: One of 'Optimal', 'Warning', 'Critical'

    Returns:
        Small colored dot component
    """
    return rx.el.div(
        class_name=rx.match(
            status,
            ("Optimal", GlassStyles.DOT_OPTIMAL),
            ("Warning", GlassStyles.DOT_WARNING),
            ("Critical", GlassStyles.DOT_CRITICAL),
            GlassStyles.DOT_DEFAULT,
        )
    )


# =============================================================================
# Metric Cards
# =============================================================================


def metric_card(metric: BiomarkerMetric) -> rx.Component:
    """Render a biomarker metric card with trend chart.

    Args:
        metric: BiomarkerMetric dict with name, value, unit, status,
                reference_range, and history

    Returns:
        Styled card with value, status, chart, and reference range
    """
    # Emerald for optimal to match app theme
    color = rx.match(
        metric["status"],
        ("Optimal", "#34D399"),  # emerald-400
        ("Warning", "#FBBF24"),  # amber-400
        ("Critical", "#F87171"),  # red-400
        "#94A3B8",  # slate-400
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    metric["name"],
                    class_name=f"{GlassStyles.METRIC_LABEL} mb-3",
                ),
                rx.el.div(
                    rx.el.span(
                        metric["value"],
                        class_name=f"{GlassStyles.METRIC_VALUE} mr-1",
                    ),
                    rx.el.span(
                        metric["unit"],
                        class_name=GlassStyles.METRIC_UNIT,
                    ),
                    class_name="flex items-baseline mb-1",
                ),
            ),
            biomarker_status_badge(metric["status"]),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            trend_chart(metric["history"], color),
            class_name="h-20 w-full mb-4 opacity-70 hover:opacity-100 transition-all duration-500 -ml-2",
        ),
        rx.el.div(
            status_dot(metric["status"]),
            rx.el.span(
                "OPTIMAL RANGE",
                class_name=GlassStyles.REFERENCE_LABEL,
            ),
            rx.el.span(
                metric["reference_range"],
                class_name=GlassStyles.REFERENCE_VALUE,
            ),
            class_name=GlassStyles.REFERENCE_RANGE_PILL,
        ),
        class_name=GlassStyles.BIOMARKER_CARD,
    )


# =============================================================================
# Category Sections
# =============================================================================


def category_section(category: BiomarkerCategory) -> rx.Component:
    """Render a category section with its biomarker metrics (non-collapsible).

    Args:
        category: BiomarkerCategory dict with 'category' name and 'metrics' list

    Returns:
        Section with title and grid of metric cards
    """
    return rx.el.div(
        rx.el.h3(
            category["category"],
            class_name=GlassStyles.SECTION_TITLE,
        ),
        rx.el.div(
            rx.foreach(category["metrics"], metric_card),
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
        ),
        class_name="mb-12",
    )


def collapsible_category_section(category: BiomarkerCategory) -> rx.Component:
    """Render a collapsible category section with biomarker metrics and charts.

    Uses the generic collapsible_section component with biomarker-specific rendering.

    Args:
        category: BiomarkerCategory dict with 'category' name and 'metrics' list

    Returns:
        Accordion item with expandable metric cards
    """

    return collapsible_section(
        title=category["category"],
        value=category["category"],
        icon="activity",
        icon_color="text-teal-500",
        badge_count=category["metrics"].length(),
        content=collapsible_grid(
            items=category["metrics"],
            render_item=metric_card,
            columns="grid-cols-1 md:grid-cols-2 xl:grid-cols-3",
        ),
    )


def collapsible_panels_container(
    panels: list[BiomarkerCategory],
    default_expanded: list[str] | rx.Var | None = None,
) -> rx.Component:
    """Container for collapsible biomarker panels.

    Args:
        panels: List of biomarker category panels to display
        default_expanded: List of category names to expand by default.
                         Pass a state var like BiomarkerState.all_panel_names
                         to expand all panels by default.

    Returns:
        Accordion root with all panels
    """
    from ..collapsible import collapsible_container

    return collapsible_container(
        children=[rx.foreach(panels, collapsible_category_section)],
        default_expanded=default_expanded,
    )
