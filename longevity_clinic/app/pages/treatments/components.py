"""Treatment page components."""

import reflex as rx
from ...config import current_config
from ...data import TREATMENT_CATEGORIES
from ...states.treatment_state import TreatmentProtocol, TreatmentState
from ...styles import styles


def category_badge(category: str) -> rx.Component:
    """Category badge with styled colors."""
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
    """Treatment protocol card component."""
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
    """Protocol filter controls."""
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
