"""Shared health metrics components for the Longevity Clinic application.

This module contains reusable health metric display components used in both
patient portal and admin patient health views.
"""

import reflex as rx
from ...styles.constants import GlassStyles
from ...states import HealthDashboardState


def nutrition_summary_cards() -> rx.Component:
    """Nutrition summary cards grid showing calories, protein, carbs, fat."""
    return rx.el.div(
        rx.el.h3(
            "Nutrition Overview",
            class_name="text-lg font-semibold text-white mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("flame", class_name="w-5 h-5 text-orange-400"),
                    class_name="w-10 h-10 rounded-xl bg-orange-500/10 flex items-center justify-center mb-2 border border-orange-500/20",
                ),
                rx.el.p(
                    "Calories",
                    class_name="text-xs text-slate-400 uppercase tracking-wider",
                ),
                rx.el.p(
                    HealthDashboardState.nutrition_summary["total_calories"],
                    class_name="text-2xl font-bold text-white",
                ),
                class_name=f"{GlassStyles.PANEL} p-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("beef", class_name="w-5 h-5 text-red-400"),
                    class_name="w-10 h-10 rounded-xl bg-red-500/10 flex items-center justify-center mb-2 border border-red-500/20",
                ),
                rx.el.p(
                    "Protein",
                    class_name="text-xs text-slate-400 uppercase tracking-wider",
                ),
                rx.el.p(
                    rx.text(
                        HealthDashboardState.nutrition_summary["total_protein"], "g"
                    ),
                    class_name="text-2xl font-bold text-white",
                ),
                class_name=f"{GlassStyles.PANEL} p-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("wheat", class_name="w-5 h-5 text-amber-400"),
                    class_name="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center mb-2 border border-amber-500/20",
                ),
                rx.el.p(
                    "Carbs",
                    class_name="text-xs text-slate-400 uppercase tracking-wider",
                ),
                rx.el.p(
                    rx.text(HealthDashboardState.nutrition_summary["total_carbs"], "g"),
                    class_name="text-2xl font-bold text-white",
                ),
                class_name=f"{GlassStyles.PANEL} p-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("droplet", class_name="w-5 h-5 text-blue-400"),
                    class_name="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center mb-2 border border-blue-500/20",
                ),
                rx.el.p(
                    "Fat",
                    class_name="text-xs text-slate-400 uppercase tracking-wider",
                ),
                rx.el.p(
                    rx.text(HealthDashboardState.nutrition_summary["total_fat"], "g"),
                    class_name="text-2xl font-bold text-white",
                ),
                class_name=f"{GlassStyles.PANEL} p-4",
            ),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-4",
        ),
        class_name="mb-8",
    )


def medications_list() -> rx.Component:
    """Medications list with adherence info."""
    return rx.el.div(
        rx.el.h3(
            "Medications",
            class_name="text-lg font-semibold text-white mb-4",
        ),
        rx.el.div(
            rx.cond(
                HealthDashboardState.medications.length() > 0,
                rx.foreach(
                    HealthDashboardState.medications,
                    lambda med: rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon("pill", class_name="w-4 h-4 text-purple-400"),
                                class_name="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center mr-3 border border-purple-500/20",
                            ),
                            rx.el.div(
                                rx.el.h4(
                                    med["name"],
                                    class_name="text-sm font-semibold text-white",
                                ),
                                rx.el.p(
                                    med["dosage"], class_name="text-xs text-slate-400"
                                ),
                                rx.el.p(
                                    med["frequency"],
                                    class_name="text-xs text-slate-500",
                                ),
                            ),
                            class_name="flex items-center flex-1",
                        ),
                        rx.el.div(
                            rx.el.span(
                                rx.text(med["adherence_rate"], "%"),
                                class_name=rx.cond(
                                    med["adherence_rate"] >= 90,
                                    "text-lg font-bold text-teal-400",
                                    "text-lg font-bold text-amber-400",
                                ),
                            ),
                            rx.el.p(
                                "Adherence",
                                class_name="text-[10px] text-slate-400 uppercase",
                            ),
                            class_name="text-right",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 flex items-center justify-between",
                    ),
                ),
                rx.el.p("No medications found", class_name="text-slate-400 text-sm"),
            ),
            class_name="space-y-3",
        ),
        class_name="mb-8",
    )


