import reflex as rx
from app.states.global_state import GlobalState
from app.styles.glass_styles import GlassStyles


def sidebar_item(
    text: str, icon: str, href: str, is_active: bool = False
) -> rx.Component:
    return rx.el.a(
        rx.icon(
            icon,
            class_name=f"w-5 h-5 mr-3 transition-colors {('text-teal-400' if is_active else 'text-slate-400 group-hover:text-teal-300')}",
        ),
        rx.el.span(text),
        href=href,
        class_name=f"flex items-center px-4 py-3 mb-1 rounded-xl text-sm font-medium transition-all duration-200 group {('bg-teal-500/10 text-white border border-teal-500/20' if is_active else 'text-slate-400 hover:text-white hover:bg-white/5 border border-transparent')}",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="w-8 h-8 text-teal-400 mr-3"),
                rx.el.div(
                    rx.el.span(
                        "Aether",
                        class_name="block font-bold text-lg tracking-tight text-white leading-none",
                    ),
                    rx.el.span(
                        "Longevity",
                        class_name="block text-xs text-teal-400 uppercase tracking-widest",
                    ),
                ),
                class_name="flex items-center px-4 py-6 mb-6 border-b border-white/10",
            ),
            rx.el.nav(
                sidebar_item("Dashboard", "layout-dashboard", "/"),
                rx.cond(
                    GlobalState.is_patient,
                    rx.fragment(
                        rx.el.p(
                            "PATIENT PORTAL",
                            class_name="px-4 mt-6 mb-3 text-[10px] font-bold text-slate-500 uppercase tracking-widest",
                        ),
                        sidebar_item("My Profile", "user", "/intake"),
                        sidebar_item("Protocols", "pill", "/patient/protocols"),
                        sidebar_item("Analytics", "line-chart", "/patient/analytics"),
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    GlobalState.is_admin,
                    rx.fragment(
                        rx.el.p(
                            "CLINICIAN PORTAL",
                            class_name="px-4 mt-6 mb-3 text-[10px] font-bold text-slate-500 uppercase tracking-widest",
                        ),
                        sidebar_item("Patient Cohort", "users", "/admin/cohort"),
                        sidebar_item("Protocol Mgmt", "file-text", "/admin/protocols"),
                        sidebar_item(
                            "Clinic Analytics", "bar-chart-2", "/admin/analytics"
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name="flex flex-col px-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src="/placeholder.svg",
                        class_name="w-10 h-10 rounded-full bg-teal-900/50 p-0.5 border border-teal-500/30",
                    ),
                    rx.el.div(
                        rx.el.p(
                            GlobalState.user_name,
                            class_name="text-sm font-medium text-white leading-none mb-1",
                        ),
                        rx.el.p(
                            GlobalState.role_display_name,
                            class_name="text-[10px] text-teal-400 uppercase tracking-wider",
                        ),
                        class_name="flex flex-col ml-3",
                    ),
                    class_name="flex items-center mb-4",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="w-4 h-4 mr-2"),
                    "Sign Out",
                    on_click=GlobalState.logout,
                    class_name="flex items-center justify-center w-full px-4 py-2 text-sm font-medium text-slate-400 bg-white/5 hover:bg-red-500/10 hover:text-red-400 rounded-lg border border-white/5 transition-all",
                ),
                class_name="mt-auto p-4 border-t border-white/10 bg-slate-900/30",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="fixed top-0 left-0 h-full w-64 bg-slate-900/80 backdrop-blur-xl border-r border-white/10 hidden md:block z-40",
    )