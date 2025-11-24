import reflex as rx
from app.states.global_state import GlobalState
from app.styles.glass_styles import GlassStyles


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.icon("activity", class_name="w-6 h-6 text-teal-400 mr-3 md:hidden"),
            rx.el.span(
                GlobalState.clinic_name,
                class_name="font-bold text-lg tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400 md:hidden",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "bell",
                    class_name="w-5 h-5 text-slate-400 hover:text-white cursor-pointer transition-colors",
                ),
                class_name="p-2 hover:bg-white/5 rounded-full",
            ),
            class_name="ml-auto flex items-center gap-2",
        ),
        class_name=f"fixed top-0 right-0 left-0 md:left-64 h-16 z-30 bg-slate-900/80 backdrop-blur-md border-b border-white/10 flex items-center px-6 justify-between",
    )