def conditions_list() -> rx.Component:
    """Health conditions list with status badges."""
    return rx.el.div(
        rx.el.h3(
            "Health Conditions",
            class_name="text-lg font-semibold text-white mb-4",
        ),
        rx.el.div(
            rx.cond(
                HealthDashboardState.conditions.length() > 0,
                rx.foreach(
                    HealthDashboardState.conditions,
                    lambda cond: rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "heart-pulse", class_name="w-4 h-4 text-rose-400"
                                ),
                                class_name="w-10 h-10 rounded-xl bg-rose-500/10 flex items-center justify-center mr-3 border border-rose-500/20",
                            ),
                            rx.el.div(
                                rx.el.h4(
                                    cond["name"],
                                    class_name="text-sm font-semibold text-white",
                                ),
                                rx.el.p(
                                    rx.text("ICD-10: ", cond["icd_code"]),
                                    class_name="text-xs text-slate-400",
                                ),
                                rx.el.p(
                                    rx.text("Diagnosed: ", cond["diagnosed_date"]),
                                    class_name="text-xs text-slate-500",
                                ),
                            ),
                            class_name="flex items-center flex-1",
                        ),
                        rx.el.span(
                            cond["status"],
                            class_name=rx.cond(
                                cond["status"] == "active",
                                "px-2 py-1 text-xs font-medium rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30",
                                rx.cond(
                                    cond["status"] == "managed",
                                    "px-2 py-1 text-xs font-medium rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/30",
                                    "px-2 py-1 text-xs font-medium rounded-full bg-slate-500/20 text-slate-300 border border-slate-500/30",
                                ),
                            ),
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 flex items-center justify-between",
                    ),
                ),
                rx.el.p("No conditions found", class_name="text-slate-400 text-sm"),
            ),
            class_name="space-y-3",
        ),
        class_name="mb-8",
    )


def symptoms_list() -> rx.Component:
    """Symptoms list with trend indicators."""
    return rx.el.div(
        rx.el.h3(
            "Current Symptoms",
            class_name="text-lg font-semibold text-white mb-4",
        ),
        rx.el.div(
            rx.cond(
                HealthDashboardState.symptoms.length() > 0,
                rx.foreach(
                    HealthDashboardState.symptoms,
                    lambda sym: rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "thermometer", class_name="w-4 h-4 text-orange-400"
                                ),
                                class_name="w-10 h-10 rounded-xl bg-orange-500/10 flex items-center justify-center mr-3 border border-orange-500/20",
                            ),
                            rx.el.div(
                                rx.el.h4(
                                    sym["name"],
                                    class_name="text-sm font-semibold text-white",
                                ),
                                rx.el.p(
                                    rx.text("Severity: ", sym["severity"]),
                                    class_name="text-xs text-slate-400",
                                ),
                                rx.el.p(
                                    rx.text("Frequency: ", sym["frequency"]),
                                    class_name="text-xs text-slate-500",
                                ),
                            ),
                            class_name="flex items-center flex-1",
                        ),
                        rx.el.div(
                            rx.match(
                                sym["trend"],
                                (
                                    "improving",
                                    rx.el.span(
                                        "↓ Improving",
                                        class_name="text-xs text-teal-400",
                                    ),
                                ),
                                (
                                    "worsening",
                                    rx.el.span(
                                        "↑ Worsening", class_name="text-xs text-red-400"
                                    ),
                                ),
                                rx.el.span(
                                    "→ Stable", class_name="text-xs text-slate-400"
                                ),
                            ),
                            class_name="text-right",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 flex items-center justify-between",
                    ),
                ),
                rx.el.p("No symptoms tracked", class_name="text-slate-400 text-sm"),
            ),
            class_name="space-y-3",
        ),
        class_name="mb-8",
    )


def food_entries_list() -> rx.Component:
    """Food entries list showing recent meals."""
    return rx.el.div(
        rx.el.h3(
            "Recent Food Entries",
            class_name="text-lg font-semibold text-white mb-4",
        ),
        rx.el.div(
            rx.cond(
                HealthDashboardState.food_entries.length() > 0,
                rx.foreach(
                    HealthDashboardState.food_entries,
                    lambda entry: rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon("utensils", class_name="w-4 h-4 text-teal-400"),
                                class_name="w-10 h-10 rounded-xl bg-teal-500/10 flex items-center justify-center mr-3 border border-teal-500/20",
                            ),
                            rx.el.div(
                                rx.el.h4(
                                    entry["name"],
                                    class_name="text-sm font-semibold text-white",
                                ),
                                rx.el.p(
                                    rx.text(entry["time"], " • ", entry["meal_type"]),
                                    class_name="text-xs text-slate-400",
                                ),
                            ),
                            class_name="flex items-center flex-1",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    entry["calories"],
                                    class_name="text-lg font-bold text-white",
                                ),
                                rx.el.span(
                                    " kcal", class_name="text-xs text-slate-400 ml-1"
                                ),
                                class_name="flex items-baseline",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    rx.text("P:", entry["protein"], "g"),
                                    class_name="text-xs text-red-400 mr-2",
                                ),
                                rx.el.span(
                                    rx.text("C:", entry["carbs"], "g"),
                                    class_name="text-xs text-amber-400 mr-2",
                                ),
                                rx.el.span(
                                    rx.text("F:", entry["fat"], "g"),
                                    class_name="text-xs text-blue-400",
                                ),
                                class_name="flex mt-1",
                            ),
                            class_name="text-right",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 flex items-center justify-between",
                    ),
                ),
                rx.el.p(
                    "No food entries recorded", class_name="text-slate-400 text-sm"
                ),
            ),
            class_name="space-y-3",
        ),
    )


def health_metrics_dashboard() -> rx.Component:
    """Complete health metrics dashboard component.

    This is the main component that displays all health metrics including
    nutrition, medications, conditions, symptoms, and food entries.
    Data is sourced from the database via CDC pipeline.
    """
    return rx.el.div(
        nutrition_summary_cards(),
        medications_list(),
        conditions_list(),
        symptoms_list(),
        food_entries_list(),
    )
