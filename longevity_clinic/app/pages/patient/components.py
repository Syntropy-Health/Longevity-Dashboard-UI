"""Shared components for the patient portal."""

import reflex as rx
from ...states.patient_biomarker_state import (
    PatientBiomarkerState,
    Biomarker,
    PortalAppointment,
    PortalTreatment,
)
from ...states.patient_dashboard_state import PatientDashboardState
from ...components.charts import biomarker_history_chart
from ...styles.constants import GlassStyles


def status_badge(status: str) -> rx.Component:
    """Status badge with dark theme styling."""
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
    """Trend indicator with dark theme styling."""
    return rx.match(
        trend,
        (
            "up",
            rx.el.div(
                rx.icon("trending-up", class_name="w-4 h-4 mr-1 text-teal-400"),
                rx.el.span("Increasing", class_name="text-xs text-teal-300"),
                class_name="flex items-center",
            ),
        ),
        (
            "down",
            rx.el.div(
                rx.icon("trending-down", class_name="w-4 h-4 mr-1 text-teal-400"),
                rx.el.span("Decreasing", class_name="text-xs text-teal-300"),
                class_name="flex items-center",
            ),
        ),
        (
            "stable",
            rx.el.div(
                rx.icon("minus", class_name="w-4 h-4 mr-1 text-slate-400"),
                rx.el.span("Stable", class_name="text-xs text-slate-300"),
                class_name="flex items-center",
            ),
        ),
        rx.el.div(),
    )


def biomarker_card(biomarker: Biomarker) -> rx.Component:
    """Biomarker card with dark theme styling."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    biomarker["name"],
                    class_name="text-sm font-semibold text-white truncate",
                ),
                rx.el.p(
                    biomarker["category"],
                    class_name="text-[10px] text-slate-400 truncate uppercase tracking-widest font-semibold mt-1",
                ),
            ),
            status_badge(biomarker["status"]),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.span(
                biomarker["current_value"],
                class_name="text-4xl font-thin text-white tracking-tighter",
            ),
            rx.el.span(
                f" {biomarker['unit']}",
                class_name="text-xs font-medium text-slate-400 ml-1",
            ),
            class_name="flex items-baseline mb-3",
        ),
        trend_indicator(biomarker["trend"]),
        on_click=lambda: PatientBiomarkerState.select_biomarker(biomarker),
        class_name=rx.cond(
            PatientBiomarkerState.selected_biomarker["id"] == biomarker["id"],
            f"{GlassStyles.BIOMARKER_CARD} ring-1 ring-teal-500/40 cursor-pointer transition-all duration-300 scale-[1.02]",
            f"{GlassStyles.BIOMARKER_CARD} cursor-pointer",
        ),
    )


def biomarker_detail_panel() -> rx.Component:
    """Detail panel for selected biomarker with dark theme."""
    return rx.cond(
        PatientBiomarkerState.selected_biomarker,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        PatientBiomarkerState.selected_biomarker["name"],
                        class_name="text-xl font-bold text-white",
                    ),
                    rx.el.p(
                        PatientBiomarkerState.selected_biomarker["description"],
                        class_name="text-sm text-slate-400 mt-1",
                    ),
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-5 h-5"),
                    on_click=PatientBiomarkerState.clear_selected_biomarker,
                    class_name="p-2 hover:bg-white/10 rounded-full text-slate-400 hover:text-white transition-colors",
                ),
                class_name="flex justify-between items-start mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        "Historical Trend",
                        class_name="text-sm font-semibold text-slate-300 mb-4",
                    ),
                    biomarker_history_chart(),
                    class_name="flex-1 min-h-[300px]",
                ),
                rx.el.div(
                    rx.el.h4(
                        "Analysis",
                        class_name="text-sm font-semibold text-slate-300 mb-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Current Status",
                                class_name="text-xs text-slate-400 uppercase font-semibold",
                            ),
                            rx.el.p(
                                PatientBiomarkerState.selected_biomarker["status"],
                                class_name=rx.match(
                                    PatientBiomarkerState.selected_biomarker["status"],
                                    ("Optimal", "text-teal-400 font-bold"),
                                    ("Warning", "text-amber-400 font-bold"),
                                    ("Critical", "text-red-400 font-bold"),
                                    "text-slate-300 font-bold",
                                ),
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Optimal Range",
                                class_name="text-xs text-slate-400 uppercase font-semibold",
                            ),
                            rx.el.p(
                                f"{PatientBiomarkerState.selected_biomarker['optimal_min']} - {PatientBiomarkerState.selected_biomarker['optimal_max']} {PatientBiomarkerState.selected_biomarker['unit']}",
                                class_name="text-white font-medium",
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Latest Reading",
                                class_name="text-xs text-slate-400 uppercase font-semibold",
                            ),
                            rx.el.p(
                                f"{PatientBiomarkerState.selected_biomarker['current_value']} {PatientBiomarkerState.selected_biomarker['unit']}",
                                class_name="text-white font-medium",
                            ),
                        ),
                        class_name="bg-slate-800/50 p-4 rounded-xl border border-slate-700/50",
                    ),
                    class_name="w-full lg:w-64 shrink-0 lg:ml-6 mt-6 lg:mt-0",
                ),
                class_name="flex flex-col lg:flex-row",
            ),
            class_name=f"{GlassStyles.PANEL} p-6 rounded-xl mb-8 animate-fade-in",
        ),
    )


def sub_filter_button(label: str, filter_value: str, current_filter: str, set_filter) -> rx.Component:
    """Sub-filter button for tab content."""
    return rx.el.button(
        label,
        on_click=lambda: set_filter(filter_value),
        class_name=rx.cond(
            current_filter == filter_value,
            "px-3 py-1.5 rounded-lg text-xs font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
            "px-3 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
        ),
    )
    
def treatment_card(treatment: PortalTreatment) -> rx.Component:
    """Treatment card with dark theme styling."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="w-5 h-5 text-teal-400"),
                class_name="w-10 h-10 rounded-full bg-teal-500/10 flex items-center justify-center mr-3 shrink-0 border border-teal-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    treatment["name"], class_name="text-sm font-semibold text-white"
                ),
                rx.el.p(
                    f"{treatment['frequency']} • {treatment['duration']}",
                    class_name="text-xs text-slate-400",
                ),
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.span(
                treatment["status"],
                class_name="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20",
            ),
            class_name="ml-auto",
        ),
        class_name=f"{GlassStyles.PANEL} p-4 rounded-xl hover:bg-white/10 transition-all",
    )


