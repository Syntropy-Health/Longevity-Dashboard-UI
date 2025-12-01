import reflex as rx
from ..states.auth_state import AuthState
from ..styles.constants import GlassStyles


def sidebar_item(text: str, icon_name: str, href: str, is_active: bool = False) -> rx.Component:
    """A single sidebar navigation item with dark theme styling."""
    return rx.el.a(
        rx.icon(
            icon_name,
            class_name=f"w-5 h-5 mr-3 transition-colors {('text-teal-400' if is_active else 'text-slate-400 group-hover:text-teal-300')}",
        ),
        rx.el.span(text),
        href=href,
        class_name=f"flex items-center px-4 py-3 mb-1 rounded-xl text-sm font-medium transition-all duration-200 group {('bg-teal-500/10 text-white border border-teal-500/20' if is_active else 'text-slate-400 hover:text-white hover:bg-white/5 border border-transparent')}",
    )


def mobile_sidebar_item(text: str, icon_name: str, href: str) -> rx.Component:
    """Sidebar item optimized for mobile menu with dark theme."""
    return rx.el.a(
        rx.icon(icon_name, class_name="w-6 h-6 mr-4 text-teal-400"),
        rx.el.span(text, class_name="font-medium text-lg text-white"),
        href=href,
        on_click=AuthState.close_mobile_menu,
        class_name="flex items-center px-4 py-4 border-b border-white/10 hover:bg-white/5 transition-colors",
    )


def sidebar_content() -> rx.Component:
    """The actual content of the sidebar (logo + links) with dark theme."""
    return rx.el.div(
        rx.el.div(
            rx.icon("activity", class_name="w-8 h-8 text-teal-400 mr-3"),
            rx.el.div(
                rx.el.span(
                    "Longevity",
                    class_name="block font-bold text-lg tracking-tight text-white leading-none",
                ),
                rx.el.span(
                    "Clinic",
                    class_name="block text-xs text-teal-400 uppercase tracking-widest",
                ),
            ),
            class_name="flex items-center px-4 py-6 mb-6 border-b border-white/10",
        ),
        rx.el.nav(
            rx.cond(
                AuthState.is_admin,
                rx.el.div(
                    rx.el.p(
                        "ADMINISTRATION",
                        class_name="px-4 mt-6 mb-3 text-[10px] font-bold text-slate-500 uppercase tracking-widest",
                    ),
                    sidebar_item("Dashboard", "layout-dashboard", "/admin/dashboard"),
                    sidebar_item(
                        "Treatment Library", "stethoscope", "/admin/treatments"
                    ),
                    class_name="flex flex-col px-3",
                ),
                rx.el.div(
                    rx.el.p(
                        "PATIENT PORTAL",
                        class_name="px-4 mt-6 mb-3 text-[10px] font-bold text-slate-500 uppercase tracking-widest",
                    ),
                    sidebar_item("Portal Home", "home", "/patient/portal"),
                    sidebar_item("My Analytics", "bar-chart", "/patient/analytics"),
                    sidebar_item(
                        "Treatment Search", "search", "/patient/treatment-search"
                    ),
                    class_name="flex flex-col px-3",
                ),
            ),
            class_name="flex-1 py-4 overflow-y-auto scrollbar-hide",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        AuthState.user_initials,
                        class_name="text-xs font-bold text-teal-300",
                    ),
                    class_name="w-10 h-10 rounded-full bg-teal-900/50 flex items-center justify-center mr-3 border border-teal-500/30",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.user["full_name"],
                        class_name="text-sm font-medium text-white leading-none mb-1 truncate max-w-[120px]",
                    ),
                    rx.el.p(
                        AuthState.role_label,
                        class_name="text-[10px] text-teal-400 uppercase tracking-wider",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center mb-4",
            ),
            class_name="mt-auto p-4 border-t border-white/10 bg-slate-900/30",
        ),
        class_name="flex flex-col h-full",
    )


def sidebar() -> rx.Component:
    """The desktop sidebar component with dark theme."""
    return rx.el.aside(
        sidebar_content(),
        class_name="fixed top-0 left-0 h-full w-64 bg-slate-900/80 backdrop-blur-xl border-r border-white/10 hidden md:flex flex-col z-40",
    )


def mobile_menu() -> rx.Component:
    """Mobile slide-over menu with dark theme."""
    return rx.el.div(
        rx.el.div(
            class_name="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity",
            on_click=AuthState.toggle_mobile_menu,
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="w-8 h-8 text-teal-400 mr-2"),
                rx.el.span(
                    "Longevity Clinic", class_name="text-xl font-bold text-white"
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-6 h-6 text-slate-400 hover:text-white"),
                    on_click=AuthState.toggle_mobile_menu,
                    class_name="ml-auto p-2 hover:bg-white/10 rounded-lg transition-colors",
                ),
                class_name="flex items-center p-4 border-b border-white/10",
            ),
            rx.el.nav(
                rx.cond(
                    AuthState.is_admin,
                    rx.fragment(
                        mobile_sidebar_item(
                            "Dashboard", "layout-dashboard", "/admin/dashboard"
                        ),
                        mobile_sidebar_item(
                            "Treatments", "stethoscope", "/admin/treatments"
                        ),
                    ),
                    rx.fragment(
                        mobile_sidebar_item("Portal Home", "home", "/patient/portal"),
                        mobile_sidebar_item(
                            "My Analytics", "bar-chart", "/patient/analytics"
                        ),
                        mobile_sidebar_item(
                            "Treatment Search", "search", "/patient/treatment-search"
                        ),
                    ),
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            AuthState.user_initials,
                            class_name="text-lg font-bold text-teal-300",
                        ),
                        class_name="w-12 h-12 rounded-full bg-teal-900/50 flex items-center justify-center mr-3 border border-teal-500/30",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AuthState.user["full_name"],
                            class_name="text-base font-medium text-white",
                        ),
                        rx.el.p(
                            AuthState.role_label, class_name="text-sm text-teal-400"
                        ),
                    ),
                    class_name="flex items-center mb-4",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="w-5 h-5 mr-2"),
                    "Sign Out",
                    on_click=AuthState.logout,
                    class_name="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-slate-400 bg-white/5 hover:bg-red-500/10 hover:text-red-400 rounded-lg border border-white/5 transition-all",
                ),
                class_name="p-6 border-t border-white/10 bg-slate-900/50",
            ),
            class_name="relative flex flex-col w-4/5 max-w-xs h-full bg-slate-900/95 backdrop-blur-xl shadow-2xl",
        ),
        class_name=rx.cond(
            AuthState.show_mobile_menu, "fixed inset-0 z-50 flex", "hidden"
        ),
    )