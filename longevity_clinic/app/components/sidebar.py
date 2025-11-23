import reflex as rx
from ..states.auth_state import AuthState
from ..config import current_config


def sidebar_item(text: str, icon_name: str, href: str) -> rx.Component:
    """A single sidebar navigation item."""
    return rx.el.a(
        rx.icon(
            icon_name,
            class_name="w-5 h-5 mr-3 text-gray-500 group-hover:text-emerald-600 transition-colors opacity-70 group-hover:opacity-100",
        ),
        rx.el.span(
            text,
            class_name="font-medium text-gray-600 group-hover:text-gray-900 transition-colors tracking-wide",
        ),
        href=href,
        class_name="flex items-center px-5 py-3.5 mb-2 rounded-2xl transition-all duration-300 hover:bg-white/40 hover:shadow-[0_8px_20px_-4px_rgba(31,38,135,0.05)] hover:backdrop-blur-md group text-sm mx-4 border border-transparent hover:border-white/40 active:scale-[0.98]",
    )


def mobile_sidebar_item(text: str, icon_name: str, href: str) -> rx.Component:
    """Sidebar item optimized for mobile menu."""
    return rx.el.a(
        rx.icon(icon_name, class_name="w-6 h-6 mr-4 text-emerald-600"),
        rx.el.span(text, class_name="font-medium text-lg text-gray-700"),
        href=href,
        on_click=AuthState.close_mobile_menu,
        class_name="flex items-center px-4 py-4 border-b border-gray-100 hover:bg-emerald-50 transition-colors",
    )


def sidebar_content() -> rx.Component:
    """The actual content of the sidebar (logo + links)."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "activity", class_name="w-8 h-8 text-emerald-500 mr-2 opacity-90"
                ),
                class_name="p-2 bg-white/50 rounded-2xl border border-white/60 shadow-sm backdrop-blur-md",
            ),
            rx.el.span(
                current_config.clinic_name,
                class_name="text-lg font-light text-gray-800 tracking-tight leading-tight",
            ),
            class_name="flex items-center px-6 py-8 h-28 border-b border-white/10",
        ),
        rx.el.nav(
            rx.cond(
                AuthState.is_admin,
                rx.el.div(
                    rx.el.p(
                        "ADMINISTRATION",
                        class_name="px-6 mt-6 mb-4 text-[10px] font-bold text-gray-400 uppercase tracking-widest opacity-60",
                    ),
                    sidebar_item("Dashboard", "layout-dashboard", "/admin/dashboard"),
                    sidebar_item(
                        "Treatment Library", "stethoscope", "/admin/treatments"
                    ),
                    class_name="flex flex-col gap-1",
                ),
                rx.el.div(
                    rx.el.p(
                        "MY WELLNESS",
                        class_name="px-6 mt-6 mb-4 text-[10px] font-bold text-gray-400 uppercase tracking-widest opacity-60",
                    ),
                    sidebar_item("Portal Home", "home", "/patient/portal"),
                    sidebar_item("My Analytics", "bar-chart", "/patient/analytics"),
                    sidebar_item(
                        "Treatment Search", "search", "/patient/treatment-search"
                    ),
                    class_name="flex flex-col gap-1",
                ),
            ),
            class_name="flex-1 py-4 overflow-y-auto scrollbar-hide",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        AuthState.user_initials,
                        class_name="text-xs font-bold text-emerald-700",
                    ),
                    class_name="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-50 to-white flex items-center justify-center mr-3 border border-white/60 shadow-sm",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.user["full_name"],
                        class_name="text-xs font-semibold text-gray-700 truncate max-w-[120px]",
                    ),
                    rx.el.p(
                        AuthState.role_label,
                        class_name="text-[10px] text-gray-400 uppercase tracking-wider",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="p-4 border-t border-white/20 bg-white/40 backdrop-blur-xl mb-4 mx-4 rounded-2xl border border-white/40 shadow-[0_4px_20px_0_rgba(0,0,0,0.02)]",
        ),
        class_name="flex flex-col h-full",
    )


def sidebar() -> rx.Component:
    """The desktop sidebar component."""
    return rx.el.aside(
        sidebar_content(),
        class_name=f"hidden md:flex flex-col w-72 h-screen {current_config.glass_sidebar_style} shrink-0 z-40",
    )


def mobile_menu() -> rx.Component:
    """Mobile slide-over menu."""
    return rx.el.div(
        rx.el.div(
            class_name="absolute inset-0 bg-slate-900/20 backdrop-blur-sm transition-opacity",
            on_click=AuthState.toggle_mobile_menu,
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="w-8 h-8 text-emerald-600 mr-2"),
                rx.el.span(
                    "Vitality Clinic", class_name="text-xl font-bold text-gray-900"
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-6 h-6 text-gray-500"),
                    on_click=AuthState.toggle_mobile_menu,
                    class_name="ml-auto p-2",
                ),
                class_name="flex items-center p-4 border-b border-gray-100",
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
                            class_name="text-lg font-bold text-emerald-800",
                        ),
                        class_name="w-12 h-12 rounded-full bg-emerald-100 flex items-center justify-center mr-3",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AuthState.user["full_name"],
                            class_name="text-base font-medium text-gray-900",
                        ),
                        rx.el.p(
                            AuthState.role_label, class_name="text-sm text-gray-500"
                        ),
                    ),
                    class_name="flex items-center mb-4",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="w-5 h-5 mr-2"),
                    "Sign Out",
                    on_click=AuthState.logout,
                    class_name="w-full flex items-center justify-center px-4 py-2 border border-gray-200 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50",
                ),
                class_name="p-6 border-t border-gray-100 bg-gray-50",
            ),
            class_name="relative flex flex-col w-4/5 max-w-xs h-full bg-white shadow-2xl",
        ),
        class_name=rx.cond(
            AuthState.show_mobile_menu, "fixed inset-0 z-50 flex", "hidden"
        ),
    )