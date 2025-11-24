import reflex as rx
from app.states.global_state import GlobalState
from app.styles.glass_styles import GlassStyles


def role_card(title: str, description: str, icon: str, on_click_event) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="w-12 h-12 text-teal-400 mb-4"),
            rx.el.h3(title, class_name="text-xl font-bold text-white mb-2"),
            rx.el.p(description, class_name="text-slate-400 text-sm"),
            class_name="flex flex-col items-center text-center z-10 relative",
        ),
        rx.el.div(
            class_name="absolute inset-0 bg-gradient-to-b from-teal-500/0 to-teal-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        ),
        on_click=on_click_event,
        class_name=f"{GlassStyles.CARD_INTERACTIVE} w-full md:w-64 h-64 flex items-center justify-center",
    )


def role_selector() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50 animate-in fade-in duration-300"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Select Portal Access",
                    class_name=f"text-2xl {GlassStyles.HEADING} text-center mb-2",
                ),
                rx.radix.primitives.dialog.description(
                    "Please identify your role to access the longevity dashboard.",
                    class_name="text-center text-slate-400 mb-8",
                ),
                rx.el.div(
                    role_card(
                        "Patient Portal",
                        "Access your biomarkers, longevity score, and treatment protocols.",
                        "user",
                        GlobalState.set_role_patient,
                    ),
                    role_card(
                        "Clinician Portal",
                        "Manage patient cohorts, approve protocols, and analyze clinic metrics.",
                        "stethoscope",
                        GlobalState.set_role_admin,
                    ),
                    class_name="flex flex-col md:flex-row gap-6 justify-center items-center",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90vw] max-w-2xl p-8 {GlassStyles.PANEL} z-50 outline-none data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
            ),
        ),
        open=GlobalState.is_role_selector_open,
        on_open_change=GlobalState.handle_role_selector_open_change,
    )