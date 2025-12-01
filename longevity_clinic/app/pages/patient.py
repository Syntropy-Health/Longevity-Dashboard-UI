import reflex as rx
from ..components.layout import authenticated_layout
from ..states.auth_state import AuthState
from ..states.patient_biomarker_state import (
    PatientBiomarkerState,
    Biomarker,
    PortalAppointment,
    PortalTreatment,
)
from ..states.patient_dashboard_state import PatientDashboardState
from ..components.charts import biomarker_history_chart
from ..styles.constants import GlassStyles


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
                                class_name="text-xs text-slate-500 uppercase font-semibold",
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
                                class_name="text-xs text-slate-500 uppercase font-semibold",
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
                                class_name="text-xs text-slate-500 uppercase font-semibold",
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


# =============================================================================
# Dashboard Tab Components
# =============================================================================

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


def dashboard_tabs() -> rx.Component:
    """Main dashboard tab navigation."""
    return rx.el.div(
        rx.el.div(
            tab_button("Overview", "overview", "layout-dashboard"),
            tab_button("Food Tracker", "food", "apple"),
            tab_button("Medications", "medications", "pill"),
            tab_button("Conditions", "conditions", "heart-pulse"),
            tab_button("Symptoms", "symptoms", "thermometer"),
            tab_button("Data Sources", "data_sources", "link"),
            tab_button("Check-ins", "checkins", "mic"),
            tab_button("Settings", "settings", "settings"),
            class_name="flex flex-wrap gap-2 p-2 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10",
        ),
        class_name="mb-8",
    )


# =============================================================================
# Food Tracker Tab
# =============================================================================

