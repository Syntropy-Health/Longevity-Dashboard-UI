"""Standalone Settings page for patient portal."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...states import AuthState
from ...states import HealthDashboardState
from ...styles.constants import GlassStyles
from .tabs import data_source_card, import_drop_zone
from .modals import connect_source_modal, suggest_integration_modal


def settings_page() -> rx.Component:
    """Standalone Settings page."""
    return authenticated_layout(
        rx.el.div(
            # Page Header
            rx.el.div(
                rx.el.h1(
                    "Settings",
                    class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-2",
                ),
                rx.el.p(
                    rx.el.span("Manage your profile, preferences, and data sources"),
                    class_name="text-slate-400 text-sm",
                ),
                class_name="mb-6",
            ),
            # Settings Content
            rx.el.div(
                # Profile Section
                rx.el.div(
                    rx.el.h3(
                        "Profile", class_name="text-lg font-semibold text-white mb-4"
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.span(
                                    AuthState.user_initials,
                                    class_name="text-2xl font-bold text-teal-300",
                                ),
                                class_name="w-20 h-20 rounded-full bg-teal-900/50 flex items-center justify-center border border-teal-500/30",
                            ),
                            rx.el.div(
                                rx.el.h4(
                                    AuthState.user_full_name,
                                    class_name="text-lg font-semibold text-white",
                                ),
                                rx.el.p(
                                    AuthState.role_label,
                                    class_name="text-sm text-teal-400",
                                ),
                                class_name="ml-4",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-6",
                    ),
                    class_name="mb-8",
                ),
                # Notification Settings
                rx.el.div(
                    rx.el.h3(
                        "Notifications",
                        class_name="text-lg font-semibold text-white mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Email Notifications",
                                    class_name="text-sm text-white",
                                ),
                                rx.el.p(
                                    "Receive updates via email",
                                    class_name="text-xs text-slate-400",
                                ),
                                class_name="flex-1",
                            ),
                            rx.el.button(
                                rx.el.div(
                                    rx.el.div(
                                        class_name=rx.cond(
                                            HealthDashboardState.email_notifications,
                                            "w-5 h-5 bg-white rounded-full shadow-md transform translate-x-6 transition-transform duration-200",
                                            "w-5 h-5 bg-slate-300 rounded-full shadow-md transform translate-x-0 transition-transform duration-200",
                                        ),
                                    ),
                                    class_name=rx.cond(
                                        HealthDashboardState.email_notifications,
                                        "w-12 h-6 bg-teal-500 rounded-full p-0.5 flex items-center transition-colors duration-200",
                                        "w-12 h-6 bg-slate-600 rounded-full p-0.5 flex items-center transition-colors duration-200",
                                    ),
                                ),
                                on_click=HealthDashboardState.toggle_email_notifications,
                                class_name="focus:outline-none",
                            ),
                            class_name="flex items-center justify-between p-4 border-b border-white/5",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Push Notifications",
                                    class_name="text-sm text-white",
                                ),
                                rx.el.p(
                                    "Receive push notifications",
                                    class_name="text-xs text-slate-400",
                                ),
                                class_name="flex-1",
                            ),
                            rx.el.button(
                                rx.el.div(
                                    rx.el.div(
                                        class_name=rx.cond(
                                            HealthDashboardState.push_notifications,
                                            "w-5 h-5 bg-white rounded-full shadow-md transform translate-x-6 transition-transform duration-200",
                                            "w-5 h-5 bg-slate-300 rounded-full shadow-md transform translate-x-0 transition-transform duration-200",
                                        ),
                                    ),
                                    class_name=rx.cond(
                                        HealthDashboardState.push_notifications,
                                        "w-12 h-6 bg-teal-500 rounded-full p-0.5 flex items-center transition-colors duration-200",
                                        "w-12 h-6 bg-slate-600 rounded-full p-0.5 flex items-center transition-colors duration-200",
                                    ),
                                ),
                                on_click=HealthDashboardState.toggle_push_notifications,
                                class_name="focus:outline-none",
                            ),
                            class_name="flex items-center justify-between p-4",
                        ),
                        class_name=f"{GlassStyles.PANEL}",
                    ),
                    class_name="mb-8",
                ),
                # Data Sources Section
                rx.el.div(
                    rx.el.h3(
                        "Data Sources",
                        class_name="text-lg font-semibold text-white mb-4",
                    ),
                    rx.el.p(
                        "Connect and manage your health data sources.",
                        class_name="text-slate-400 text-sm mb-6",
                    ),
                    # Sub-filters
                    rx.el.div(
                        rx.el.button(
                            "Devices & Wearables",
                            on_click=lambda: HealthDashboardState.set_data_sources_filter(
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
                            on_click=lambda: HealthDashboardState.set_data_sources_filter(
                                "api_connections"
                            ),
                            class_name=rx.cond(
                                HealthDashboardState.data_sources_filter
                                == "api_connections",
                                "px-4 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                                "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent",
                            ),
                        ),
                        rx.el.button(
                            "Import History",
                            on_click=lambda: HealthDashboardState.set_data_sources_filter(
                                "import_history"
                            ),
                            class_name=rx.cond(
                                HealthDashboardState.data_sources_filter
                                == "import_history",
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
                            # Sources List
                            rx.el.div(
                                rx.foreach(
                                    HealthDashboardState.filtered_data_sources,
                                    data_source_card,
                                ),
                                class_name="space-y-4",
                            ),
                            # "Not here?" link
                            rx.el.div(
                                rx.el.span(
                                    "Don't see your device? ",
                                    class_name="text-slate-500 text-sm",
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
                ),
            ),
            # Modals
            connect_source_modal(),
            suggest_integration_modal(),
            on_mount=[
                # BiomarkerState.load_biomarkers,
                # HealthDashboardState.load_dashboard_data,
            ],
        )
    )
