import reflex as rx

from ..components.layout import authenticated_layout
from ..components.page_components import page_header
from ..config import current_config
from ..data import (
    TREATMENT_CATEGORIES,
    TREATMENT_FREQUENCIES,
    TREATMENT_STATUSES,
)
from ..states.patient_state import PatientState
from ..states.treatment_state import TreatmentProtocol, TreatmentState
from ..styles import styles, GlassStyles


def category_badge(category: str) -> rx.Component:
    category_styles = {
        "IV Therapy": styles.badges.blue,
        "Cryotherapy": styles.badges.cyan,
        "Supplements": styles.badges.green,
        "Hormone Therapy": styles.badges.purple,
        "Physical Therapy": styles.badges.orange,
        "Spa Services": styles.badges.pink,
    }
    return rx.el.span(
        category,
        class_name=category_styles.get(category, styles.badges.gray),
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


def protocol_filters() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("search", class_name="w-5 h-5 text-gray-400 absolute left-3"),
            rx.el.input(
                placeholder="Search protocols...",
                on_change=TreatmentState.set_search_query,
                class_name=f"pl-10 block w-full {current_config.glass_input_style} sm:text-sm py-2",
            ),
            class_name="relative flex-1 max-w-md mr-4",
        ),
        rx.el.select(
            rx.el.option("All Categories", value="All"),
            *[rx.el.option(cat, value=cat) for cat in TREATMENT_CATEGORIES],
            on_change=TreatmentState.set_category_filter,
            class_name=f"block {current_config.glass_input_style} py-2 pl-3 pr-10 text-base sm:text-sm",
        ),
        class_name="flex flex-wrap items-center mb-6",
    )


def treatment_editor_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name=GlassStyles.MODAL_OVERLAY
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    # Header
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            rx.cond(
                                TreatmentState.editing_protocol,
                                "Edit Protocol",
                                "New Treatment Protocol",
                            ),
                            class_name=GlassStyles.MODAL_TITLE,
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name=GlassStyles.CLOSE_BUTTON,
                            )
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    # Form fields
                    rx.el.div(
                        # Protocol Name
                        rx.el.div(
                            rx.el.label("Protocol Name", class_name=GlassStyles.LABEL),
                            rx.el.input(
                                value=TreatmentState.form_name,
                                on_change=TreatmentState.set_form_name,
                                placeholder="Enter protocol name",
                                class_name=GlassStyles.MODAL_INPUT,
                            ),
                            class_name="mb-4",
                        ),
                        # Category and Status row
                        rx.el.div(
                            rx.el.div(
                                rx.el.label("Category", class_name=GlassStyles.LABEL),
                                rx.el.select(
                                    *[rx.el.option(cat, value=cat) for cat in TREATMENT_CATEGORIES],
                                    value=TreatmentState.form_category,
                                    on_change=TreatmentState.set_form_category,
                                    class_name=GlassStyles.MODAL_SELECT,
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Status", class_name=GlassStyles.LABEL),
                                rx.el.select(
                                    *[rx.el.option(status, value=status) for status in TREATMENT_STATUSES],
                                    value=TreatmentState.form_status,
                                    on_change=TreatmentState.set_form_status,
                                    class_name=GlassStyles.MODAL_SELECT,
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-4 mb-4",
                        ),
                        # Description
                        rx.el.div(
                            rx.el.label("Description", class_name=GlassStyles.LABEL),
                            rx.el.textarea(
                                value=TreatmentState.form_description,
                                on_change=TreatmentState.set_form_description,
                                placeholder="Enter protocol description",
                                rows="3",
                                class_name=GlassStyles.MODAL_TEXTAREA,
                            ),
                            class_name="mb-4",
                        ),
                        # Duration, Frequency, Cost row
                        rx.el.div(
                            rx.el.div(
                                rx.el.label("Duration", class_name=GlassStyles.LABEL),
                                rx.el.input(
                                    placeholder="e.g., 60 mins",
                                    value=TreatmentState.form_duration,
                                    on_change=TreatmentState.set_form_duration,
                                    class_name=GlassStyles.MODAL_INPUT,
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Frequency", class_name=GlassStyles.LABEL),
                                rx.el.select(
                                    *[rx.el.option(freq, value=freq) for freq in TREATMENT_FREQUENCIES],
                                    value=TreatmentState.form_frequency,
                                    on_change=TreatmentState.set_form_frequency,
                                    class_name=GlassStyles.MODAL_SELECT,
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Cost ($)", class_name=GlassStyles.LABEL),
                                rx.el.input(
                                    type="number",
                                    placeholder="150.00",
                                    value=TreatmentState.form_cost,
                                    on_change=TreatmentState.set_form_cost,
                                    class_name=GlassStyles.MODAL_INPUT,
                                ),
                            ),
                            class_name="grid grid-cols-3 gap-4 mb-6",
                        ),
                    ),
                    # Footer buttons
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                type="button",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            )
                        ),
                        rx.el.button(
                            "Save Protocol",
                            on_click=TreatmentState.save_protocol,
                            class_name=GlassStyles.BUTTON_PRIMARY,
                        ),
                        class_name=GlassStyles.MODAL_FOOTER,
                    ),
                ),
                class_name=f"{GlassStyles.MODAL_CONTENT_LG} {GlassStyles.MODAL_PANEL}",
            ),
        ),
        open=TreatmentState.is_editor_open,
        on_open_change=TreatmentState.handle_editor_open_change,
    )