def food_entry_card(entry: dict) -> rx.Component:
    """Food entry card."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("utensils", class_name="w-4 h-4 text-teal-400"),
                class_name="w-10 h-10 rounded-xl bg-teal-500/10 flex items-center justify-center mr-3 border border-teal-500/20",
            ),
            rx.el.div(
                rx.el.h4(entry["name"], class_name="text-sm font-semibold text-white"),
                rx.el.p(
                    f"{entry['time']} • {entry['meal_type'].capitalize()}",
                    class_name="text-xs text-slate-400",
                ),
            ),
            class_name="flex items-center flex-1",
        ),
        rx.el.div(
            rx.el.span(f"{entry['calories']}", class_name="text-lg font-bold text-white"),
            rx.el.span(" kcal", class_name="text-xs text-slate-400 ml-1"),
            class_name="flex items-baseline",
        ),
        class_name=f"{GlassStyles.PANEL} p-4 flex items-center justify-between hover:bg-white/10 transition-all cursor-pointer",
    )


def nutrition_progress_bar(label: str, current: float, goal: float, color: str) -> rx.Component:
    """Nutrition progress bar."""
    progress = min((current / goal) * 100, 100) if goal > 0 else 0
    return rx.el.div(
        rx.el.div(
            rx.el.span(label, class_name="text-xs text-slate-400 uppercase tracking-wider"),
            rx.el.span(f"{current:.0f}/{goal:.0f}g", class_name="text-xs text-slate-300"),
            class_name="flex justify-between mb-1",
        ),
        rx.el.div(
            rx.el.div(
                class_name=f"h-2 rounded-full bg-{color}-500/80 transition-all",
                style={"width": f"{progress}%"},
            ),
            class_name="h-2 rounded-full bg-slate-700/50 overflow-hidden",
        ),
        class_name="mb-3",
    )


def food_tracker_tab() -> rx.Component:
    """Food tracker tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Today's Nutrition", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p("Track your daily food intake and nutrition goals.", class_name="text-slate-400 text-sm"),
            class_name="mb-6",
        ),
        # Nutrition Summary Cards
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("flame", class_name="w-6 h-6 text-orange-400"),
                    class_name="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mb-3 border border-orange-500/20",
                ),
                rx.el.p("Calories", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                rx.el.div(
                    rx.el.span(
                        PatientDashboardState.nutrition_summary["total_calories"],
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span(
                        f" / {PatientDashboardState.nutrition_summary['goal_calories']}",
                        class_name="text-sm text-slate-400",
                    ),
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("beef", class_name="w-6 h-6 text-red-400"),
                    class_name="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center mb-3 border border-red-500/20",
                ),
                rx.el.p("Protein", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                rx.el.div(
                    rx.el.span(
                        f"{PatientDashboardState.nutrition_summary['total_protein']:.0f}",
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span("g", class_name="text-sm text-slate-400 ml-1"),
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("wheat", class_name="w-6 h-6 text-amber-400"),
                    class_name="w-12 h-12 rounded-xl bg-amber-500/10 flex items-center justify-center mb-3 border border-amber-500/20",
                ),
                rx.el.p("Carbs", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                rx.el.div(
                    rx.el.span(
                        f"{PatientDashboardState.nutrition_summary['total_carbs']:.0f}",
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span("g", class_name="text-sm text-slate-400 ml-1"),
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("droplet", class_name="w-6 h-6 text-blue-400"),
                    class_name="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center mb-3 border border-blue-500/20",
                ),
                rx.el.p("Water", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                rx.el.div(
                    rx.el.span(
                        f"{PatientDashboardState.nutrition_summary['water_intake']:.1f}",
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span("L", class_name="text-sm text-slate-400 ml-1"),
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8",
        ),
        # Food Entries
        rx.el.div(
            rx.el.div(
                rx.el.h3("Today's Meals", class_name="text-lg font-semibold text-white"),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                    "Add Food",
                    class_name=GlassStyles.BUTTON_PRIMARY,
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.foreach(PatientDashboardState.food_entries, food_entry_card),
                class_name="space-y-3",
            ),
        ),
    )


# =============================================================================
# Medications Tab
# =============================================================================

def medication_card(med: dict) -> rx.Component:
    """Medication card."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("pill", class_name="w-5 h-5 text-purple-400"),
                class_name="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center mr-4 border border-purple-500/20",
            ),
            rx.el.div(
                rx.el.h4(med["name"], class_name="text-base font-semibold text-white mb-1"),
                rx.el.p(med["dosage"], class_name="text-sm text-slate-300"),
                rx.el.p(med["frequency"], class_name="text-xs text-slate-400 mt-1"),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span("Adherence", class_name="text-[10px] text-slate-400 uppercase tracking-wider"),
                rx.el.span(
                    f"{med['adherence_rate']:.0f}%",
                    class_name=rx.cond(
                        med["adherence_rate"] >= 90,
                        "text-lg font-bold text-teal-400",
                        "text-lg font-bold text-amber-400",
                    ),
                ),
                class_name="text-right",
            ),
            rx.el.span(
                med["status"].capitalize(),
                class_name=rx.cond(
                    med["status"] == "active",
                    "mt-2 inline-block px-2 py-0.5 rounded text-[10px] font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20",
                    "mt-2 inline-block px-2 py-0.5 rounded text-[10px] font-medium bg-slate-500/10 text-slate-300 border border-slate-500/20",
                ),
            ),
            class_name="flex flex-col items-end",
        ),
        on_click=lambda: PatientDashboardState.open_medication_modal(med),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def medications_tab() -> rx.Component:
    """Medications tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Medications", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p("Manage your medications and track adherence.", class_name="text-slate-400 text-sm"),
            class_name="mb-6",
        ),
        # Medication Efficacy Summary
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("chart-line", class_name="w-6 h-6 text-teal-400"),
                    class_name="w-12 h-12 rounded-xl bg-teal-500/10 flex items-center justify-center mb-3 border border-teal-500/20",
                ),
                rx.el.p("Overall Adherence", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                rx.el.span(
                    f"{PatientDashboardState.total_medication_adherence:.0f}%",
                    class_name="text-3xl font-bold text-teal-400",
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("pill", class_name="w-6 h-6 text-purple-400"),
                    class_name="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center mb-3 border border-purple-500/20",
                ),
                rx.el.p("Active Medications", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                rx.el.span(
                    len(PatientDashboardState.medications),
                    class_name="text-3xl font-bold text-white",
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            class_name="grid grid-cols-2 gap-4 mb-8",
        ),
        # Medication List
        rx.el.div(
            rx.foreach(PatientDashboardState.medications, medication_card),
            class_name="space-y-4",
        ),
    )


# =============================================================================
# Conditions Tab
# =============================================================================

def condition_card(condition: dict) -> rx.Component:
    """Condition card."""
    status_styles = {
        "active": "bg-amber-500/10 text-amber-300 border-amber-500/20",
        "managed": "bg-teal-500/10 text-teal-300 border-teal-500/20",
        "resolved": "bg-slate-500/10 text-slate-300 border-slate-500/20",
    }
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("heart-pulse", class_name="w-5 h-5 text-rose-400"),
                class_name="w-12 h-12 rounded-xl bg-rose-500/10 flex items-center justify-center mr-4 border border-rose-500/20",
            ),
            rx.el.div(
                rx.el.h4(condition["name"], class_name="text-base font-semibold text-white mb-1"),
                rx.el.p(f"ICD-10: {condition['icd_code']}", class_name="text-xs text-slate-400"),
                rx.el.p(f"Diagnosed: {condition['diagnosed_date']}", class_name="text-xs text-slate-400 mt-1"),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.span(
                condition["status"].capitalize(),
                class_name=f"px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border {status_styles.get(condition['status'], status_styles['active'])}",
            ),
            rx.el.p(condition["severity"].capitalize(), class_name="text-xs text-slate-400 mt-2"),
            class_name="flex flex-col items-end",
        ),
        on_click=lambda: PatientDashboardState.open_condition_modal(condition),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def conditions_tab() -> rx.Component:
    """Conditions tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Health Conditions", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p("Track and manage your health conditions.", class_name="text-slate-400 text-sm"),
            class_name="mb-6",
        ),
        # Filter buttons
        rx.el.div(
            rx.el.button(
                f"All ({len(PatientDashboardState.conditions)})",
                on_click=lambda: PatientDashboardState.set_conditions_filter("all"),
                class_name=rx.cond(
                    PatientDashboardState.conditions_filter == "all",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                f"Active ({PatientDashboardState.active_conditions_count})",
                on_click=lambda: PatientDashboardState.set_conditions_filter("active"),
                class_name=rx.cond(
                    PatientDashboardState.conditions_filter == "active",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-amber-500/20 text-amber-300 border border-amber-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                f"Managed ({PatientDashboardState.managed_conditions_count})",
                on_click=lambda: PatientDashboardState.set_conditions_filter("managed"),
                class_name=rx.cond(
                    PatientDashboardState.conditions_filter == "managed",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                f"Resolved ({PatientDashboardState.resolved_conditions_count})",
                on_click=lambda: PatientDashboardState.set_conditions_filter("resolved"),
                class_name=rx.cond(
                    PatientDashboardState.conditions_filter == "resolved",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-slate-500/20 text-slate-300 border border-slate-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6",
        ),
        # Conditions List
        rx.el.div(
            rx.foreach(PatientDashboardState.filtered_conditions, condition_card),
            class_name="space-y-4",
        ),
    )


# =============================================================================
# Symptoms Tab
# =============================================================================

def symptom_card(symptom: dict) -> rx.Component:
    """Symptom card."""
    trend_icon = {
        "improving": ("trending-down", "text-teal-400"),
        "stable": ("minus", "text-slate-400"),
        "worsening": ("trending-up", "text-red-400"),
    }
    icon_name, icon_class = trend_icon.get(symptom.get("trend", "stable"), ("minus", "text-slate-400"))
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("thermometer", class_name="w-5 h-5 text-orange-400"),
                class_name="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mr-4 border border-orange-500/20",
            ),
            rx.el.div(
                rx.el.h4(symptom["name"], class_name="text-base font-semibold text-white mb-1"),
                rx.el.p(f"Severity: {symptom['severity'].capitalize()}", class_name="text-sm text-slate-300"),
                rx.el.p(f"Frequency: {symptom['frequency']}", class_name="text-xs text-slate-400 mt-1"),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(icon_name, class_name=f"w-4 h-4 {icon_class} mr-1"),
                rx.el.span(symptom["trend"].capitalize(), class_name=f"text-xs {icon_class}"),
                class_name="flex items-center",
            ),
            rx.el.button(
                "Log",
                on_click=lambda: PatientDashboardState.open_symptom_modal(symptom),
                class_name="mt-2 px-3 py-1 text-xs font-medium bg-white/5 hover:bg-white/10 text-slate-300 rounded-lg border border-white/10 transition-all",
            ),
            class_name="flex flex-col items-end",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def symptom_log_item(log: dict) -> rx.Component:
    """Symptom log item."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(log["timestamp"], class_name="text-xs text-teal-400 font-medium"),
            rx.el.p(log["symptom_name"], class_name="text-sm font-semibold text-white"),
            rx.el.p(log["notes"], class_name="text-xs text-slate-400 mt-1"),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.span(
                f"Severity: {log['severity']}/10",
                class_name="text-xs text-slate-300 bg-slate-700/50 px-2 py-1 rounded",
            ),
        ),
        class_name="flex items-start justify-between py-3 border-b border-white/5 last:border-0",
    )


def symptoms_tab() -> rx.Component:
    """Symptoms tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Symptom Tracker", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p("Track and log your symptoms over time.", class_name="text-slate-400 text-sm"),
            class_name="mb-6",
        ),
        # Sub-filters
        rx.el.div(
            rx.el.button(
                "Timeline",
                on_click=lambda: PatientDashboardState.set_symptoms_filter("timeline"),
                class_name=rx.cond(
                    PatientDashboardState.symptoms_filter == "timeline",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Symptoms",
                on_click=lambda: PatientDashboardState.set_symptoms_filter("symptoms"),
                class_name=rx.cond(
                    PatientDashboardState.symptoms_filter == "symptoms",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Reminders",
                on_click=lambda: PatientDashboardState.set_symptoms_filter("reminders"),
                class_name=rx.cond(
                    PatientDashboardState.symptoms_filter == "reminders",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Trends",
                on_click=lambda: PatientDashboardState.set_symptoms_filter("trends"),
                class_name=rx.cond(
                    PatientDashboardState.symptoms_filter == "trends",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6",
        ),
        # Content based on filter
        rx.cond(
            PatientDashboardState.symptoms_filter == "timeline",
            rx.el.div(
                rx.el.h3("Recent Symptom Logs", class_name="text-lg font-semibold text-white mb-4"),
                rx.el.div(
                    rx.foreach(PatientDashboardState.symptom_logs, symptom_log_item),
                    class_name=f"{GlassStyles.PANEL} p-4",
                ),
            ),
            rx.cond(
                PatientDashboardState.symptoms_filter == "symptoms",
                rx.el.div(
                    rx.foreach(PatientDashboardState.symptoms, symptom_card),
                    class_name="space-y-4",
                ),
                rx.el.div(
                    rx.el.p("Content coming soon...", class_name="text-slate-400"),
                    class_name=f"{GlassStyles.PANEL} p-6 text-center",
                ),
            ),
        ),
    )


# =============================================================================
# Data Sources Tab
# =============================================================================

def data_source_card(source: dict) -> rx.Component:
    """Data source card."""
    status_color = "teal" if source.get("status") == "connected" else "red"
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(source.get("icon", "link"), class_name=f"w-5 h-5 text-{status_color}-400"),
                class_name=f"w-12 h-12 rounded-xl bg-{status_color}-500/10 flex items-center justify-center mr-4 border border-{status_color}-500/20",
            ),
            rx.el.div(
                rx.el.h4(source["name"], class_name="text-base font-semibold text-white mb-1"),
                rx.el.p(source["type"].capitalize(), class_name="text-xs text-slate-400"),
                rx.el.p(f"Last sync: {source['last_sync']}", class_name="text-xs text-slate-500 mt-1"),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.span(
                source["status"].capitalize(),
                class_name=rx.cond(
                    source["status"] == "connected",
                    "px-3 py-1 rounded-full text-[10px] font-bold bg-teal-500/10 text-teal-300 border border-teal-500/20 uppercase tracking-wide",
                    "px-3 py-1 rounded-full text-[10px] font-bold bg-red-500/10 text-red-300 border border-red-500/20 uppercase tracking-wide",
                ),
            ),
            class_name="flex flex-col items-end",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def data_sources_tab() -> rx.Component:
    """Data sources tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Data Sources", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p("Connect and manage your health data sources.", class_name="text-slate-400 text-sm"),
            class_name="mb-6",
        ),
        # Sub-filters
        rx.el.div(
            rx.el.button(
                "Devices & Wearables",
                on_click=lambda: PatientDashboardState.set_data_sources_filter("devices"),
                class_name=rx.cond(
                    PatientDashboardState.data_sources_filter == "devices",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "API Connections",
                on_click=lambda: PatientDashboardState.set_data_sources_filter("api_connections"),
                class_name=rx.cond(
                    PatientDashboardState.data_sources_filter == "api_connections",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Import History",
                on_click=lambda: PatientDashboardState.set_data_sources_filter("import_history"),
                class_name=rx.cond(
                    PatientDashboardState.data_sources_filter == "import_history",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-4 h-4 mr-2"),
                "Connect New",
                on_click=PatientDashboardState.open_connect_modal,
                class_name=GlassStyles.BUTTON_PRIMARY,
            ),
            class_name="flex flex-wrap gap-2 mb-6",
        ),
        # Summary Card
        rx.el.div(
            rx.el.div(
                rx.icon("link", class_name="w-6 h-6 text-teal-400"),
                class_name="w-12 h-12 rounded-xl bg-teal-500/10 flex items-center justify-center mb-3 border border-teal-500/20",
            ),
            rx.el.p("Connected Sources", class_name="text-xs text-slate-500 uppercase tracking-wider mb-1"),
            rx.el.span(
                PatientDashboardState.connected_sources_count,
                class_name="text-3xl font-bold text-white",
            ),
            class_name=f"{GlassStyles.PANEL} p-5 mb-6",
        ),
        # Sources List
        rx.el.div(
            rx.foreach(PatientDashboardState.filtered_data_sources, data_source_card),
            class_name="space-y-4",
        ),
    )


# =============================================================================
# Check-ins Tab
# =============================================================================

def checkin_card(checkin: dict) -> rx.Component:
    """Check-in card."""
    type_icons = {
        "voice": "mic",
        "text": "message-square",
        "call": "phone",
    }
    sentiment_colors = {
        "positive": "teal",
        "neutral": "slate",
        "negative": "amber",
    }
    icon = type_icons.get(checkin.get("type", "text"), "message-square")
    color = sentiment_colors.get(checkin.get("sentiment", "neutral"), "slate")
    
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"w-5 h-5 text-{color}-400"),
                class_name=f"w-12 h-12 rounded-xl bg-{color}-500/10 flex items-center justify-center mr-4 border border-{color}-500/20",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(checkin["type"].capitalize(), class_name="text-xs font-medium text-teal-400 mr-2"),
                    rx.el.span(checkin["timestamp"], class_name="text-xs text-slate-500"),
                    class_name="flex items-center mb-1",
                ),
                rx.el.p(checkin["summary"], class_name="text-sm text-white line-clamp-2"),
                rx.cond(
                    len(checkin.get("key_topics", [])) > 0,
                    rx.el.div(
                        rx.foreach(
                            checkin["key_topics"],
                            lambda topic: rx.el.span(
                                topic,
                                class_name="px-2 py-0.5 bg-white/5 rounded text-[10px] text-slate-400 mr-1",
                            ),
                        ),
                        class_name="mt-2 flex flex-wrap gap-1",
                    ),
                    rx.fragment(),
                ),
                class_name="flex-1",
            ),
            class_name="flex items-start",
        ),
        rx.el.div(
            rx.cond(
                checkin["provider_reviewed"],
                rx.el.span(
                    "Reviewed",
                    class_name="px-2 py-1 rounded text-[10px] font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20",
                ),
                rx.el.span(
                    "Pending",
                    class_name="px-2 py-1 rounded text-[10px] font-medium bg-amber-500/10 text-amber-300 border border-amber-500/20",
                ),
            ),
            class_name="ml-4",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def checkins_tab() -> rx.Component:
    """Check-ins tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Self Check-ins", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p("Voice and text logs between visits.", class_name="text-slate-400 text-sm"),
            class_name="mb-6",
        ),
        # Quick action buttons
        rx.el.div(
            rx.el.button(
                rx.icon("mic", class_name="w-5 h-5 mr-2"),
                "Voice Check-in",
                on_click=PatientDashboardState.open_checkin_modal,
                class_name=GlassStyles.BUTTON_PRIMARY,
            ),
            rx.el.button(
                rx.icon("message-square", class_name="w-5 h-5 mr-2"),
                "Text Note",
                on_click=PatientDashboardState.open_checkin_modal,
                class_name=GlassStyles.BUTTON_SECONDARY,
            ),
            class_name="flex gap-3 mb-6",
        ),
        # Summary Cards
        rx.el.div(
            rx.el.div(
                rx.icon("mic", class_name="w-6 h-6 text-teal-400 mb-2"),
                rx.el.p("This Week", class_name="text-xs text-slate-500 uppercase tracking-wider"),
                rx.el.span(len(PatientDashboardState.checkins), class_name="text-2xl font-bold text-white"),
                rx.el.span(" check-ins", class_name="text-sm text-slate-400 ml-1"),
                class_name=f"{GlassStyles.PANEL} p-4",
            ),
            rx.el.div(
                rx.icon("clock", class_name="w-6 h-6 text-amber-400 mb-2"),
                rx.el.p("Pending Review", class_name="text-xs text-slate-500 uppercase tracking-wider"),
                rx.el.span(PatientDashboardState.unreviewed_checkins_count, class_name="text-2xl font-bold text-white"),
                class_name=f"{GlassStyles.PANEL} p-4",
            ),
            class_name="grid grid-cols-2 gap-4 mb-6",
        ),
        # Check-ins List
        rx.el.div(
            rx.el.h3("Recent Check-ins", class_name="text-lg font-semibold text-white mb-4"),
            rx.el.div(
                rx.foreach(PatientDashboardState.checkins, checkin_card),
                class_name="space-y-4",
            ),
        ),
    )


# =============================================================================
# Settings Tab
# =============================================================================

def settings_tab() -> rx.Component:
    """Settings/Profile tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Settings", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p("Manage your profile and preferences.", class_name="text-slate-400 text-sm"),
            class_name="mb-6",
        ),
        rx.el.div(
            # Profile Section
            rx.el.div(
                rx.el.h3("Profile", class_name="text-lg font-semibold text-white mb-4"),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                AuthState.user_initials,
                                class_name="text-2xl font-bold text-teal-300",
                            ),
                            class_name="w-20 h-20 rounded-full bg-teal-900/50 flex items-center justify-center border border-teal-500/30",
                        ),
                        rx.el.div(
                            rx.el.h4(AuthState.user["full_name"], class_name="text-lg font-semibold text-white"),
                            rx.el.p(AuthState.role_label, class_name="text-sm text-teal-400"),
                            class_name="ml-4",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name=f"{GlassStyles.PANEL} p-6",
                ),
                class_name="mb-8",
            ),
            # Notification Settings
            rx.el.div(
                rx.el.h3("Notifications", class_name="text-lg font-semibold text-white mb-4"),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Email Notifications", class_name="text-sm text-white"),
                        rx.el.p("Receive updates via email", class_name="text-xs text-slate-400"),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        class_name="w-10 h-6 bg-teal-500/30 rounded-full relative cursor-pointer",
                    ),
                    class_name="flex items-center justify-between p-4 border-b border-white/5",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Push Notifications", class_name="text-sm text-white"),
                        rx.el.p("Receive push notifications", class_name="text-xs text-slate-400"),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        class_name="w-10 h-6 bg-teal-500/30 rounded-full relative cursor-pointer",
                    ),
                    class_name="flex items-center justify-between p-4",
                ),
                class_name=f"{GlassStyles.PANEL}",
            ),
        ),
    )


