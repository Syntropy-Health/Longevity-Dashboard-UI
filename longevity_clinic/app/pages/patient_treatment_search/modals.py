"""Patient treatment search modals."""

import reflex as rx
from ...states.treatment_search_state import TreatmentSearchState
from ...styles import GlassStyles


def treatment_details_modal() -> rx.Component:
    """Treatment details and request modal."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name=GlassStyles.MODAL_OVERLAY
            ),
            rx.radix.primitives.dialog.content(
                rx.cond(
                    TreatmentSearchState.selected_protocol,
                    rx.el.div(
                        # Header
                        rx.el.div(
                            rx.radix.primitives.dialog.title(
                                "Treatment Details",
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
                        # Protocol name and description
                        rx.el.h4(
                            TreatmentSearchState.selected_protocol["name"],
                            class_name="text-2xl font-semibold text-emerald-700 mb-3",
                        ),
                        rx.radix.primitives.dialog.description(
                            TreatmentSearchState.selected_protocol["description"],
                            class_name="text-gray-600 mb-6 leading-relaxed",
                        ),
                        # Protocol details grid
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    "Category",
                                    class_name="text-[10px] text-gray-400 uppercase font-bold block mb-1 tracking-widest",
                                ),
                                rx.el.span(
                                    TreatmentSearchState.selected_protocol["category"],
                                    class_name="text-sm text-gray-800 font-medium",
                                ),
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Frequency",
                                    class_name="text-[10px] text-gray-400 uppercase font-bold block mb-1 tracking-widest",
                                ),
                                rx.el.span(
                                    TreatmentSearchState.selected_protocol["frequency"],
                                    class_name="text-sm text-gray-800 font-medium",
                                ),
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Duration",
                                    class_name="text-[10px] text-gray-400 uppercase font-bold block mb-1 tracking-widest",
                                ),
                                rx.el.span(
                                    TreatmentSearchState.selected_protocol["duration"],
                                    class_name="text-sm text-gray-800 font-medium",
                                ),
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Cost",
                                    class_name="text-[10px] text-gray-400 uppercase font-bold block mb-1 tracking-widest",
                                ),
                                rx.el.span(
                                    f"${TreatmentSearchState.selected_protocol['cost']}",
                                    class_name="text-sm text-gray-800 font-medium",
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-4 mb-6 bg-emerald-50/50 p-4 rounded-xl border border-emerald-100/50",
                        ),
                        # Notes textarea
                        rx.el.label(
                            "Notes for Provider (Optional)",
                            class_name=GlassStyles.LABEL,
                        ),
                        rx.el.textarea(
                            placeholder="Any specific concerns or questions...",
                            value=TreatmentSearchState.request_note,
                            on_change=TreatmentSearchState.set_request_note,
                            class_name=f"{GlassStyles.MODAL_TEXTAREA} h-28 mb-6",
                        ),
                        # Footer buttons
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Cancel",
                                    type="button",
                                    class_name=GlassStyles.BUTTON_CANCEL,
                                )
                            ),
                            rx.el.button(
                                "Submit Request",
                                on_click=TreatmentSearchState.submit_request,
                                class_name=GlassStyles.BUTTON_PRIMARY,
                            ),
                            class_name="flex justify-end gap-3",
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name=f"{GlassStyles.MODAL_CONTENT_MD} {GlassStyles.MODAL_PANEL}",
            ),
        ),
        open=TreatmentSearchState.is_details_open,
        on_open_change=TreatmentSearchState.handle_details_open_change,
    )
