"""Data sources tab component for patient portal."""

import reflex as rx

from ....components.paginated_view import paginated_list
from ....components.tabs import data_source_card, import_drop_zone
from ....states import HealthDashboardState
from ....styles.constants import GlassStyles


def data_sources_tab() -> rx.Component:
    """Data sources tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Data Sources", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p(
                "Connect and manage your health data sources.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        # Sub-filters
        rx.el.div(
            rx.el.button(
                "Devices & Wearables",
                on_click=lambda: HealthDashboardState.set_data_sources_filter_with_reset(
                    "devices"
                ),
                class_name=rx.cond(
                    HealthDashboardState.data_sources_filter == "devices",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "API Connections",
                on_click=lambda: HealthDashboardState.set_data_sources_filter_with_reset(
                    "api_connections"
                ),
                class_name=rx.cond(
                    HealthDashboardState.data_sources_filter == "api_connections",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            rx.el.button(
                "Import History",
                on_click=lambda: HealthDashboardState.set_data_sources_filter_with_reset(
                    "import_history"
                ),
                class_name=rx.cond(
                    HealthDashboardState.data_sources_filter == "import_history",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6",
        ),
        # Content based on filter
        rx.cond(
            HealthDashboardState.data_sources_filter == "import_history",
            import_drop_zone(),
            rx.el.div(
                # Summary Card
                rx.el.div(
                    rx.el.div(
                        rx.icon("link", class_name="w-6 h-6 text-teal-400"),
                        class_name="w-12 h-12 rounded-xl bg-teal-500/10 flex items-center justify-center mb-3 border border-teal-500/20",
                    ),
                    rx.el.p(
                        "Connected Sources",
                        class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                    ),
                    rx.el.span(
                        HealthDashboardState.connected_sources_count,
                        class_name="text-3xl font-bold text-white",
                    ),
                    class_name=f"{GlassStyles.PANEL} p-5 mb-6",
                ),
                # Sources List (Paginated)
                paginated_list(
                    items=HealthDashboardState.data_sources_paginated,
                    item_renderer=data_source_card,
                    has_previous=HealthDashboardState.data_sources_has_previous,
                    has_next=HealthDashboardState.data_sources_has_next,
                    page_info=HealthDashboardState.data_sources_page_info,
                    showing_info=HealthDashboardState.data_sources_showing_info,
                    on_previous=HealthDashboardState.data_sources_previous_page,
                    on_next=HealthDashboardState.data_sources_next_page,
                    empty_icon="link",
                    empty_message="No data sources found",
                    empty_subtitle="Connect a device or service to get started",
                    list_class="space-y-4",
                ),
                # "Not here?" link
                rx.el.div(
                    rx.el.span(
                        "Don't see your device? ", class_name="text-slate-500 text-sm"
                    ),
                    rx.el.button(
                        "Suggest an integration",
                        on_click=HealthDashboardState.open_suggest_integration_modal,
                        class_name="text-teal-400 text-sm hover:text-teal-300 underline underline-offset-2 transition-colors",
                    ),
                    class_name="mt-6 text-center",
                ),
            ),
        ),
    )
