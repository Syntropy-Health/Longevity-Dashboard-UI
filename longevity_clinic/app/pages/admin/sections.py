"""Admin dashboard sections (patient management, etc.)."""

import reflex as rx

from ...components.page import section_header
from ...components.shared import (
    TABLE_DATA_CELL,
    TABLE_HEADER_CELL,
    TABLE_ROW_HOVER,
    avatar_circle,
    empty_table_state,
    filter_select,
    health_score_bar,
    search_input_box,
    table_loading_skeleton,
    table_status_badge,
)
from ...states import PatientState
from ...styles import GlassStyles

# =============================================================================
# FILTER OPTIONS
# =============================================================================

STATUS_OPTIONS = [
    ("All Statuses", "All"),
    ("Active", "Active"),
    ("Inactive", "Inactive"),
    ("Onboarding", "Onboarding"),
]

SORT_OPTIONS = [
    ("Sort by Name", "name"),
    ("Recent Visit", "recent"),
    ("Overall Health", "score"),
]


# =============================================================================
# TABLE COMPONENTS
# =============================================================================


def _patient_row(patient: dict) -> rx.Component:
    """Single patient table row."""
    return rx.el.tr(
        # Patient info (avatar + name + email)
        rx.el.td(
            rx.el.div(
                avatar_circle(patient["full_name"][0], size="sm"),
                rx.el.div(
                    rx.el.p(
                        patient["full_name"],
                        class_name="text-sm font-medium text-white",
                    ),
                    rx.el.p(
                        patient["email"],
                        class_name="text-xs text-slate-400 truncate max-w-[180px]",
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name=TABLE_DATA_CELL,
        ),
        # Phone
        rx.el.td(
            rx.el.span(
                rx.cond(patient["phone"] != "", patient["phone"], "—"),
                class_name="text-sm text-slate-300",
            ),
            class_name=TABLE_DATA_CELL,
        ),
        # Last visit
        rx.el.td(
            rx.el.span(
                rx.cond(patient["last_visit"] != "", patient["last_visit"], "Never"),
                class_name="text-sm text-slate-300",
            ),
            class_name=TABLE_DATA_CELL,
        ),
        # Status
        rx.el.td(
            table_status_badge(patient["status"]),
            class_name=TABLE_DATA_CELL,
        ),
        # Overall health (score bar)
        rx.el.td(
            health_score_bar(patient["biomarker_score"]),
            class_name=TABLE_DATA_CELL,
        ),
        # Actions
        rx.el.td(
            rx.el.button(
                "View",
                on_click=PatientState.open_view_patient(patient),
                class_name="text-teal-400 hover:text-teal-300 text-sm font-medium",
            ),
            class_name=f"{TABLE_DATA_CELL} text-right",
        ),
        class_name=TABLE_ROW_HOVER,
    )


def _patients_table_header() -> rx.Component:
    """Patient table header row."""
    columns = ["Patient", "Phone", "Last Visit", "Status", "Overall Health", ""]
    return rx.el.thead(
        rx.el.tr(
            *[rx.el.th(col, class_name=TABLE_HEADER_CELL) for col in columns],
        ),
        class_name="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700/50",
    )


def _patients_table() -> rx.Component:
    """Patient table with rows."""
    return rx.el.table(
        _patients_table_header(),
        rx.el.tbody(
            rx.foreach(PatientState.filtered_patients, _patient_row),
            class_name="bg-slate-900/30",
        ),
        class_name="min-w-full",
    )


def _filters_toolbar() -> rx.Component:
    """Filters toolbar with search, status filter, and sort."""
    return rx.el.div(
        search_input_box(
            placeholder="Search patients...",
            value=PatientState.search_query,
            on_change=PatientState.set_search_query,
        ),
        rx.el.div(
            filter_select(
                options=STATUS_OPTIONS,
                value=PatientState.status_filter,
                on_change=PatientState.set_status_filter,
            ),
            filter_select(
                options=SORT_OPTIONS,
                value=PatientState.sort_key,
                on_change=PatientState.set_sort_key,
            ),
            class_name="flex gap-3",
        ),
        class_name="flex flex-wrap items-center justify-between gap-4 mb-6",
    )


# =============================================================================
# MAIN SECTION COMPONENT
# =============================================================================


def patient_management_section() -> rx.Component:
    """Patient management section with table and filters."""
    return rx.el.div(
        section_header(
            title="Patient Management",
            button_text="Add Patient",
            button_icon="plus",
            button_onclick=PatientState.open_add_patient,
        ),
        _filters_toolbar(),
        # Conditional content based on loading/data state
        rx.cond(
            PatientState.is_loading,
            # Loading state
            rx.el.div(
                table_loading_skeleton(rows=5, cols=6),
                class_name="overflow-hidden border border-slate-700/50 rounded-2xl",
            ),
            # Loaded state
            rx.cond(
                PatientState.filtered_patients.length() > 0,
                # Has patients
                rx.el.div(
                    _patients_table(),
                    class_name="overflow-hidden border border-slate-700/50 rounded-2xl overflow-x-auto",
                ),
                # Empty state
                rx.el.div(
                    empty_table_state(
                        "No patients found. Add a patient to get started."
                    ),
                    class_name="border border-slate-700/50 rounded-2xl",
                ),
            ),
        ),
        # Patient count footer
        rx.el.div(
            rx.el.span(
                rx.cond(
                    ~PatientState.is_loading,
                    PatientState.filtered_patients.length().to_string() + " patients",
                    "Loading...",
                ),
                class_name="text-sm text-slate-400",
            ),
            class_name="mt-4 text-right",
        ),
        class_name=f"{GlassStyles.PANEL} p-6",
    )
