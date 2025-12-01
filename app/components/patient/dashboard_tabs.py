import reflex as rx
from app.styles.glass_styles import GlassStyles
from app.components.patient.conditions import conditions_tab
from app.components.patient.symptoms import symptoms_tab
from app.components.patient.data_sources import data_sources_tab
from app.components.patient.nutrition import nutrition_tab
from app.components.patient.medication import medication_tab
from app.states.nutrition_state import NutritionState
from app.states.medication_state import MedicationState
from app.states.checkin_state import CheckInState
from app.patient_intake import patient_intake_page


class TabState(rx.State):
    current_tab: str = "dashboard"

    @rx.event
    def set_tab(self, tab: str):
        self.current_tab = tab


def tab_button(label: str, value: str, icon: str) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="w-4 h-4 mr-2"),
        label,
        on_click=lambda: TabState.set_tab(value),
        class_name=rx.cond(
            TabState.current_tab == value,
            "flex items-center px-4 py-2.5 rounded-xl text-sm font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20 transition-all",
            "flex items-center px-4 py-2.5 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent transition-all",
        ),
    )


def check_in_logger() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Daily Check-in", class_name="text-lg font-bold text-white mb-4"),
        rx.el.div(
            rx.el.button(
                rx.el.div(
                    rx.icon(
                        rx.cond(CheckInState.is_voice_recording, "loader-2", "mic"),
                        class_name=f"w-6 h-6 mb-2 {rx.cond(CheckInState.is_voice_recording, 'animate-spin text-red-400', 'text-teal-400')}",
                    ),
                    rx.el.span(
                        rx.cond(
                            CheckInState.is_voice_recording, "Recording...", "Voice Log"
                        ),
                        class_name="text-xs font-bold uppercase tracking-wider text-slate-300",
                    ),
                    class_name="flex flex-col items-center",
                ),
                on_click=CheckInState.toggle_voice_recording,
                class_name=f"flex-1 p-6 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all {rx.cond(CheckInState.is_voice_recording, 'border-red-500/50 bg-red-500/10', '')}",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.input(
                        placeholder="Type a quick note...",
                        on_change=CheckInState.set_new_note_content,
                        class_name="w-full bg-transparent border-none text-white placeholder-slate-500 focus:outline-none focus:ring-0 p-0",
                        default_value=CheckInState.new_note_content,
                    ),
                    rx.el.button(
                        rx.icon("send", class_name="w-4 h-4 text-teal-400"),
                        on_click=CheckInState.save_text_note,
                        class_name="p-2 hover:bg-white/10 rounded-lg transition-colors",
                    ),
                    class_name="flex items-center gap-2 border-b border-white/10 pb-2 mb-2",
                ),
                rx.el.span(
                    "Text Log",
                    class_name="text-xs font-bold uppercase tracking-wider text-slate-500",
                ),
                class_name="flex-[2] p-6 rounded-xl bg-white/5 border border-white/10 flex flex-col justify-between",
            ),
            class_name="flex gap-4 h-32 mb-6",
        ),
    )


def dashboard_overview() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Health Overview", class_name="text-2xl font-bold text-white mb-6"),
        rx.el.div(
            rx.el.div(
                rx.el.p("Overall Health", class_name="text-sm text-slate-400 mb-2"),
                rx.el.h3("82%", class_name="text-3xl font-bold text-teal-400"),
                rx.el.div(
                    rx.el.div(class_name="h-2 rounded-full bg-teal-500 w-[82%]"),
                    class_name="h-2 rounded-full bg-slate-700 mt-2",
                ),
                class_name=f"{GlassStyles.PANEL} p-6",
            ),
            rx.el.div(
                rx.el.p("Nutrition Score", class_name="text-sm text-slate-400 mb-2"),
                rx.el.h3(
                    NutritionState.current_day.nutrition_score.to_string(),
                    class_name="text-3xl font-bold text-teal-400",
                ),
                rx.el.div(
                    rx.el.div(class_name="h-2 rounded-full bg-teal-500 w-[76%]"),
                    class_name="h-2 rounded-full bg-slate-700 mt-2",
                ),
                class_name=f"{GlassStyles.PANEL} p-6",
            ),
            rx.el.div(
                rx.el.p(
                    "Medication Efficacy", class_name="text-sm text-slate-400 mb-2"
                ),
                rx.el.h3(
                    MedicationState.overall_efficacy_score.to_string() + "%",
                    class_name="text-3xl font-bold text-teal-400",
                ),
                rx.el.div(
                    rx.el.div(class_name="h-2 rounded-full bg-teal-500 w-[88%]"),
                    class_name="h-2 rounded-full bg-slate-700 mt-2",
                ),
                class_name=f"{GlassStyles.PANEL} p-6",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                check_in_logger(),
                rx.el.div(
                    rx.el.h3(
                        "Recent Check-ins",
                        class_name="text-lg font-bold text-white mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            CheckInState.checkins,
                            lambda c: rx.el.div(
                                rx.icon(
                                    rx.cond(c.type == "Voice", "mic", "message-square"),
                                    class_name="w-5 h-5 text-teal-400 mr-3 mt-1",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        c.content,
                                        class_name="text-slate-200 text-sm font-medium",
                                    ),
                                    rx.el.p(
                                        c.timestamp,
                                        class_name="text-xs text-slate-500 mt-1",
                                    ),
                                ),
                                class_name="flex items-start p-3 rounded-lg bg-white/5 mb-2 border border-white/5",
                            ),
                        ),
                        class_name="max-h-[300px] overflow-y-auto pr-2",
                    ),
                    class_name="flex-1",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
            ),
            class_name=f"{GlassStyles.PANEL} p-6",
        ),
    )


def patient_dashboard_container() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                tab_button("Dashboard", "dashboard", "layout-dashboard"),
                tab_button("Food Tracker", "nutrition", "utensils"),
                tab_button("Medication", "medication", "pill"),
                tab_button("Conditions", "conditions", "activity"),
                tab_button("Symptoms", "symptoms", "stethoscope"),
                tab_button("Data Sources", "datasources", "database"),
                tab_button("Settings", "settings", "settings"),
                class_name="flex flex-wrap gap-2 mb-8 border-b border-white/10 pb-4",
            ),
            rx.cond(TabState.current_tab == "dashboard", dashboard_overview()),
            rx.cond(TabState.current_tab == "nutrition", nutrition_tab()),
            rx.cond(TabState.current_tab == "medication", medication_tab()),
            rx.cond(TabState.current_tab == "conditions", conditions_tab()),
            rx.cond(TabState.current_tab == "symptoms", symptoms_tab()),
            rx.cond(TabState.current_tab == "datasources", data_sources_tab()),
            rx.cond(TabState.current_tab == "settings", patient_intake_page()),
            class_name="w-full",
        ),
        class_name="max-w-7xl mx-auto",
    )