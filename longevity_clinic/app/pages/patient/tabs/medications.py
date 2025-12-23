"""Medications tab component for patient portal."""

import reflex as rx

from ....components.paginated_view import paginated_list
from ....states import HealthDashboardState
from ....styles.constants import GlassStyles


def medication_card(med) -> rx.Component:
    """Medication card.

    Args:
        med: Medication instance from PatientDashboardState
    """
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
                rx.el.p(med.frequency, class_name="text-xs text-slate-400 mt-1"),
            ),
            class_name="flex items-start flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Adherence",
                    class_name="text-[10px] text-slate-400 uppercase tracking-wider",
                ),
                rx.el.span(
                    rx.text(f"{med.adherence_rate:.0f}%"),
                    class_name=rx.cond(
                        med.adherence_rate >= 90,
                        "text-lg font-bold text-teal-400",
                        "text-lg font-bold text-amber-400",
                    ),
                ),
                class_name="text-right",
            ),
            rx.el.span(
                med.status.capitalize(),
                class_name=rx.cond(
                    med.status == "active",
                    "mt-2 inline-block px-2 py-0.5 rounded text-[10px] font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20",
                    "mt-2 inline-block px-2 py-0.5 rounded text-[10px] font-medium bg-slate-500/10 text-slate-300 border border-slate-500/20",
                ),
            ),
            class_name="flex flex-col items-end",
        ),
        on_click=lambda: HealthDashboardState.open_medication_modal(med),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex justify-between",
    )


def medications_tab() -> rx.Component:
    """Medications tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Medications", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p(
                "Manage your medications and track adherence.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        # Medication Summary
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("chart-line", class_name="w-6 h-6 text-teal-400"),
                    class_name="w-12 h-12 rounded-xl bg-teal-500/10 flex items-center justify-center mb-3 border border-teal-500/20",
                ),
                rx.el.p(
                    "Overall Adherence",
                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                ),
                rx.el.span(
                    f"{HealthDashboardState.total_medication_adherence:.0f}%",
                    class_name="text-3xl font-bold text-teal-400",
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("pill", class_name="w-6 h-6 text-purple-400"),
                    class_name="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center mb-3 border border-purple-500/20",
                ),
                rx.el.p(
                    "Active Medications",
                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                ),
                rx.el.span(
                    HealthDashboardState.medications.length(),
                    class_name="text-3xl font-bold text-white",
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            class_name="grid grid-cols-2 gap-4 mb-8",
        ),
        # Medication List (Paginated)
        paginated_list(
            items=HealthDashboardState.medications_paginated,
            item_renderer=medication_card,
            has_previous=HealthDashboardState.medications_has_previous,
            has_next=HealthDashboardState.medications_has_next,
            page_info=HealthDashboardState.medications_page_info,
            showing_info=HealthDashboardState.medications_showing_info,
            on_previous=HealthDashboardState.medications_previous_page,
            on_next=HealthDashboardState.medications_next_page,
            empty_icon="pill",
            empty_message="No medications found",
            empty_subtitle="Your medication list is empty",
            list_class="space-y-4",
        ),
    )
