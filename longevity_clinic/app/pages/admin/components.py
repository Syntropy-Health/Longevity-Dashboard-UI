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
                rx.el.p(title, class_name="text-sm font-medium text-gray-500 truncate"),
                rx.el.p(
                    value,
                    class_name="mt-1 text-3xl font-bold text-gray-800 tracking-tight",
                ),
            ),
            rx.el.div(
                rx.icon(icon, class_name="w-6 h-6 text-teal-600"),
                class_name="p-3 bg-teal-50/50 rounded-2xl border border-teal-100/50",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.span(
                trend,
                class_name=rx.cond(
                    trend_up,
                    "text-teal-600 text-sm font-medium",
                    "text-red-600 text-sm font-medium",
                ),
            ),
            rx.el.span(" from last month", class_name="text-sm text-gray-500 ml-2"),
            class_name="mt-4",
        ),
        class_name=f"{GlassStyles.STAT_CARD_LIGHT} {current_config.glass_card_hover}",
    )


def efficiency_stat_card(
    title: str, value: str, subtitle: str, icon: str, color: str = "teal"
) -> rx.Component:
    """Stat card for clinical efficiency metrics."""
    color_classes = {
        "teal": "text-teal-600 bg-teal-50/50 border-teal-100/50",
        "blue": "text-blue-600 bg-blue-50/50 border-blue-100/50",
        "purple": "text-purple-600 bg-purple-50/50 border-purple-100/50",
        "amber": "text-amber-600 bg-amber-50/50 border-amber-100/50",
        "emerald": "text-emerald-600 bg-emerald-50/50 border-emerald-100/50",
    }
    
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-5 h-5 {color_classes.get(color, color_classes['teal']).split()[0]}"),
            class_name=f"p-2.5 rounded-xl border {color_classes.get(color, color_classes['teal'])}",
        ),
        rx.el.div(
            rx.el.p(
                value,
                class_name="text-2xl font-bold text-gray-800 mt-3",
            ),
            rx.el.p(title, class_name="text-sm font-medium text-gray-700 mt-1"),
            rx.el.p(subtitle, class_name="text-xs text-gray-500 mt-0.5"),
        ),
        class_name=f"{GlassStyles.PANEL_LIGHT} p-4 hover:shadow-md transition-all",
    )


def chart_card(title: str, chart: rx.Component) -> rx.Component:
    """Card wrapper for charts."""
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-bold text-gray-800 mb-6"),
        rx.el.div(chart, class_name="w-full h-64"),
        class_name=f"{current_config.glass_panel_style} p-6 rounded-2xl",
    )


def efficiency_chart_placeholder(title: str, description: str) -> rx.Component:
    """Placeholder for efficiency charts."""
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-bold text-gray-800 mb-2"),
        rx.el.p(description, class_name="text-sm text-gray-500 mb-4"),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    ["Mon", "Tue", "Wed", "Thu", "Fri"],
                    lambda day: rx.el.div(
                        rx.el.div(
                            class_name="w-full bg-gradient-to-t from-teal-500 to-teal-300 rounded-t",
                            style={"height": f"{60 + (hash(day) % 40)}%"}
                        ),
                        rx.el.span(day, class_name="text-xs text-gray-500 mt-2"),
                        class_name="flex flex-col items-center justify-end h-40 w-1/5",
                    ),
                ),
                class_name="flex items-end justify-between h-48 px-4",
            ),
            class_name="bg-gray-50/50 rounded-xl p-4",
        ),
        class_name=f"{GlassStyles.PANEL_LIGHT} p-6",
    )


def patient_table_row(patient: Patient) -> rx.Component:
    """Patient table row component."""
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.span("P", class_name="text-xs font-bold text-teal-700"),
                    class_name="w-8 h-8 rounded-full bg-teal-100 flex items-center justify-center mr-3",
                ),
                rx.el.div(
                    rx.el.p(
                        patient["full_name"],
                        class_name="text-sm font-medium text-gray-900",
                    ),
                    rx.el.p(
                        patient["email"], class_name="text-xs text-gray-500 truncate"
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(patient["age"], class_name="text-sm text-gray-700"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(patient["last_visit"], class_name="text-sm text-gray-700"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                patient["status"],
                class_name=rx.cond(
                    patient["status"] == "Active",
                    "px-2 py-1 text-xs font-semibold rounded-full bg-teal-100 text-teal-800",
                    rx.cond(
                        patient["status"] == "Inactive",
                        "px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800",
                        "px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800",
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
                class_name="w-20 h-2 bg-gray-200 rounded-full",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                "View",
                on_click=lambda: PatientState.open_view_patient(patient),
                class_name="text-teal-600 hover:text-teal-900 text-sm font-medium",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
    )


def dashboard_tabs() -> rx.Component:
    """Dashboard tab navigation."""
    return rx.el.div(
        rx.el.button(
            rx.icon("layout-dashboard", class_name="w-4 h-4 mr-2"),
            "Overview",
            on_click=lambda: AdminDashboardState.set_tab("overview"),
            class_name=f"""
                px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center
                {rx.cond(
                    AdminDashboardState.active_tab == "overview",
                    "bg-white/80 text-teal-700 shadow-sm border border-teal-200/50",
                    "text-gray-600 hover:bg-white/50 hover:text-gray-900"
                )}
            """,
        ),
        rx.el.button(
            rx.icon("users", class_name="w-4 h-4 mr-2"),
            "Patients",
            on_click=lambda: AdminDashboardState.set_tab("patients"),
            class_name=f"""
                px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center
                {rx.cond(
                    AdminDashboardState.active_tab == "patients",
                    "bg-white/80 text-teal-700 shadow-sm border border-teal-200/50",
                    "text-gray-600 hover:bg-white/50 hover:text-gray-900"
                )}
            """,
        ),
        rx.el.button(
            rx.icon("gauge", class_name="w-4 h-4 mr-2"),
            "Clinical Efficiency",
            on_click=lambda: AdminDashboardState.set_tab("efficiency"),
            class_name=f"""
                px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center
                {rx.cond(
                    AdminDashboardState.active_tab == "efficiency",
                    "bg-white/80 text-teal-700 shadow-sm border border-teal-200/50",
                    "text-gray-600 hover:bg-white/50 hover:text-gray-900"
                )}
            """,
        ),
        class_name=f"{GlassStyles.TAB_LIST_LIGHT} mb-6",
    )
