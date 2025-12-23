"""Admin dashboard reusable components.

This module re-exports shared stat card components and provides admin-specific tabs.
"""

import reflex as rx

from ...components.shared import (
    chart_card,
    dashboard_stat_card as stat_card,
    efficiency_stat_card,
)
from .state import AdminDashboardState

# Re-export shared components for backward compatibility
__all__ = ["chart_card", "dashboard_tabs", "efficiency_stat_card", "stat_card"]


def dashboard_tabs() -> rx.Component:
    """Dashboard tab navigation."""
    return rx.el.div(
        rx.el.button(
            rx.icon("layout-dashboard", class_name="w-4 h-4 mr-2"),
            "Overview",
            on_click=lambda: AdminDashboardState.set_tab("overview"),
            class_name=rx.cond(
                AdminDashboardState.active_tab == "overview",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center bg-teal-500/20 text-teal-300 border border-teal-500/30",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center text-slate-400 hover:bg-slate-800/50 hover:text-white border border-transparent",
            ),
        ),
        rx.el.button(
            rx.icon("users", class_name="w-4 h-4 mr-2"),
            "Patients",
            on_click=lambda: AdminDashboardState.set_tab("patients"),
            class_name=rx.cond(
                AdminDashboardState.active_tab == "patients",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center bg-teal-500/20 text-teal-300 border border-teal-500/30",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center text-slate-400 hover:bg-slate-800/50 hover:text-white border border-transparent",
            ),
        ),
        rx.el.button(
            rx.icon("gauge", class_name="w-4 h-4 mr-2"),
            "Clinical Efficiency",
            on_click=lambda: AdminDashboardState.set_tab("efficiency"),
            class_name=rx.cond(
                AdminDashboardState.active_tab == "efficiency",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center bg-teal-500/20 text-teal-300 border border-teal-500/30",
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center text-slate-400 hover:bg-slate-800/50 hover:text-white border border-transparent",
            ),
        ),
        class_name="flex gap-2 p-1.5 bg-slate-800/30 backdrop-blur-sm rounded-2xl border border-slate-700/50 mb-6",
    )
