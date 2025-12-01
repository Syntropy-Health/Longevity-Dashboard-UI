import reflex as rx
from app.states.symptom_state import SymptomState
from app.styles.glass_styles import GlassStyles
from app.schemas.symptom import Symptom


def symptom_card(symptom: Symptom) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h4(symptom.name, class_name="font-bold text-white"),
                rx.el.span(symptom.timestamp, class_name="text-xs text-slate-400"),
                class_name="flex justify-between items-center mb-2",
            ),
            rx.el.div(
                rx.el.span(
                    f"Severity: {symptom.severity}/10",
                    class_name=f"text-xs font-medium px-2 py-1 rounded-full border {rx.cond(symptom.severity > 7, 'bg-red-500/10 text-red-400 border-red-500/20', rx.cond(symptom.severity > 4, 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20', 'bg-green-500/10 text-green-400 border-green-500/20'))}",
                ),
                class_name="mb-2",
            ),
            rx.el.p(symptom.notes, class_name="text-sm text-slate-300"),
            class_name="flex-1",
        ),
        class_name=f"{GlassStyles.PANEL} p-4 flex flex-col",
    )


def symptoms_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Symptom Tracker", class_name="text-2xl font-bold text-white"),
            rx.el.button(
                "+ Log Symptom",
                on_click=SymptomState.log_symptom,
                class_name=GlassStyles.BUTTON_PRIMARY,
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.foreach(
                SymptomState.filter_options,
                lambda option: rx.el.button(
                    option,
                    on_click=lambda: SymptomState.set_view_mode(option),
                    class_name=rx.cond(
                        SymptomState.view_mode == option,
                        "px-4 py-2 rounded-lg text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30 transition-all",
                        "px-4 py-2 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 transition-all",
                    ),
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-6 bg-white/5 p-1 rounded-xl w-fit",
        ),
        rx.cond(
            SymptomState.view_mode == "Timeline",
            rx.el.div(
                rx.foreach(SymptomState.symptoms, symptom_card), class_name="space-y-4"
            ),
            rx.el.div(
                rx.el.p(
                    f"{SymptomState.view_mode} view is currently empty.",
                    class_name="text-slate-500 italic",
                ),
                class_name=f"{GlassStyles.PANEL} p-8 text-center",
            ),
        ),
        class_name="animate-in fade-in duration-500",
    )