# =============================================================================
# Overview Tab (Default)
# =============================================================================

def overview_tab() -> rx.Component:
    """Overview tab with key metrics and biomarkers."""
    return rx.el.div(
        # Key Metrics Grid
        rx.el.div(
            rx.el.h2("Health Metrics", class_name="text-lg font-semibold text-white mb-4"),
            rx.el.div(
                static_metric_card("Nutrition Score", "82", "/100", "apple", "up", "+5 this week"),
                static_metric_card("Med Adherence", "94", "%", "pill", "stable", "Consistent"),
                static_metric_card("Active Conditions", "3", "", "heart-pulse", "down", "-1 resolved"),
                static_metric_card("Symptom Score", "Low", "", "thermometer", "down", "Improving"),
                static_metric_card("Data Sources", "6", "connected", "link", "stable", "All synced"),
                static_metric_card("Check-ins", "5", "this week", "mic", "up", "+2 vs last week"),
                class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8",
            ),
        ),
        # Biomarker Intelligence
        rx.el.div(
            rx.el.h2(
                "Biomarker Intelligence",
                class_name="text-lg font-semibold text-white mb-4",
            ),
            rx.el.div(
                rx.foreach(PatientBiomarkerState.biomarkers, biomarker_card),
                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-6",
            ),
            biomarker_detail_panel(),
            class_name="mb-10",
        ),
        # Active Protocols and Schedule
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Active Protocols",
                        class_name="text-lg font-semibold text-white mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            PatientBiomarkerState.my_treatments, treatment_card
                        ),
                        class_name="space-y-3",
                    ),
                    class_name="col-span-1 lg:col-span-2",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Upcoming Schedule",
                        class_name="text-lg font-semibold text-white mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            PatientBiomarkerState.upcoming_appointments,
                            appointment_item,
                        ),
                        rx.el.button(
                            "View Full Calendar",
                            class_name="w-full mt-4 py-2 text-sm text-teal-400 font-medium hover:text-teal-300 border border-teal-500/30 rounded-xl hover:bg-teal-500/10 transition-colors",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-5",
                    ),
                    class_name="col-span-1",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
            ),
        ),
    )


