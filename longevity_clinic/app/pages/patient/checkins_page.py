"""Standalone Check-ins page for patient portal and admin view."""

import reflex as rx
from ...components.layout import authenticated_layout
from ...states.auth_state import AuthState
from ...states.patient_biomarker_state import PatientBiomarkerState
from ...states.patient_dashboard_state import PatientDashboardState
from ...states.patient_state import PatientState
from ...states.voice_transcription_state import VoiceTranscriptionState
from ...states.admin_checkins_state import AdminCheckinsState
from ...styles.constants import GlassStyles
from .tabs import checkins_tab, checkin_card
from .modals import checkin_modal


def call_log_card(call_summary: dict) -> rx.Component:
    """Card component for displaying a call log entry."""
    return rx.el.div(
        rx.el.div(
            # Header with type icon and timestamp
            rx.el.div(
                rx.el.div(
                    rx.icon("phone", class_name="w-4 h-4 text-purple-400 mr-2"),
                    rx.el.span("Voice Call", class_name="text-sm font-medium text-white"),
                    class_name="flex items-center",
                ),
                rx.el.span(
                    call_summary["timestamp"],
                    class_name="text-xs text-slate-500",
                ),
                class_name="flex items-center justify-between mb-2",
            ),
            # AI Summary
            rx.el.p(
                call_summary["ai_summary"],
                class_name="text-sm text-slate-300 line-clamp-3 mb-2",
            ),
            # Original summary (if different)
            rx.cond(
                call_summary["summary"] != "",
                rx.el.div(
                    rx.el.p("Original Summary", class_name="text-xs text-slate-500 uppercase tracking-wider mb-1"),
                    rx.el.p(
                        call_summary["summary"],
                        class_name="text-xs text-slate-400 line-clamp-2",
                    ),
                    class_name="mt-2 pt-2 border-t border-white/5",
                ),
                rx.fragment(),
            ),
            class_name=f"{GlassStyles.PANEL} p-4 border-l-2 border-purple-500/50",
        ),
    )


def admin_checkin_card(checkin: dict) -> rx.Component:
    """Card component for admin check-in view."""
    return rx.el.div(
        rx.el.div(
            # Header with patient name and timestamp
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        checkin["patient_name"],
                        class_name="font-semibold text-white",
                    ),
                    rx.el.span(
                        rx.match(
                            checkin["type"],
                            ("voice", rx.icon("mic", class_name="w-3 h-3 ml-2 inline text-teal-400")),
                            ("call", rx.icon("phone", class_name="w-3 h-3 ml-2 inline text-purple-400")),
                            rx.icon("message-square", class_name="w-3 h-3 ml-2 inline text-blue-400"),
                        ),
                    ),
                    class_name="flex items-center",
                ),
                rx.el.span(
                    checkin["timestamp"],
                    class_name="text-xs text-slate-500",
                ),
                class_name="flex items-center justify-between mb-2",
            ),
            # Summary
            rx.el.p(
                checkin["summary"],
                class_name="text-sm text-slate-300 line-clamp-2 mb-3",
            ),
            # Topics and status
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        checkin["key_topics"],
                        lambda topic: rx.el.span(
                            topic,
                            class_name="px-2 py-0.5 rounded-full text-xs bg-white/5 text-slate-400 border border-white/10",
                        ),
                    ),
                    class_name="flex flex-wrap gap-1.5",
                ),
                rx.el.span(
                    checkin["status"],
                    class_name=rx.cond(
                        checkin["status"] == "pending",
                        "px-2 py-0.5 rounded-full text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 capitalize",
                        rx.cond(
                            checkin["status"] == "flagged",
                            "px-2 py-0.5 rounded-full text-xs bg-red-500/10 text-red-400 border border-red-500/20 capitalize",
                            "px-2 py-0.5 rounded-full text-xs bg-teal-500/10 text-teal-400 border border-teal-500/20 capitalize",
                        ),
                    ),
                ),
                class_name="flex items-center justify-between mt-2",
            ),
            class_name=rx.cond(
                checkin["type"] == "call",
                f"{GlassStyles.PANEL} p-4 hover:bg-white/10 transition-all cursor-pointer border-l-2 border-purple-500/50",
                f"{GlassStyles.PANEL} p-4 hover:bg-white/10 transition-all cursor-pointer",
            ),
        ),
        on_click=lambda: AdminCheckinsState.open_checkin_detail(checkin),
    )


