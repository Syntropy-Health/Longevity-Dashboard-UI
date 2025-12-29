"""Food tracker tab component for patient portal."""

import reflex as rx

from ....components.modals import food_detail_modal
from ....components.paginated_view import paginated_list
from ....components.tabs import food_entry_card
from ....states import FoodState
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
                        FoodState.nutrition_summary["total_calories"],
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span(
                        f" / {FoodState.nutrition_summary['goal_calories']}",
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
                        f"{FoodState.nutrition_summary['total_protein']:.0f}",
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
                        f"{FoodState.nutrition_summary['total_carbs']:.0f}",
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
                        f"{FoodState.nutrition_summary['water_intake']:.1f}",
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span("L", class_name="text-sm text-slate-400 ml-1"),
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8",
        ),
        # Today's Food Entries
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Today's Meals", class_name="text-lg font-semibold text-white"
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                    "Add Food",
                    on_click=FoodState.open_add_food_modal,
                    class_name=GlassStyles.BUTTON_PRIMARY + " flex items-center",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            paginated_list(
                items=FoodState.todays_meals_paginated,
                item_renderer=food_entry_card,
                has_previous=FoodState.todays_meals_has_previous,
                has_next=FoodState.todays_meals_has_next,
                page_info=FoodState.todays_meals_page_info,
                showing_info=FoodState.todays_meals_showing_info,
                on_previous=FoodState.todays_meals_previous_page,
                on_next=FoodState.todays_meals_next_page,
                empty_icon="utensils",
                empty_message="No food entries yet today",
                empty_subtitle="Add your first meal to start tracking",
                list_class="space-y-3",
            ),
            class_name="mb-8",
        ),
        # Past Meals Section (only shown if there are past meals)
        rx.cond(
            FoodState.has_past_meals,
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Past Meals", class_name="text-lg font-semibold text-white"
                    ),
                    rx.el.span(
                        FoodState.past_meals_count,
                        class_name="text-xs bg-slate-700 text-slate-300 px-2 py-1 rounded-full ml-2",
                    ),
                    class_name="flex items-center mb-4",
                ),
                paginated_list(
                    items=FoodState.past_meals_paginated,
                    item_renderer=food_entry_card,
                    has_previous=FoodState.past_meals_has_previous,
                    has_next=FoodState.past_meals_has_next,
                    page_info=FoodState.past_meals_page_info,
                    showing_info=FoodState.past_meals_showing_info,
                    on_previous=FoodState.past_meals_previous_page,
                    on_next=FoodState.past_meals_next_page,
                    empty_icon="history",
                    empty_message="No past meals",
                    empty_subtitle="",
                    list_class="space-y-3",
                ),
                class_name=f"{GlassStyles.PANEL} p-4 border border-slate-700/50",
            ),
        ),
        # Food detail modal
        food_detail_modal(
            show_modal=FoodState.show_food_detail_modal,
            entry_name=FoodState.selected_food_name,
            entry_calories=FoodState.selected_food_calories,
            entry_protein=FoodState.selected_food_protein,
            entry_carbs=FoodState.selected_food_carbs,
            entry_fat=FoodState.selected_food_fat,
            entry_time=FoodState.selected_food_time,
            entry_meal_type=FoodState.selected_food_meal_type,
            on_close=FoodState.close_food_detail_modal,
        ),
        on_mount=FoodState.load_food_data,
    )
