import reflex as rx
from app.states.nutrition_state import NutritionState
from app.schemas.nutrition import Meal, FoodItem
from app.styles.glass_styles import GlassStyles


def food_item_row(item: FoodItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(item.name, class_name="font-medium text-slate-200"),
            rx.el.p(f"{item.calories} kcal", class_name="text-xs text-slate-500"),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.span(
                f"P: {item.protein}g",
                class_name="text-xs text-blue-400 bg-blue-500/10 px-1.5 py-0.5 rounded border border-blue-500/20 mr-2",
            ),
            rx.el.span(
                f"C: {item.carbs}g",
                class_name="text-xs text-green-400 bg-green-500/10 px-1.5 py-0.5 rounded border border-green-500/20 mr-2",
            ),
            rx.el.span(
                f"F: {item.fat}g",
                class_name="text-xs text-yellow-400 bg-yellow-500/10 px-1.5 py-0.5 rounded border border-yellow-500/20",
            ),
            class_name="flex items-center",
        ),
        class_name="flex justify-between items-center py-2 border-b border-white/5 last:border-0",
    )


def meal_card(meal: Meal) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4(meal.type, class_name="font-bold text-white capitalize"),
            rx.el.span(meal.time, class_name="text-xs text-slate-400"),
            class_name="flex justify-between items-center mb-3",
        ),
        rx.el.div(rx.foreach(meal.food_items, food_item_row), class_name="mb-3"),
        rx.el.div(
            rx.el.span("Total:", class_name="text-sm text-slate-400"),
            rx.el.span(
                f"{meal.total_calories} kcal",
                class_name="text-sm font-bold text-teal-400 ml-2",
            ),
            class_name="flex justify-end items-center pt-2 border-t border-white/10",
        ),
        class_name=f"{GlassStyles.PANEL} p-4",
    )


def nutrition_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Food Tracker", class_name="text-2xl font-bold text-white"),
                rx.el.p(
                    "Track your macros and caloric intake.",
                    class_name="text-slate-400 text-sm",
                ),
            ),
            rx.el.button(
                "+ Log Meal",
                on_click=NutritionState.log_meal,
                class_name=GlassStyles.BUTTON_PRIMARY,
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Daily Summary", class_name="text-lg font-bold text-white mb-4"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Calories",
                            class_name="text-xs text-slate-500 uppercase tracking-wider",
                        ),
                        rx.el.h4(
                            f"{NutritionState.total_calories} / 2500",
                            class_name="text-xl font-bold text-white",
                        ),
                        class_name="bg-white/5 p-3 rounded-xl",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Protein",
                            class_name="text-xs text-slate-500 uppercase tracking-wider",
                        ),
                        rx.el.h4(
                            "45g / 180g", class_name="text-xl font-bold text-blue-400"
                        ),
                        class_name="bg-white/5 p-3 rounded-xl",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Carbs",
                            class_name="text-xs text-slate-500 uppercase tracking-wider",
                        ),
                        rx.el.h4(
                            "120g / 250g", class_name="text-xl font-bold text-green-400"
                        ),
                        class_name="bg-white/5 p-3 rounded-xl",
                    ),
                    class_name="grid grid-cols-3 gap-4 mb-6",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.foreach(NutritionState.current_day.meals, meal_card),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
        ),
        class_name="animate-in fade-in duration-500",
    )