# =============================================================================
# Check-in Modal
# =============================================================================

def checkin_modal() -> rx.Component:
    """Modal for creating new check-ins."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name=GlassStyles.MODAL_OVERLAY
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        "New Check-in",
                        class_name="text-xl font-bold text-white mb-2",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Record a voice or text check-in.",
                        class_name="text-slate-400 mb-6 text-sm",
                    ),
                    # Type selector
                    rx.el.div(
                        rx.el.button(
                            rx.icon("message-square", class_name="w-4 h-4 mr-2"),
                            "Text",
                            on_click=lambda: PatientDashboardState.set_checkin_type("text"),
                            class_name=rx.cond(
                                PatientDashboardState.new_checkin_type == "text",
                                "flex items-center px-4 py-2 rounded-xl bg-teal-500/20 text-teal-300 border border-teal-500/30",
                                "flex items-center px-4 py-2 rounded-xl text-slate-400 hover:bg-white/5 border border-transparent",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("mic", class_name="w-4 h-4 mr-2"),
                            "Voice",
                            on_click=lambda: PatientDashboardState.set_checkin_type("voice"),
                            class_name=rx.cond(
                                PatientDashboardState.new_checkin_type == "voice",
                                "flex items-center px-4 py-2 rounded-xl bg-teal-500/20 text-teal-300 border border-teal-500/30",
                                "flex items-center px-4 py-2 rounded-xl text-slate-400 hover:bg-white/5 border border-transparent",
                            ),
                        ),
                        class_name="flex gap-2 mb-6",
                    ),
                    # Text input
                    rx.cond(
                        PatientDashboardState.new_checkin_type == "text",
                        rx.el.textarea(
                            placeholder="How are you feeling today? Any symptoms, updates, or notes to share...",
                            value=PatientDashboardState.new_checkin_text,
                            on_change=PatientDashboardState.set_checkin_text,
                            class_name="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 mb-6 h-40 resize-none",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon(
                                    rx.cond(PatientDashboardState.is_recording, "square", "mic"),
                                    class_name="w-8 h-8",
                                ),
                                on_click=PatientDashboardState.toggle_recording,
                                class_name=rx.cond(
                                    PatientDashboardState.is_recording,
                                    "w-20 h-20 rounded-full bg-red-500/20 text-red-400 border border-red-500/30 flex items-center justify-center hover:bg-red-500/30 transition-all",
                                    "w-20 h-20 rounded-full bg-teal-500/20 text-teal-400 border border-teal-500/30 flex items-center justify-center hover:bg-teal-500/30 transition-all",
                                ),
                            ),
                            rx.el.p(
                                rx.cond(
                                    PatientDashboardState.is_recording,
                                    "Recording... Tap to stop",
                                    "Tap to start recording",
                                ),
                                class_name="text-sm text-slate-400 mt-4",
                            ),
                            class_name="flex flex-col items-center py-8",
                        ),
                    ),
                    # Actions
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=PatientDashboardState.close_checkin_modal,
                            class_name="px-4 py-2 text-slate-400 hover:text-white transition-colors mr-2",
                        ),
                        rx.el.button(
                            "Submit Check-in",
                            on_click=PatientDashboardState.submit_checkin,
                            class_name=GlassStyles.BUTTON_PRIMARY,
                        ),
                        class_name="flex justify-end items-center",
                    ),
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90vw] max-w-md p-6 {GlassStyles.PANEL} z-50",
            ),
        ),
        open=PatientDashboardState.show_checkin_modal,
        on_open_change=PatientDashboardState.handle_checkin_modal_change,
    )


# =============================================================================
# Main Patient Portal
# =============================================================================

def patient_portal() -> rx.Component:
    """Main patient portal with tabbed dashboard."""
    return authenticated_layout(
        rx.el.div(
            # Header
            rx.el.div(
                rx.el.h1(
                    f"Welcome back, {AuthState.user['full_name']}",
                    class_name="text-2xl font-bold text-white",
                ),
                rx.el.p(
                    "Your personalized health dashboard.",
                    class_name="text-slate-400 mt-1",
                ),
                class_name="mb-8",
            ),
            # Dashboard Tabs
            dashboard_tabs(),
            # Tab Content
            rx.match(
                PatientDashboardState.active_tab,
                ("overview", overview_tab()),
                ("food", food_tracker_tab()),
                ("medications", medications_tab()),
                ("conditions", conditions_tab()),
                ("symptoms", symptoms_tab()),
                ("data_sources", data_sources_tab()),
                ("checkins", checkins_tab()),
                ("settings", settings_tab()),
                overview_tab(),
            ),
            # Modals
            checkin_modal(),
        )
    )