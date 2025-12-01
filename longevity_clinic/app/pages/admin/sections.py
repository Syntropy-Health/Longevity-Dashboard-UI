"""Admin dashboard sections (patient management, etc.)."""

import reflex as rx
from ...components.page_components import section_header
from ...states.patient_state import PatientState
from ...styles import GlassStyles
from .components import patient_table_row


def patient_management_section() -> rx.Component:
    """Patient management section with table and filters."""
    return rx.el.div(
        section_header(
            title="Patient Management",
            button_text="Add Patient",
            button_icon="plus",
            button_onclick=PatientState.open_add_patient,
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("search", class_name="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2"),
                rx.el.input(
                    placeholder="Search patients...",
                    on_change=PatientState.set_search_query,
                    class_name="pl-10 block w-full bg-slate-800/50 border border-slate-700/50 rounded-xl text-white placeholder-slate-500 sm:text-sm py-2.5 focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500/50",
                    default_value=PatientState.search_query,
                ),
                class_name="relative flex-1 max-w-xs mr-4",
            ),
            rx.el.select(
                rx.el.option("All Statuses", value="All"),
                rx.el.option("Active", value="Active"),
                rx.el.option("Inactive", value="Inactive"),
                rx.el.option("Onboarding", value="Onboarding"),
                value=PatientState.status_filter,
                on_change=PatientState.set_status_filter,
                class_name="block bg-slate-800/50 border border-slate-700/50 rounded-xl text-white py-2.5 pl-3 pr-10 text-sm mr-4 focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500/50",
            ),
            rx.el.select(
                rx.el.option("Sort by Name", value="name"),
                rx.el.option("Recent Visit", value="recent"),
                rx.el.option("Biomarker Score", value="score"),
                value=PatientState.sort_key,
                on_change=PatientState.set_sort_key,
                class_name="block bg-slate-800/50 border border-slate-700/50 rounded-xl text-white py-2.5 pl-3 pr-10 text-sm focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500/50",
            ),
            class_name="flex flex-wrap items-center mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Patient",
                            class_name="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Age",
                            class_name="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Last Visit",
                            class_name="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Wellness Score",
                            class_name="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            rx.el.span("Actions", class_name="sr-only"),
                            class_name="px-6 py-3 relative",
                        ),
                    ),
                    class_name="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700/50",
                ),
                rx.el.tbody(
                    rx.foreach(PatientState.filtered_patients, patient_table_row),
                    class_name="bg-slate-900/30",
                ),
                class_name="min-w-full",
            ),
            class_name="overflow-hidden border border-slate-700/50 rounded-2xl overflow-x-auto",
        ),
        class_name=f"{GlassStyles.PANEL} p-6",
    )
