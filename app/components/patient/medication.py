import reflex as rx
from app.states.medication_state import MedicationState
from app.schemas.medication import Medication
from app.styles.glass_styles import GlassStyles


def medication_card(med: Medication) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("pill", class_name="w-6 h-6 text-teal-400 mb-2"),
                rx.el.h3(med.name, class_name="text-lg font-bold text-white"),
                rx.el.p(
                    f"{med.dosage} • {med.frequency}",
                    class_name="text-sm text-slate-400",
                ),
                class_name="flex flex-col items-start mb-4",
            ),
            rx.el.div(
                rx.el.span(
                    f"Efficacy: {med.efficacy_rating}/10",
                    class_name="text-xs font-bold text-teal-400 bg-teal-500/10 px-2 py-1 rounded border border-teal-500/20",
                ),
                class_name="absolute top-4 right-4",
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Adherence", class_name="text-xs text-slate-500 uppercase"),
                rx.el.p(
                    f"{med.adherence_score}%", class_name="text-sm font-bold text-white"
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Refill By",
                    class_name="text-xs text-slate-500 uppercase text-right",
                ),
                rx.el.p(
                    med.next_refill,
                    class_name="text-sm font-bold text-slate-300 text-right",
                ),
            ),
            class_name="flex justify-between items-center mt-4 pt-4 border-t border-white/10 w-full",
        ),
        rx.el.button(
            "Mark Taken",
            on_click=lambda: MedicationState.mark_taken(med.id),
            class_name="w-full mt-4 py-2 rounded-lg bg-white/5 hover:bg-teal-500/20 hover:text-teal-300 text-slate-300 border border-white/10 transition-all text-sm font-medium",
        ),
        class_name=f"{GlassStyles.CARD_INTERACTIVE} flex flex-col justify-between",
    )


def medication_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Medication Protocol", class_name="text-2xl font-bold text-white"
                ),
                rx.el.p(
                    "Manage your prescriptions and adherence.",
                    class_name="text-slate-400 text-sm",
                ),
            ),
            rx.el.button("Refill All", class_name=GlassStyles.BUTTON_SECONDARY),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Adherence Score",
                    class_name="text-sm font-medium text-slate-400 mb-2",
                ),
                rx.el.div(
                    rx.el.h2(
                        f"{MedicationState.overall_efficacy_score}%",
                        class_name="text-4xl font-bold text-teal-400",
                    ),
                    rx.el.p(
                        "Excellent consistency",
                        class_name="text-sm text-green-400 mt-1",
                    ),
                    class_name="mb-4",
                ),
                class_name=f"{GlassStyles.PANEL} p-6 mb-8 flex flex-col items-center justify-center text-center",
            ),
            class_name="grid grid-cols-1 mb-6",
        ),
        rx.el.div(
            rx.foreach(MedicationState.medications, medication_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        class_name="animate-in fade-in duration-500",
    )