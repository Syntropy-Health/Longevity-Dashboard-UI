"""Medications tab component for patient portal.

Dual-panel view:
- Left: Medication Entries (what patient has taken)
- Right: Medication Subscriptions (prescriptions with adherence tracking)
"""

import reflex as rx

from ....components.paginated_view import paginated_list
from ....components.tabs import medication_entry_card, medication_subscription_card
from ....states import HealthDashboardState
from ....styles.constants import GlassStyles


def _summary_stats() -> rx.Component:
    """Summary statistics row."""
    return rx.el.div(
        # Overall Adherence
        rx.el.div(
            rx.el.div(
                rx.icon("chart-line", class_name="w-5 h-5 text-teal-400"),
                class_name="w-10 h-10 rounded-lg bg-teal-500/10 flex items-center justify-center mb-2 border border-teal-500/20",
            ),
            rx.el.p(
                "Overall Adherence",
                class_name="text-[10px] text-slate-400 uppercase tracking-wider mb-0.5",
            ),
            rx.el.span(
                f"{HealthDashboardState.total_medication_adherence:.0f}%",
                class_name="text-2xl font-bold text-teal-400",
            ),
            class_name=f"{GlassStyles.PANEL} p-4",
        ),
        # Active Prescriptions
        rx.el.div(
            rx.el.div(
                rx.icon("pill", class_name="w-5 h-5 text-purple-400"),
                class_name="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center mb-2 border border-purple-500/20",
            ),
            rx.el.p(
                "Active Prescriptions",
                class_name="text-[10px] text-slate-400 uppercase tracking-wider mb-0.5",
            ),
            rx.el.span(
                HealthDashboardState.active_subscriptions_count,
                class_name="text-2xl font-bold text-white",
            ),
            class_name=f"{GlassStyles.PANEL} p-4",
        ),
        # Logged Today
        rx.el.div(
            rx.el.div(
                rx.icon("clipboard-check", class_name="w-5 h-5 text-blue-400"),
                class_name="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center mb-2 border border-blue-500/20",
            ),
            rx.el.p(
                "Doses Logged",
                class_name="text-[10px] text-slate-400 uppercase tracking-wider mb-0.5",
            ),
            rx.el.span(
                HealthDashboardState.medication_entries_count,
                class_name="text-2xl font-bold text-white",
            ),
            class_name=f"{GlassStyles.PANEL} p-4",
        ),
        class_name="grid grid-cols-3 gap-3 mb-6",
    )


def _medication_entries_panel() -> rx.Component:
    """Left panel: Medication Entries (what was taken)."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("clipboard-list", class_name="w-5 h-5 text-teal-400"),
                rx.el.h3(
                    "Medication Entry",
                    class_name="text-lg font-semibold text-white ml-2",
                ),
            ),
            rx.el.p(
                "Recent doses taken",
                class_name="text-xs text-slate-400 mt-1",
            ),
            class_name="flex flex-col mb-4",
        ),
        paginated_list(
            items=HealthDashboardState.medication_entries_paginated,
            item_renderer=medication_entry_card,
            has_previous=HealthDashboardState.medication_entries_has_previous,
            has_next=HealthDashboardState.medication_entries_has_next,
            page_info=HealthDashboardState.medication_entries_page_info,
            showing_info=HealthDashboardState.medication_entries_showing_info,
            on_previous=HealthDashboardState.medication_entries_previous_page,
            on_next=HealthDashboardState.medication_entries_next_page,
            empty_icon="clipboard-check",
            empty_message="No doses logged",
            empty_subtitle="Log your first dose to start tracking",
            list_class="space-y-2",
        ),
        class_name=f"{GlassStyles.PANEL} p-4 h-full",
    )


def _medication_subscriptions_panel() -> rx.Component:
    """Right panel: Medication Subscriptions (prescriptions with adherence)."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("pill", class_name="w-5 h-5 text-purple-400"),
                rx.el.h3(
                    "Prescriptions", class_name="text-lg font-semibold text-white ml-2"
                ),
            ),
            rx.el.p(
                "Active medications & adherence",
                class_name="text-xs text-slate-400 mt-1",
            ),
            class_name="flex flex-col mb-4",
        ),
        paginated_list(
            items=HealthDashboardState.medication_subscriptions_paginated,
            item_renderer=medication_subscription_card,
            has_previous=HealthDashboardState.medication_subscriptions_has_previous,
            has_next=HealthDashboardState.medication_subscriptions_has_next,
            page_info=HealthDashboardState.medication_subscriptions_page_info,
            showing_info=HealthDashboardState.medication_subscriptions_showing_info,
            on_previous=HealthDashboardState.medication_subscriptions_previous_page,
            on_next=HealthDashboardState.medication_subscriptions_next_page,
            empty_icon="pill",
            empty_message="No prescriptions",
            empty_subtitle="Your prescription list is empty",
            list_class="space-y-2",
        ),
        class_name=f"{GlassStyles.PANEL} p-4 h-full",
    )


def medications_tab() -> rx.Component:
    """Medications tab content with dual-panel view."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h2("Medications", class_name="text-xl font-bold text-white mb-1"),
            rx.el.p(
                "Track your prescriptions and log doses taken.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-5",
        ),
        # Summary Stats
        _summary_stats(),
        # Dual Panel Layout
        rx.el.div(
            _medication_entries_panel(),
            _medication_subscriptions_panel(),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4",
        ),
    )
