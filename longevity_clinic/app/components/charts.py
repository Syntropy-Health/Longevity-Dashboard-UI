import reflex as rx
from ..states.patient_state import PatientState
from ..states.patient_biomarker_state import PatientBiomarkerState

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
    "separator": "",
}


def overview_trend_chart() -> rx.Component:
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
        data=PatientState.trend_data,
        height=250,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )


def biomarker_history_chart() -> rx.Component:
    return rx.recharts.composed_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, class_name="opacity-20 stroke-slate-600"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.reference_line(
            y=PatientBiomarkerState.selected_biomarker_optimal_range["max"],
            stroke="#2DD4BF",
            stroke_dasharray="3 3",
            label="Optimal Max",
        ),
        rx.recharts.reference_line(
            y=PatientBiomarkerState.selected_biomarker_optimal_range["min"],
            stroke="#2DD4BF",
            stroke_dasharray="3 3",
            label="Optimal Min",
        ),
        rx.recharts.area(
            data_key="value",
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
        data=PatientBiomarkerState.selected_biomarker_history,
        height=300,
        width="100%",
        margin={"top": 20, "right": 20, "left": 0, "bottom": 0},
    )


def treatment_distribution_chart() -> rx.Component:
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
        data=PatientState.treatment_data,
        height=250,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )


def biomarker_improvement_chart() -> rx.Component:
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
        data=PatientState.biomarker_data,
        height=250,
        width="100%",
        margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
    )