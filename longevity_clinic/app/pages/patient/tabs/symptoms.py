"""Symptoms tab component for patient portal."""

import reflex as rx

from ....components.modals import symptom_detail_modal, symptom_log_detail_modal
from ....components.paginated_view import paginated_list
from ....components.tabs import (
    medication_notification_card,
    symptom_card,
    symptom_log_item,
    symptom_trend_item,
)
from ....states import NotificationState, SymptomState
from ....styles.constants import GlassStyles


def symptoms_tab() -> rx.Component:
    """Symptoms tab content with compact layout."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Symptom Tracker", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p(
                "Track and log your symptoms over time.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        # Summary Cards Row (similar to food_tracker)
        rx.el.div(
            # Active Symptoms Card
            rx.el.div(
                rx.el.div(
                    rx.icon("thermometer", class_name="w-6 h-6 text-orange-400"),
                    class_name="w-12 h-12 rounded-xl bg-orange-500/10 flex items-center justify-center mb-3 border border-orange-500/20",
                ),
                rx.el.p(
                    "Active Symptoms",
                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                ),
                rx.el.span(
                    SymptomState.symptoms.length(),
                    class_name="text-3xl font-bold text-white",
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            # Recent Logs Card
            rx.el.div(
                rx.el.div(
                    rx.icon("clipboard-list", class_name="w-6 h-6 text-teal-400"),
                    class_name="w-12 h-12 rounded-xl bg-teal-500/10 flex items-center justify-center mb-3 border border-teal-500/20",
                ),
                rx.el.p(
                    "Recent Logs",
                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                ),
                rx.el.span(
                    SymptomState.symptom_logs.length(),
                    class_name="text-3xl font-bold text-white",
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            # Trends Card
            rx.el.div(
                rx.el.div(
                    rx.icon("trending-up", class_name="w-6 h-6 text-blue-400"),
                    class_name="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center mb-3 border border-blue-500/20",
                ),
                rx.el.p(
                    "Trends",
                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                ),
                rx.el.span(
                    SymptomState.symptom_trends.length(),
                    class_name="text-3xl font-bold text-white",
                ),
                class_name=f"{GlassStyles.PANEL} p-5",
            ),
            class_name="grid grid-cols-3 gap-4 mb-8",
        ),
        # Sub-filters (simplified: removed reminders as separate view)
        rx.el.div(
            rx.el.button(
                "Timeline",
                on_click=lambda: SymptomState.set_symptoms_filter("timeline"),
                class_name=rx.cond(
                    SymptomState.symptoms_filter == "timeline",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Symptoms",
                on_click=lambda: SymptomState.set_symptoms_filter("symptoms"),
                class_name=rx.cond(
                    SymptomState.symptoms_filter == "symptoms",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Medications",
                on_click=lambda: SymptomState.set_symptoms_filter("medications"),
                class_name=rx.cond(
                    SymptomState.symptoms_filter == "medications",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Trends",
                on_click=lambda: SymptomState.set_symptoms_filter("trends"),
                class_name=rx.cond(
                    SymptomState.symptoms_filter == "trends",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6",
        ),
        # Content based on filter
        rx.cond(
            SymptomState.symptoms_filter == "timeline",
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Recent Symptom Logs",
                        class_name="text-lg font-semibold text-white",
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.el.div(
                    paginated_list(
                        items=SymptomState.symptom_logs_paginated,
                        item_renderer=symptom_log_item,
                        has_previous=SymptomState.symptom_logs_has_previous,
                        has_next=SymptomState.symptom_logs_has_next,
                        page_info=SymptomState.symptom_logs_page_info,
                        showing_info=SymptomState.symptom_logs_showing_info,
                        on_previous=SymptomState.symptom_logs_previous_page,
                        on_next=SymptomState.symptom_logs_next_page,
                        empty_icon="clipboard-list",
                        empty_message="No symptom logs yet",
                        empty_subtitle="Start logging symptoms to track them over time",
                        list_class="",
                    ),
                    class_name=f"{GlassStyles.PANEL} p-4",
                ),
            ),
            rx.cond(
                SymptomState.symptoms_filter == "symptoms",
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Active Symptoms",
                            class_name="text-lg font-semibold text-white",
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="w-4 h-4 mr-2"),
                            "Log Symptom",
                            class_name=GlassStyles.BUTTON_PRIMARY
                            + " flex items-center",
                        ),
                        class_name="flex justify-between items-center mb-4",
                    ),
                    paginated_list(
                        items=SymptomState.symptoms_paginated,
                        item_renderer=symptom_card,
                        has_previous=SymptomState.symptoms_has_previous,
                        has_next=SymptomState.symptoms_has_next,
                        page_info=SymptomState.symptoms_page_info,
                        showing_info=SymptomState.symptoms_showing_info,
                        on_previous=SymptomState.symptoms_previous_page,
                        on_next=SymptomState.symptoms_next_page,
                        empty_icon="thermometer",
                        empty_message="No symptoms tracked",
                        empty_subtitle="Your tracked symptoms will appear here",
                        list_class="space-y-3",
                    ),
                ),
                rx.cond(
                    SymptomState.symptoms_filter == "medications",
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Medication Schedule",
                                class_name="text-lg font-semibold text-white",
                            ),
                            class_name="flex justify-between items-center mb-4",
                        ),
                        paginated_list(
                            items=NotificationState.medication_notifications_paginated,
                            item_renderer=medication_notification_card,
                            has_previous=NotificationState.medications_has_previous,
                            has_next=NotificationState.medications_has_next,
                            page_info=NotificationState.medications_page_info,
                            showing_info=NotificationState.medications_showing_info,
                            on_previous=NotificationState.medications_previous_page,
                            on_next=NotificationState.medications_next_page,
                            empty_icon="pill",
                            empty_message="No medications scheduled",
                            empty_subtitle="Your medication schedule will appear here",
                            list_class="space-y-3",
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Symptom Trends",
                                class_name="text-lg font-semibold text-white",
                            ),
                            class_name="flex justify-between items-center mb-4",
                        ),
                        rx.el.p(
                            "Track how your symptoms are changing over time.",
                            class_name="text-sm text-slate-400 mb-4",
                        ),
                        paginated_list(
                            items=SymptomState.symptom_trends_paginated,
                            item_renderer=symptom_trend_item,
                            has_previous=SymptomState.symptom_trends_has_previous,
                            has_next=SymptomState.symptom_trends_has_next,
                            page_info=SymptomState.symptom_trends_page_info,
                            showing_info=SymptomState.symptom_trends_showing_info,
                            on_previous=SymptomState.symptom_trends_previous_page,
                            on_next=SymptomState.symptom_trends_next_page,
                            empty_icon="trending-up",
                            empty_message="No trend data",
                            empty_subtitle="Symptom trends will appear as you log more data",
                            list_class="space-y-0",
                        ),
                    ),
                ),
            ),
        ),
        # Symptom detail modal
        symptom_detail_modal(
            show_modal=SymptomState.show_symptom_modal,
            symptom_name=SymptomState.selected_symptom_name,
            symptom_severity=SymptomState.selected_symptom_severity,
            symptom_frequency=SymptomState.selected_symptom_frequency,
            symptom_trend=SymptomState.selected_symptom_trend,
            on_close=SymptomState.close_symptom_modal,
            on_log_symptom=SymptomState.save_symptom_log,
        ),
        # Symptom log detail modal
        symptom_log_detail_modal(
            show_modal=SymptomState.show_symptom_log_modal,
            log_symptom_name=SymptomState.selected_log_symptom_name,
            log_severity=SymptomState.selected_log_severity,
            log_notes=SymptomState.selected_log_notes,
            log_timestamp=SymptomState.selected_log_timestamp,
            on_close=SymptomState.close_symptom_log_modal,
        ),
        on_mount=[
            SymptomState.load_symptom_data,
            NotificationState.load_medication_notifications,
        ],
    )
