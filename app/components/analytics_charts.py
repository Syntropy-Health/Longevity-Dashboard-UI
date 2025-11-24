import reflex as rx
from app.states.analytics_state import AnalyticsState
from app.styles.glass_styles import GlassStyles

TOOLTIP_PROPS = {
    "content_style": {
        "backgroundColor": "rgba(15, 23, 42, 0.9)",
        "borderColor": "rgba(255, 255, 255, 0.1)",
        "borderRadius": "0.75rem",
        "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "backdropFilter": "blur(12px)",
        "color": "#e2e8f0",
        "border": "1px solid rgba(255, 255, 255, 0.1)",
    },
    "item_style": {"color": "#94a3b8", "fontSize": "0.875rem"},
    "label_style": {"color": "#f8fafc", "fontWeight": "600", "marginBottom": "0.25rem"},
    "cursor": False,
}


def custom_legend_item(color: str, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            class_name=f"w-3 h-3 rounded-full mr-2 inline-block",
            style={"backgroundColor": color},
        ),
        rx.el.span(label, class_name="text-xs text-slate-400 font-medium"),
        class_name="flex items-center mr-4",
    )


def admin_volume_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            custom_legend_item("#2dd4bf", "New Patients"),
            custom_legend_item("#818cf8", "Requests"),
            class_name="flex justify-end mb-2",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#475569", opacity=0.3
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="month",
                stroke="#94a3b8",
                tick_line=False,
                axis_line=False,
                tick={"fontSize": 12},
                dy=10,
            ),
            rx.recharts.y_axis(
                stroke="#94a3b8",
                tick_line=False,
                axis_line=False,
                tick={"fontSize": 12},
                dx=-10,
            ),
            rx.recharts.area(
                data_key="patients",
                stroke="#2dd4bf",
                fill="#2dd4bf",
                fill_opacity=0.2,
                stroke_width=2,
                type_="monotone",
            ),
            rx.recharts.area(
                data_key="requests",
                stroke="#818cf8",
                fill="#818cf8",
                fill_opacity=0.2,
                stroke_width=2,
                type_="monotone",
            ),
            data=AnalyticsState.operational_data,
            width="100%",
            height=300,
        ),
        class_name="w-full",
    )


def admin_protocol_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            custom_legend_item("#2dd4bf", "Active Protocols"),
            class_name="flex justify-end mb-2",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#475569", opacity=0.3, vertical=False
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="name",
                stroke="#94a3b8",
                tick_line=False,
                axis_line=False,
                tick={"fontSize": 11},
                dy=10,
            ),
            rx.recharts.y_axis(
                stroke="#94a3b8",
                tick_line=False,
                axis_line=False,
                tick={"fontSize": 12},
                dx=-10,
            ),
            rx.recharts.bar(
                data_key="count", fill="#2dd4bf", radius=[4, 4, 0, 0], bar_size=40
            ),
            data=AnalyticsState.protocol_usage_data,
            width="100%",
            height=300,
        ),
        class_name="w-full",
    )


def admin_biomarker_improvement_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            custom_legend_item("#2dd4bf", "Improvement %"),
            class_name="flex justify-end mb-2",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#475569", opacity=0.3, vertical=False
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="category",
                stroke="#94a3b8",
                tick_line=False,
                axis_line=False,
                tick={"fontSize": 11},
                dy=10,
            ),
            rx.recharts.y_axis(
                stroke="#94a3b8",
                tick_line=False,
                axis_line=False,
                tick={"fontSize": 12},
                dx=-10,
                unit="%",
            ),
            rx.recharts.bar(
                data_key="improvement", fill="#2dd4bf", radius=[4, 4, 0, 0], bar_size=40
            ),
            data=AnalyticsState.biomarker_improvement_data,
            width="100%",
            height=300,
        ),
        class_name="w-full",
    )


def patient_biomarker_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            custom_legend_item("#2dd4bf", "NAD+ (µM)"),
            custom_legend_item("#fbbf24", "Vitamin D (ng/mL)"),
            class_name="flex justify-end mb-2",
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#475569", opacity=0.3
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="date",
                stroke="#94a3b8",
                tick_line=False,
                axis_line=False,
                tick={"fontSize": 12},
                dy=10,
            ),
            rx.recharts.y_axis(
                stroke="#94a3b8",
                tick_line=False,
                axis_line=False,
                tick={"fontSize": 12},
                dx=-10,
            ),
            rx.recharts.line(
                data_key="NAD",
                stroke="#2dd4bf",
                stroke_width=3,
                dot={"fill": "#0f172a", "stroke": "#2dd4bf", "strokeWidth": 2, "r": 4},
                type_="monotone",
            ),
            rx.recharts.line(
                data_key="VitaminD",
                stroke="#fbbf24",
                stroke_width=3,
                dot={"fill": "#0f172a", "stroke": "#fbbf24", "strokeWidth": 2, "r": 4},
                type_="monotone",
            ),
            data=AnalyticsState.biomarker_history,
            width="100%",
            height=350,
        ),
        class_name="w-full",
    )


def patient_inflammation_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            custom_legend_item("#f87171", "hs-CRP (mg/L)"),
            custom_legend_item("#a78bfa", "Cortisol (µg/dL)"),
            class_name="flex justify-end mb-2",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#475569", opacity=0.3
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="date",
                stroke="#94a3b8",
                tick_line=False,
                axis_line=False,
                tick={"fontSize": 12},
                dy=10,
            ),
            rx.recharts.y_axis(
                stroke="#94a3b8",
                tick_line=False,
                axis_line=False,
                tick={"fontSize": 12},
                dx=-10,
            ),
            rx.recharts.area(
                data_key="Cortisol",
                stroke="#a78bfa",
                fill="#a78bfa",
                fill_opacity=0.2,
                stroke_width=2,
                type_="monotone",
            ),
            rx.recharts.area(
                data_key="hsCRP",
                stroke="#f87171",
                fill="#f87171",
                fill_opacity=0.2,
                stroke_width=2,
                type_="monotone",
            ),
            data=AnalyticsState.biomarker_history,
            width="100%",
            height=300,
        ),
        class_name="w-full",
    )