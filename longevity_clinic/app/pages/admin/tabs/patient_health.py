"""Admin dashboard patient health tab for viewing individual patient metrics."""

import reflex as rx

from ....styles import GlassStyles
from ....states import AdminDashboardState, HealthDashboardState, BiomarkerState
from ....components.shared import (
    search_input,
    loading_spinner,
    empty_state,
    health_metrics_dashboard,
)
from ...patient.analytics.components import category_section


def _patient_dropdown_item(patient: dict) -> rx.Component:
    """Render a patient item in the dropdown.

    Uses patient["id"] directly in the event handler to avoid
    lambda capture issues with Reflex foreach.
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    patient["full_name"][0],
                    class_name="text-xs font-bold text-teal-300",
                ),
                class_name="w-8 h-8 rounded-full bg-teal-500/20 flex items-center justify-center mr-3 border border-teal-500/30",
            ),
            rx.el.div(
                rx.el.p(
                    patient["full_name"],
                    class_name="text-sm font-medium text-white",
                ),
                rx.el.p(
                    patient["email"],
                    class_name="text-xs text-slate-400",
                ),
            ),
            class_name="flex items-center",
        ),
        on_click=[
            AdminDashboardState.select_patient_by_id(patient["id"]),
            HealthDashboardState.load_patient_health_data(patient["id"]),
            BiomarkerState.load_biomarkers,
        ],
        class_name="p-3 hover:bg-slate-700/50 cursor-pointer transition-colors border-b border-slate-700/30 last:border-0",
    )


def _patient_search_dropdown() -> rx.Component:
    """Patient search dropdown for selecting a patient to view."""
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Select Patient",
                class_name="text-sm font-medium text-slate-300 mb-2 block",
            ),
            search_input(
                placeholder="Search patients by name or email...",
                value=AdminDashboardState.patient_search_query,
                on_change=AdminDashboardState.set_patient_search_query,
            ),
            class_name="mb-4",
        ),
        # Dropdown results
        rx.cond(
            AdminDashboardState.patient_search_query != "",
            rx.el.div(
                rx.foreach(
                    AdminDashboardState.filtered_patients,
                    _patient_dropdown_item,
                ),
                class_name=f"{GlassStyles.PANEL} mt-2 max-h-60 overflow-y-auto",
            ),
        ),
        # Quick access: Recently active patients
        rx.cond(
            AdminDashboardState.patient_search_query == "",
            rx.el.div(
                rx.el.div(
                    rx.icon("clock", class_name="w-4 h-4 mr-2 text-teal-400"),
                    rx.el.span(
                        "Recently Active",
                        class_name="text-sm font-medium text-slate-300",
                    ),
                    class_name="flex items-center mb-3 mt-4",
                ),
                rx.cond(
                    AdminDashboardState.recently_active_patients.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            AdminDashboardState.recently_active_patients,
                            _patient_dropdown_item,
                        ),
                        class_name=f"{GlassStyles.PANEL} max-h-80 overflow-y-auto",
                    ),
                    rx.el.p(
                        "No recent patient activity",
                        class_name="text-sm text-slate-400 italic py-4 text-center",
                    ),
                ),
            ),
        ),
        class_name="w-full max-w-md",
    )


def _selected_patient_header() -> rx.Component:
    """Header showing selected patient info."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    AdminDashboardState.selected_patient["full_name"][0],
                    class_name="text-lg font-bold text-teal-300",
                ),
                class_name="w-12 h-12 rounded-full bg-teal-500/20 flex items-center justify-center mr-4 border border-teal-500/30",
            ),
            rx.el.div(
                rx.el.h3(
                    AdminDashboardState.selected_patient["full_name"],
                    class_name="text-lg font-semibold text-white",
                ),
                rx.el.p(
                    AdminDashboardState.selected_patient["email"],
                    class_name="text-sm text-slate-400",
                ),
            ),
            class_name="flex items-center",
        ),
        rx.el.button(
            rx.icon("x", class_name="w-4 h-4"),
            "Clear Selection",
            on_click=[
                AdminDashboardState.clear_selected_patient,
                HealthDashboardState.clear_patient_health_data,
            ],
            class_name="px-3 py-2 text-sm text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-lg flex items-center gap-2 transition-all",
        ),
        class_name="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl border border-slate-700/50 mb-6",
    )


def _tab_button(label: str, tab_id: str, icon: str) -> rx.Component:
    """Tab button for switching between Health and Analytics views."""
    is_active = HealthDashboardState.active_tab == tab_id
    return rx.el.button(
        rx.icon(icon, class_name="w-4 h-4 mr-2"),
        label,
        on_click=HealthDashboardState.set_active_tab(tab_id),
        class_name=rx.cond(
            is_active,
            "flex items-center px-4 py-2 text-sm font-medium text-teal-300 bg-teal-500/10 border border-teal-500/30 rounded-lg",
            "flex items-center px-4 py-2 text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-700/30 rounded-lg transition-all",
        ),
    )


def _tabs_navigation() -> rx.Component:
    """Tabs for switching between Health Overview and Analytics."""
    return rx.el.div(
        _tab_button("Health Overview", "overview", "heart-pulse"),
        _tab_button("Biomarker Analytics", "analytics", "chart-line"),
        class_name="flex gap-2 mb-6",
    )


def _health_overview_content() -> rx.Component:
    """Health overview content - medications, nutrition, conditions."""
    return rx.cond(
        HealthDashboardState.is_loading,
        loading_spinner("Loading patient data..."),
        health_metrics_dashboard(),
    )


def _analytics_content() -> rx.Component:
    """Analytics content - biomarker panels and trends."""
    return rx.cond(
        BiomarkerState.is_loading,
        loading_spinner("Loading biomarker data..."),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Biomarker Analytics",
                    class_name=f"text-2xl {GlassStyles.HEADING_LIGHT}",
                ),
                rx.el.p(
                    "Comprehensive health intelligence report",
                    class_name="text-slate-400 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.foreach(BiomarkerState.biomarker_panels, category_section),
        ),
    )


def _patient_content() -> rx.Component:
    """Content area showing selected patient's data with tabs."""
    return rx.fragment(
        _selected_patient_header(),
        _tabs_navigation(),
        rx.match(
            HealthDashboardState.active_tab,
            ("overview", _health_overview_content()),
            ("analytics", _analytics_content()),
            _health_overview_content(),  # default
        ),
    )


def patient_health_tab() -> rx.Component:
    """Patient health tab for admin to view patient metrics.

    Allows admin to search and select patients to view their
    health dashboard with medications, nutrition, symptoms, etc.
    Also includes biomarker analytics tab.
    """
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h2(
                "Patient Health Dashboard",
                class_name="text-xl font-bold text-white mb-2",
            ),
            rx.el.p(
                "Search and select a patient to view their health metrics and biomarker analytics.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        # Patient selection or health data
        rx.cond(
            AdminDashboardState.has_selected_patient,
            _patient_content(),
            rx.el.div(
                _patient_search_dropdown(),
                empty_state(
                    icon="user-search",
                    message="Select a patient to view their health data",
                ),
            ),
        ),
        on_mount=[
            AdminDashboardState.load_patients_for_selection,
            AdminDashboardState.load_recently_active_patients,
        ],
    )
