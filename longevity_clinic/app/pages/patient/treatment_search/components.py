"""Patient treatment search components."""

import reflex as rx
from ....states import TreatmentSearchState, TreatmentProtocol
from ....config import current_config


def treatment_card(protocol: TreatmentProtocol) -> rx.Component:
    """Treatment protocol card for patient browsing."""
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
