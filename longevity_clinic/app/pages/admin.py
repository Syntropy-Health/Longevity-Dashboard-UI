import reflex as rx
from ..components.layout import authenticated_layout
from ..states.auth_state import AuthState
from ..states.patient_state import PatientState, Patient
from ..components.charts import (
    overview_trend_chart,
    treatment_distribution_chart,
    biomarker_improvement_chart,
)
from ..config import current_config


def stat_card(
    title: str, value: str, trend: str, trend_up: bool, icon: str
) -> rx.Component:
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
                rx.icon(icon, class_name="w-6 h-6 text-emerald-600"),
                class_name="p-3 bg-emerald-50/50 rounded-2xl border border-emerald-100/50",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.span(
                trend,
                class_name=rx.cond(
                    trend_up,
                    "text-emerald-600 text-sm font-medium",
                    "text-red-600 text-sm font-medium",
                ),
            ),
            rx.el.span(" from last month", class_name="text-sm text-gray-500 ml-2"),
            class_name="mt-4",
        ),
        class_name=f"{current_config.glass_panel_style} p-6 {current_config.glass_card_hover}",
    )


def chart_card(title: str, chart: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-bold text-gray-800 mb-6"),
        rx.el.div(chart, class_name="w-full h-64"),
        class_name=f"{current_config.glass_panel_style} p-6 rounded-2xl",
    )


def patient_table_row(patient: Patient) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.span("P", class_name="text-xs font-bold text-emerald-700"),
                    class_name="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center mr-3",
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
                    "px-2 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800",
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
                    class_name="h-2 rounded-full bg-emerald-500",
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
                class_name="text-emerald-600 hover:text-emerald-900 text-sm font-medium",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
    )


def patient_management_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Patient Management", class_name="text-xl font-bold text-gray-900"
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-4 h-4 mr-2"),
                "Add Patient",
                on_click=PatientState.open_add_patient,
                class_name=f"flex items-center px-4 py-2 {current_config.glass_button_primary} text-sm font-medium rounded-xl transition-all",
            ),
            class_name="flex justify-between items-center mb-6",
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


def add_patient_modal() -> rx.Component:
    return rx.cond(
        PatientState.is_add_patient_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity",
                on_click=PatientState.close_add_patient,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "New Patient Intake",
                            class_name="text-lg leading-6 font-medium text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6 text-gray-400"),
                            on_click=PatientState.close_add_patient,
                            class_name="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none",
                        ),
                        class_name="flex justify-between items-center mb-5",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Full Name",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                type="text",
                                on_change=PatientState.set_new_patient_name,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                                default_value=PatientState.new_patient_name,
                            ),
                            class_name="col-span-6 sm:col-span-3",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Email Address",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                type="email",
                                on_change=PatientState.set_new_patient_email,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                                default_value=PatientState.new_patient_email,
                            ),
                            class_name="col-span-6 sm:col-span-3",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Phone Number",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                type="tel",
                                on_change=PatientState.set_new_patient_phone,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                                default_value=PatientState.new_patient_phone,
                            ),
                            class_name="col-span-6 sm:col-span-3",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Age",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                type="number",
                                on_change=PatientState.set_new_patient_age,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                                default_value=PatientState.new_patient_age,
                            ),
                            class_name="col-span-6 sm:col-span-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Gender",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.select(
                                rx.el.option("Select...", value=""),
                                rx.el.option("Male", value="Male"),
                                rx.el.option("Female", value="Female"),
                                rx.el.option("Other", value="Other"),
                                value=PatientState.new_patient_gender,
                                on_change=PatientState.set_new_patient_gender,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                            ),
                            class_name="col-span-6 sm:col-span-2",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Medical History Summary",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.textarea(
                                rows=3,
                                on_change=PatientState.set_new_patient_history,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                                default_value=PatientState.new_patient_history,
                            ),
                            class_name="col-span-6",
                        ),
                        class_name="grid grid-cols-6 gap-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=PatientState.close_add_patient,
                            class_name="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 mr-3",
                        ),
                        rx.el.button(
                            "Create Patient Profile",
                            on_click=PatientState.add_patient,
                            class_name="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500",
                        ),
                        class_name="mt-8 flex justify-end",
                    ),
                    class_name="bg-white rounded-lg px-4 pt-5 pb-4 overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full sm:p-6",
                ),
                class_name="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0 flex items-center justify-center",
            ),
            class_name="fixed z-30 inset-0 overflow-y-auto",
        ),
    )


