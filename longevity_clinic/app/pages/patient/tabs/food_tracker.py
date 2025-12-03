"""Food tracker tab component for patient portal."""

import reflex as rx
from ....states.patient_dashboard_state import PatientDashboardState
from ....styles.constants import GlassStyles


def food_entry_card(entry: dict) -> rx.Component:
    """Food entry card."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("utensils", class_name="w-4 h-4 text-teal-400"),
                class_name="w-10 h-10 rounded-xl bg-teal-500/10 flex items-center justify-center mr-3 border border-teal-500/20",
            ),
            rx.el.div(
                rx.el.h4(entry["name"], class_name="text-sm font-semibold text-white"),
                rx.el.p(
                    f"{entry['time']} • {entry['meal_type'].capitalize()}",
                    class_name="text-xs text-slate-400",
                ),
            ),
            class_name="flex items-center flex-1",
        ),
        rx.el.div(
            rx.el.span(f"{entry['calories']}", class_name="text-lg font-bold text-white"),
            rx.el.span(" kcal", class_name="text-xs text-slate-400 ml-1"),
            class_name="flex items-baseline",
        ),
        class_name=f"{GlassStyles.PANEL} p-4 flex items-center justify-between hover:bg-white/10 transition-all cursor-pointer",
    )


def food_tracker_tab() -> rx.Component:
    """Food tracker tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Today's Nutrition", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p("Track your daily food intake and nutrition goals.", class_name="text-slate-400 text-sm"),
            class_name="mb-6",
        ),
        # Nutrition Summary Cards
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("flame", class_name="w-6 h-6 text-orange-400"),
                    class_name="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mb-3 border border-orange-500/20",
                ),
                rx.el.p("Calories", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                rx.el.div(
                    rx.el.span(
                        PatientDashboardState.nutrition_summary["total_calories"],
                        class_name="text-3xl font-bold text-white",
                    ),
                    rx.el.span(
                        f" / {PatientDashboardState.nutrition_summary['goal_calories']}",
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
                rx.el.p("Protein", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                rx.el.div(
                    rx.el.span(
                        f"{PatientDashboardState.nutrition_summary['total_protein']:.0f}",
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
                rx.el.p("Carbs", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                rx.el.div(
                    rx.el.span(
                        f"{PatientDashboardState.nutrition_summary['total_carbs']:.0f}",
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
                rx.el.p("Water", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                rx.el.div(
                    rx.el.span(
                        f"{PatientDashboardState.nutrition_summary['water_intake']:.1f}",
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
                rx.el.h3("Today's Meals", class_name="text-lg font-semibold text-white"),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                    "Add Food",
                    on_click=PatientDashboardState.open_add_food_modal,
                    class_name=GlassStyles.BUTTON_PRIMARY + " flex items-center",
                ),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.foreach(PatientDashboardState.food_entries, food_entry_card),
                class_name="space-y-3",
            ),
        ),
    )
