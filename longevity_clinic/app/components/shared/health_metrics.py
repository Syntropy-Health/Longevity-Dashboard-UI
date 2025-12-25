"""Shared health metrics components for the Longevity Clinic application.

This module provides the health_metrics_dashboard for admin patient health views.
Uses paginated lists with inline card renderers to avoid circular imports.

The dashboard displays:
- Nutrition summary cards (calories, protein, carbs, fat)
- Medications (paginated list with adherence)
- Conditions (paginated list with status)
- Symptoms (paginated list with trends)
- Food entries (paginated list with macros)
"""

import reflex as rx

from ...components.paginated_view import paginated_list
from ...states import HealthDashboardState
from ...styles.constants import GlassStyles

# =============================================================================
# CARD RENDERERS (inline to avoid circular imports with patient tabs)
# =============================================================================


def _medication_card(med) -> rx.Component:
    """Medication Entry card for paginated list."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("pill", class_name="w-5 h-5 text-purple-400"),
                class_name="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center mr-4 border border-purple-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    med.name, class_name="text-base font-semibold text-white mb-1"
                ),
                rx.el.p(med.dosage, class_name="text-sm text-slate-300"),
                rx.cond(
                    med.taken_at != "",
                    rx.el.p(med.taken_at, class_name="text-xs text-slate-400 mt-1"),
                    rx.el.span(),
                ),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.cond(
            med.notes != "",
            rx.el.div(
                rx.el.span(
                    med.notes,
                    class_name="text-xs text-slate-500 truncate max-w-[150px]",
                ),
                class_name="text-right",
            ),
            rx.el.span(),
        ),
        class_name=GlassStyles.CARD_INTERACTIVE + " flex items-center justify-between",
    )


def _condition_card(condition) -> rx.Component:
    """Condition card for paginated list."""
    status_styles = {
        "active": "bg-amber-500/10 text-amber-300 border-amber-500/20",
        "managed": "bg-teal-500/10 text-teal-300 border-teal-500/20",
        "resolved": "bg-slate-500/10 text-slate-300 border-slate-500/20",
    }
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("heart-pulse", class_name="w-5 h-5 text-rose-400"),
                class_name="w-12 h-12 rounded-xl bg-rose-500/10 flex items-center justify-center mr-4 border border-rose-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    condition.name,
                    class_name="text-base font-semibold text-white mb-1",
                ),
                rx.el.p(
                    rx.text("ICD-10: ", condition.icd_code),
                    class_name="text-xs text-slate-400",
                ),
                rx.el.p(
                    rx.text("Diagnosed: ", condition.diagnosed_date),
                    class_name="text-xs text-slate-400 mt-1",
                ),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.span(
                condition.status.capitalize(),
                class_name=rx.match(
                    condition.status,
                    (
                        "active",
                        f"px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border {status_styles['active']}",
                    ),
                    (
                        "managed",
                        f"px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border {status_styles['managed']}",
                    ),
                    (
                        "resolved",
                        f"px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border {status_styles['resolved']}",
                    ),
                    f"px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border {status_styles['active']}",
                ),
            ),
            rx.el.p(
                condition.severity.capitalize(),
                class_name="text-xs text-slate-400 mt-2",
            ),
            class_name="flex flex-col items-end",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def _symptom_card(symptom) -> rx.Component:
    """Symptom card for paginated list."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("thermometer", class_name="w-5 h-5 text-orange-400"),
                class_name="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mr-4 border border-orange-500/20",
            ),
            rx.el.div(
                rx.el.h4(
                    symptom.name,
                    class_name="text-base font-semibold text-white mb-1",
                ),
                rx.el.p(
                    rx.text("Severity: ", symptom.severity.capitalize()),
                    class_name="text-sm text-slate-300",
                ),
                rx.el.p(
                    rx.text("Frequency: ", symptom.frequency),
                    class_name="text-xs text-slate-400 mt-1",
                ),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.match(
                symptom.trend,
                (
                    "improving",
                    rx.el.span("↓ Improving", class_name="text-xs text-teal-400"),
                ),
                (
                    "worsening",
                    rx.el.span("↑ Worsening", class_name="text-xs text-red-400"),
                ),
                rx.el.span("→ Stable", class_name="text-xs text-slate-400"),
            ),
            class_name="flex flex-col items-end",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def _food_entry_card(entry) -> rx.Component:
    """Food entry card for paginated list."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("utensils", class_name="w-4 h-4 text-teal-400"),
                class_name="w-10 h-10 rounded-xl bg-teal-500/10 flex items-center justify-center mr-3 border border-teal-500/20",
            ),
            rx.el.div(
                rx.el.h4(entry.name, class_name="text-sm font-semibold text-white"),
                rx.el.p(
                    rx.text(entry.time, " • ", entry.meal_type.capitalize()),
                    class_name="text-xs text-slate-400",
                ),
            ),
            class_name="flex items-center flex-1",
        ),
        rx.el.div(
            rx.el.span(entry.calories, class_name="text-lg font-bold text-white"),
            rx.el.span(" kcal", class_name="text-xs text-slate-400 ml-1"),
            class_name="flex items-baseline",
        ),
        class_name=f"{GlassStyles.PANEL} p-4 flex items-center justify-between hover:bg-white/10 transition-all cursor-pointer",
    )


# =============================================================================
# NUTRITION SUMMARY
# =============================================================================


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


# =============================================================================
# PAGINATED SECTIONS
# =============================================================================


def medications_section() -> rx.Component:
    """Medications section with paginated list."""
    return rx.el.div(
        rx.el.h3(
            "Medications",
            class_name="text-lg font-semibold text-white mb-4",
        ),
        paginated_list(
            items=HealthDashboardState.medication_entries_paginated,
            item_renderer=_medication_card,
            has_previous=HealthDashboardState.medication_entries_has_previous,
            has_next=HealthDashboardState.medication_entries_has_next,
            page_info=HealthDashboardState.medication_entries_page_info,
            showing_info=HealthDashboardState.medication_entries_showing_info,
            on_previous=HealthDashboardState.medication_entries_previous_page,
            on_next=HealthDashboardState.medication_entries_next_page,
            empty_icon="pill",
            empty_message="No medications found",
            list_class="space-y-3",
        ),
        class_name="mb-8",
    )


def conditions_section() -> rx.Component:
    """Conditions section with paginated list."""
    return rx.el.div(
        rx.el.h3(
            "Health Conditions",
            class_name="text-lg font-semibold text-white mb-4",
        ),
        paginated_list(
            items=HealthDashboardState.conditions_paginated,
            item_renderer=_condition_card,
            has_previous=HealthDashboardState.conditions_has_previous,
            has_next=HealthDashboardState.conditions_has_next,
            page_info=HealthDashboardState.conditions_page_info,
            showing_info=HealthDashboardState.conditions_showing_info,
            on_previous=HealthDashboardState.conditions_previous_page,
            on_next=HealthDashboardState.conditions_next_page,
            empty_icon="heart-pulse",
            empty_message="No conditions found",
            list_class="space-y-3",
        ),
        class_name="mb-8",
    )


def symptoms_section() -> rx.Component:
    """Symptoms section with paginated list."""
    return rx.el.div(
        rx.el.h3(
            "Current Symptoms",
            class_name="text-lg font-semibold text-white mb-4",
        ),
        paginated_list(
            items=HealthDashboardState.symptoms_paginated,
            item_renderer=_symptom_card,
            has_previous=HealthDashboardState.symptoms_has_previous,
            has_next=HealthDashboardState.symptoms_has_next,
            page_info=HealthDashboardState.symptoms_page_info,
            showing_info=HealthDashboardState.symptoms_showing_info,
            on_previous=HealthDashboardState.symptoms_previous_page,
            on_next=HealthDashboardState.symptoms_next_page,
            empty_icon="thermometer",
            empty_message="No symptoms tracked",
            list_class="space-y-3",
        ),
        class_name="mb-8",
    )


def food_entries_section() -> rx.Component:
    """Food entries section with paginated list."""
    return rx.el.div(
        rx.el.h3(
            "Recent Food Entries",
            class_name="text-lg font-semibold text-white mb-4",
        ),
        paginated_list(
            items=HealthDashboardState.food_entries_paginated,
            item_renderer=_food_entry_card,
            has_previous=HealthDashboardState.food_entries_has_previous,
            has_next=HealthDashboardState.food_entries_has_next,
            page_info=HealthDashboardState.food_entries_page_info,
            showing_info=HealthDashboardState.food_entries_showing_info,
            on_previous=HealthDashboardState.food_entries_previous_page,
            on_next=HealthDashboardState.food_entries_next_page,
            empty_icon="utensils",
            empty_message="No food entries recorded",
            list_class="space-y-3",
        ),
    )


# =============================================================================
# MAIN DASHBOARD
# =============================================================================


def health_metrics_dashboard() -> rx.Component:
    """Complete health metrics dashboard component.

    This is the main component that displays all health metrics including
    nutrition, medications, conditions, symptoms, and food entries.
    Uses paginated lists for better UX with large datasets.
    """
    return rx.el.div(
        nutrition_summary_cards(),
        medications_section(),
        conditions_section(),
        symptoms_section(),
        food_entries_section(),
    )
