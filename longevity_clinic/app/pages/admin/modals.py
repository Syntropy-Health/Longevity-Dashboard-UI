"""Admin dashboard modal components."""

import reflex as rx
from ...states.patient_state import PatientState
from ...styles import GlassStyles


def add_patient_modal() -> rx.Component:
    """Modal for adding new patients."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(class_name=GlassStyles.MODAL_OVERLAY),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    # Header
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "New Patient Intake",
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
                        # Name and Email row
                        rx.el.div(
                            rx.el.div(
                                rx.el.label("Full Name", class_name=GlassStyles.LABEL),
                                rx.el.input(
                                    type="text",
                                    value=PatientState.new_patient_name,
                                    on_change=PatientState.set_new_patient_name,
                                    placeholder="Enter patient name",
                                    class_name=GlassStyles.MODAL_INPUT,
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Email Address", class_name=GlassStyles.LABEL
                                ),
                                rx.el.input(
                                    type="email",
                                    value=PatientState.new_patient_email,
                                    on_change=PatientState.set_new_patient_email,
                                    placeholder="email@example.com",
                                    class_name=GlassStyles.MODAL_INPUT,
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-4 mb-4",
                        ),
                        # Phone, Age, Gender row
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Phone Number", class_name=GlassStyles.LABEL
                                ),
                                rx.el.input(
                                    type="tel",
                                    value=PatientState.new_patient_phone,
                                    on_change=PatientState.set_new_patient_phone,
                                    placeholder="(555) 123-4567",
                                    class_name=GlassStyles.MODAL_INPUT,
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Age", class_name=GlassStyles.LABEL),
                                rx.el.input(
                                    type="number",
                                    value=PatientState.new_patient_age,
                                    on_change=PatientState.set_new_patient_age,
                                    placeholder="30",
                                    class_name=GlassStyles.MODAL_INPUT,
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Gender", class_name=GlassStyles.LABEL),
                                rx.el.select(
                                    rx.el.option("Select...", value=""),
                                    rx.el.option("Male", value="Male"),
                                    rx.el.option("Female", value="Female"),
                                    rx.el.option("Other", value="Other"),
                                    value=PatientState.new_patient_gender,
                                    on_change=PatientState.set_new_patient_gender,
                                    class_name=GlassStyles.MODAL_SELECT,
                                ),
                            ),
                            class_name="grid grid-cols-3 gap-4 mb-4",
                        ),
                        # Medical History
                        rx.el.div(
                            rx.el.label(
                                "Medical History Summary", class_name=GlassStyles.LABEL
                            ),
                            rx.el.textarea(
                                rows="3",
                                value=PatientState.new_patient_history,
                                on_change=PatientState.set_new_patient_history,
                                placeholder="Enter relevant medical history...",
                                class_name=GlassStyles.MODAL_TEXTAREA,
                            ),
                            class_name="mb-4",
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
                            "Create Patient Profile",
                            on_click=PatientState.add_patient,
                            class_name=GlassStyles.BUTTON_PRIMARY,
                        ),
                        class_name=GlassStyles.MODAL_FOOTER,
                    ),
                ),
                class_name=f"{GlassStyles.MODAL_CONTENT_LG} {GlassStyles.MODAL_PANEL}",
            ),
        ),
        open=PatientState.is_add_patient_open,
        on_open_change=PatientState.handle_add_patient_open_change,
    )


def view_patient_modal() -> rx.Component:
    """Modal for viewing patient details."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(class_name=GlassStyles.MODAL_OVERLAY),
            rx.radix.primitives.dialog.content(
                rx.cond(
                    PatientState.selected_patient,
                    rx.el.div(
                        # Header
                        rx.el.div(
                            rx.radix.primitives.dialog.title(
                                "Patient Profile",
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
                        # Patient avatar and name
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    "P",
                                    class_name="text-2xl font-bold text-teal-300",
                                ),
                                class_name="h-16 w-16 rounded-full bg-teal-500/20 flex items-center justify-center mb-4 mx-auto border border-teal-500/30",
                            ),
                            rx.el.h4(
                                PatientState.selected_patient["full_name"],
                                class_name="text-xl font-bold text-white text-center",
                            ),
                            rx.el.p(
                                PatientState.selected_patient["status"],
                                class_name="text-sm text-center text-teal-400 font-medium mt-1",
                            ),
                            class_name="mb-6",
                        ),
                        # Contact and Medical info
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Contact Information",
                                    class_name="font-semibold text-white mb-2",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "mail", class_name="w-4 h-4 text-slate-400 mr-2"
                                    ),
                                    rx.el.span(
                                        PatientState.selected_patient["email"],
                                        class_name="text-sm text-slate-300",
                                    ),
                                    class_name="flex items-center mb-1",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "phone",
                                        class_name="w-4 h-4 text-slate-400 mr-2",
                                    ),
                                    rx.el.span(
                                        PatientState.selected_patient["phone"],
                                        class_name="text-sm text-slate-300",
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Medical Details",
                                    class_name="font-semibold text-white mb-2",
                                ),
                                rx.el.p(
                                    f"Age: {PatientState.selected_patient['age']} • Gender: {PatientState.selected_patient['gender']}",
                                    class_name="text-sm text-slate-300 mb-1",
                                ),
                                rx.el.p(
                                    f"History: {PatientState.selected_patient['medical_history']}",
                                    class_name="text-sm text-slate-300",
                                ),
                                class_name="mb-4",
                            ),
                            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-slate-800/50 p-4 rounded-xl border border-slate-700/50",
                        ),
                        # Assigned Treatments section
                        rx.el.div(
                            rx.el.h4(
                                "Assigned Treatments",
                                class_name="text-md font-semibold text-white mb-3 mt-2",
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
                                                    class_name="font-medium text-white text-sm",
                                                ),
                                                rx.el.p(
                                                    f"{t['frequency']} • {t['duration']}",
                                                    class_name="text-xs text-slate-400",
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
                                                class_name="p-1 hover:bg-red-500/20 rounded-full transition-colors",
                                            ),
                                            class_name="flex justify-between items-center p-3 bg-slate-800/50 border border-slate-700/50 rounded-xl",
                                        ),
                                    ),
                                    class_name="space-y-2",
                                ),
                                rx.el.p(
                                    "No active treatments assigned.",
                                    class_name="text-sm text-slate-500 italic",
                                ),
                            ),
                            class_name="bg-slate-800/30 p-4 rounded-xl border border-slate-700/30 mt-4",
                        ),
                        # Footer
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Close",
                                    class_name=f"w-full {GlassStyles.BUTTON_SECONDARY}",
                                )
                            ),
                            class_name="mt-6",
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name=f"{GlassStyles.MODAL_CONTENT_LG} {GlassStyles.MODAL_PANEL}",
            ),
        ),
        open=PatientState.is_view_patient_open,
        on_open_change=PatientState.handle_view_patient_open_change,
    )
