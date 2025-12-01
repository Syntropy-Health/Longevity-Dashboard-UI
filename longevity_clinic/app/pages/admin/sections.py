"""Admin dashboard sections (patient management, etc.)."""

import reflex as rx
from ...components.page_components import section_header
from ...states.patient_state import PatientState
from ...config import current_config
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
                rx.icon("search", class_name="w-5 h-5 text-gray-400 absolute left-3"),
                rx.el.input(
                    placeholder="Search patients...",
                    on_change=PatientState.set_search_query,
                    class_name=f"pl-10 block w-full {current_config.glass_input_style} sm:text-sm py-2",
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
                class_name=f"block {current_config.glass_input_style} py-2 pl-3 pr-10 text-base sm:text-sm mr-4",
            ),
            rx.el.select(
                rx.el.option("Sort by Name", value="name"),
                rx.el.option("Recent Visit", value="recent"),
                rx.el.option("Biomarker Score", value="score"),
                value=PatientState.sort_key,
                on_change=PatientState.set_sort_key,
                class_name=f"block {current_config.glass_input_style} py-2 pl-3 pr-10 text-base sm:text-sm",
            ),
            class_name="flex flex-wrap items-center mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Patient",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Age",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Last Visit",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Wellness Score",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            rx.el.span("Actions", class_name="sr-only"),
                            class_name="px-6 py-3 relative",
                        ),
                    ),
                    class_name="bg-gray-50/30 backdrop-blur-sm",
                ),
                rx.el.tbody(
                    rx.foreach(PatientState.filtered_patients, patient_table_row),
                    class_name="bg-white/20 divide-y divide-gray-100/50",
                ),
                class_name="min-w-full divide-y divide-gray-200/50",
            ),
            class_name="shadow-sm overflow-hidden border border-white/50 sm:rounded-2xl overflow-x-auto",
        ),
        class_name=f"{current_config.glass_panel_style} p-6",
    )
