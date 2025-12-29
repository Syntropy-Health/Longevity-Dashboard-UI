"""Settings tab component for patient portal."""

import reflex as rx

from ....states import AuthState, SettingsState
from ....styles.constants import GlassStyles


def settings_tab() -> rx.Component:
    """Settings/Profile tab content."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Settings", class_name="text-xl font-bold text-white mb-2"),
            rx.el.p(
                "Manage your profile and preferences.",
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            # Profile Section
            rx.el.div(
                rx.el.h3("Profile", class_name="text-lg font-semibold text-white mb-4"),
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
                                AuthState.role_label, class_name="text-sm text-teal-400"
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
                    "Notifications", class_name="text-lg font-semibold text-white mb-4"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Email Notifications", class_name="text-sm text-white"
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
                                        SettingsState.email_notifications,
                                        "w-5 h-5 bg-white rounded-full shadow-md transform translate-x-6 transition-transform duration-200",
                                        "w-5 h-5 bg-slate-300 rounded-full shadow-md transform translate-x-0 transition-transform duration-200",
                                    ),
                                ),
                                class_name=rx.cond(
                                    SettingsState.email_notifications,
                                    "w-12 h-6 bg-teal-500 rounded-full p-0.5 flex items-center transition-colors duration-200",
                                    "w-12 h-6 bg-slate-600 rounded-full p-0.5 flex items-center transition-colors duration-200",
                                ),
                            ),
                            on_click=SettingsState.toggle_email_notifications,
                            class_name="focus:outline-none",
                        ),
                        class_name="flex items-center justify-between p-4 border-b border-white/5",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Push Notifications", class_name="text-sm text-white"
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
                                        SettingsState.push_notifications,
                                        "w-5 h-5 bg-white rounded-full shadow-md transform translate-x-6 transition-transform duration-200",
                                        "w-5 h-5 bg-slate-300 rounded-full shadow-md transform translate-x-0 transition-transform duration-200",
                                    ),
                                ),
                                class_name=rx.cond(
                                    SettingsState.push_notifications,
                                    "w-12 h-6 bg-teal-500 rounded-full p-0.5 flex items-center transition-colors duration-200",
                                    "w-12 h-6 bg-slate-600 rounded-full p-0.5 flex items-center transition-colors duration-200",
                                ),
                            ),
                            on_click=SettingsState.toggle_push_notifications,
                            class_name="focus:outline-none",
                        ),
                        class_name="flex items-center justify-between p-4",
                    ),
                    class_name=f"{GlassStyles.PANEL}",
                ),
                class_name="mb-8",
            ),
            # Timezone Settings
            rx.el.div(
                rx.el.h3(
                    "Timezone", class_name="text-lg font-semibold text-white mb-4"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("Your Timezone", class_name="text-sm text-white"),
                            rx.el.p(
                                "Used for displaying meal times and daily tracking",
                                class_name="text-xs text-slate-400",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.select(
                            rx.foreach(
                                SettingsState.timezone_options,
                                lambda opt: rx.el.option(
                                    opt["label"],
                                    value=opt["value"],
                                ),
                            ),
                            value=SettingsState.user_timezone,
                            on_change=SettingsState.set_user_timezone,
                            class_name="bg-slate-700 text-white text-sm rounded-lg border border-slate-600 px-3 py-2 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none min-w-[200px]",
                        ),
                        class_name="flex items-center justify-between p-4",
                    ),
                    class_name=f"{GlassStyles.PANEL}",
                ),
            ),
        ),
    )
