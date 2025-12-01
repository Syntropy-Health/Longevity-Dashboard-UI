import reflex as rx
from ..components.layout import authenticated_layout
from ..states.treatment_search_state import TreatmentSearchState, TreatmentProtocol
from ..config import current_config
from ..styles import GlassStyles


def treatment_card(protocol: TreatmentProtocol) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    protocol["category"],
                    class_name="px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-sky-50/60 text-sky-700 mb-3 inline-block border border-sky-100/60 backdrop-blur-sm",
                ),
                rx.el.h3(
                    protocol["name"],
                    class_name="text-xl font-medium text-gray-800 mb-2 tracking-tight",
                ),
                rx.el.p(
                    protocol["description"],
                    class_name="text-sm text-gray-500 line-clamp-2 mb-6 font-light leading-relaxed h-10",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("clock", class_name="w-3.5 h-3.5 text-gray-400 mr-1.5"),
                    rx.el.span(
                        protocol["duration"],
                        class_name="text-xs text-gray-600 font-semibold",
                    ),
                    class_name="flex items-center bg-white/40 px-3 py-1.5 rounded-lg border border-white/40 shadow-sm backdrop-blur-sm",
                ),
                rx.el.div(
                    rx.icon(
                        "dollar-sign", class_name="w-3.5 h-3.5 text-gray-400 mr-1.5"
                    ),
                    rx.el.span(
                        f"${protocol['cost']}",
                        class_name="text-xs text-gray-600 font-semibold",
                    ),
                    class_name="flex items-center bg-white/40 px-3 py-1.5 rounded-lg border border-white/40 shadow-sm backdrop-blur-sm",
                ),
                class_name="flex items-center gap-3 mb-6",
            ),
        ),
        rx.el.button(
            "View Details",
            on_click=lambda: TreatmentSearchState.open_details(protocol),
            class_name=f"w-full py-3 text-sm font-semibold {current_config.glass_button_secondary} rounded-xl transition-all duration-300",
        ),
        class_name=f"{current_config.glass_panel_style} p-6 flex flex-col justify-between h-full {current_config.glass_card_hover}",
    )


def treatment_details_modal() -> rx.Component:
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


def treatment_search_page() -> rx.Component:
    return authenticated_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Treatment Library",
                    class_name="text-3xl font-light text-gray-900 tracking-tight",
                ),
                rx.el.p(
                    "Explore and request specialized longevity treatments",
                    class_name="text-gray-500 mt-1 text-lg font-light",
                ),
                class_name="mb-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="w-5 h-5 text-gray-400 absolute left-4 top-3.5",
                    ),
                    rx.el.input(
                        placeholder="Search treatments...",
                        on_change=TreatmentSearchState.set_search_query,
                        class_name=f"pl-12 w-full py-3 {current_config.glass_input_style} text-sm font-medium",
                    ),
                    class_name="relative flex-1 max-w-md",
                ),
                rx.el.select(
                    rx.el.option("All Categories", value="All"),
                    rx.el.option("IV Therapy", value="IV Therapy"),
                    rx.el.option("Cryotherapy", value="Cryotherapy"),
                    rx.el.option("Supplements", value="Supplements"),
                    rx.el.option("Hormone Therapy", value="Hormone Therapy"),
                    rx.el.option("Physical Therapy", value="Physical Therapy"),
                    rx.el.option("Spa Services", value="Spa Services"),
                    on_change=TreatmentSearchState.set_category_filter,
                    class_name=f"py-3 px-6 {current_config.glass_input_style} cursor-pointer text-sm font-medium text-gray-700",
                ),
                class_name="flex gap-4 mb-10 flex-wrap items-center",
            ),
            rx.el.div(
                rx.foreach(TreatmentSearchState.filtered_treatments, treatment_card),
                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
            ),
            treatment_details_modal(),
        )
    )