def admin_checkin_detail_modal() -> rx.Component:
    """Modal for viewing check-in details in admin view."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
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
                            rx.el.span(
                                AdminCheckinsState.selected_checkin.get("status", ""),
                                class_name=rx.cond(
                                    AdminCheckinsState.selected_checkin.get("status", "") == "pending",
                                    "ml-3 px-2 py-0.5 rounded-full text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 capitalize",
                                    rx.cond(
                                        AdminCheckinsState.selected_checkin.get("status", "") == "flagged",
                                        "ml-3 px-2 py-0.5 rounded-full text-xs bg-red-500/10 text-red-400 border border-red-500/20 capitalize",
                                        "ml-3 px-2 py-0.5 rounded-full text-xs bg-teal-500/10 text-teal-400 border border-teal-500/20 capitalize",
                                    ),
                                ),
                            ),
                            class_name="flex items-center",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name="text-slate-400 hover:text-white transition-colors",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-6",
                    ),
                    # Patient info
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("Patient", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                            rx.el.p(
                                AdminCheckinsState.selected_checkin.get("patient_name", ""),
                                class_name="text-white font-medium",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Submitted", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                            rx.el.p(
                                AdminCheckinsState.selected_checkin.get("timestamp", ""),
                                class_name="text-white",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Type", class_name="text-xs text-slate-400 uppercase tracking-wider mb-1"),
                            rx.el.div(
                                rx.cond(
                                    AdminCheckinsState.selected_checkin.get("type", "") == "voice",
                                    rx.el.div(
                                        rx.icon("mic", class_name="w-4 h-4 text-teal-400 mr-1"),
                                        "Voice",
                                        class_name="flex items-center text-white",
                                    ),
                                    rx.el.div(
                                        rx.icon("message-square", class_name="w-4 h-4 text-blue-400 mr-1"),
                                        "Text",
                                        class_name="flex items-center text-white",
                                    ),
                                ),
                            ),
                        ),
                        class_name=f"grid grid-cols-3 gap-4 {GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Content
                    rx.el.div(
                        rx.el.p("Check-in Content", class_name="text-xs text-slate-400 uppercase tracking-wider mb-2"),
                        rx.el.p(
                            AdminCheckinsState.selected_checkin.get("summary", ""),
                            class_name="text-sm text-white leading-relaxed",
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 mb-4",
                    ),
                    # Topics
                    rx.el.div(
                        rx.el.p("Topics", class_name="text-xs text-slate-400 uppercase tracking-wider mb-2"),
                        rx.el.div(
                            rx.foreach(
                                AdminCheckinsState.selected_checkin.get("key_topics", []),
                                lambda topic: rx.el.span(
                                    topic,
                                    class_name="px-3 py-1 rounded-full text-xs bg-teal-500/10 text-teal-300 border border-teal-500/20",
                                ),
                            ),
                            class_name="flex flex-wrap gap-2",
                        ),
                        class_name="mb-6",
                    ),
                    # Actions
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Close",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            ),
                        ),
                        rx.cond(
                            AdminCheckinsState.selected_checkin.get("status", "") == "pending",
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("flag", class_name="w-4 h-4 mr-2"),
                                    "Flag for Follow-up",
                                    on_click=lambda: AdminCheckinsState.flag_checkin(
                                        AdminCheckinsState.selected_checkin.get("id", "")
                                    ),
                                    class_name="px-4 py-2 rounded-xl text-sm font-medium bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 transition-all flex items-center",
                                ),
                                rx.el.button(
                                    rx.icon("check", class_name="w-4 h-4 mr-2"),
                                    "Mark as Reviewed",
                                    on_click=lambda: AdminCheckinsState.mark_as_reviewed(
                                        AdminCheckinsState.selected_checkin.get("id", "")
                                    ),
                                    class_name=GlassStyles.BUTTON_PRIMARY + " flex items-center",
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
            ),
        ),
        open=AdminCheckinsState.show_checkin_detail_modal,
        on_open_change=AdminCheckinsState.set_show_checkin_detail_modal,
    )


def admin_checkins_view() -> rx.Component:
    """Admin view for managing all patient check-ins."""
    return rx.el.div(
        # Page Header
        rx.el.div(
            rx.el.h1(
                "Patient Check-ins",
                class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-2",
            ),
            rx.el.p(
                rx.el.span("Review and manage patient voice and text logs"),
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        
        # Search Bar
        rx.el.div(
            rx.el.div(
                rx.icon("search", class_name="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2"),
                rx.el.input(
                    placeholder="Search by patient name, topic, or content...",
                    value=AdminCheckinsState.search_query,
                    on_change=AdminCheckinsState.set_search_query,
                    class_name="w-full bg-white/5 border border-white/10 rounded-xl pl-10 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 transition-all",
                ),
                class_name="relative",
            ),
            class_name="mb-6",
        ),
        
        # Status Tabs
        rx.el.div(
            rx.el.button(
                rx.el.span("Pending", class_name="mr-2"),
                rx.el.span(
                    AdminCheckinsState.pending_count,
                    class_name="px-2 py-0.5 rounded-full text-xs bg-amber-500/20 text-amber-400",
                ),
                on_click=lambda: AdminCheckinsState.set_active_status_tab("pending"),
                class_name=rx.cond(
                    AdminCheckinsState.active_status_tab == "pending",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-white/10 text-white border border-white/20 flex items-center",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent flex items-center",
                ),
            ),
            rx.el.button(
                rx.el.span("Reviewed", class_name="mr-2"),
                rx.el.span(
                    AdminCheckinsState.reviewed_count,
                    class_name="px-2 py-0.5 rounded-full text-xs bg-teal-500/20 text-teal-400",
                ),
                on_click=lambda: AdminCheckinsState.set_active_status_tab("reviewed"),
                class_name=rx.cond(
                    AdminCheckinsState.active_status_tab == "reviewed",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-white/10 text-white border border-white/20 flex items-center",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent flex items-center",
                ),
            ),
            rx.el.button(
                rx.el.span("Flagged", class_name="mr-2"),
                rx.el.span(
                    AdminCheckinsState.flagged_count,
                    class_name="px-2 py-0.5 rounded-full text-xs bg-red-500/20 text-red-400",
                ),
                on_click=lambda: AdminCheckinsState.set_active_status_tab("flagged"),
                class_name=rx.cond(
                    AdminCheckinsState.active_status_tab == "flagged",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-white/10 text-white border border-white/20 flex items-center",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent flex items-center",
                ),
            ),
            rx.el.button(
                rx.el.span("All", class_name="mr-2"),
                rx.el.span(
                    AdminCheckinsState.total_count,
                    class_name="px-2 py-0.5 rounded-full text-xs bg-white/10 text-slate-400",
                ),
                on_click=lambda: AdminCheckinsState.set_active_status_tab("all"),
                class_name=rx.cond(
                    AdminCheckinsState.active_status_tab == "all",
                    "px-4 py-2 rounded-xl text-sm font-medium bg-white/10 text-white border border-white/20 flex items-center",
                    "px-4 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-transparent flex items-center",
                ),
            ),
            class_name="flex gap-2 mb-6",
        ),
        
        # Check-ins List
        rx.el.div(
            rx.cond(
                AdminCheckinsState.filtered_checkins.length() > 0,
                rx.el.div(
                    rx.foreach(AdminCheckinsState.filtered_checkins, admin_checkin_card),
                    class_name="space-y-4",
                ),
                rx.el.div(
                    rx.icon("inbox", class_name="w-12 h-12 text-slate-600 mb-4"),
                    rx.el.p("No check-ins found", class_name="text-slate-400"),
                    class_name="flex flex-col items-center justify-center py-12",
                ),
            ),
        ),
        
        # Detail Modal
        admin_checkin_detail_modal(),
    )


def patient_checkins_view() -> rx.Component:
    """Patient view for their own check-ins."""
    return rx.el.div(
        # Page Header
        rx.el.div(
            rx.el.h1(
                "Self Check-ins",
                class_name=f"text-2xl {GlassStyles.HEADING_LIGHT} mb-2",
            ),
            rx.el.p(
                rx.el.span("Voice and text logs between visits"),
                class_name="text-slate-400 text-sm",
            ),
            class_name="mb-6",
        ),
        
        # Check-ins Content
        rx.el.div(
            # Single Check-in Now button
            rx.el.div(
                rx.el.button(
                    rx.icon("circle-plus", class_name="w-5 h-5 mr-2"),
                    "Check-in Now",
                    on_click=PatientDashboardState.open_checkin_modal,
                    class_name=GlassStyles.BUTTON_PRIMARY + " flex items-center",
                ),
                class_name="flex gap-3 mb-6",
            ),
            # Summary Cards
            rx.el.div(
                rx.el.div(
                    rx.icon("mic", class_name="w-6 h-6 text-teal-400 mb-2"),
                    rx.el.p("This Week", class_name="text-xs text-slate-400 uppercase tracking-wider"),
                    rx.el.span(PatientDashboardState.checkins.length(), class_name="text-2xl font-bold text-white"),
                    rx.el.span(" check-ins", class_name="text-sm text-slate-400 ml-1"),
                    class_name=f"{GlassStyles.PANEL} p-4",
                ),
                rx.el.div(
                    rx.icon("phone", class_name="w-6 h-6 text-purple-400 mb-2"),
                    rx.el.p("Voice Calls", class_name="text-xs text-slate-400 uppercase tracking-wider"),
                    rx.el.span(PatientState.transcript_summaries_list.length(), class_name="text-2xl font-bold text-white"),
                    rx.el.span(" logged", class_name="text-sm text-slate-400 ml-1"),
                    class_name=f"{GlassStyles.PANEL} p-4",
                ),
                rx.el.div(
                    rx.icon("clock", class_name="w-6 h-6 text-amber-400 mb-2"),
                    rx.el.p("Pending Review", class_name="text-xs text-slate-400 uppercase tracking-wider"),
                    rx.el.span(PatientDashboardState.unreviewed_checkins_count, class_name="text-2xl font-bold text-white"),
                    class_name=f"{GlassStyles.PANEL} p-4",
                ),
                class_name="grid grid-cols-3 gap-4 mb-6",
            ),
            
            # Loading indicator for call logs
            rx.cond(
                PatientState.call_logs_loading,
                rx.el.div(
                    rx.icon("loader-circle", class_name="w-5 h-5 text-teal-400 animate-spin mr-2"),
                    rx.el.span("Fetching call logs...", class_name="text-sm text-slate-400"),
                    class_name="flex items-center mb-4",
                ),
                rx.fragment(),
            ),
            
            # Last fetch time
            rx.cond(
                PatientState.last_fetch_time != "",
                rx.el.p(
                    rx.el.span("Last updated: ", class_name="text-slate-500"),
                    rx.el.span(PatientState.last_fetch_time, class_name="text-slate-400"),
                    class_name="text-xs mb-4",
                ),
                rx.fragment(),
            ),
            
            # Voice Calls Section
            rx.cond(
                PatientState.transcript_summaries_list.length() > 0,
                rx.el.div(
                    rx.el.h3(
                        rx.icon("phone", class_name="w-5 h-5 text-purple-400 mr-2 inline"),
                        "Voice Calls",
                        class_name="text-lg font-semibold text-white mb-4 flex items-center",
                    ),
                    rx.el.div(
                        rx.foreach(PatientState.transcript_summaries_list, call_log_card),
                        class_name="space-y-4",
                    ),
                    class_name="mb-8",
                ),
                rx.fragment(),
            ),
            
            # Check-ins List
            rx.el.div(
                rx.el.h3(
                    rx.icon("message-square", class_name="w-5 h-5 text-teal-400 mr-2 inline"),
                    "Recent Check-ins",
                    class_name="text-lg font-semibold text-white mb-4 flex items-center",
                ),
                rx.el.div(
                    rx.foreach(PatientDashboardState.checkins, checkin_card),
                    class_name="space-y-4",
                ),
            ),
        ),
        
        # Modal
        checkin_modal(),
    )


def checkins_page() -> rx.Component:
    """Standalone Check-ins page - shows admin or patient view based on role."""
    return authenticated_layout(
        rx.el.div(
            rx.cond(
                AuthState.is_admin,
                admin_checkins_view(),
                patient_checkins_view(),
            ),
            on_mount=[
                PatientBiomarkerState.load_biomarkers,
                PatientDashboardState.load_dashboard_data,
                PatientState.fetch_call_logs_once,
                PatientState.start_call_logs_fetching,
            ],
        )
    )
