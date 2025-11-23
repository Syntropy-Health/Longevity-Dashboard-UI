import reflex as rx
from ..components.layout import authenticated_layout
from ..states.treatment_search_state import TreatmentSearchState, TreatmentProtocol
from ..config import current_config


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
    return rx.cond(
        TreatmentSearchState.is_details_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-slate-900/10 backdrop-blur-[2px] transition-opacity",
                on_click=TreatmentSearchState.close_details,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Treatment Details",
                            class_name="text-xl font-light text-gray-900 tracking-tight",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="w-6 h-6 text-gray-400"),
                            on_click=TreatmentSearchState.close_details,
                            class_name="p-2 hover:bg-gray-100/50 rounded-full transition-colors backdrop-blur-sm",
                        ),
                        class_name="flex justify-between items-center mb-6 pb-4 border-b border-gray-100/50",
                    ),
                    rx.el.div(
                        rx.el.h4(
                            TreatmentSearchState.selected_protocol["name"],
                            class_name="text-2xl font-light text-emerald-800 mb-3",
                        ),
                        rx.el.p(
                            TreatmentSearchState.selected_protocol["description"],
                            class_name="text-gray-600 mb-8 leading-relaxed font-light",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    "Category",
                                    class_name="text-[10px] text-gray-400 uppercase font-bold block mb-2 tracking-widest",
                                ),
                                rx.el.span(
                                    TreatmentSearchState.selected_protocol["category"],
                                    class_name="text-sm text-gray-800 font-medium bg-white/40 px-3 py-1 rounded-lg border border-white/40",
                                ),
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Frequency",
                                    class_name="text-[10px] text-gray-400 uppercase font-bold block mb-2 tracking-widest",
                                ),
                                rx.el.span(
                                    TreatmentSearchState.selected_protocol["frequency"],
                                    class_name="text-sm text-gray-800 font-medium bg-white/40 px-3 py-1 rounded-lg border border-white/40",
                                ),
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Duration",
                                    class_name="text-[10px] text-gray-400 uppercase font-bold block mb-2 tracking-widest",
                                ),
                                rx.el.span(
                                    TreatmentSearchState.selected_protocol["duration"],
                                    class_name="text-sm text-gray-800 font-medium bg-white/40 px-3 py-1 rounded-lg border border-white/40",
                                ),
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Cost",
                                    class_name="text-[10px] text-gray-400 uppercase font-bold block mb-2 tracking-widest",
                                ),
                                rx.el.span(
                                    f"${TreatmentSearchState.selected_protocol['cost']}",
                                    class_name="text-sm text-gray-800 font-medium bg-white/40 px-3 py-1 rounded-lg border border-white/40",
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-6 mb-8 bg-emerald-50/30 p-6 rounded-2xl border border-emerald-100/30 backdrop-blur-sm",
                        ),
                        rx.el.label(
                            "Notes for Provider (Optional)",
                            class_name="block text-xs font-bold text-gray-500 mb-2 uppercase tracking-wider ml-1",
                        ),
                        rx.el.textarea(
                            placeholder="Any specific concerns or questions...",
                            on_change=TreatmentSearchState.set_request_note,
                            class_name=f"w-full p-4 {current_config.glass_input_style} resize-none h-28 mb-8",
                        ),
                        rx.el.button(
                            "Submit Request",
                            on_click=TreatmentSearchState.submit_request,
                            class_name=f"w-full py-4 {current_config.glass_button_primary} font-semibold rounded-2xl transition-all text-lg",
                        ),
                    ),
                    class_name=f"{current_config.glass_panel_style} p-8 max-w-lg w-full shadow-[0_20px_60px_-12px_rgba(0,0,0,0.1)] border border-white/60 backdrop-blur-3xl",
                ),
                class_name="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none",
            ),
            rx.el.div(class_name="pointer-events-auto"),
        ),
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