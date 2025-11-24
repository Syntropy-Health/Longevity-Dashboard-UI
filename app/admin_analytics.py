import reflex as rx
from app.components.navbar import navbar
from app.components.analytics_charts import (
    admin_volume_chart,
    admin_protocol_chart,
    admin_biomarker_improvement_chart,
)
from app.states.analytics_state import AnalyticsState
from app.styles.glass_styles import GlassStyles


def kpi_card(title: str, value: str, trend: str, trend_up: bool = True) -> rx.Component:
    return rx.el.div(
        rx.el.p(title, class_name="text-sm text-slate-400 font-medium mb-2"),
        rx.el.div(
            rx.el.h3(value, class_name="text-3xl font-bold text-white"),
            rx.el.span(
                trend,
                class_name=f"text-xs font-medium px-2 py-1 rounded-full border {('bg-teal-500/10 text-teal-400 border-teal-500/20' if trend_up else 'bg-red-500/10 text-red-400 border-red-500/20')}",
            ),
            class_name="flex items-end gap-3",
        ),
        class_name=f"{GlassStyles.PANEL} p-6",
    )


def detail_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    AnalyticsState.detail_title,
                    class_name="text-xl font-bold text-white mb-4",
                ),
                rx.el.div(
                    rx.cond(
                        AnalyticsState.detail_type == "volume",
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Month",
                                        class_name="text-left py-2 text-slate-400",
                                    ),
                                    rx.el.th(
                                        "Patients",
                                        class_name="text-right py-2 text-slate-400",
                                    ),
                                    rx.el.th(
                                        "Requests",
                                        class_name="text-right py-2 text-slate-400",
                                    ),
                                    rx.el.th(
                                        "Approvals",
                                        class_name="text-right py-2 text-slate-400",
                                    ),
                                ),
                                class_name="border-b border-white/10",
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    AnalyticsState.operational_data,
                                    lambda row: rx.el.tr(
                                        rx.el.td(
                                            row["month"],
                                            class_name="py-3 text-slate-300",
                                        ),
                                        rx.el.td(
                                            row["patients"],
                                            class_name="py-3 text-right text-white",
                                        ),
                                        rx.el.td(
                                            row["requests"],
                                            class_name="py-3 text-right text-white",
                                        ),
                                        rx.el.td(
                                            row["approvals"],
                                            class_name="py-3 text-right text-teal-400",
                                        ),
                                        class_name="border-b border-white/5",
                                    ),
                                )
                            ),
                            class_name="w-full",
                        ),
                    ),
                    rx.cond(
                        AnalyticsState.detail_type == "protocols",
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Protocol",
                                        class_name="text-left py-2 text-slate-400",
                                    ),
                                    rx.el.th(
                                        "Active Patients",
                                        class_name="text-right py-2 text-slate-400",
                                    ),
                                    rx.el.th(
                                        "Eff. Score",
                                        class_name="text-right py-2 text-slate-400",
                                    ),
                                ),
                                class_name="border-b border-white/10",
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    AnalyticsState.protocol_usage_data,
                                    lambda row: rx.el.tr(
                                        rx.el.td(
                                            row["name"],
                                            class_name="py-3 text-slate-300",
                                        ),
                                        rx.el.td(
                                            row["count"],
                                            class_name="py-3 text-right text-white",
                                        ),
                                        rx.el.td(
                                            rx.el.span(
                                                f"{row['effectiveness']}%",
                                                class_name="text-teal-400",
                                            ),
                                            class_name="py-3 text-right",
                                        ),
                                        class_name="border-b border-white/5",
                                    ),
                                )
                            ),
                            class_name="w-full",
                        ),
                    ),
                    class_name="max-h-[60vh] overflow-auto",
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button("Close", class_name=GlassStyles.BUTTON_SECONDARY)
                    ),
                    class_name="flex justify-end mt-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90vw] max-w-2xl p-8 {GlassStyles.PANEL} z-50",
            ),
        ),
        open=AnalyticsState.detail_modal_open,
        on_open_change=AnalyticsState.handle_detail_modal_open_change,
    )


def admin_analytics_page() -> rx.Component:
    return rx.el.div(
        detail_modal(),
        rx.el.h1(
            "Clinic Operations Analytics",
            class_name=f"text-3xl font-bold {GlassStyles.HEADING} mb-8",
        ),
        rx.el.div(
            kpi_card("Total Active Patients", "1,248", "+12% vs last month"),
            kpi_card("Revenue (MRR)", "$424k", "+8.5% vs last month"),
            kpi_card("Avg. Longevity Score", "86.4", "+1.2% vs last month"),
            kpi_card("Appointments Today", "18", "-2% vs last month", trend_up=False),
            kpi_card("Avg. Appt. Duration", "45min", "+8% vs last month"),
            kpi_card("Active Protocols", "42", "+4% vs last month"),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Patient Growth & Requests",
                        class_name="text-xl font-bold text-white",
                    ),
                    rx.el.button(
                        "View Details",
                        on_click=lambda: AnalyticsState.open_detail_modal(
                            "Monthly Growth Data", "volume"
                        ),
                        class_name="text-sm text-teal-400 hover:text-teal-300 transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                admin_volume_chart(),
                class_name=f"{GlassStyles.PANEL} p-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Protocol Distribution",
                        class_name="text-xl font-bold text-white",
                    ),
                    rx.el.button(
                        "View Details",
                        on_click=lambda: AnalyticsState.open_detail_modal(
                            "Protocol Performance", "protocols"
                        ),
                        class_name="text-sm text-teal-400 hover:text-teal-300 transition-colors",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                admin_protocol_chart(),
                class_name=f"{GlassStyles.PANEL} p-6",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Avg. Biomarker Improvements",
                    class_name="text-xl font-bold text-white mb-6",
                ),
                admin_biomarker_improvement_chart(),
                class_name=f"{GlassStyles.PANEL} p-6",
            ),
            class_name="w-full mb-8",
        ),
        class_name="max-w-7xl mx-auto",
    )