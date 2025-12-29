"""Patient portal main page."""

import reflex as rx

from ...components.layout import authenticated_layout
from ...states import AuthState, SettingsState
from ...styles.constants import GlassStyles
from .components import patient_portal_tabs
from .modals import (
    add_food_modal,
    checkin_modal,
    condition_modal,
    connect_source_modal,
    medication_modal,
    symptom_modal,
)
from .tabs import (
    conditions_tab,
    food_tracker_tab,
    medications_tab,
    overview_tab,
    symptoms_tab,
)


def _patient_portal_base(initial_tab: str = "overview") -> rx.Component:
    """Base patient dashboard component with configurable initial tab."""
    return authenticated_layout(
        rx.el.div(
            # Page Header
            rx.el.div(
                rx.el.h1(
                    "My Health Dashboard",
                    class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-2",
                ),
                rx.el.p(
                    rx.el.span("Welcome back, "),
                    rx.el.span(
                        AuthState.user_first_name,
                        class_name="text-teal-400 font-semibold",
                    ),
                    class_name="text-slate-400 text-sm",
                ),
                class_name="mb-6",
            ),
            # Main Layout: Sidebar + Content
            rx.el.div(
                # Tab Navigation (horizontal for now, could be sidebar later)
                patient_portal_tabs(),
                # Tab Content
                rx.match(
                    SettingsState.active_tab,
                    ("overview", overview_tab()),
                    ("food", food_tracker_tab()),
                    ("medications", medications_tab()),
                    ("conditions", conditions_tab()),
                    ("symptoms", symptoms_tab()),
                    overview_tab(),  # Default
                ),
            ),
            # Modals
            checkin_modal(),
            medication_modal(),
            condition_modal(),
            symptom_modal(),
            connect_source_modal(),
            add_food_modal(),
            # on_mount sets initial tab only; data loading is in on_load (longevity_clinic.py)
            on_mount=lambda: SettingsState.set_active_tab(initial_tab),
        )
    )


def patient_portal() -> rx.Component:
    """Patient dashboard page with comprehensive health tracking."""
    return _patient_portal_base("overview")