def appointment_item(apt: PortalAppointment) -> rx.Component:
    """Appointment item with dark theme styling."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                apt["date"],
                class_name="text-xs font-bold text-teal-400 uppercase tracking-wide",
            ),
            rx.el.p(apt["time"], class_name="text-xs text-slate-400"),
            class_name="w-16 shrink-0 text-center mr-4 bg-teal-500/10 rounded-lg py-2 border border-teal-500/20",
        ),
        rx.el.div(
            rx.el.h5(apt["title"], class_name="text-sm font-semibold text-white"),
            rx.el.p(
                f"{apt['type']} with {apt['provider']}",
                class_name="text-xs text-slate-400",
            ),
        ),
        class_name="flex items-center py-3 border-b border-white/10 last:border-0",
    )


def static_metric_card(name: str, value: str, unit: str, icon: str, trend: str, trend_value: str) -> rx.Component:
    """Static metric card for overview tab."""
    return rx.el.div(
        rx.el.div(
            rx.icon(
                icon,
                class_name="w-5 h-5 text-teal-400",
            ),
            rx.el.span(
                name,
                class_name="text-xs text-slate-400 uppercase tracking-wider font-semibold ml-2",
            ),
            class_name="flex items-center mb-3",
        ),
        rx.el.div(
            rx.el.span(
                value,
                class_name="text-3xl font-bold text-white",
            ),
            rx.el.span(
                unit,
                class_name="text-sm text-slate-400 ml-1",
            ),
            class_name="flex items-baseline mb-2",
        ),
        rx.el.div(
            rx.icon(
                "trending-up" if trend == "up" else ("trending-down" if trend == "down" else "minus"),
                class_name=f"w-3 h-3 {'text-teal-400' if trend in ['up', 'down'] else 'text-slate-500'} mr-1",
            ),
            rx.el.span(
                trend_value,
                class_name="text-xs text-slate-400",
            ),
            class_name="flex items-center",
        ),
        class_name=f"{GlassStyles.PANEL} p-5 hover:bg-white/10 transition-all cursor-pointer",
    )


def tab_button(label: str, tab_id: str, icon: str) -> rx.Component:
    """Tab button for dashboard navigation."""
    return rx.el.button(
        rx.icon(icon, class_name="w-4 h-4 mr-2"),
        label,
        on_click=lambda: PatientDashboardState.set_active_tab(tab_id),
        class_name=rx.cond(
            PatientDashboardState.active_tab == tab_id,
            "flex items-center px-4 py-2.5 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30 transition-all",
            "flex items-center px-4 py-2.5 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent transition-all",
        ),
    )


def patient_sidebar_tabs() -> rx.Component:
    """Patient dashboard tab navigation - streamlined version.
    
    Shows: Dashboard (overview), Check-ins, Settings (includes data sources).
    Other tabs are accessible from the overview page.
    """
    return rx.el.div(
        rx.el.div(
            tab_button("Dashboard", "overview", "layout-dashboard"),
            tab_button("Food Tracker", "food", "apple"),
            tab_button("Medications", "medications", "pill"),
            tab_button("Conditions", "conditions", "heart-pulse"),
            tab_button("Symptoms", "symptoms", "thermometer"),
            tab_button("Check-ins", "checkins", "mic"),
            tab_button("Settings", "settings", "settings"),
            class_name="flex flex-wrap gap-2 p-2 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10",
        ),
        class_name="mb-8",
    )


def dashboard_tabs() -> rx.Component:
    """Main dashboard tab navigation - legacy, now aliased to patient_sidebar_tabs."""
    return patient_sidebar_tabs()
