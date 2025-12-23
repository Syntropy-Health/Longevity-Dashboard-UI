import reflex as rx

from ..states import AuthState, NotificationState
from ..styles.constants import GlassStyles


def notification_badge() -> rx.Component:
    """Render notification count badge if there are unread notifications."""
    return rx.cond(
        NotificationState.unread_count > 0,
        rx.box(
            NotificationState.unread_count, class_name=GlassStyles.NOTIFICATION_BADGE
        ),
        rx.fragment(),
    )


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", class_name="w-6 h-6 text-slate-300"),
                on_click=AuthState.toggle_mobile_menu,
                class_name="mr-4 md:hidden p-2 rounded-2xl hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-teal-500/20 transition-all",
            ),
            rx.el.h2(
                rx.cond(AuthState.is_admin, "Clinic Dashboard", "Patient Portal"),
                class_name="text-xl font-light text-white tracking-tight",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            # Notifications button with badge
            rx.el.button(
                rx.icon(
                    "bell",
                    class_name="w-5 h-5 text-slate-400 hover:text-teal-300 transition-colors",
                ),
                notification_badge(),
                on_click=rx.redirect("/notifications"),
                class_name=f"{GlassStyles.ICON_BUTTON} mr-2",
                title="Notifications",
            ),
            # Appointments button
            rx.el.button(
                rx.icon(
                    "calendar-plus",
                    class_name="w-5 h-5 text-slate-400 hover:text-teal-300 transition-colors",
                ),
                on_click=rx.redirect("/appointments"),
                class_name=f"{GlassStyles.ICON_BUTTON} mr-4 hidden sm:block",
                title="Schedule Appointment",
            ),
            rx.el.div(class_name="h-6 w-px bg-white/10 mr-4 hidden sm:block"),
            rx.el.button(
                rx.el.span("Sign out", class_name="mr-2 hidden sm:inline"),
                rx.icon("log-out", class_name="w-4 h-4"),
                on_click=AuthState.logout,
                class_name="flex items-center px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:bg-red-500/10 hover:text-red-400 transition-all border border-transparent hover:border-red-500/20 active:scale-95 backdrop-blur-sm",
            ),
            class_name="flex items-center",
        ),
        class_name="h-20 px-6 sm:px-8 md:px-10 bg-slate-900/60 backdrop-blur-xl border-b border-white/10 flex items-center justify-between z-10 sticky top-0 transition-all duration-300",
    )