def view_patient_modal() -> rx.Component:
    return rx.cond(
        PatientState.is_view_patient_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity",
                on_click=PatientState.close_view_patient,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Patient Profile",
                            class_name="text-lg leading-6 font-medium text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6 text-gray-400"),
                            on_click=PatientState.close_view_patient,
                            class_name="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none",
                        ),
                        class_name="flex justify-between items-center mb-5 border-b pb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    "P",
                                    class_name="text-2xl font-bold text-emerald-700",
                                ),
                                class_name="h-16 w-16 rounded-full bg-emerald-100 flex items-center justify-center mb-4 mx-auto",
                            ),
                            rx.el.h4(
                                PatientState.selected_patient["full_name"],
                                class_name="text-xl font-bold text-gray-900 text-center",
                            ),
                            rx.el.p(
                                PatientState.selected_patient["status"],
                                class_name="text-sm text-center text-emerald-600 font-medium mt-1",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Contact Information",
                                    class_name="font-semibold text-gray-900 mb-2",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "mail", class_name="w-4 h-4 text-gray-400 mr-2"
                                    ),
                                    rx.el.span(
                                        PatientState.selected_patient["email"],
                                        class_name="text-sm text-gray-600",
                                    ),
                                    class_name="flex items-center mb-1",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "phone", class_name="w-4 h-4 text-gray-400 mr-2"
                                    ),
                                    rx.el.span(
                                        PatientState.selected_patient["phone"],
                                        class_name="text-sm text-gray-600",
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Medical Details",
                                    class_name="font-semibold text-gray-900 mb-2",
                                ),
                                rx.el.p(
                                    f"Age: {PatientState.selected_patient['age']} • Gender: {PatientState.selected_patient['gender']}",
                                    class_name="text-sm text-gray-600 mb-1",
                                ),
                                rx.el.p(
                                    f"History: {PatientState.selected_patient['medical_history']}",
                                    class_name="text-sm text-gray-600",
                                ),
                                class_name="mb-4",
                            ),
                            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-gray-50 p-4 rounded-lg",
                        ),
                        rx.el.div(
                            rx.el.h4(
                                "Assigned Treatments",
                                class_name="text-md font-semibold text-gray-900 mb-3 mt-2",
                            ),
                            rx.cond(
                                PatientState.selected_patient[
                                    "assigned_treatments"
                                ].length()
                                > 0,
                                rx.el.div(
                                    rx.foreach(
                                        PatientState.selected_patient[
                                            "assigned_treatments"
                                        ],
                                        lambda t: rx.el.div(
                                            rx.el.div(
                                                rx.el.p(
                                                    t["name"],
                                                    class_name="font-medium text-gray-900 text-sm",
                                                ),
                                                rx.el.p(
                                                    f"{t['frequency']} • {t['duration']}",
                                                    class_name="text-xs text-gray-500",
                                                ),
                                            ),
                                            rx.el.button(
                                                rx.icon(
                                                    "trash-2",
                                                    class_name="w-4 h-4 text-red-400",
                                                ),
                                                on_click=lambda: PatientState.remove_treatment_from_patient(
                                                    PatientState.selected_patient["id"],
                                                    t["id"],
                                                ),
                                                class_name="p-1 hover:bg-red-50 rounded-full transition-colors",
                                            ),
                                            class_name="flex justify-between items-center p-3 bg-white border border-gray-200 rounded-md shadow-sm",
                                        ),
                                    ),
                                    class_name="space-y-2",
                                ),
                                rx.el.p(
                                    "No active treatments assigned.",
                                    class_name="text-sm text-gray-500 italic",
                                ),
                            ),
                            class_name="bg-gray-50 p-4 rounded-lg mt-4",
                        ),
                        class_name="space-y-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Close",
                            on_click=PatientState.close_view_patient,
                            class_name="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 sm:text-sm",
                        ),
                        class_name="mt-6",
                    ),
                    class_name="bg-white rounded-lg px-4 pt-5 pb-4 overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full sm:p-6",
                ),
                class_name="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0 flex items-center justify-center",
            ),
            class_name="fixed z-30 inset-0 overflow-y-auto",
        ),
    )


def admin_dashboard() -> rx.Component:
    return authenticated_layout(
        rx.el.div(
            rx.el.h1(
                "Dashboard Overview", class_name="text-2xl font-bold text-gray-900 mb-8"
            ),
            rx.el.div(
                stat_card("Total Patients", "1,284", "+12%", True, "users"),
                stat_card("Active Protocols", "42", "+4%", True, "activity"),
                stat_card("Appointments Today", "18", "-2%", False, "calendar"),
                stat_card("Avg. Throughput", "45min", "+8%", True, "clock"),
                class_name="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8",
            ),
            rx.el.div(
                chart_card("Patient Growth Trends", overview_trend_chart()),
                chart_card(
                    "Treatment Protocol Distribution", treatment_distribution_chart()
                ),
                chart_card(
                    "Avg. Biomarker Improvements", biomarker_improvement_chart()
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8",
            ),
            patient_management_section(),
            add_patient_modal(),
            view_patient_modal(),
        )
    )