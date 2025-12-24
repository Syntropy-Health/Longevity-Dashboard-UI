"""Data sources tab component for patient portal."""

import reflex as rx

from ....components.paginated_view import paginated_list
from ....data.schemas.llm import DataSource
from ....states import HealthDashboardState
from ....styles.constants import GlassStyles


def data_source_card(source: DataSource) -> rx.Component:
    """Data source card with device image and connection toggle.

    Args:
        source: DataSource instance from PatientDashboardState
    """
    return rx.el.div(
        rx.el.div(
            # Device image/icon
            rx.el.div(
                rx.el.img(
                    src=source.image,
                    class_name="w-10 h-10 object-contain",
                ),
                class_name=rx.cond(
                    source.connected,
                    "w-14 h-14 rounded-xl bg-teal-500/10 flex items-center justify-center mr-4 border border-teal-500/20",
                    "w-14 h-14 rounded-xl bg-slate-500/10 flex items-center justify-center mr-4 border border-slate-500/20 opacity-60",
                ),
            ),
            rx.el.div(
                rx.el.h4(
                    source.name,
                    class_name=rx.cond(
                        source.connected,
                        "text-base font-semibold text-white mb-1",
                        "text-base font-semibold text-slate-400 mb-1",
                    ),
                ),
                rx.el.p(source.type.capitalize(), class_name="text-xs text-slate-400"),
                rx.el.p(
                    rx.fragment("Last sync: ", source.last_sync),
                    class_name=rx.cond(
                        source.connected,
                        "text-xs text-slate-400 mt-1",
                        "text-xs text-slate-500 mt-1",
                    ),
                ),
            ),
            class_name="flex items-center flex-1",
        ),
        rx.el.div(
            # Connection toggle switch
            rx.el.button(
                rx.el.div(
                    rx.el.div(
                        class_name=rx.cond(
                            source.connected,
                            "w-5 h-5 bg-white rounded-full shadow-md transform translate-x-6 transition-transform duration-200",
                            "w-5 h-5 bg-slate-300 rounded-full shadow-md transform translate-x-0 transition-transform duration-200",
                        ),
                    ),
                    class_name=rx.cond(
                        source.connected,
                        "w-12 h-6 bg-teal-500 rounded-full p-0.5 flex items-center transition-colors duration-200",
                        "w-12 h-6 bg-slate-600 rounded-full p-0.5 flex items-center transition-colors duration-200",
                    ),
                ),
                on_click=lambda: HealthDashboardState.toggle_data_source_connection(
                    source.id
                ),
                class_name="focus:outline-none",
            ),
            rx.el.span(
                rx.cond(source.connected, "Connected", "Disconnected"),
                class_name=rx.cond(
                    source.connected,
                    "text-xs text-teal-400 mt-2",
                    "text-xs text-slate-500 mt-2",
                ),
            ),
            class_name="flex flex-col items-center",
        ),
        class_name=rx.cond(
            source.connected,
            f"{GlassStyles.CARD_INTERACTIVE} flex justify-between items-center",
            "group relative overflow-hidden rounded-2xl p-6 bg-white/3 border border-white/5 backdrop-blur-md transition-all duration-300 flex justify-between items-center opacity-80",
        ),
    )


def import_drop_zone() -> rx.Component:
    """Drag and drop zone for file imports."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("cloud-upload", class_name="w-12 h-12 text-slate-400 mb-4"),
                rx.el.h4(
                    "Drop files here to import",
                    class_name="text-lg font-semibold text-white mb-2",
                ),
                rx.el.p(
                    "Supported formats: CSV, JSON, FHIR, HL7",
                    class_name="text-sm text-slate-400 mb-4",
                ),
                rx.el.div(
                    rx.el.span("or", class_name="text-slate-500 text-sm px-3"),
                    class_name="flex items-center mb-4",
                ),
                rx.el.button(
                    rx.icon("folder-open", class_name="w-4 h-4 mr-2"),
                    "Browse Files",
                    class_name=GlassStyles.BUTTON_PRIMARY + " flex items-center",
                ),
                class_name="flex flex-col items-center justify-center py-12",
            ),
            class_name="border-2 border-dashed border-slate-600 hover:border-teal-500/50 rounded-2xl bg-white/2 hover:bg-white/5 transition-all duration-300 cursor-pointer",
        ),
        rx.el.div(
            rx.el.h4(
                "Recent Imports", class_name="text-sm font-semibold text-white mb-3"
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("file-text", class_name="w-4 h-4 text-slate-400 mr-3"),
                    rx.el.div(
                        rx.el.p(
                            "lab_results_nov2024.csv", class_name="text-sm text-white"
                        ),
                        rx.el.p(
                            "Imported 3 days ago", class_name="text-xs text-slate-400"
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.span(
                        "Success",
                        class_name="text-xs text-teal-400 bg-teal-500/10 px-2 py-1 rounded",
                    ),
                    class_name="flex items-center p-3 border-b border-white/5",
                ),
                rx.el.div(
                    rx.icon("file-text", class_name="w-4 h-4 text-slate-400 mr-3"),
                    rx.el.div(
                        rx.el.p(
                            "medication_history.json", class_name="text-sm text-white"
                        ),
                        rx.el.p(
                            "Imported 1 week ago", class_name="text-xs text-slate-400"
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.span(
                        "Success",
                        class_name="text-xs text-teal-400 bg-teal-500/10 px-2 py-1 rounded",
                    ),
                    class_name="flex items-center p-3",
                ),
                class_name=f"{GlassStyles.PANEL}",
            ),
            class_name="mt-6",
        ),
        class_name="space-y-4",
    )


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
