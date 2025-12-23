"""Transcript modal component for displaying full check-in transcripts.

DEPRECATED: Use checkin_detail_modal from checkin_detail.py instead.
This module is kept for backward compatibility.
"""

import reflex as rx

from ...styles import GlassStyles


def transcript_modal(
    show_modal: rx.Var[bool],
    transcript_text: rx.Var[str],
    on_close: rx.EventHandler,
    title: str = "Full Transcript",
) -> rx.Component:
    """Reusable transcript modal with click-outside-to-close functionality.

    DEPRECATED: Use checkin_detail_modal instead for a unified modal experience
    that works for both admin and patient views.

    Args:
        show_modal: Boolean var controlling modal visibility
        transcript_text: Text content to display
        on_close: Event handler to close the modal
        title: Modal title (default: "Full Transcript")

    Returns:
        Modal component
    """
    return rx.cond(
        show_modal,
        rx.el.div(
            # Backdrop with click-outside-to-close
            rx.el.div(
                on_click=on_close,
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-40",
            ),
            # Modal content
            rx.el.div(
                rx.el.div(
                    # Header
                    rx.el.div(
                        rx.el.h3(
                            title,
                            class_name="text-lg font-semibold text-white",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="w-5 h-5"),
                            on_click=on_close,
                            class_name="text-slate-400 hover:text-white transition-colors",
                        ),
                        class_name="flex items-center justify-between mb-4",
                    ),
                    # Textarea
                    rx.el.textarea(
                        value=transcript_text,
                        read_only=True,
                        class_name="w-full h-[400px] bg-slate-800/50 border border-slate-700/50 rounded-xl text-white text-sm p-4 resize-none focus:outline-none focus:ring-2 focus:ring-teal-500/50",
                    ),
                    # Footer with close button
                    rx.el.div(
                        rx.el.button(
                            "Close",
                            on_click=on_close,
                            class_name=f"{GlassStyles.BUTTON_SECONDARY} mt-4",
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name=f"{GlassStyles.PANEL} p-6 max-w-3xl w-full",
                ),
                class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
            ),
        ),
        rx.fragment(),
    )


def status_update_modal(
    show_modal: rx.Var[bool],
    selected_status: rx.Var[str],
    on_status_change: rx.EventHandler,
    on_update: rx.EventHandler,
    on_close: rx.EventHandler,
    checkin_summary: rx.Var[str] = "",
) -> rx.Component:
    """Modal for updating check-in status.

    Args:
        show_modal: Boolean var controlling modal visibility
        selected_status: Currently selected status
        on_status_change: Event handler when status selection changes
        on_update: Event handler to confirm status update
        on_close: Event handler to close the modal
        checkin_summary: Optional summary text to display

    Returns:
        Modal component
    """
    return rx.cond(
        show_modal,
        rx.el.div(
            # Backdrop with click-outside-to-close
            rx.el.div(
                on_click=on_close,
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-40",
            ),
            # Modal content
            rx.el.div(
                rx.el.div(
                    # Header
                    rx.el.div(
                        rx.el.h3(
                            "Update Status",
                            class_name="text-lg font-semibold text-white",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="w-5 h-5"),
                            on_click=on_close,
                            class_name="text-slate-400 hover:text-white transition-colors",
                        ),
                        class_name="flex items-center justify-between mb-4",
                    ),
                    # Summary preview (if provided)
                    rx.cond(
                        checkin_summary != "",
                        rx.el.div(
                            rx.el.p(
                                "Check-in Summary",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                            ),
                            rx.el.p(
                                checkin_summary,
                                class_name="text-sm text-slate-300 line-clamp-3",
                            ),
                            class_name="mb-4 p-3 bg-slate-800/50 rounded-lg",
                        ),
                        rx.fragment(),
                    ),
                    # Status selection
                    rx.el.div(
                        rx.el.p(
                            "Select Status",
                            class_name="text-sm text-slate-400 mb-3",
                        ),
                        rx.el.div(
                            # Pending button
                            rx.el.button(
                                rx.icon("clock", class_name="w-4 h-4 mr-2"),
                                "Pending",
                                on_click=lambda: on_status_change("pending"),
                                class_name=rx.cond(
                                    selected_status == "pending",
                                    "flex items-center px-4 py-2 rounded-lg text-sm font-medium bg-amber-500/20 text-amber-400 border border-amber-500/30",
                                    "flex items-center px-4 py-2 rounded-lg text-sm font-medium text-slate-400 hover:bg-white/5 border border-transparent",
                                ),
                            ),
                            # Reviewed button
                            rx.el.button(
                                rx.icon("circle-check", class_name="w-4 h-4 mr-2"),
                                "Reviewed",
                                on_click=lambda: on_status_change("reviewed"),
                                class_name=rx.cond(
                                    selected_status == "reviewed",
                                    "flex items-center px-4 py-2 rounded-lg text-sm font-medium bg-teal-500/20 text-teal-400 border border-teal-500/30",
                                    "flex items-center px-4 py-2 rounded-lg text-sm font-medium text-slate-400 hover:bg-white/5 border border-transparent",
                                ),
                            ),
                            # Flagged button
                            rx.el.button(
                                rx.icon("flag", class_name="w-4 h-4 mr-2"),
                                "Flagged",
                                on_click=lambda: on_status_change("flagged"),
                                class_name=rx.cond(
                                    selected_status == "flagged",
                                    "flex items-center px-4 py-2 rounded-lg text-sm font-medium bg-red-500/20 text-red-400 border border-red-500/30",
                                    "flex items-center px-4 py-2 rounded-lg text-sm font-medium text-slate-400 hover:bg-white/5 border border-transparent",
                                ),
                            ),
                            class_name="flex gap-2 flex-wrap",
                        ),
                        class_name="mb-6",
                    ),
                    # Footer with action buttons
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=on_close,
                            class_name=GlassStyles.BUTTON_SECONDARY,
                        ),
                        rx.el.button(
                            "Update Status",
                            on_click=on_update,
                            class_name=GlassStyles.BUTTON_PRIMARY,
                        ),
                        class_name="flex justify-end gap-3",
                    ),
                    class_name=f"{GlassStyles.PANEL} p-6 max-w-md w-full",
                ),
                class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
            ),
        ),
        rx.fragment(),
    )
