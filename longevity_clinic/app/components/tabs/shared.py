"""Shared tab components.

Reusable components used across multiple tabs.
"""

import reflex as rx

from ...styles.constants import GlassStyles


def import_drop_zone() -> rx.Component:
    """Drag and drop zone for file imports."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("cloud-upload", class_name="w-12 h-12 text-slate-400 mb-4"),
                rx.el.h4(
                    "Drop files here to import",
                    class_name="text-lg font-semibold text-white mb-2",
                ),
                rx.el.p(
                    "Supported formats: CSV, JSON, FHIR, HL7",
                    class_name="text-sm text-slate-400 mb-4",
                ),
                rx.el.div(
                    rx.el.span("or", class_name="text-slate-500 text-sm px-3"),
                    class_name="flex items-center mb-4",
                ),
                rx.el.button(
                    rx.icon("folder-open", class_name="w-4 h-4 mr-2"),
                    "Browse Files",
                    class_name=GlassStyles.BUTTON_PRIMARY + " flex items-center",
                ),
                class_name="flex flex-col items-center justify-center py-12",
            ),
            class_name="border-2 border-dashed border-slate-600 hover:border-teal-500/50 rounded-2xl bg-white/2 hover:bg-white/5 transition-all duration-300 cursor-pointer",
        ),
        rx.el.div(
            rx.el.h4(
                "Recent Imports", class_name="text-sm font-semibold text-white mb-3"
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("file-text", class_name="w-4 h-4 text-slate-400 mr-3"),
                    rx.el.div(
                        rx.el.p(
                            "lab_results_nov2024.csv", class_name="text-sm text-white"
                        ),
                        rx.el.p(
                            "Imported 3 days ago", class_name="text-xs text-slate-400"
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.span(
                        "Success",
                        class_name="text-xs text-teal-400 bg-teal-500/10 px-2 py-1 rounded",
                    ),
                    class_name="flex items-center p-3 border-b border-white/5",
                ),
                rx.el.div(
                    rx.icon("file-text", class_name="w-4 h-4 text-slate-400 mr-3"),
                    rx.el.div(
                        rx.el.p(
                            "medication_history.json", class_name="text-sm text-white"
                        ),
                        rx.el.p(
                            "Imported 1 week ago", class_name="text-xs text-slate-400"
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.span(
                        "Success",
                        class_name="text-xs text-teal-400 bg-teal-500/10 px-2 py-1 rounded",
                    ),
                    class_name="flex items-center p-3",
                ),
                class_name=f"{GlassStyles.PANEL}",
            ),
            class_name="mt-6",
        ),
        class_name="space-y-4",
    )
