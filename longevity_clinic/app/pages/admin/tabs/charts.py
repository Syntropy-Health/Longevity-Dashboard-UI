"""Admin dashboard charts for clinic metrics.

Charts in this module are specific to the admin dashboard and
visualize clinic-wide metrics loaded from the database.
"""

import reflex as rx

from ....states.admin_metrics_state import AdminMetricsState


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


def overview_trend_chart() -> rx.Component:
    """Patient growth trend chart showing active and new patients by month."""
    return rx.recharts.area_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-20 stroke-slate-600"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.area(
            data_key="active",
            name="Active Patients",
            stroke="#2DD4BF",
            fill="rgba(45, 212, 191, 0.2)",
            type_="monotone",
            stroke_width=2,
        ),
        rx.recharts.area(
            data_key="new",
            name="New Patients",
            stroke="#38BDF8",
            fill="rgba(56, 189, 248, 0.2)",
            type_="monotone",
            stroke_width=2,
        ),
        rx.recharts.x_axis(
            data_key="name",
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
            dy=10,
        ),
        rx.recharts.y_axis(
            axis_line=False, tick_line=False, tick={"fill": "#94A3B8", "fontSize": 12}
        ),
        data=AdminMetricsState.trend_data,
        height=250,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )


def treatment_distribution_chart() -> rx.Component:
    """Bar chart showing treatment protocol distribution."""
    return rx.recharts.bar_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-20 stroke-slate-600"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.legend(
            vertical_align="top",
            height=36,
            icon_type="circle",
            wrapper_style={"paddingBottom": "10px"},
        ),
        rx.recharts.bar(
            data_key="count",
            name="Active Protocols",
            fill="#2DD4BF",
            radius=[4, 4, 0, 0],
            bar_size=32,
        ),
        rx.recharts.x_axis(
            data_key="name",
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
            dy=10,
        ),
        rx.recharts.y_axis(
            axis_line=False, tick_line=False, tick={"fill": "#94A3B8", "fontSize": 12}
        ),
        data=AdminMetricsState.treatment_data,
        height=250,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )


def biomarker_improvement_chart() -> rx.Component:
    """Line chart showing average biomarker score improvements over time."""
    return rx.recharts.line_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-20 stroke-slate-600"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.line(
            data_key="score",
            name="Avg Biomarker Score",
            stroke="#A78BFA",
            stroke_width=3,
            dot={"r": 4, "fill": "#A78BFA", "strokeWidth": 2, "stroke": "#1E293B"},
            active_dot={"r": 6, "fill": "#A78BFA", "strokeWidth": 0},
            type_="monotone",
        ),
        rx.recharts.x_axis(
            data_key="name",
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
            dy=10,
        ),
        rx.recharts.y_axis(
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
            domain=[0, 100],
        ),
        data=AdminMetricsState.biomarker_data,
        height=250,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )


def daily_patient_flow_chart() -> rx.Component:
    """Interactive bar chart showing daily patient flow by hour."""
    return rx.recharts.bar_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-20 stroke-slate-600"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.legend(
            vertical_align="top",
            height=36,
            icon_type="circle",
            wrapper_style={"paddingBottom": "10px"},
        ),
        rx.recharts.bar(
            data_key="appointments",
            name="Scheduled",
            fill="#2DD4BF",
            radius=[4, 4, 0, 0],
            bar_size=20,
            stack_id="patients",
        ),
        rx.recharts.bar(
            data_key="walkins",
            name="Walk-ins",
            fill="#38BDF8",
            radius=[4, 4, 0, 0],
            bar_size=20,
            stack_id="patients",
        ),
        rx.recharts.x_axis(
            data_key="time",
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 11},
            dy=10,
        ),
        rx.recharts.y_axis(
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
        ),
        data=AdminMetricsState.daily_flow_data,
        height=280,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )


def room_utilization_chart() -> rx.Component:
    """Interactive bar chart showing treatment room utilization."""
    return rx.recharts.bar_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-20 stroke-slate-600"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.legend(
            vertical_align="top",
            height=36,
            icon_type="circle",
            wrapper_style={"paddingBottom": "10px"},
        ),
        rx.recharts.bar(
            data_key="occupancy",
            name="Occupancy %",
            fill="#A78BFA",
            radius=[4, 4, 0, 0],
            bar_size=28,
        ),
        rx.recharts.x_axis(
            data_key="room",
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 11},
            dy=10,
        ),
        rx.recharts.y_axis(
            axis_line=False,
            tick_line=False,
            tick={"fill": "#94A3B8", "fontSize": 12},
            domain=[0, 100],
        ),
        data=AdminMetricsState.room_utilization_data,
        height=280,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )
