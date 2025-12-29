"""Shared components for the patient portal."""

import reflex as rx

from ...components.charts import biomarker_history_chart
from ...data.schemas.state import Biomarker, PortalAppointment, PortalTreatment
from ...states import BiomarkerState
from ...states.shared.dashboard import SettingsState
from ...styles.constants import GlassStyles


def status_badge(status: str) -> rx.Component:
    """Status badge with dark theme styling using GlassStyles."""
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            ("Optimal", GlassStyles.STATUS_OPTIMAL),
            ("Warning", GlassStyles.STATUS_WARNING),
            ("Critical", GlassStyles.STATUS_CRITICAL),
            GlassStyles.STATUS_DEFAULT,
        ),
    )


def trend_indicator(trend: str) -> rx.Component:
    """Trend indicator with dark theme styling using GlassStyles."""
    return rx.match(
        trend,
        (
            "up",
            rx.el.div(
                rx.icon("trending-up", class_name=GlassStyles.BIOMARKER_TREND_ICON_UP),
                rx.el.span(
                    "Increasing", class_name=GlassStyles.BIOMARKER_TREND_TEXT_UP
                ),
                class_name="flex items-center",
            ),
        ),
        (
            "down",
            rx.el.div(
                rx.icon(
                    "trending-down", class_name=GlassStyles.BIOMARKER_TREND_ICON_DOWN
                ),
                rx.el.span(
                    "Decreasing", class_name=GlassStyles.BIOMARKER_TREND_TEXT_DOWN
                ),
                class_name="flex items-center",
            ),
        ),
        (
            "stable",
            rx.el.div(
                rx.icon("minus", class_name=GlassStyles.BIOMARKER_TREND_ICON_STABLE),
                rx.el.span(
                    "Stable", class_name=GlassStyles.BIOMARKER_TREND_TEXT_STABLE
                ),
                class_name="flex items-center",
            ),
        ),
        rx.el.div(),
    )


def biomarker_card(biomarker: Biomarker) -> rx.Component:
    """Biomarker card with dark theme styling using GlassStyles."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    biomarker["name"],
                    class_name=GlassStyles.BIOMARKER_CARD_TITLE,
                ),
                rx.el.p(
                    biomarker["category"],
                    class_name=GlassStyles.BIOMARKER_CARD_CATEGORY,
                ),
            ),
            status_badge(biomarker["status"]),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.span(
                biomarker["current_value"],
                class_name=GlassStyles.BIOMARKER_CARD_VALUE,
            ),
            rx.el.span(
                f" {biomarker['unit']}",
                class_name=GlassStyles.BIOMARKER_CARD_UNIT,
            ),
            class_name="flex items-baseline mb-3",
        ),
        trend_indicator(biomarker["trend"]),
        on_click=lambda: BiomarkerState.select_biomarker(biomarker),
        class_name=rx.cond(
            BiomarkerState.selected_biomarker["id"] == biomarker["id"],
            GlassStyles.BIOMARKER_CARD_SELECTED,
            f"{GlassStyles.BIOMARKER_CARD} cursor-pointer",
        ),
    )


def biomarker_detail_panel() -> rx.Component:
    """Detail panel for selected biomarker with dark theme using GlassStyles."""
    return rx.cond(
        BiomarkerState.selected_biomarker,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        BiomarkerState.selected_biomarker["name"],
                        class_name=GlassStyles.BIOMARKER_DETAIL_TITLE,
                    ),
                    rx.el.p(
                        BiomarkerState.selected_biomarker["description"],
                        class_name=GlassStyles.BIOMARKER_DETAIL_DESCRIPTION,
                    ),
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-5 h-5"),
                    on_click=BiomarkerState.clear_selected_biomarker,
                    class_name=GlassStyles.BIOMARKER_DETAIL_CLOSE_BTN,
                ),
                class_name="flex justify-between items-start mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        "Historical Trend",
                        class_name=GlassStyles.BIOMARKER_DETAIL_LABEL,
                    ),
                    biomarker_history_chart(),
                    class_name="flex-1 min-h-[300px]",
                ),
                rx.el.div(
                    rx.el.h4(
                        "Analysis",
                        class_name=GlassStyles.BIOMARKER_DETAIL_LABEL,
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Current Status",
                                class_name=GlassStyles.BIOMARKER_DETAIL_LABEL,
                            ),
                            rx.el.p(
                                BiomarkerState.selected_biomarker["status"],
                                class_name=rx.match(
                                    BiomarkerState.selected_biomarker["status"],
                                    ("Optimal", "text-teal-400 font-bold"),
                                    ("Warning", "text-amber-400 font-bold"),
                                    ("Critical", "text-red-400 font-bold"),
                                    "text-slate-300 font-bold",
                                ),
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Optimal Range",
                                class_name=GlassStyles.BIOMARKER_DETAIL_LABEL,
                            ),
                            rx.el.p(
                                f"{BiomarkerState.selected_biomarker['optimal_min']} - {BiomarkerState.selected_biomarker['optimal_max']} {BiomarkerState.selected_biomarker['unit']}",
                                class_name=GlassStyles.BIOMARKER_DETAIL_VALUE,
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Latest Reading",
                                class_name=GlassStyles.BIOMARKER_DETAIL_LABEL,
                            ),
                            rx.el.p(
                                f"{BiomarkerState.selected_biomarker['current_value']} {BiomarkerState.selected_biomarker['unit']}",
                                class_name=GlassStyles.BIOMARKER_DETAIL_VALUE,
                            ),
                        ),
                        class_name=GlassStyles.BIOMARKER_DETAIL_ANALYSIS_BOX,
                    ),
                    class_name="w-full lg:w-64 shrink-0 lg:ml-6 mt-6 lg:mt-0",
                ),
                class_name="flex flex-col lg:flex-row",
            ),
            class_name=GlassStyles.BIOMARKER_DETAIL_PANEL,
        ),
    )


def treatment_card(treatment: PortalTreatment) -> rx.Component:
    """Treatment card with dark theme styling using GlassStyles."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", class_name=GlassStyles.PORTAL_TREATMENT_ICON),
                class_name=GlassStyles.PORTAL_TREATMENT_ICON_CONTAINER,
            ),
            rx.el.div(
                rx.el.h4(
                    treatment["name"], class_name=GlassStyles.PORTAL_TREATMENT_TITLE
                ),
                rx.el.p(
                    f"{treatment['frequency']} • {treatment['duration']}",
                    class_name=GlassStyles.PORTAL_TREATMENT_META,
                ),
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.span(
                treatment["status"],
                class_name=GlassStyles.PORTAL_TREATMENT_STATUS_BADGE,
            ),
            class_name="ml-auto",
        ),
        class_name=GlassStyles.PORTAL_TREATMENT_CARD,
    )


def appointment_item(apt: PortalAppointment) -> rx.Component:
    """Appointment item with dark theme styling."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                apt["date"],
                class_name="text-xs font-bold text-teal-400 uppercase tracking-wide",
            ),
            rx.el.p(apt["time"], class_name="text-xs text-slate-400"),
            class_name="w-16 shrink-0 text-center mr-4 bg-teal-500/10 rounded-lg py-2 border border-teal-500/20",
        ),
        rx.el.div(
            rx.el.h5(apt["title"], class_name="text-sm font-semibold text-white"),
            rx.el.p(
                f"{apt['type']} with {apt['provider']}",
                class_name="text-xs text-slate-400",
            ),
        ),
        class_name="flex items-center py-3 border-b border-white/10 last:border-0",
    )


# Re-export static_metric_card from shared for backward compatibility
from ...components.shared import static_metric_card

__all__ = [
    "appointment_item",
    "biomarker_card",
    "biomarker_detail_panel",
    "patient_portal_tabs",
    "static_metric_card",
    "status_badge",
    "tab_button",
    "treatment_card",
    "trend_indicator",
]


def tab_button(label: str, tab_id: str, icon: str) -> rx.Component:
    """Tab button for dashboard navigation."""
    return rx.el.button(
        rx.icon(icon, class_name="w-4 h-4 mr-2"),
        label,
        on_click=lambda: SettingsState.set_active_tab(tab_id),
        class_name=rx.cond(
            SettingsState.active_tab == tab_id,
            "flex items-center px-4 py-2.5 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30 transition-all",
            "flex items-center px-4 py-2.5 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent transition-all",
        ),
    )


def patient_portal_tabs() -> rx.Component:
    """Patient dashboard tab navigation - main portal tabs only.

    Shows: Dashboard (overview), Food Tracker, Medications, Conditions, Symptoms
    Check-ins and Settings are separate pages (no tabs shown on those pages).
    """
    return rx.el.div(
        rx.el.div(
            tab_button("Dashboard", "overview", "layout-dashboard"),
            tab_button("Food Tracker", "food", "apple"),
            tab_button("Medications", "medications", "pill"),
            tab_button("Conditions", "conditions", "heart-pulse"),
            tab_button("Symptoms", "symptoms", "thermometer"),
            class_name="flex flex-wrap gap-2 p-2 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10",
        ),
        class_name="mb-8",
    )
