"""Conditions tab component for patient portal."""

import reflex as rx

from ....components.paginated_view import paginated_list
from ....components.tabs import condition_card
from ....states import ConditionState


def conditions_tab() -> rx.Component:
    """Conditions tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Health Conditions", class_name="text-xl font-bold text-white mb-2"
            ),
            rx.el.p(
                "Track and manage your health conditions.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        # Filter buttons
        rx.el.div(
            rx.el.button(
                rx.fragment("All (", ConditionState.conditions.length(), ")"),
                on_click=lambda: ConditionState.set_conditions_filter_with_reset("all"),
                class_name=rx.cond(
                    ConditionState.conditions_filter == "all",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                f"Active ({ConditionState.active_conditions_count})",
                on_click=lambda: ConditionState.set_conditions_filter_with_reset(
                    "active"
                ),
                class_name=rx.cond(
                    ConditionState.conditions_filter == "active",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-amber-500/20 text-amber-300 border border-amber-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                f"Managed ({ConditionState.managed_conditions_count})",
                on_click=lambda: ConditionState.set_conditions_filter_with_reset(
                    "managed"
                ),
                class_name=rx.cond(
                    ConditionState.conditions_filter == "managed",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                f"Resolved ({ConditionState.resolved_conditions_count})",
                on_click=lambda: ConditionState.set_conditions_filter_with_reset(
                    "resolved"
                ),
                class_name=rx.cond(
                    ConditionState.conditions_filter == "resolved",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-slate-500/20 text-slate-300 border border-slate-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6",
        ),
        # Conditions List (Paginated)
        paginated_list(
            items=ConditionState.conditions_paginated,
            item_renderer=condition_card,
            has_previous=ConditionState.conditions_has_previous,
            has_next=ConditionState.conditions_has_next,
            page_info=ConditionState.conditions_page_info,
            showing_info=ConditionState.conditions_showing_info,
            on_previous=ConditionState.conditions_previous_page,
            on_next=ConditionState.conditions_next_page,
            empty_icon="heart-pulse",
            empty_message="No conditions found",
            empty_subtitle="Your health conditions will appear here",
            list_class="space-y-4",
        ),
        on_mount=ConditionState.load_condition_data,
    )
