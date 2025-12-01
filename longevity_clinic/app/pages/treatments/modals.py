"""Treatment page modal components."""

import reflex as rx
from ...data import (
    TREATMENT_CATEGORIES,
    TREATMENT_FREQUENCIES,
    TREATMENT_STATUSES,
)
from ...states.patient_state import PatientState
from ...states.treatment_state import TreatmentState
from ...styles import GlassStyles


def treatment_editor_modal() -> rx.Component:
    """Modal for creating and editing treatment protocols."""
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
    """Modal for assigning treatment protocols to patients."""
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
