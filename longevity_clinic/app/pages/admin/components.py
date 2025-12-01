"""Admin dashboard reusable components."""

import reflex as rx
from ...states.patient_state import PatientState, Patient
from ...styles import GlassStyles
from ...config import current_config
from .state import AdminDashboardState


def stat_card(
    title: str, value: str, trend: str, trend_up: bool, icon: str
) -> rx.Component:
    """Stats card for dashboard metrics."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-slate-400 truncate"),
                rx.el.p(
                    value,
                    class_name="mt-1 text-3xl font-bold text-white tracking-tight",
                ),
            ),
            rx.el.div(
                rx.icon(icon, class_name="w-6 h-6 text-teal-400"),
                class_name="p-3 bg-teal-500/10 rounded-2xl border border-teal-500/20",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.span(
                trend,
                class_name=rx.cond(
                    trend_up,
                    "text-teal-400 text-sm font-medium",
                    "text-red-400 text-sm font-medium",
                ),
            ),
            rx.el.span(" from last month", class_name="text-sm text-slate-500 ml-2"),
            class_name="mt-4",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} p-5",
    )


def efficiency_stat_card(
    title: str, value: str, subtitle: str, icon: str, color: str = "teal"
) -> rx.Component:
    """Stat card for clinical efficiency metrics."""
    color_classes = {
        "teal": "text-teal-400 bg-teal-500/10 border-teal-500/20",
        "blue": "text-blue-400 bg-blue-500/10 border-blue-500/20",
        "purple": "text-purple-400 bg-purple-500/10 border-purple-500/20",
        "amber": "text-amber-400 bg-amber-500/10 border-amber-500/20",
        "emerald": "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
    }
    
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-5 h-5 {color_classes.get(color, color_classes['teal']).split()[0]}"),
            class_name=f"p-2.5 rounded-xl border {color_classes.get(color, color_classes['teal'])}",
        ),
        rx.el.div(
            rx.el.p(
                value,
                class_name="text-2xl font-bold text-white mt-3",
            ),
            rx.el.p(title, class_name="text-sm font-medium text-slate-300 mt-1"),
            rx.el.p(subtitle, class_name="text-xs text-slate-500 mt-0.5"),
        ),
        class_name=f"{GlassStyles.PANEL} p-4 hover:border-teal-500/30 transition-all",
    )


def chart_card(title: str, chart: rx.Component) -> rx.Component:
    """Card wrapper for charts."""
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-bold text-white mb-6"),
        rx.el.div(chart, class_name="w-full h-64"),
        class_name=f"{GlassStyles.PANEL} p-6",
    )


def efficiency_chart_placeholder(title: str, description: str) -> rx.Component:
    """Placeholder for efficiency charts."""
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-bold text-white mb-2"),
        rx.el.p(description, class_name="text-sm text-slate-400 mb-4"),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    ["Mon", "Tue", "Wed", "Thu", "Fri"],
                    lambda day: rx.el.div(
                        rx.el.div(
                            class_name="w-full bg-gradient-to-t from-teal-500 to-teal-300 rounded-t",
                            style={"height": f"{60 + (hash(day) % 40)}%"}
                        ),
                        rx.el.span(day, class_name="text-xs text-slate-400 mt-2"),
                        class_name="flex flex-col items-center justify-end h-40 w-1/5",
                    ),
                ),
                class_name="flex items-end justify-between h-48 px-4",
            ),
            class_name="bg-slate-800/50 rounded-xl p-4",
        ),
        class_name=f"{GlassStyles.PANEL} p-6",
    )


def patient_table_row(patient: Patient) -> rx.Component:
    """Patient table row component."""
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.span("P", class_name="text-xs font-bold text-teal-300"),
                    class_name="w-8 h-8 rounded-full bg-teal-500/20 flex items-center justify-center mr-3 border border-teal-500/30",
                ),
                rx.el.div(
                    rx.el.p(
                        patient["full_name"],
                        class_name="text-sm font-medium text-white",
                    ),
                    rx.el.p(
                        patient["email"], class_name="text-xs text-slate-400 truncate"
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(patient["age"], class_name="text-sm text-slate-300"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(patient["last_visit"], class_name="text-sm text-slate-300"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                patient["status"],
                class_name=rx.cond(
                    patient["status"] == "Active",
                    "px-2 py-1 text-xs font-semibold rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    rx.cond(
                        patient["status"] == "Inactive",
                        "px-2 py-1 text-xs font-semibold rounded-full bg-slate-700/50 text-slate-400 border border-slate-600/30",
                        "px-2 py-1 text-xs font-semibold rounded-full bg-yellow-500/20 text-yellow-300 border border-yellow-500/30",
                    ),
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    class_name="h-2 rounded-full bg-teal-500",
                    style={"width": f"{patient['biomarker_score']}%%"},
                ),
                class_name="w-20 h-2 bg-slate-700 rounded-full",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                "View",
                on_click=lambda: PatientState.open_view_patient(patient),
                class_name="text-teal-400 hover:text-teal-300 text-sm font-medium",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="border-b border-slate-700/30 hover:bg-slate-800/30 transition-colors",
    )


def dashboard_tabs() -> rx.Component:
    """Dashboard tab navigation."""
    return rx.el.div(
        rx.el.button(
            rx.icon("layout-dashboard", class_name="w-4 h-4 mr-2"),
            "Overview",
            on_click=lambda: AdminDashboardState.set_tab("overview"),
            class_name=rx.cond(
                AdminDashboardState.active_tab == "overview",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center bg-teal-500/20 text-teal-300 border border-teal-500/30",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center text-slate-400 hover:bg-slate-800/50 hover:text-white border border-transparent"
            ),
        ),
        rx.el.button(
            rx.icon("users", class_name="w-4 h-4 mr-2"),
            "Patients",
            on_click=lambda: AdminDashboardState.set_tab("patients"),
            class_name=rx.cond(
                AdminDashboardState.active_tab == "patients",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center bg-teal-500/20 text-teal-300 border border-teal-500/30",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center text-slate-400 hover:bg-slate-800/50 hover:text-white border border-transparent"
            ),
        ),
        rx.el.button(
            rx.icon("gauge", class_name="w-4 h-4 mr-2"),
            "Clinical Efficiency",
            on_click=lambda: AdminDashboardState.set_tab("efficiency"),
            class_name=rx.cond(
                AdminDashboardState.active_tab == "efficiency",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center bg-teal-500/20 text-teal-300 border border-teal-500/30",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center text-slate-400 hover:bg-slate-800/50 hover:text-white border border-transparent"
            ),
        ),
        class_name="flex gap-2 p-1.5 bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-slate-700/50 mb-6",
    )
