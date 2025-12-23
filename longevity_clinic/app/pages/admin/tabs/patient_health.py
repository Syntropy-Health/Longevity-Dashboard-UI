"""Admin dashboard patient health tab for viewing individual patient metrics."""

import reflex as rx

from ....components.shared import (
    collapsible_panels_container,
    empty_state,
    health_metrics_dashboard,
    loading_spinner,
    search_input,
)
from ....states import BiomarkerState, HealthDashboardState, PatientState
from ....styles import GlassStyles

# =============================================================================
# SHARED PATIENT SELECTION COMPONENTS
# =============================================================================


def patient_avatar(name: str, size: str = "sm") -> rx.Component:
    """Patient avatar with initials.

    Args:
        name: Patient's full name (extracts first letter)
        size: "sm" (8x8) or "lg" (12x12)
    """
    size_classes = {
        "sm": "w-8 h-8 text-xs",
        "lg": "w-12 h-12 text-lg",
    }
    return rx.el.div(
        rx.el.span(name[0], class_name="font-bold text-teal-300"),
        class_name=f"{size_classes.get(size, size_classes['sm'])} rounded-full bg-teal-500/20 flex items-center justify-center border border-teal-500/30",
    )


def patient_dropdown_item(
    patient: dict,
    on_select_handler,
    additional_handlers: list | None = None,
) -> rx.Component:
    """Reusable patient dropdown item.

    Args:
        patient: Patient dict with id, full_name, email
        on_select_handler: Handler to call with patient["id"]
        additional_handlers: Optional additional handlers to chain
    """
    handlers = [on_select_handler(patient["id"])]
    if additional_handlers:
        handlers.extend(additional_handlers)

    return rx.el.div(
        rx.el.div(
            patient_avatar(patient["full_name"], "sm"),
            rx.el.div(
                rx.el.p(
                    patient["full_name"], class_name="text-sm font-medium text-white"
                ),
                rx.el.p(patient["email"], class_name="text-xs text-slate-400"),
                class_name="ml-3",
            ),
            class_name="flex items-center",
        ),
        on_click=handlers,
        class_name="p-3 hover:bg-slate-700/50 cursor-pointer transition-colors border-b border-slate-700/30 last:border-0",
    )


def _patient_item_for_health(patient: dict) -> rx.Component:
    """Patient item configured for health tab selection."""
    return patient_dropdown_item(
        patient,
        PatientState.select_patient_by_id,
        [
            HealthDashboardState.load_patient_health_data(patient["id"]),
            BiomarkerState.load_biomarkers,
        ],
    )


# =============================================================================
# PATIENT SEARCH & SELECTION
# =============================================================================


def patient_search_dropdown() -> rx.Component:
    """Patient search dropdown with recently active quick access."""
    return rx.el.div(
        # Search input
        rx.el.div(
            rx.el.label(
                "Select Patient",
                class_name="text-sm font-medium text-slate-300 mb-2 block",
            ),
            search_input(
                placeholder="Search patients by name or email...",
                value=PatientState.search_query,
                on_change=PatientState.set_search_query,
            ),
            class_name="mb-4",
        ),
        # Search results (when searching)
        rx.cond(
            PatientState.search_query != "",
            rx.el.div(
                rx.foreach(
                    PatientState.search_filtered_patients,
                    _patient_item_for_health,
                ),
                class_name=f"{GlassStyles.PANEL} mt-2 max-h-60 overflow-y-auto",
            ),
        ),
        # Recently active (when not searching)
        rx.cond(
            PatientState.search_query == "",
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
                    PatientState.recently_active_patients.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            PatientState.recently_active_patients,
                            _patient_item_for_health,
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


def selected_patient_header() -> rx.Component:
    """Header showing selected patient info with clear button."""
    return rx.el.div(
        rx.el.div(
            patient_avatar(PatientState.selected_patient["full_name"], "lg"),
            rx.el.div(
                rx.el.h3(
                    PatientState.selected_patient["full_name"],
                    class_name="text-lg font-semibold text-white",
                ),
                rx.el.p(
                    PatientState.selected_patient["email"],
                    class_name="text-sm text-slate-400",
                ),
                class_name="ml-4",
            ),
            class_name="flex items-center",
        ),
        rx.el.button(
            rx.icon("x", class_name="w-4 h-4"),
            "Clear Selection",
            on_click=[
                PatientState.clear_selected_patient,
                HealthDashboardState.clear_patient_health_data,
            ],
            class_name="px-3 py-2 text-sm text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-lg flex items-center gap-2 transition-all",
        ),
        class_name="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl border border-slate-700/50 mb-6",
    )


# =============================================================================
# HEALTH VIEW TABS & CONTENT
# =============================================================================


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
    """Analytics content - collapsible biomarker panels with charts."""
    return rx.cond(
        BiomarkerState.is_loading,
        loading_spinner("Loading biomarker data..."),
        rx.el.div(
            # Header with title and panel count
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Biomarker Analytics",
                        class_name=f"text-2xl {GlassStyles.HEADING_LIGHT}",
                    ),
                    rx.el.p(
                        "Click panels to expand and view detailed metrics with trend charts",
                        class_name="text-slate-400 mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.span(
                        BiomarkerState.total_panel_count,
                        class_name="text-sm font-semibold text-teal-300",
                    ),
                    rx.el.span(" panels", class_name="text-sm text-slate-400"),
                    class_name="px-3 py-1 bg-slate-800/50 rounded-full border border-slate-700/50",
                ),
                class_name="flex items-start justify-between mb-6",
            ),
            collapsible_panels_container(BiomarkerState.biomarker_panels_limited),
            rx.cond(
                BiomarkerState.has_more_panels,
                rx.el.div(
                    rx.el.a(
                        rx.icon("chart-line", class_name="w-4 h-4 mr-2"),
                        "View All Biomarker Panels",
                        href="/patient/analytics",
                        class_name="inline-flex items-center px-4 py-2 text-sm font-medium text-teal-300 bg-teal-500/10 border border-teal-500/30 rounded-lg hover:bg-teal-500/20 transition-colors",
                    ),
                    class_name="mt-6 text-center",
                ),
            ),
        ),
    )


def _patient_content() -> rx.Component:
    """Content area showing selected patient's data with tabs."""
    return rx.fragment(
        selected_patient_header(),
        _tabs_navigation(),
        rx.match(
            HealthDashboardState.active_tab,
            ("overview", _health_overview_content()),
            ("analytics", _analytics_content()),
            _health_overview_content(),
        ),
    )


# =============================================================================
# MAIN TAB COMPONENT
# =============================================================================


def patient_health_tab() -> rx.Component:
    """Patient health tab for admin to view patient metrics.

    Uses PatientState for patient selection and data.
    Patient data is loaded on dashboard mount via PatientState.load_patients.
    """
    return rx.el.div(
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
        rx.cond(
            PatientState.has_selected_patient,
            _patient_content(),
            rx.el.div(
                patient_search_dropdown(),
                empty_state(
                    icon="user-search",
                    message="Select a patient to view their health data",
                ),
            ),
        ),
        # No on_mount needed - data loaded on admin dashboard mount
    )
