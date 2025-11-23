import reflex as rx
from ..components.layout import authenticated_layout
from ..states.patient_analytics_state import (
    PatientAnalyticsState,
    BiomarkerCategory,
    BiomarkerMetric,
)
from ..components.charts import TOOLTIP_PROPS
from ..config import current_config


def trend_chart(data: list[dict], color: str) -> rx.Component:
    return rx.recharts.area_chart(
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.area(
            data_key="value",
            stroke=color,
            fill=color,
            type_="monotone",
            stroke_width=2,
            fill_opacity=0.1,
        ),
        rx.recharts.x_axis(data_key="date", hide=True),
        rx.recharts.y_axis(hide=True, domain=["auto", "auto"]),
        data=data,
        height=70,
        width="100%",
        margin={"top": 5, "right": 0, "bottom": 0, "left": 0},
    )


def metric_card(metric: BiomarkerMetric) -> rx.Component:
    color = rx.match(
        metric["status"],
        ("Optimal", "#10B981"),
        ("Warning", "#F59E0B"),
        ("Critical", "#EF4444"),
        "#6B7280",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    metric["name"],
                    class_name="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-3",
                ),
                rx.el.div(
                    rx.el.span(
                        metric["value"],
                        class_name="text-4xl font-light text-gray-800 mr-1 tracking-tighter",
                    ),
                    rx.el.span(
                        metric["unit"],
                        class_name="text-[10px] text-gray-400 font-semibold uppercase",
                    ),
                    class_name="flex items-baseline mb-1",
                ),
            ),
            rx.el.span(
                metric["status"],
                class_name=rx.match(
                    metric["status"],
                    (
                        "Optimal",
                        "px-3 py-1 rounded-full bg-emerald-50/60 text-emerald-700 text-[10px] font-bold border border-emerald-100/60 backdrop-blur-md shadow-sm",
                    ),
                    (
                        "Warning",
                        "px-3 py-1 rounded-full bg-amber-50/60 text-amber-700 text-[10px] font-bold border border-amber-100/60 backdrop-blur-md shadow-sm",
                    ),
                    (
                        "Critical",
                        "px-3 py-1 rounded-full bg-red-50/60 text-red-700 text-[10px] font-bold border border-red-100/60 backdrop-blur-md shadow-sm",
                    ),
                    "px-3 py-1 rounded-full bg-gray-50/60 text-gray-700 text-[10px] font-bold border border-gray-100/60 backdrop-blur-md shadow-sm",
                ),
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            trend_chart(metric["history"], color),
            class_name="h-20 w-full mb-4 opacity-70 hover:opacity-100 transition-all duration-500 -ml-2",
        ),
        rx.el.div(
            rx.el.div(
                class_name=rx.match(
                    metric["status"],
                    (
                        "Optimal",
                        "h-1.5 w-1.5 rounded-full bg-emerald-500 mr-2 shadow-[0_0_8px_rgba(16,185,129,0.4)]",
                    ),
                    (
                        "Warning",
                        "h-1.5 w-1.5 rounded-full bg-amber-500 mr-2 shadow-[0_0_8px_rgba(245,158,11,0.4)]",
                    ),
                    (
                        "Critical",
                        "h-1.5 w-1.5 rounded-full bg-red-500 mr-2 shadow-[0_0_8px_rgba(239,68,68,0.4)]",
                    ),
                    "h-1.5 w-1.5 rounded-full bg-gray-500 mr-2",
                )
            ),
            rx.el.span(
                "OPTIMAL RANGE",
                class_name="text-[9px] text-gray-400 mr-2 uppercase tracking-widest font-bold",
            ),
            rx.el.span(
                metric["reference_range"],
                class_name="text-xs font-semibold text-gray-700",
            ),
            class_name="flex items-center bg-white/30 rounded-full px-3 py-1.5 w-fit border border-white/40 backdrop-blur-sm",
        ),
        class_name=f"{current_config.glass_panel_style} p-6 {current_config.glass_card_hover}",
    )


def category_section(category: BiomarkerCategory) -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            category["category"],
            class_name="text-lg font-medium text-gray-800 mb-5 ml-1 flex items-center gap-2",
        ),
        rx.el.div(
            rx.foreach(category["metrics"], metric_card),
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
        ),
        class_name="mb-12",
    )


def analytics_page() -> rx.Component:
    return authenticated_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Biomarker Analytics",
                        class_name="text-4xl font-thin text-gray-900 tracking-tight",
                    ),
                    rx.el.p(
                        "Comprehensive health intelligence report",
                        class_name="text-gray-500 mt-2 font-light text-lg",
                    ),
                ),
                rx.el.button(
                    rx.icon("download", class_name="w-4 h-4 mr-2"),
                    "Export Report",
                    on_click=PatientAnalyticsState.export_report,
                    class_name=f"{current_config.glass_button_secondary} px-6 py-3 rounded-2xl text-sm font-semibold",
                ),
                class_name="flex flex-col sm:flex-row justify-between items-start sm:items-end mb-16 gap-4",
            ),
            rx.foreach(PatientAnalyticsState.biomarker_panels, category_section),
            class_name="max-w-7xl mx-auto pb-20",
        )
    )