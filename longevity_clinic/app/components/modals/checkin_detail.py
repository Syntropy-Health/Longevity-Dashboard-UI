"""Check-in detail modal component for viewing full check-in details.

This module provides the unified detail modal used by both admin and patient views
for displaying complete check-in information including:
- Patient info (admin only)
- Timestamp and type
- Full content/summary
- Topics/keywords
- Action buttons (admin only)
"""

import reflex as rx
from ..shared.checkin_components import status_badge, type_icon
from ...styles.constants import GlassStyles


def checkin_detail_modal(
    show_modal: rx.Var[bool],
    checkin_status: rx.Var[str],
    checkin_patient_name: rx.Var[str],
    checkin_timestamp: rx.Var[str],
    checkin_type: rx.Var[str],
    checkin_summary: rx.Var[str],
    checkin_topics: rx.Var[list],
    checkin_id: rx.Var[str],
    on_close: rx.EventHandler,
    on_flag: rx.EventHandler | None = None,
    on_mark_reviewed: rx.EventHandler | None = None,
    show_patient_name: bool = True,
    show_actions: bool = True,
    checkin_raw_transcript: rx.Var[str] | None = None,
) -> rx.Component:
    """Unified check-in detail modal for admin and patient views.

    Args:
        show_modal: Boolean var controlling modal visibility
        checkin_status: Status of the check-in (pending/reviewed/flagged)
        checkin_patient_name: Patient name
        checkin_timestamp: Timestamp string
        checkin_type: Type (voice/call/text)
        checkin_summary: Content/summary text
        checkin_topics: List of topics/keywords
        checkin_id: Check-in ID for action handlers
        on_close: Event handler to close modal
        on_flag: Optional event handler for flagging (admin only)
        on_mark_reviewed: Optional event handler for marking reviewed (admin only)
        show_patient_name: Whether to display patient name (True for admin)
        show_actions: Whether to show action buttons (True for admin)
        checkin_raw_transcript: Optional raw transcript text for admin view

    Returns:
        Modal component
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
                on_click=on_close,  # Click overlay to close
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    # Header
                    rx.el.div(
                        rx.el.div(
                            rx.radix.primitives.dialog.title(
                                "Check-in Details",
                                class_name="text-xl font-bold text-white",
                            ),
                            status_badge(checkin_status),
                            class_name="flex items-center gap-3",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name="text-slate-400 hover:text-white transition-colors",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-6",
                    ),
                    # Info grid - conditionally show patient name
                    rx.cond(
                        show_patient_name,
                        # Admin: 3-column grid with patient name
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Patient",
                                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                                ),
                                rx.el.p(
                                    checkin_patient_name,
                                    class_name="text-white font-medium",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Submitted",
                                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                                ),
                                rx.el.p(
                                    checkin_timestamp,
                                    class_name="text-white",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Type",
                                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                                ),
                                rx.el.div(
                                    type_icon(checkin_type),
                                    rx.el.span(
                                        checkin_type.to(str).capitalize(),
                                        class_name="ml-2",
                                    ),
                                    class_name="flex items-center text-white",
                                ),
                            ),
                            class_name=f"grid grid-cols-3 gap-4 {GlassStyles.PANEL} p-4 mb-4",
                        ),
                        # Patient: 2-column grid without patient name
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Submitted",
                                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                                ),
                                rx.el.p(
                                    checkin_timestamp,
                                    class_name="text-white",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Type",
                                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                                ),
                                rx.el.div(
                                    type_icon(checkin_type),
                                    rx.el.span(
                                        checkin_type.to(str).capitalize(),
                                        class_name="ml-2",
                                    ),
                                    class_name="flex items-center text-white",
                                ),
                            ),
                            class_name=f"grid grid-cols-2 gap-4 {GlassStyles.PANEL} p-4 mb-4",
                        ),
                    ),
                    # Content section
                    rx.el.div(
                        rx.el.p(
                            "Check-in Content",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.p(
                            checkin_summary,
                            class_name="text-sm text-white leading-relaxed",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Topics section
                    rx.el.div(
                        rx.el.p(
                            "Topics",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.div(
                            rx.foreach(
                                checkin_topics,
                                lambda t: rx.el.span(
                                    t,
                                    class_name="px-3 py-1 rounded-full text-xs bg-teal-500/10 text-teal-300 border border-teal-500/20",
                                ),
                            ),
                            class_name="flex flex-wrap gap-2",
                        ),
                        class_name="mb-4",
                    ),
                    # Raw transcript section (optional, for admin view)
                    rx.cond(
                        checkin_raw_transcript is not None and checkin_raw_transcript != "",
                        rx.el.div(
                            rx.el.p(
                                "Full Transcript",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    checkin_raw_transcript,
                                    class_name="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap",
                                ),
                                class_name="max-h-48 overflow-y-auto",
                            ),
                            class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                        ),
                        rx.fragment(),
                    ) if checkin_raw_transcript is not None else rx.fragment(),
                    # Actions
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Close", class_name=GlassStyles.BUTTON_SECONDARY
                            ),
                        ),
                        rx.cond(
                            show_actions & (checkin_status == "pending"),
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("flag", class_name="w-4 h-4 mr-2"),
                                    "Flag",
                                    on_click=lambda: on_flag(checkin_id) if on_flag else None,  # type: ignore[arg-type]
                                    class_name="px-4 py-2 rounded-xl text-sm font-medium bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 transition-all flex items-center",
                                ),
                                rx.el.button(
                                    rx.icon("check", class_name="w-4 h-4 mr-2"),
                                    "Mark Reviewed",
                                    on_click=lambda: on_mark_reviewed(checkin_id) if on_mark_reviewed else None,  # type: ignore[arg-type]
                                    class_name=f"{GlassStyles.BUTTON_PRIMARY} flex items-center",
                                ),
                                class_name="flex gap-3",
                            ),
                            rx.fragment(),
                        ),
                        class_name="flex justify-between",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-lg {GlassStyles.MODAL} z-50",
                on_escape_key_down=on_close,
                on_pointer_down_outside=on_close,
            ),
        ),
        open=show_modal,
        on_open_change=on_close,
        modal=False,  # Prevent scroll lock/restore behavior
    )
