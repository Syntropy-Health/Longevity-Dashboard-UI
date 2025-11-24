import reflex as rx
from app.components.navbar import navbar
from app.components.analytics_charts import (
    patient_biomarker_chart,
    patient_inflammation_chart,
)
from app.states.analytics_state import AnalyticsState
from app.styles.glass_styles import GlassStyles


def biomarker_summary_card(name: str, value: str, status: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(name, class_name="text-sm text-slate-400 font-medium"),
            rx.el.span(
                status,
                class_name="text-[10px] uppercase tracking-wider font-bold text-teal-400",
            ),
            class_name="flex justify-between items-start mb-2",
        ),
        rx.el.h3(value, class_name="text-2xl font-bold text-white"),
        class_name=f"{GlassStyles.PANEL} p-4",
    )


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.cond(
            status == "Optimal",
            "px-2 py-1 rounded-full text-[10px] font-bold bg-teal-500/10 text-teal-400 border border-teal-500/20 uppercase tracking-wide",
            rx.cond(
                status == "Warning",
                "px-2 py-1 rounded-full text-[10px] font-bold bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 uppercase tracking-wide",
                "px-2 py-1 rounded-full text-[10px] font-bold bg-red-500/10 text-red-400 border border-red-500/20 uppercase tracking-wide",
            ),
        ),
    )


def trend_indicator(trend: str) -> rx.Component:
    return rx.cond(
        trend == "up",
        rx.icon("arrow-up", class_name="w-4 h-4 text-teal-400"),
        rx.cond(
            trend == "down",
            rx.icon("arrow-down", class_name="w-4 h-4 text-teal-400"),
            rx.icon("minus", class_name="w-4 h-4 text-slate-500"),
        ),
    )


def detailed_biomarker_card(biomarker: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4(
                biomarker["name"], class_name="font-medium text-slate-200 text-sm mb-1"
            ),
            rx.el.p(
                biomarker["description"],
                class_name="text-xs text-slate-500 line-clamp-1",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.span(
                biomarker["value"].to_string(),
                class_name="text-2xl font-bold text-white mr-1",
            ),
            rx.el.span(
                biomarker["unit"], class_name="text-xs text-slate-400 font-medium"
            ),
            class_name="flex items-baseline mb-4",
        ),
        rx.el.div(
            status_badge(biomarker["status"]),
            trend_indicator(biomarker["trend"]),
            class_name="flex justify-between items-center",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} !p-4",
    )


def category_section(category: str) -> rx.Component:
    return rx.el.details(
        rx.el.summary(
            rx.el.span(category, class_name="font-bold text-lg text-white"),
            rx.icon(
                "chevron-down",
                class_name="w-5 h-5 text-slate-400 transition-transform duration-300 group-open:rotate-180",
            ),
            class_name=f"flex items-center justify-between cursor-pointer list-none p-4 {GlassStyles.PANEL} mb-4 hover:bg-white/10 transition-colors",
        ),
        rx.el.div(
            rx.foreach(
                AnalyticsState.comprehensive_biomarkers[category],
                detailed_biomarker_card,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4 pt-0",
        ),
        class_name="group mb-2",
        open=True,
    )


def patient_analytics_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Your Biological Trends",
            class_name=f"text-3xl font-bold {GlassStyles.HEADING} mb-2",
        ),
        rx.el.p(
            "Track your optimization journey over time.",
            class_name="text-slate-400 mb-8",
        ),
        rx.el.div(
            biomarker_summary_card("Biological Age", "34.2", "OPTIMAL"),
            biomarker_summary_card("NAD+ Levels", "38.2 µM", "HIGH"),
            biomarker_summary_card("Inflammation", "0.3 mg/L", "LOW"),
            biomarker_summary_card("Sleep Score", "92/100", "EXCELLENT"),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Cellular Energy & Immune Function",
                        class_name="text-xl font-bold text-white mb-6",
                    ),
                    patient_biomarker_chart(),
                    class_name=f"{GlassStyles.PANEL} p-6",
                ),
                class_name="col-span-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Stress & Inflammation Markers",
                        class_name="text-xl font-bold text-white mb-6",
                    ),
                    patient_inflammation_chart(),
                    class_name=f"{GlassStyles.PANEL} p-6",
                ),
                class_name="col-span-1",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12",
        ),
        rx.el.div(
            rx.el.h3(
                "Comprehensive Biomarker Panel",
                class_name=f"text-2xl font-bold {GlassStyles.HEADING} mb-6",
            ),
            rx.foreach(AnalyticsState.biomarker_categories, category_section),
            class_name="mb-12",
        ),
        rx.el.div(
            rx.el.h3(
                "Optimization Insights", class_name="text-xl font-bold text-white mb-4"
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("trending-up", class_name="w-5 h-5 text-teal-400 mt-1"),
                    rx.el.div(
                        rx.el.p(
                            "NAD+ levels have increased by 45% since starting the protocol.",
                            class_name="text-slate-200 font-medium",
                        ),
                        rx.el.p(
                            "Your cellular energy production is now in the top 5% for your age group.",
                            class_name="text-slate-400 text-sm mt-1",
                        ),
                        class_name="ml-3",
                    ),
                    class_name="flex items-start",
                ),
                rx.el.div(
                    rx.icon("check_check", class_name="w-5 h-5 text-teal-400 mt-1"),
                    rx.el.div(
                        rx.el.p(
                            "Inflammation (hs-CRP) is consistently suppressed.",
                            class_name="text-slate-200 font-medium",
                        ),
                        rx.el.p(
                            "Low inflammation is a key indicator of reduced aging velocity.",
                            class_name="text-slate-400 text-sm mt-1",
                        ),
                        class_name="ml-3",
                    ),
                    class_name="flex items-start",
                ),
                class_name="space-y-4",
            ),
            class_name=f"{GlassStyles.PANEL} p-6 mt-8",
        ),
        class_name="max-w-7xl mx-auto",
    )