"""Food tracker tab component for patient portal."""

import reflex as rx

from ....components.paginated_view import paginated_list
from ....components.tabs import food_entry_card
from ....states import HealthDashboardState
from ....styles.constants import GlassStyles


def food_tracker_tab() -> rx.Component:
    """Food tracker tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Today's Nutrition", class_name="text-xl font-bold text-white mb-2"
            ),
            rx.el.p(
                "Track your daily food intake and nutrition goals.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        # Nutrition Summary Cards
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("flame", class_name="w-6 h-6 text-orange-400"),
                    class_name="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mb-3 border border-orange-500/20",
                ),
                rx.el.p(
                    "Calories",
                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                ),
                rx.el.div(
                    rx.el.span(
                        HealthDashboardState.nutrition_summary["total_calories"],
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span(
                        f" / {HealthDashboardState.nutrition_summary['goal_calories']}",
                        class_name="text-sm text-slate-400",
                    ),
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("beef", class_name="w-6 h-6 text-red-400"),
                    class_name="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center mb-3 border border-red-500/20",
                ),
                rx.el.p(
                    "Protein",
                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                ),
                rx.el.div(
                    rx.el.span(
                        f"{HealthDashboardState.nutrition_summary['total_protein']:.0f}",
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span("g", class_name="text-sm text-slate-400 ml-1"),
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("wheat", class_name="w-6 h-6 text-amber-400"),
                    class_name="w-12 h-12 rounded-xl bg-amber-500/10 flex items-center justify-center mb-3 border border-amber-500/20",
                ),
                rx.el.p(
                    "Carbs",
                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                ),
                rx.el.div(
                    rx.el.span(
                        f"{HealthDashboardState.nutrition_summary['total_carbs']:.0f}",
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span("g", class_name="text-sm text-slate-400 ml-1"),
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("droplet", class_name="w-6 h-6 text-blue-400"),
                    class_name="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center mb-3 border border-blue-500/20",
                ),
                rx.el.p(
                    "Water",
                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                ),
                rx.el.div(
                    rx.el.span(
                        f"{HealthDashboardState.nutrition_summary['water_intake']:.1f}",
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span("L", class_name="text-sm text-slate-400 ml-1"),
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8",
        ),
        # Food Entries
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Today's Meals", class_name="text-lg font-semibold text-white"
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                    "Add Food",
                    on_click=HealthDashboardState.open_add_food_modal,
                    class_name=GlassStyles.BUTTON_PRIMARY + " flex items-center",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            paginated_list(
                items=HealthDashboardState.food_entries_paginated,
                item_renderer=food_entry_card,
                has_previous=HealthDashboardState.food_entries_has_previous,
                has_next=HealthDashboardState.food_entries_has_next,
                page_info=HealthDashboardState.food_entries_page_info,
                showing_info=HealthDashboardState.food_entries_showing_info,
                on_previous=HealthDashboardState.food_entries_previous_page,
                on_next=HealthDashboardState.food_entries_next_page,
                empty_icon="utensils",
                empty_message="No food entries yet",
                empty_subtitle="Add your first meal to start tracking",
                list_class="space-y-3",
            ),
        ),
    )
