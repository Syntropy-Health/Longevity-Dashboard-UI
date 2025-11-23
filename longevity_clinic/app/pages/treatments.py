import reflex as rx
from ..components.layout import authenticated_layout
from ..states.treatment_state import TreatmentState, TreatmentProtocol
from ..states.patient_state import PatientState

from ..config import current_config


def category_badge(category: str) -> rx.Component:
    colors = {
        "IV Therapy": "bg-blue-100 text-blue-800",
        "Cryotherapy": "bg-cyan-100 text-cyan-800",
        "Supplements": "bg-green-100 text-green-800",
        "Hormone Therapy": "bg-purple-100 text-purple-800",
        "Physical Therapy": "bg-orange-100 text-orange-800",
        "Spa Services": "bg-pink-100 text-pink-800",
    }
    return rx.el.span(
        category,
        class_name=rx.match(
            category,
            (
                "IV Therapy",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
            ),
            (
                "Cryotherapy",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-cyan-100 text-cyan-800",
            ),
            (
                "Supplements",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
            ),
            (
                "Hormone Therapy",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800",
            ),
            (
                "Physical Therapy",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800",
            ),
            (
                "Spa Services",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-pink-100 text-pink-800",
            ),
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
        ),
    )




def protocol_card(protocol: TreatmentProtocol) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    protocol["name"],
                    class_name="text-lg font-semibold text-gray-900 truncate",
                ),
                category_badge(protocol["category"]),
                class_name="flex justify-between items-start gap-2 mb-2",
            ),
            rx.el.p(
                protocol["description"],
                class_name="text-sm text-gray-500 line-clamp-2 mb-4 h-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("clock", class_name="w-4 h-4 text-gray-400 mr-1.5"),
                    rx.el.span(
                        protocol["duration"], class_name="text-xs text-gray-600"
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.icon("repeat", class_name="w-4 h-4 text-gray-400 mr-1.5"),
                    rx.el.span(
                        protocol["frequency"], class_name="text-xs text-gray-600"
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.icon("dollar-sign", class_name="w-4 h-4 text-gray-400 mr-1.5"),
                    rx.el.span(
                        f"${protocol['cost']}", class_name="text-xs text-gray-600"
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center justify-between mt-auto pt-4 border-t border-gray-100/50",
            ),
            class_name="p-5 flex-1 flex flex-col",
        ),
        rx.el.div(
            rx.el.button(
                "Edit",
                on_click=lambda: TreatmentState.open_edit_modal(protocol),
                class_name="flex-1 py-3 text-sm font-medium text-gray-700 hover:text-emerald-600 hover:bg-emerald-50/50 border-r border-gray-200/50 transition-colors",
            ),
            rx.el.button(
                "Assign",
                on_click=lambda: TreatmentState.open_assign_modal(protocol),
                class_name="flex-1 py-3 text-sm font-medium text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50/50 transition-colors",
            ),
            class_name="flex border-t border-gray-200/50",
        ),
        class_name=f"{current_config.glass_panel_style} rounded-lg flex flex-col hover:shadow-lg transition-shadow duration-200",
    )


def treatment_editor_modal() -> rx.Component:
    return rx.cond(
        TreatmentState.is_editor_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity",
                on_click=TreatmentState.close_editor,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            rx.cond(
                                TreatmentState.editing_protocol,
                                "Edit Protocol",
                                "New Treatment Protocol",
                            ),
                            class_name="text-lg leading-6 font-medium text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6 text-gray-400"),
                            on_click=TreatmentState.close_editor,
                            class_name="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none",
                        ),
                        class_name="flex justify-between items-center mb-5 pb-4 border-b",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Protocol Name",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                on_change=TreatmentState.set_form_name,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                                default_value=TreatmentState.form_name,
                            ),
                            class_name="col-span-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Category",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.select(
                                rx.el.option("IV Therapy", value="IV Therapy"),
                                rx.el.option("Cryotherapy", value="Cryotherapy"),
                                rx.el.option("Supplements", value="Supplements"),
                                rx.el.option(
                                    "Hormone Therapy", value="Hormone Therapy"
                                ),
                                rx.el.option(
                                    "Physical Therapy", value="Physical Therapy"
                                ),
                                rx.el.option("Spa Services", value="Spa Services"),
                                value=TreatmentState.form_category,
                                on_change=TreatmentState.set_form_category,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                            ),
                            class_name="col-span-6 sm:col-span-3",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Status",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.select(
                                rx.el.option("Active", value="Active"),
                                rx.el.option("Archived", value="Archived"),
                                rx.el.option("Draft", value="Draft"),
                                value=TreatmentState.form_status,
                                on_change=TreatmentState.set_form_status,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                            ),
                            class_name="col-span-6 sm:col-span-3",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Description",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.textarea(
                                on_change=TreatmentState.set_form_description,
                                rows=3,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                                default_value=TreatmentState.form_description,
                            ),
                            class_name="col-span-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Duration (e.g. 60 mins)",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                on_change=TreatmentState.set_form_duration,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                                default_value=TreatmentState.form_duration,
                            ),
                            class_name="col-span-6 sm:col-span-2",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Frequency",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.select(
                                rx.el.option("Daily", value="Daily"),
                                rx.el.option("Weekly", value="Weekly"),
                                rx.el.option("Bi-Weekly", value="Bi-Weekly"),
                                rx.el.option("Monthly", value="Monthly"),
                                rx.el.option("As-needed", value="As-needed"),
                                value=TreatmentState.form_frequency,
                                on_change=TreatmentState.set_form_frequency,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                            ),
                            class_name="col-span-6 sm:col-span-2",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Cost ($)",
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.input(
                                type="number",
                                on_change=TreatmentState.set_form_cost,
                                class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm",
                                default_value=TreatmentState.form_cost,
                            ),
                            class_name="col-span-6 sm:col-span-2",
                        ),
                        class_name="grid grid-cols-6 gap-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=TreatmentState.close_editor,
                            class_name="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 mr-3",
                        ),
                        rx.el.button(
                            "Save Protocol",
                            on_click=TreatmentState.save_protocol,
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


def assignment_modal() -> rx.Component:
    return rx.cond(
        TreatmentState.is_assign_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity",
                on_click=TreatmentState.close_assign_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Assign Treatment Protocol",
                            class_name="text-lg leading-6 font-medium text-gray-900",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6 text-gray-400"),
                            on_click=TreatmentState.close_assign_modal,
                            class_name="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none",
                        ),
                        class_name="flex justify-between items-center mb-5 pb-4 border-b",
                    ),
                    rx.el.div(
                        rx.el.p(
                            f"Assigning: {TreatmentState.protocol_to_assign['name']}",
                            class_name="text-sm font-medium text-emerald-700 mb-4 bg-emerald-50 p-3 rounded-md border border-emerald-100",
                        ),
                        rx.el.label(
                            "Select Patient",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.el.select(
                            rx.el.option("Select a patient...", value=""),
                            rx.foreach(
                                PatientState.patients,
                                lambda p: rx.el.option(p["full_name"], value=p["id"]),
                            ),
                            on_change=TreatmentState.set_selected_patient_id_for_assignment,
                            class_name="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm rounded-md border",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=TreatmentState.close_assign_modal,
                            class_name="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 mr-3",
                        ),
                        rx.el.button(
                            "Confirm Assignment",
                            on_click=TreatmentState.confirm_assignment,
                            disabled=TreatmentState.selected_patient_id_for_assignment
                            == "",
                            class_name="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed",
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name="bg-white rounded-lg px-4 pt-5 pb-4 overflow-hidden shadow-xl transform transition-all sm:max-w-md sm:w-full sm:p-6",
                ),
                class_name="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0 flex items-center justify-center",
            ),
            class_name="fixed z-30 inset-0 overflow-y-auto",
        ),
    )