def assignment_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name=GlassStyles.MODAL_OVERLAY
            ),
            rx.radix.primitives.dialog.content(
                rx.cond(
                    TreatmentState.protocol_to_assign,
                    rx.el.div(
                        # Header
                        rx.el.div(
                            rx.radix.primitives.dialog.title(
                                "Assign Treatment Protocol",
                                class_name=GlassStyles.MODAL_TITLE,
                            ),
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    rx.icon("x", class_name="w-5 h-5"),
                                    class_name=GlassStyles.CLOSE_BUTTON,
                                )
                            ),
                            class_name="flex justify-between items-center mb-4",
                        ),
                        # Protocol info
                        rx.radix.primitives.dialog.description(
                            rx.el.div(
                                rx.el.span("Assigning: ", class_name="text-gray-500"),
                                rx.el.span(
                                    TreatmentState.protocol_to_assign["name"],
                                    class_name="font-semibold text-emerald-700",
                                ),
                            ),
                            class_name="bg-emerald-50/50 p-3 rounded-xl border border-emerald-100/50 mb-6",
                        ),
                        # Patient selector
                        rx.el.div(
                            rx.el.label("Select Patient", class_name=GlassStyles.LABEL),
                            rx.el.select(
                                rx.el.option("Select a patient...", value=""),
                                rx.foreach(
                                    PatientState.patients,
                                    lambda p: rx.el.option(p["full_name"], value=p["id"]),
                                ),
                                value=TreatmentState.selected_patient_id_for_assignment,
                                on_change=TreatmentState.set_selected_patient_id_for_assignment,
                                class_name=GlassStyles.MODAL_SELECT,
                            ),
                            class_name="mb-6",
                        ),
                        # Footer buttons
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Cancel",
                                    type="button",
                                    class_name=GlassStyles.BUTTON_SECONDARY,
                                )
                            ),
                            rx.el.button(
                                "Confirm Assignment",
                                on_click=TreatmentState.confirm_assignment,
                                disabled=TreatmentState.selected_patient_id_for_assignment == "",
                                class_name=f"{GlassStyles.BUTTON_PRIMARY} disabled:opacity-50 disabled:cursor-not-allowed",
                            ),
                            class_name=GlassStyles.MODAL_FOOTER,
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name=f"{GlassStyles.MODAL_CONTENT_MD} {GlassStyles.MODAL_PANEL}",
            ),
        ),
        open=TreatmentState.is_assign_open,
        on_open_change=TreatmentState.handle_assign_open_change,
    )


def treatments_page() -> rx.Component:
    return authenticated_layout(
        rx.el.div(
            page_header(
                "Treatment Protocols",
                button_text="Create Protocol",
                button_icon="plus",
                button_onclick=TreatmentState.open_add_modal,
            ),
            protocol_filters(),
            rx.el.div(
                rx.foreach(TreatmentState.filtered_protocols, protocol_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            treatment_editor_modal(),
            assignment_modal(),
        )
    )