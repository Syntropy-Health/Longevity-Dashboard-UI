import reflex as rx
from ..components.layout import authenticated_layout
from ..states.auth_state import AuthState
from ..states.patient_biomarker_state import (
    PatientBiomarkerState,
    Biomarker,
    PortalAppointment,
    PortalTreatment,
)
from ..components.charts import biomarker_history_chart


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Optimal",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800",
            ),
            (
                "Warning",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800",
            ),
            (
                "Critical",
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
            ),
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800",
        ),
    )


def trend_indicator(trend: str) -> rx.Component:
    return rx.match(
        trend,
        (
            "up",
            rx.el.div(
                rx.icon("trending-up", class_name="w-4 h-4 mr-1 text-emerald-500"),
                rx.el.span("Increasing", class_name="text-xs text-emerald-600"),
                class_name="flex items-center",
            ),
        ),
        (
            "down",
            rx.el.div(
                rx.icon("trending-down", class_name="w-4 h-4 mr-1 text-emerald-500"),
                rx.el.span("Decreasing", class_name="text-xs text-emerald-600"),
                class_name="flex items-center",
            ),
        ),
        (
            "stable",
            rx.el.div(
                rx.icon("minus", class_name="w-4 h-4 mr-1 text-gray-400"),
                rx.el.span("Stable", class_name="text-xs text-gray-500"),
                class_name="flex items-center",
            ),
        ),
        rx.el.div(),
    )


from ..config import current_config


def biomarker_card(biomarker: Biomarker) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    biomarker["name"],
                    class_name="text-sm font-semibold text-gray-800 truncate",
                ),
                rx.el.p(
                    biomarker["category"],
                    class_name="text-[10px] text-gray-400 truncate uppercase tracking-widest font-semibold mt-1",
                ),
            ),
            status_badge(biomarker["status"]),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.span(
                biomarker["current_value"],
                class_name="text-4xl font-thin text-gray-800 tracking-tighter",
            ),
            rx.el.span(
                f" {biomarker['unit']}",
                class_name="text-xs font-medium text-gray-400 ml-1",
            ),
            class_name="flex items-baseline mb-3",
        ),
        trend_indicator(biomarker["trend"]),
        on_click=lambda: PatientBiomarkerState.select_biomarker(biomarker),
        class_name=rx.cond(
            PatientBiomarkerState.selected_biomarker["id"] == biomarker["id"],
            f"bg-emerald-50/40 backdrop-blur-xl ring-1 ring-emerald-500/30 p-6 rounded-[1.5rem] shadow-lg border border-emerald-100/50 cursor-pointer transition-all duration-300 scale-[1.02]",
            f"{current_config.glass_panel_style} p-6 rounded-[1.5rem] {current_config.glass_card_hover} cursor-pointer",
        ),
    )


def biomarker_detail_panel() -> rx.Component:
    return rx.cond(
        PatientBiomarkerState.selected_biomarker,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        PatientBiomarkerState.selected_biomarker["name"],
                        class_name="text-xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        PatientBiomarkerState.selected_biomarker["description"],
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-5 h-5"),
                    on_click=PatientBiomarkerState.clear_selected_biomarker,
                    class_name="p-2 hover:bg-gray-100 rounded-full text-gray-500",
                ),
                class_name="flex justify-between items-start mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        "Historical Trend",
                        class_name="text-sm font-semibold text-gray-700 mb-4",
                    ),
                    biomarker_history_chart(),
                    class_name="flex-1 min-h-[300px]",
                ),
                rx.el.div(
                    rx.el.h4(
                        "Analysis",
                        class_name="text-sm font-semibold text-gray-700 mb-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Current Status",
                                class_name="text-xs text-gray-500 uppercase font-semibold",
                            ),
                            rx.el.p(
                                PatientBiomarkerState.selected_biomarker["status"],
                                class_name=rx.match(
                                    PatientBiomarkerState.selected_biomarker["status"],
                                    ("Optimal", "text-emerald-600 font-bold"),
                                    ("Warning", "text-yellow-600 font-bold"),
                                    ("Critical", "text-red-600 font-bold"),
                                    "text-gray-600 font-bold",
                                ),
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Optimal Range",
                                class_name="text-xs text-gray-500 uppercase font-semibold",
                            ),
                            rx.el.p(
                                f"{PatientBiomarkerState.selected_biomarker['optimal_min']} - {PatientBiomarkerState.selected_biomarker['optimal_max']} {PatientBiomarkerState.selected_biomarker['unit']}",
                                class_name="text-gray-900 font-medium",
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Latest Reading",
                                class_name="text-xs text-gray-500 uppercase font-semibold",
                            ),
                            rx.el.p(
                                f"{PatientBiomarkerState.selected_biomarker['current_value']} {PatientBiomarkerState.selected_biomarker['unit']}",
                                class_name="text-gray-900 font-medium",
                            ),
                        ),
                        class_name="bg-gray-50/50 p-4 rounded-lg border border-gray-100/50",
                    ),
                    class_name="w-full lg:w-64 shrink-0 lg:ml-6 mt-6 lg:mt-0",
                ),
                class_name="flex flex-col lg:flex-row",
            ),
            class_name=f"{current_config.glass_panel_style} p-6 rounded-xl mb-8 animate-fade-in",
        ),
    )


def treatment_card(treatment: PortalTreatment) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name="w-5 h-5 text-emerald-600"),
                class_name="w-10 h-10 rounded-full bg-emerald-100/50 flex items-center justify-center mr-3 shrink-0 border border-emerald-100",
            ),
            rx.el.div(
                rx.el.h4(
                    treatment["name"], class_name="text-sm font-semibold text-gray-900"
                ),
                rx.el.p(
                    f"{treatment['frequency']} • {treatment['duration']}",
                    class_name="text-xs text-gray-500",
                ),
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.span(
                treatment["status"],
                class_name="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100/50 text-green-800 border border-green-200/50",
            ),
            class_name="ml-auto",
        ),
        class_name=f"{current_config.glass_panel_style} p-4 rounded-lg hover:shadow-md transition-shadow",
    )


def appointment_item(apt: PortalAppointment) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                apt["date"],
                class_name="text-xs font-bold text-emerald-600 uppercase tracking-wide",
            ),
            rx.el.p(apt["time"], class_name="text-xs text-gray-500"),
            class_name="w-16 shrink-0 text-center mr-4 bg-emerald-50/50 rounded-md py-2 border border-emerald-100/50",
        ),
        rx.el.div(
            rx.el.h5(apt["title"], class_name="text-sm font-semibold text-gray-900"),
            rx.el.p(
                f"{apt['type']} with {apt['provider']}",
                class_name="text-xs text-gray-500",
            ),
        ),
        class_name="flex items-center py-3 border-b border-gray-100/50 last:border-0",
    )


def patient_portal() -> rx.Component:
    return authenticated_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    f"Welcome back, {AuthState.user['full_name']}",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Here is your latest health intelligence report.",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Biomarker Intelligence",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.foreach(PatientBiomarkerState.biomarkers, biomarker_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-6",
                ),
                biomarker_detail_panel(),
                class_name="mb-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Active Protocols",
                            class_name="text-lg font-bold text-gray-900 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                PatientBiomarkerState.my_treatments, treatment_card
                            ),
                            class_name="space-y-3",
                        ),
                        class_name="col-span-1 lg:col-span-2",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Upcoming Schedule",
                            class_name="text-lg font-bold text-gray-900 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                PatientBiomarkerState.upcoming_appointments,
                                appointment_item,
                            ),
                            rx.el.button(
                                "View Full Calendar",
                                class_name="w-full mt-4 py-2 text-sm text-emerald-600 font-medium hover:text-emerald-700 border border-emerald-200 rounded-md hover:bg-emerald-50 transition-colors",
                            ),
                            class_name="bg-white p-5 rounded-xl shadow-sm border border-gray-200",
                        ),
                        class_name="col-span-1",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
                ),
                class_name="mb-8",
            ),
        )
    )