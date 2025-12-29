"""Biomarker card and panel components for patient portal.

This module contains reusable biomarker components:
- status_badge: Status indicator (Optimal/Warning/Critical)
- trend_indicator: Trend arrow with label
- biomarker_card: Compact biomarker metric card
- biomarker_detail_panel: Expanded detail panel with chart

Usage:
    from longevity_clinic.app.components.tabs.biomarkers import (
        biomarker_card,
        biomarker_detail_panel,
    )
"""

import reflex as rx

from ...styles.constants import GlassStyles
from ..charts import biomarker_history_chart


def status_badge(status: str) -> rx.Component:
    """Status badge with dark theme styling.

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


def trend_indicator(trend: str) -> rx.Component:
    """Trend indicator with icon and label.

    Args:
        trend: One of 'up', 'down', 'stable'

    Returns:
        Trend indicator component
    """
    return rx.match(
        trend,
        (
            "up",
            rx.el.div(
                rx.icon("trending-up", class_name=GlassStyles.BIOMARKER_TREND_ICON_UP),
                rx.el.span(
                    "Increasing", class_name=GlassStyles.BIOMARKER_TREND_TEXT_UP
                ),
                class_name="flex items-center",
            ),
        ),
        (
            "down",
            rx.el.div(
                rx.icon(
                    "trending-down", class_name=GlassStyles.BIOMARKER_TREND_ICON_DOWN
                ),
                rx.el.span(
                    "Decreasing", class_name=GlassStyles.BIOMARKER_TREND_TEXT_DOWN
                ),
                class_name="flex items-center",
            ),
        ),
        (
            "stable",
            rx.el.div(
                rx.icon("minus", class_name=GlassStyles.BIOMARKER_TREND_ICON_STABLE),
                rx.el.span(
                    "Stable", class_name=GlassStyles.BIOMARKER_TREND_TEXT_STABLE
                ),
                class_name="flex items-center",
            ),
        ),
        rx.el.div(),
    )


def biomarker_card(
    biomarker: dict,
    on_click: rx.EventHandler | None = None,
    is_selected: bool | rx.Var = False,
) -> rx.Component:
    """Biomarker card with dark theme styling.

    Args:
        biomarker: Biomarker dict with name, category, current_value, unit, status, trend
        on_click: Optional click handler
        is_selected: Whether the card is currently selected

    Returns:
        Styled biomarker card component
    """
    card_class = rx.cond(
        is_selected,
        f"{GlassStyles.BIOMARKER_CARD} {GlassStyles.BIOMARKER_CARD_SELECTED}",
        f"{GlassStyles.BIOMARKER_CARD} cursor-pointer",
    )

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    biomarker["name"],
                    class_name=GlassStyles.BIOMARKER_CARD_TITLE,
                ),
                rx.el.p(
                    biomarker["category"],
                    class_name=GlassStyles.BIOMARKER_CARD_CATEGORY,
                ),
            ),
            status_badge(biomarker["status"]),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.span(
                biomarker["current_value"],
                class_name=GlassStyles.BIOMARKER_CARD_VALUE,
            ),
            rx.el.span(
                f" {biomarker['unit']}",
                class_name=GlassStyles.BIOMARKER_CARD_UNIT,
            ),
            class_name="flex items-baseline mb-3",
        ),
        trend_indicator(biomarker["trend"]),
        on_click=on_click,
        class_name=card_class,
    )


def biomarker_detail_panel(
    biomarker: dict | rx.Var,
    on_close: rx.EventHandler,
    show: bool | rx.Var = True,
) -> rx.Component:
    """Expanded detail panel for a selected biomarker.

    Args:
        biomarker: Biomarker dict or Var with full details
        on_close: Handler for close button
        show: Whether to show the panel

    Returns:
        Detail panel component with chart and analysis
    """
    return rx.cond(
        show,
        rx.el.div(
            # Header
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        biomarker["name"],
                        class_name=GlassStyles.BIOMARKER_DETAIL_TITLE,
                    ),
                    rx.el.p(
                        biomarker["description"],
                        class_name=GlassStyles.BIOMARKER_DETAIL_DESCRIPTION,
                    ),
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-5 h-5"),
                    on_click=on_close,
                    class_name=GlassStyles.BIOMARKER_DETAIL_CLOSE_BTN,
                ),
                class_name="flex justify-between items-start mb-6",
            ),
            # Content: Chart + Analysis
            rx.el.div(
                # Chart section
                rx.el.div(
                    rx.el.h4(
                        "Historical Trend",
                        class_name=GlassStyles.BIOMARKER_DETAIL_SECTION_TITLE,
                    ),
                    biomarker_history_chart(),
                    class_name="flex-1 min-h-[300px]",
                ),
                # Analysis section
                rx.el.div(
                    rx.el.h4(
                        "Analysis",
                        class_name=GlassStyles.BIOMARKER_DETAIL_SECTION_TITLE,
                    ),
                    rx.el.div(
                        # Current Status
                        rx.el.div(
                            rx.el.p(
                                "Current Status",
                                class_name=GlassStyles.BIOMARKER_DETAIL_LABEL,
                            ),
                            rx.el.p(
                                biomarker["status"],
                                class_name=rx.match(
                                    biomarker["status"],
                                    (
                                        "Optimal",
                                        GlassStyles.BIOMARKER_STATUS_OPTIMAL_TEXT,
                                    ),
                                    (
                                        "Warning",
                                        GlassStyles.BIOMARKER_STATUS_WARNING_TEXT,
                                    ),
                                    (
                                        "Critical",
                                        GlassStyles.BIOMARKER_STATUS_CRITICAL_TEXT,
                                    ),
                                    GlassStyles.BIOMARKER_STATUS_DEFAULT_TEXT,
                                ),
                            ),
                            class_name="mb-3",
                        ),
                        # Optimal Range
                        rx.el.div(
                            rx.el.p(
                                "Optimal Range",
                                class_name=GlassStyles.BIOMARKER_DETAIL_LABEL,
                            ),
                            rx.el.p(
                                f"{biomarker['optimal_min']} - {biomarker['optimal_max']} {biomarker['unit']}",
                                class_name=GlassStyles.BIOMARKER_DETAIL_VALUE,
                            ),
                            class_name="mb-3",
                        ),
                        # Latest Reading
                        rx.el.div(
                            rx.el.p(
                                "Latest Reading",
                                class_name=GlassStyles.BIOMARKER_DETAIL_LABEL,
                            ),
                            rx.el.p(
                                f"{biomarker['current_value']} {biomarker['unit']}",
                                class_name=GlassStyles.BIOMARKER_DETAIL_VALUE,
                            ),
                        ),
                        class_name=GlassStyles.BIOMARKER_DETAIL_ANALYSIS_BOX,
                    ),
                    class_name="w-full lg:w-64 shrink-0 lg:ml-6 mt-6 lg:mt-0",
                ),
                class_name="flex flex-col lg:flex-row",
            ),
            class_name=GlassStyles.BIOMARKER_DETAIL_PANEL,
        ),
    )


__all__ = [
    "biomarker_card",
    "biomarker_detail_panel",
    "status_badge",
    "trend_indicator",
]
