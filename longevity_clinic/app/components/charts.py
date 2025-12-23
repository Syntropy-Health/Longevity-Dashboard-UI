"""Reusable chart components for patient data visualization.

This module contains patient-specific charts that are used across
multiple pages (patient portal, admin patient health view).

Admin dashboard charts have been moved to:
    pages/admin/tabs/charts.py
"""

import reflex as rx

from ..states import BiomarkerState

# Shared tooltip configuration for consistent styling
TOOLTIP_PROPS = {
    "content_style": {
        "backgroundColor": "rgba(30, 41, 59, 0.95)",
        "backdropFilter": "blur(10px)",
        "borderColor": "rgba(71, 85, 105, 0.5)",
        "borderRadius": "1rem",
        "boxShadow": "0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2)",
        "fontFamily": "Open Sans, sans-serif",
        "fontSize": "0.875rem",
        "padding": "0.75rem 1rem",
        "border": "1px solid rgba(71, 85, 105, 0.5)",
    },
    "item_style": {"color": "#94A3B8", "padding": "0"},
    "label_style": {"color": "#F1F5F9", "fontWeight": "600", "marginBottom": "0.25rem"},
    "cursor": {"stroke": "#475569", "strokeWidth": 1, "strokeDasharray": "4 4"},
    "separator": ": ",
}


def biomarker_history_chart() -> rx.Component:
    """Patient biomarker history chart with optimal range indicators.

    Shows the historical trend of a selected biomarker with reference
    lines for the optimal min/max range. Used in patient portal and
    admin patient health views.
    """
    return rx.recharts.composed_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-20 stroke-slate-600"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.reference_line(
            y=BiomarkerState.selected_biomarker_optimal_range["max"],
            stroke="#2DD4BF",
            stroke_dasharray="3 3",
            label="Optimal Max",
        ),
        rx.recharts.reference_line(
            y=BiomarkerState.selected_biomarker_optimal_range["min"],
            stroke="#2DD4BF",
            stroke_dasharray="3 3",
            label="Optimal Min",
        ),
        rx.recharts.area(
            data_key="value",
            name="Reading",
            stroke="#2DD4BF",
            fill="rgba(45, 212, 191, 0.2)",
            type_="monotone",
            stroke_width=3,
        ),
        rx.recharts.x_axis(
            data_key="date",
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
            dy=10,
        ),
        rx.recharts.y_axis(
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
            domain=["auto", "auto"],
        ),
        data=BiomarkerState.selected_biomarker_history,
        height=300,
        width="100%",
        margin={"top": 20, "right": 20, "left": 0, "bottom": 0},
    )


def generic_area_chart(
    data: list[dict],
    data_key: str,
    x_key: str = "name",
    name: str = "Value",
    stroke: str = "#2DD4BF",
    fill: str = "rgba(45, 212, 191, 0.2)",
    height: int = 250,
) -> rx.Component:
    """Generic reusable area chart component.

    Args:
        data: List of data points with x_key and data_key values
        data_key: Key for the y-axis values
        x_key: Key for the x-axis labels
        name: Legend name for the data series
        stroke: Line stroke color
        fill: Area fill color
        height: Chart height in pixels
    """
    return rx.recharts.area_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-20 stroke-slate-600"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.area(
            data_key=data_key,
            name=name,
            stroke=stroke,
            fill=fill,
            type_="monotone",
            stroke_width=2,
        ),
        rx.recharts.x_axis(
            data_key=x_key,
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
            dy=10,
        ),
        rx.recharts.y_axis(
            axis_line=False, tick_line=False, tick={"fill": "#94A3B8", "fontSize": 12}
        ),
        data=data,
        height=height,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )


def generic_bar_chart(
    data: list[dict],
    data_key: str,
    x_key: str = "name",
    name: str = "Value",
    fill: str = "#2DD4BF",
    height: int = 250,
    show_legend: bool = True,
) -> rx.Component:
    """Generic reusable bar chart component.

    Args:
        data: List of data points with x_key and data_key values
        data_key: Key for the bar values
        x_key: Key for the x-axis labels
        name: Legend name for the data series
        fill: Bar fill color
        height: Chart height in pixels
        show_legend: Whether to show the chart legend
    """
    legend = (
        rx.recharts.legend(
            vertical_align="top",
            height=36,
            icon_type="circle",
            wrapper_style={"paddingBottom": "10px"},
        )
        if show_legend
        else rx.fragment()
    )

    return rx.recharts.bar_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-20 stroke-slate-600"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        legend,
        rx.recharts.bar(
            data_key=data_key,
            name=name,
            fill=fill,
            radius=[4, 4, 0, 0],
            bar_size=32,
        ),
        rx.recharts.x_axis(
            data_key=x_key,
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
            dy=10,
        ),
        rx.recharts.y_axis(
            axis_line=False, tick_line=False, tick={"fill": "#94A3B8", "fontSize": 12}
        ),
        data=data,
        height=height,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )


def generic_line_chart(
    data: list[dict],
    data_key: str,
    x_key: str = "name",
    name: str = "Value",
    stroke: str = "#A78BFA",
    height: int = 250,
    y_domain: list = None,
) -> rx.Component:
    """Generic reusable line chart component.

    Args:
        data: List of data points with x_key and data_key values
        data_key: Key for the y-axis values
        x_key: Key for the x-axis labels
        name: Legend name for the data series
        stroke: Line stroke color
        height: Chart height in pixels
        y_domain: Optional y-axis domain [min, max]
    """
    y_axis_props = {
        "axis_line": False,
        "tick_line": False,
        "tick": {"fill": "#94A3B8", "fontSize": 12},
    }
    if y_domain:
        y_axis_props["domain"] = y_domain

    return rx.recharts.line_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-20 stroke-slate-600"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.line(
            data_key=data_key,
            name=name,
            stroke=stroke,
            stroke_width=3,
            dot={"r": 4, "fill": stroke, "strokeWidth": 2, "stroke": "#1E293B"},
            active_dot={"r": 6, "fill": stroke, "strokeWidth": 0},
            type_="monotone",
        ),
        rx.recharts.x_axis(
            data_key=x_key,
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
            dy=10,
        ),
        rx.recharts.y_axis(**y_axis_props),
        data=data,
        height=height,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )
