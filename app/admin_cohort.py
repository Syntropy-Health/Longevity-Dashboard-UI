import reflex as rx
from app.states.cohort_state import CohortState
from app.styles.glass_styles import GlassStyles
from app.models import CohortPatient
from app.enums import PatientStatus


def kpi_card(title: str, value: str, icon: str, subtext: str = "") -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="w-6 h-6 text-teal-400 mb-3"),
            rx.el.h3(value, class_name="text-3xl font-bold text-white mb-1"),
            rx.el.p(title, class_name="text-sm text-slate-400 font-medium"),
            rx.el.p(subtext, class_name="text-xs text-teal-400/80 mt-2"),
            class_name="flex flex-col",
        ),
        class_name=f"{GlassStyles.PANEL} p-6 transition-all hover:scale-[1.02] duration-300",
    )


def patient_detail_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50 animate-in fade-in duration-200"
            ),
            rx.radix.primitives.dialog.content(
                rx.cond(
                    CohortState.selected_patient,
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.h2(
                                    CohortState.selected_patient.name,
                                    class_name="text-2xl font-bold text-white",
                                ),
                                rx.el.span(
                                    CohortState.selected_patient.status,
                                    class_name="px-3 py-1 rounded-full text-xs font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20 uppercase tracking-wider",
                                ),
                                class_name="flex items-center gap-3 mb-1",
                            ),
                            rx.el.p(
                                CohortState.selected_patient.email,
                                class_name="text-slate-400 text-sm",
                            ),
                            class_name="mb-8 pb-6 border-b border-white/10",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Biological Age",
                                    class_name="text-xs text-slate-500 uppercase tracking-wider",
                                ),
                                rx.el.p(
                                    CohortState.selected_patient.biological_age,
                                    class_name="text-xl font-bold text-white",
                                ),
                                class_name="bg-white/5 rounded-xl p-4 border border-white/5",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Chronological",
                                    class_name="text-xs text-slate-500 uppercase tracking-wider",
                                ),
                                rx.el.p(
                                    CohortState.selected_patient.age,
                                    class_name="text-xl font-bold text-slate-300",
                                ),
                                class_name="bg-white/5 rounded-xl p-4 border border-white/5",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Longevity Score",
                                    class_name="text-xs text-slate-500 uppercase tracking-wider",
                                ),
                                rx.el.p(
                                    CohortState.selected_patient.longevity_score,
                                    class_name="text-xl font-bold text-teal-400",
                                ),
                                class_name="bg-white/5 rounded-xl p-4 border border-white/5",
                            ),
                            class_name="grid grid-cols-3 gap-4 mb-8",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Active Protocols",
                                    class_name="text-sm font-bold text-white mb-4 uppercase tracking-wider",
                                ),
                                rx.cond(
                                    CohortState.selected_patient.active_protocols,
                                    rx.el.div(
                                        rx.foreach(
                                            CohortState.selected_patient.active_protocols,
                                            lambda p: rx.el.div(
                                                rx.icon(
                                                    "pill",
                                                    class_name="w-4 h-4 text-teal-400 mr-2",
                                                ),
                                                p,
                                                class_name="flex items-center p-3 rounded-lg bg-white/5 border border-white/5 text-sm text-slate-300 mb-2",
                                            ),
                                        )
                                    ),
                                    rx.el.p(
                                        "No active protocols.",
                                        class_name="text-slate-500 italic text-sm",
                                    ),
                                ),
                                class_name="col-span-1",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    "Recent Biomarkers",
                                    class_name="text-sm font-bold text-white mb-4 uppercase tracking-wider",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            "NAD+", class_name="text-slate-400 text-sm"
                                        ),
                                        rx.el.span(
                                            rx.text(
                                                CohortState.selected_patient.biomarkers[
                                                    "NAD+"
                                                ]
                                            ),
                                            " µM",
                                            class_name="text-white font-medium text-sm",
                                        ),
                                        class_name="flex justify-between items-center py-2 border-b border-white/5",
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            "hs-CRP",
                                            class_name="text-slate-400 text-sm",
                                        ),
                                        rx.el.span(
                                            rx.text(
                                                CohortState.selected_patient.biomarkers[
                                                    "hs-CRP"
                                                ]
                                            ),
                                            " mg/L",
                                            class_name="text-white font-medium text-sm",
                                        ),
                                        class_name="flex justify-between items-center py-2 border-b border-white/5",
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            "Vitamin D",
                                            class_name="text-slate-400 text-sm",
                                        ),
                                        rx.el.span(
                                            rx.text(
                                                CohortState.selected_patient.biomarkers[
                                                    "Vitamin D"
                                                ]
                                            ),
                                            " ng/mL",
                                            class_name="text-white font-medium text-sm",
                                        ),
                                        class_name="flex justify-between items-center py-2 border-b border-white/5",
                                    ),
                                    class_name="bg-white/5 rounded-xl p-4 border border-white/5",
                                ),
                                class_name="col-span-1",
                            ),
                            class_name="grid grid-cols-2 gap-8 mb-8",
                        ),
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Close", class_name=GlassStyles.BUTTON_SECONDARY
                                )
                            ),
                            rx.el.button(
                                "Message Patient",
                                on_click=CohortState.send_message,
                                class_name=f"{GlassStyles.BUTTON_PRIMARY} ml-2",
                            ),
                            class_name="flex justify-end pt-4 border-t border-white/10",
                        ),
                    ),
                    rx.fragment(),
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90vw] max-w-2xl p-8 {GlassStyles.PANEL} z-50 outline-none data-[state=open]:animate-in data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
            ),
        ),
        open=CohortState.is_detail_open,
        on_open_change=CohortState.handle_detail_modal_open_change,
    )


def patient_row(patient: CohortPatient) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=patient.img_url,
                    class_name="w-10 h-10 rounded-full object-cover border border-white/10",
                ),
                rx.el.div(
                    rx.el.p(patient.name, class_name="font-medium text-white"),
                    rx.el.p(patient.email, class_name="text-xs text-slate-500"),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="py-4 px-4",
        ),
        rx.el.td(
            rx.el.span(
                patient.status,
                class_name=f"px-2 py-1 rounded-full text-xs font-medium border uppercase tracking-wider {rx.cond(patient.status == 'Active', 'bg-teal-500/10 text-teal-300 border-teal-500/20', rx.cond(patient.status == 'Onboarding', 'bg-blue-500/10 text-blue-300 border-blue-500/20', 'bg-slate-500/10 text-slate-400 border-slate-500/20'))}",
            ),
            class_name="py-4 px-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"{patient.biological_age} yrs",
                    class_name="text-teal-300 font-bold",
                ),
                rx.el.span(f" / {patient.age}", class_name="text-slate-500 text-xs"),
            ),
            class_name="py-4 px-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(patient.longevity_score, class_name="font-bold text-white"),
                rx.el.span("/100", class_name="text-xs text-slate-500"),
            ),
            class_name="py-4 px-4",
        ),
        rx.el.td(patient.last_visit, class_name="py-4 px-4 text-slate-400 text-sm"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "Details",
                    on_click=lambda: CohortState.open_detail_modal(patient),
                    class_name="text-xs font-medium text-teal-400 hover:text-teal-300 bg-teal-500/10 hover:bg-teal-500/20 px-3 py-1.5 rounded-lg border border-teal-500/20 transition-colors mr-2",
                ),
                rx.el.button(
                    rx.icon("message-square", class_name="w-4 h-4"),
                    on_click=CohortState.send_message,
                    class_name="p-1.5 text-slate-400 hover:text-white transition-colors",
                ),
                class_name="flex items-center justify-end",
            ),
            class_name="py-4 px-4 text-right",
        ),
        class_name="border-b border-white/5 hover:bg-white/5 transition-colors group",
    )


def admin_cohort_page() -> rx.Component:
    return rx.el.div(
        patient_detail_modal(),
        rx.el.div(
            rx.el.h1(
                "Patient Cohort", class_name=f"text-3xl font-bold {GlassStyles.HEADING}"
            ),
            rx.el.button(
                "+ Add Patient",
                on_click=CohortState.edit_patient,
                class_name=GlassStyles.BUTTON_PRIMARY,
            ),
            class_name="flex justify-between items-center mb-8",
        ),
        rx.el.div(
            kpi_card(
                "Total Patients",
                CohortState.total_patients.to_string(),
                "users",
                "Lifetime total",
            ),
            kpi_card(
                "Active Patients",
                CohortState.active_patients_count.to_string(),
                "activity",
                "Currently enrolled",
            ),
            kpi_card(
                "Avg Longevity Score",
                CohortState.avg_longevity_score.to_string(),
                "heart-pulse",
                "Cohort average",
            ),
            kpi_card(
                "New This Month",
                CohortState.patients_this_month.to_string(),
                "user-plus",
                "Growth rate",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2",
                    ),
                    rx.el.input(
                        placeholder="Search by name or email...",
                        on_change=CohortState.set_search_query,
                        class_name="w-full pl-10 pr-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 transition-all",
                    ),
                    class_name="relative w-full md:w-96",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("All Statuses", value="All"),
                        rx.foreach(
                            ["Active", "Inactive", "Onboarding"],
                            lambda s: rx.el.option(s, value=s),
                        ),
                        on_change=CohortState.set_status_filter,
                        class_name="px-4 py-2.5 bg-slate-800/50 border border-white/10 rounded-xl text-slate-300 focus:outline-none focus:border-teal-500/50",
                    ),
                    class_name="flex gap-4",
                ),
                class_name="flex flex-col md:flex-row justify-between items-center gap-4 mb-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Patient",
                                class_name="text-left py-3 px-4 text-slate-400 font-medium text-sm",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="text-left py-3 px-4 text-slate-400 font-medium text-sm",
                            ),
                            rx.el.th(
                                "Bio / Chron Age",
                                class_name="text-left py-3 px-4 text-slate-400 font-medium text-sm",
                            ),
                            rx.el.th(
                                "Longevity Score",
                                class_name="text-left py-3 px-4 text-slate-400 font-medium text-sm",
                            ),
                            rx.el.th(
                                "Last Visit",
                                class_name="text-left py-3 px-4 text-slate-400 font-medium text-sm",
                            ),
                            rx.el.th(
                                "Actions",
                                class_name="text-right py-3 px-4 text-slate-400 font-medium text-sm",
                            ),
                        ),
                        class_name="border-b border-white/10",
                    ),
                    rx.el.tbody(
                        rx.cond(
                            CohortState.filtered_patients,
                            rx.foreach(CohortState.filtered_patients, patient_row),
                            rx.el.tr(
                                rx.el.td(
                                    "No patients found matching your criteria.",
                                    col_span=6,
                                    class_name="py-8 text-center text-slate-500 italic",
                                )
                            ),
                        )
                    ),
                    class_name="w-full table-auto",
                ),
                class_name="overflow-x-auto",
            ),
            class_name=f"{GlassStyles.PANEL} p-6",
        ),
        class_name="max-w-7xl mx-auto",
    )