def treatments_page() -> rx.Component:
    return authenticated_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Treatment Protocols", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                    "Create Protocol",
                    on_click=TreatmentState.open_add_modal,
                    class_name=f"flex items-center px-4 py-2 {current_config.glass_button_primary} text-sm font-medium rounded-xl transition-all",
                ),
                class_name="flex justify-between items-center mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search", class_name="w-5 h-5 text-gray-400 absolute left-3"
                    ),
                    rx.el.input(
                        placeholder="Search protocols...",
                        on_change=TreatmentState.set_search_query,
                        class_name=f"pl-10 block w-full {current_config.glass_input_style} sm:text-sm py-2",
                    ),
                    class_name="relative flex-1 max-w-md mr-4",
                ),
                rx.el.select(
                    rx.el.option("All Categories", value="All"),
                    rx.el.option("IV Therapy", value="IV Therapy"),
                    rx.el.option("Cryotherapy", value="Cryotherapy"),
                    rx.el.option("Supplements", value="Supplements"),
                    rx.el.option("Hormone Therapy", value="Hormone Therapy"),
                    rx.el.option("Physical Therapy", value="Physical Therapy"),
                    rx.el.option("Spa Services", value="Spa Services"),
                    on_change=TreatmentState.set_category_filter,
                    class_name=f"block {current_config.glass_input_style} py-2 pl-3 pr-10 text-base sm:text-sm",
                ),
                class_name="flex flex-wrap items-center mb-6",
            ),
            rx.el.div(
                rx.foreach(TreatmentState.filtered_protocols, protocol_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            treatment_editor_modal(),
            assignment_modal(),
        )
    )