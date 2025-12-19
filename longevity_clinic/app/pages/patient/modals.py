"""Patient portal modal components."""

import reflex as rx
from ...states import HealthDashboardState, VoiceTranscriptionState, audio_capture
from ...states.shared.checkin import CheckinState
from ...styles.constants import GlassStyles


def _format_duration(seconds: float) -> str:
    """Format seconds to MM:SS display."""
    minutes = int(seconds // 60)
    remaining = int(seconds % 60)
    return f"{minutes}:{remaining:02d}"


def voice_recording_button() -> rx.Component:
    """Voice recording button with animated states using real audio capture."""
    return rx.el.div(
        # Include the audio capture component (invisible)
        audio_capture,
        # Recording button container with pulse animation when recording
        rx.el.div(
            rx.el.button(
                rx.icon(
                    rx.cond(
                        audio_capture.is_recording,
                        "square",  # Stop icon when recording
                        "mic",  # Mic icon when idle
                    ),
                    class_name=rx.cond(
                        audio_capture.is_recording,
                        "w-10 h-10 text-white",
                        "w-12 h-12 text-teal-400",
                    ),
                ),
                on_click=rx.cond(
                    audio_capture.is_recording,
                    VoiceTranscriptionState.stop_recording,
                    VoiceTranscriptionState.start_recording,
                ),
                class_name=rx.cond(
                    audio_capture.is_recording,
                    # Recording state - red pulsing button
                    "w-24 h-24 rounded-full bg-red-500 flex items-center justify-center border-4 border-red-400 shadow-[0_0_30px_rgba(239,68,68,0.5)] animate-pulse cursor-pointer transition-all duration-300 hover:bg-red-600",
                    # Idle state - teal button
                    "w-24 h-24 rounded-full bg-teal-500/10 flex items-center justify-center border border-teal-500/20 cursor-pointer transition-all duration-300 hover:bg-teal-500/20 hover:border-teal-500/40 hover:scale-105",
                ),
            ),
            class_name="mb-4",
        ),
        # Status text and processing indicator
        rx.cond(
            audio_capture.is_recording,
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "● REC",
                        class_name="text-red-400 font-bold text-sm animate-pulse mr-2",
                    ),
                    rx.el.span(
                        "Recording...",
                        class_name="text-white font-mono text-sm",
                    ),
                    class_name="flex items-center justify-center mb-2",
                ),
                rx.el.p("Tap to stop recording", class_name="text-sm text-slate-400"),
            ),
            rx.cond(
                VoiceTranscriptionState.processing,
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "loader-circle",
                            class_name="w-5 h-5 text-teal-400 animate-spin mr-2",
                        ),
                        rx.el.span(
                            "Transcribing...", class_name="text-teal-400 text-sm"
                        ),
                        class_name="flex items-center justify-center mb-2",
                    ),
                ),
                rx.cond(
                    VoiceTranscriptionState.transcript != "",
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "circle-check", class_name="w-5 h-5 text-teal-400 mr-2"
                            ),
                            rx.el.span(
                                "Transcription complete",
                                class_name="text-teal-400 text-sm",
                            ),
                            class_name="flex items-center justify-center mb-2",
                        ),
                    ),
                    rx.el.p(
                        "Tap to start recording", class_name="text-sm text-slate-400"
                    ),
                ),
            ),
        ),
        # Error display
        rx.cond(
            VoiceTranscriptionState.has_error,
            rx.el.div(
                rx.el.p(
                    VoiceTranscriptionState.error_message,
                    class_name="text-red-400 text-xs text-center",
                ),
                class_name="mt-2",
            ),
            rx.fragment(),
        ),
        class_name="flex flex-col items-center py-6",
    )


def transcription_display() -> rx.Component:
    """Display transcribed text from voice recording."""
    return rx.cond(
        VoiceTranscriptionState.transcript != "",
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Transcription",
                    class_name="text-xs text-slate-400 uppercase tracking-wider",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-3 h-3"),
                    on_click=VoiceTranscriptionState.clear_transcript,
                    class_name="p-1 text-slate-400 hover:text-red-400 transition-colors",
                ),
                class_name="flex items-center justify-between mb-2",
            ),
            rx.el.div(
                rx.el.p(
                    VoiceTranscriptionState.transcript,
                    class_name="text-sm text-white leading-relaxed",
                ),
                class_name="bg-white/5 border border-white/10 rounded-xl p-4 max-h-32 overflow-y-auto",
            ),
            class_name="mb-4",
        ),
        rx.fragment(),
    )


def topic_button(topic: str, icon_name: str) -> rx.Component:
    """Topic selection button with toggle state."""
    # Use rx.match to check if topic is in selected_topics list
    is_selected = CheckinState.selected_topics.contains(topic)
    return rx.el.button(
        rx.icon(icon_name, class_name="w-3 h-3 mr-1"),
        topic,
        on_click=lambda: CheckinState.toggle_topic(topic),
        class_name=rx.cond(
            is_selected,
            "px-3 py-1.5 rounded-full text-xs font-medium bg-teal-500/30 text-teal-200 border-2 border-teal-400/50 flex items-center transition-all shadow-[0_0_10px_rgba(20,184,166,0.3)]",
            "px-3 py-1.5 rounded-full text-xs text-slate-400 border border-white/10 hover:bg-white/5 flex items-center transition-all",
        ),
    )


def checkin_modal() -> rx.Component:
    """Check-in modal for voice/text logging."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "New Check-in",
                            class_name="text-xl font-bold text-white",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name="text-slate-400 hover:text-white transition-colors",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-6",
                    ),
                    # Check-in type selector
                    rx.el.div(
                        rx.el.p(
                            "Type",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("mic", class_name="w-5 h-5 mr-2"),
                                "Voice",
                                on_click=lambda: CheckinState.set_checkin_type("voice"),
                                class_name=rx.cond(
                                    CheckinState.checkin_type == "voice",
                                    "flex-1 py-3 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30 flex items-center justify-center transition-all",
                                    "flex-1 py-3 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-white/10 flex items-center justify-center transition-all",
                                ),
                            ),
                            rx.el.button(
                                rx.icon("message-square", class_name="w-5 h-5 mr-2"),
                                "Text",
                                on_click=lambda: CheckinState.set_checkin_type("text"),
                                class_name=rx.cond(
                                    CheckinState.checkin_type == "text",
                                    "flex-1 py-3 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30 flex items-center justify-center transition-all",
                                    "flex-1 py-3 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-white/10 flex items-center justify-center transition-all",
                                ),
                            ),
                            class_name="flex gap-3",
                        ),
                        class_name="mb-6",
                    ),
                    # Content area - Voice or Text
                    rx.cond(
                        CheckinState.checkin_type == "voice",
                        rx.el.div(
                            voice_recording_button(),
                            transcription_display(),
                        ),
                        rx.el.div(
                            rx.el.textarea(
                                placeholder="How are you feeling today? Any symptoms, concerns, or updates...",
                                value=CheckinState.checkin_text,
                                on_change=CheckinState.set_checkin_text,
                                class_name="w-full h-40 bg-white/5 border border-white/10 rounded-xl p-4 text-white placeholder-slate-500 resize-none focus:outline-none focus:border-teal-500/50 transition-all",
                            ),
                        ),
                    ),
                    # Topic tags
                    rx.el.div(
                        rx.el.p(
                            "Topics (optional)",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.div(
                            topic_button("Medication", "pill"),
                            topic_button("Symptoms", "thermometer"),
                            topic_button("Diet", "utensils"),
                            topic_button("Exercise", "dumbbell"),
                            topic_button("Sleep", "moon"),
                            topic_button("Mood", "smile"),
                            class_name="flex flex-wrap gap-2",
                        ),
                        class_name="mt-6 mb-6",
                    ),
                    # Actions
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            ),
                        ),
                        rx.el.button(
                            rx.cond(
                                VoiceTranscriptionState.processing | CheckinState.checkin_saving,
                                rx.fragment(
                                    rx.icon(
                                        "loader-circle",
                                        class_name="w-4 h-4 mr-2 animate-spin",
                                    ),
                                    rx.cond(
                                        CheckinState.checkin_saving,
                                        "Saving...",
                                        "Processing...",
                                    ),
                                ),
                                "Save Check-in",
                            ),
                            on_click=CheckinState.save_checkin_with_voice,
                            disabled=VoiceTranscriptionState.processing | CheckinState.checkin_saving,
                            class_name=GlassStyles.BUTTON_PRIMARY
                            + " disabled:opacity-50 disabled:cursor-not-allowed",
                        ),
                        class_name="flex justify-end gap-3",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-lg {GlassStyles.MODAL} z-50",
            ),
        ),
        open=CheckinState.show_checkin_modal,
        on_open_change=CheckinState.set_show_checkin_modal,
    )


def medication_modal() -> rx.Component:
    """Medication detail modal."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            HealthDashboardState.selected_medication.get(
                                "name", "Medication"
                            ),
                            class_name="text-xl font-bold text-white",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name="text-slate-400 hover:text-white transition-colors",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-6",
                    ),
                    # Medication details
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Dosage",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.p(
                                HealthDashboardState.selected_medication.get(
                                    "dosage", "N/A"
                                ),
                                class_name="text-white font-medium",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Frequency",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.p(
                                HealthDashboardState.selected_medication.get(
                                    "frequency", "N/A"
                                ),
                                class_name="text-white font-medium",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Status",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.span(
                                HealthDashboardState.selected_medication.get(
                                    "status", "active"
                                ),
                                class_name="px-3 py-1 rounded-full text-xs font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20 capitalize",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Adherence Rate",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    f"{HealthDashboardState.selected_medication.get('adherence_rate', 0):.0f}%",
                                    class_name="text-2xl font-bold text-teal-400",
                                ),
                            ),
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 mb-6",
                    ),
                    # Actions
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Close",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            ),
                        ),
                        rx.el.button(
                            "Log Dose",
                            on_click=lambda: HealthDashboardState.log_dose(
                                HealthDashboardState.selected_medication.get("id", "")
                            ),
                            class_name=GlassStyles.BUTTON_PRIMARY,
                        ),
                        class_name="flex justify-end gap-3",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md {GlassStyles.MODAL} z-50",
            ),
        ),
        open=HealthDashboardState.show_medication_modal,
        on_open_change=HealthDashboardState.set_show_medication_modal,
    )


def condition_modal() -> rx.Component:
    """Condition detail modal."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            HealthDashboardState.selected_condition.get(
                                "name", "Condition"
                            ),
                            class_name="text-xl font-bold text-white",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name="text-slate-400 hover:text-white transition-colors",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-6",
                    ),
                    # Condition details
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "ICD-10 Code",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.p(
                                HealthDashboardState.selected_condition.get(
                                    "icd_code", "N/A"
                                ),
                                class_name="text-white font-medium",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Diagnosed",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.p(
                                HealthDashboardState.selected_condition.get(
                                    "diagnosed_date", "N/A"
                                ),
                                class_name="text-white font-medium",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Severity",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.p(
                                HealthDashboardState.selected_condition.get(
                                    "severity", "N/A"
                                ),
                                class_name="text-white font-medium capitalize",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Status",
                                class_name="text-xs text-slate-400 uppercase tracking-wider mb-1",
                            ),
                            rx.el.span(
                                HealthDashboardState.selected_condition.get(
                                    "status", "active"
                                ),
                                class_name="px-3 py-1 rounded-full text-xs font-medium bg-teal-500/10 text-teal-300 border border-teal-500/20 capitalize",
                            ),
                        ),
                        class_name=f"{GlassStyles.PANEL} p-4 mb-6",
                    ),
                    # Related treatments
                    rx.el.div(
                        rx.el.p(
                            "Related Treatments",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.p(
                            HealthDashboardState.selected_condition.get(
                                "treatments", "No treatments linked"
                            ),
                            class_name="text-sm text-slate-300",
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
                        class_name="flex justify-end",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md {GlassStyles.MODAL} z-50",
            ),
        ),
        open=HealthDashboardState.show_condition_modal,
        on_open_change=HealthDashboardState.set_show_condition_modal,
    )


def symptom_modal() -> rx.Component:
    """Symptom logging modal."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            f"Log: {HealthDashboardState.selected_symptom.get('name', 'Symptom')}",
                            class_name="text-xl font-bold text-white",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name="text-slate-400 hover:text-white transition-colors",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-6",
                    ),
                    # Severity slider
                    rx.el.div(
                        rx.el.p(
                            "Severity",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.div(
                            rx.el.span("1", class_name="text-sm text-slate-400"),
                            rx.el.div(
                                class_name="flex-1 h-2 bg-white/10 rounded-full mx-3",
                            ),
                            rx.el.span("10", class_name="text-sm text-slate-400"),
                            class_name="flex items-center",
                        ),
                        class_name="mb-6",
                    ),
                    # Notes
                    rx.el.div(
                        rx.el.p(
                            "Notes",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.textarea(
                            placeholder="Any additional details about this symptom...",
                            class_name="w-full h-24 bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-slate-500 resize-none focus:outline-none focus:border-teal-500/50",
                        ),
                        class_name="mb-6",
                    ),
                    # Actions
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            ),
                        ),
                        rx.el.button(
                            "Save Log",
                            on_click=HealthDashboardState.save_symptom_log,
                            class_name=GlassStyles.BUTTON_PRIMARY,
                        ),
                        class_name="flex justify-end gap-3",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md {GlassStyles.MODAL} z-50",
            ),
        ),
        open=HealthDashboardState.show_symptom_modal,
        on_open_change=HealthDashboardState.set_show_symptom_modal,
    )


def connect_source_modal() -> rx.Component:
    """Connect data source modal."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "Connect Data Source",
                            class_name="text-xl font-bold text-white",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name="text-slate-400 hover:text-white transition-colors",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-6",
                    ),
                    # Available sources
                    rx.el.div(
                        rx.el.p(
                            "Available Connections",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-3",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "watch", class_name="w-6 h-6 text-teal-400 mr-3"
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Apple Watch",
                                        class_name="text-sm font-medium text-white",
                                    ),
                                    rx.el.p(
                                        "Wearable device",
                                        class_name="text-xs text-slate-400",
                                    ),
                                    class_name="flex-1",
                                ),
                                rx.el.button(
                                    "Connect",
                                    class_name="px-3 py-1.5 text-xs font-medium bg-teal-500/20 text-teal-300 rounded-lg border border-teal-500/30 hover:bg-teal-500/30 transition-colors",
                                ),
                                class_name="flex items-center p-4 border-b border-white/5",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "smartphone",
                                    class_name="w-6 h-6 text-purple-400 mr-3",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Oura Ring",
                                        class_name="text-sm font-medium text-white",
                                    ),
                                    rx.el.p(
                                        "Sleep & activity tracker",
                                        class_name="text-xs text-slate-400",
                                    ),
                                    class_name="flex-1",
                                ),
                                rx.el.button(
                                    "Connect",
                                    class_name="px-3 py-1.5 text-xs font-medium bg-teal-500/20 text-teal-300 rounded-lg border border-teal-500/30 hover:bg-teal-500/30 transition-colors",
                                ),
                                class_name="flex items-center p-4 border-b border-white/5",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "stethoscope",
                                    class_name="w-6 h-6 text-blue-400 mr-3",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Epic MyChart",
                                        class_name="text-sm font-medium text-white",
                                    ),
                                    rx.el.p(
                                        "EHR Integration",
                                        class_name="text-xs text-slate-400",
                                    ),
                                    class_name="flex-1",
                                ),
                                rx.el.button(
                                    "Connect",
                                    class_name="px-3 py-1.5 text-xs font-medium bg-teal-500/20 text-teal-300 rounded-lg border border-teal-500/30 hover:bg-teal-500/30 transition-colors",
                                ),
                                class_name="flex items-center p-4",
                            ),
                            class_name=f"{GlassStyles.PANEL}",
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
                        class_name="flex justify-end",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md {GlassStyles.MODAL} z-50",
            ),
        ),
        open=HealthDashboardState.show_connect_modal,
        on_open_change=HealthDashboardState.set_show_connect_modal,
    )


def add_food_modal() -> rx.Component:
    """Add food entry modal."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "Add Food Entry",
                            class_name="text-xl font-bold text-white",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name="text-slate-400 hover:text-white transition-colors",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-6",
                    ),
                    # Food name
                    rx.el.div(
                        rx.el.p(
                            "Food Name",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.input(
                            placeholder="e.g., Grilled Chicken Salad",
                            value=HealthDashboardState.new_food_name,
                            on_change=HealthDashboardState.set_new_food_name,
                            class_name="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 transition-all",
                        ),
                        class_name="mb-4",
                    ),
                    # Meal type
                    rx.el.div(
                        rx.el.p(
                            "Meal Type",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Breakfast",
                                on_click=lambda: HealthDashboardState.set_new_food_meal_type(
                                    "breakfast"
                                ),
                                class_name=rx.cond(
                                    HealthDashboardState.new_food_meal_type
                                    == "breakfast",
                                    "flex-1 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                                    "flex-1 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-white/10",
                                ),
                            ),
                            rx.el.button(
                                "Lunch",
                                on_click=lambda: HealthDashboardState.set_new_food_meal_type(
                                    "lunch"
                                ),
                                class_name=rx.cond(
                                    HealthDashboardState.new_food_meal_type == "lunch",
                                    "flex-1 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                                    "flex-1 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-white/10",
                                ),
                            ),
                            rx.el.button(
                                "Dinner",
                                on_click=lambda: HealthDashboardState.set_new_food_meal_type(
                                    "dinner"
                                ),
                                class_name=rx.cond(
                                    HealthDashboardState.new_food_meal_type == "dinner",
                                    "flex-1 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                                    "flex-1 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-white/10",
                                ),
                            ),
                            rx.el.button(
                                "Snack",
                                on_click=lambda: HealthDashboardState.set_new_food_meal_type(
                                    "snack"
                                ),
                                class_name=rx.cond(
                                    HealthDashboardState.new_food_meal_type == "snack",
                                    "flex-1 py-2 rounded-xl text-sm font-medium bg-teal-500/20 text-teal-300 border border-teal-500/30",
                                    "flex-1 py-2 rounded-xl text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5 border border-white/10",
                                ),
                            ),
                            class_name="flex gap-2",
                        ),
                        class_name="mb-4",
                    ),
                    # Nutrition info grid
                    rx.el.div(
                        rx.el.p(
                            "Nutrition Info",
                            class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "Calories", class_name="text-xs text-slate-400 mb-1"
                                ),
                                rx.el.input(
                                    placeholder="0",
                                    type="number",
                                    value=HealthDashboardState.new_food_calories,
                                    on_change=HealthDashboardState.set_new_food_calories,
                                    class_name="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 transition-all",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Protein (g)",
                                    class_name="text-xs text-slate-400 mb-1",
                                ),
                                rx.el.input(
                                    placeholder="0",
                                    type="number",
                                    value=HealthDashboardState.new_food_protein,
                                    on_change=HealthDashboardState.set_new_food_protein,
                                    class_name="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 transition-all",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Carbs (g)",
                                    class_name="text-xs text-slate-400 mb-1",
                                ),
                                rx.el.input(
                                    placeholder="0",
                                    type="number",
                                    value=HealthDashboardState.new_food_carbs,
                                    on_change=HealthDashboardState.set_new_food_carbs,
                                    class_name="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 transition-all",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Fat (g)", class_name="text-xs text-slate-400 mb-1"
                                ),
                                rx.el.input(
                                    placeholder="0",
                                    type="number",
                                    value=HealthDashboardState.new_food_fat,
                                    on_change=HealthDashboardState.set_new_food_fat,
                                    class_name="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 transition-all",
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-3",
                        ),
                        class_name="mb-6",
                    ),
                    # Actions
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancel",
                                class_name=GlassStyles.BUTTON_SECONDARY,
                            ),
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("plus", class_name="w-4 h-4 mr-2"),
                                "Add Food",
                                on_click=HealthDashboardState.save_food_entry,
                                class_name=GlassStyles.BUTTON_PRIMARY
                                + " flex items-center",
                            ),
                        ),
                        class_name="flex justify-end gap-3",
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md {GlassStyles.MODAL} z-50",
            ),
        ),
        open=HealthDashboardState.show_add_food_modal,
        on_open_change=HealthDashboardState.set_show_add_food_modal,
    )


def suggest_integration_modal() -> rx.Component:
    """Modal for suggesting new integrations."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.fragment()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-50",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "Suggest an Integration",
                            class_name="text-xl font-bold text-white",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="w-5 h-5"),
                                class_name="text-slate-400 hover:text-white transition-colors",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-4",
                    ),
                    rx.el.p(
                        "Don't see your device or service? Let us know what integration you'd like to see.",
                        class_name="text-slate-400 text-sm mb-6",
                    ),
                    rx.cond(
                        HealthDashboardState.integration_suggestion_submitted,
                        # Success state
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "circle-check",
                                    class_name="w-12 h-12 text-teal-400 mb-4",
                                ),
                                rx.el.h3(
                                    "Thank you!",
                                    class_name="text-lg font-semibold text-white mb-2",
                                ),
                                rx.el.p(
                                    "We've received your suggestion and will review it for future updates.",
                                    class_name="text-slate-400 text-sm text-center",
                                ),
                                class_name="flex flex-col items-center py-6",
                            ),
                            rx.el.div(
                                rx.radix.primitives.dialog.close(
                                    rx.el.button(
                                        "Close",
                                        class_name=GlassStyles.BUTTON_PRIMARY,
                                    ),
                                ),
                                class_name="flex justify-center mt-4",
                            ),
                        ),
                        # Form state
                        rx.el.div(
                            # Integration name
                            rx.el.div(
                                rx.el.p(
                                    "Device / Service Name",
                                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                                ),
                                rx.el.input(
                                    placeholder="e.g., Whoop, Levels, Eight Sleep",
                                    value=HealthDashboardState.suggested_integration_name,
                                    on_change=HealthDashboardState.set_suggested_integration_name,
                                    class_name="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 transition-all",
                                ),
                                class_name="mb-4",
                            ),
                            # Description
                            rx.el.div(
                                rx.el.p(
                                    "Why would this be helpful? (optional)",
                                    class_name="text-xs text-slate-400 uppercase tracking-wider mb-2",
                                ),
                                rx.el.textarea(
                                    placeholder="Tell us how this integration would help you track your health...",
                                    value=HealthDashboardState.suggested_integration_description,
                                    on_change=HealthDashboardState.set_suggested_integration_description,
                                    rows=3,
                                    class_name="w-full bg-white/5 border border-white/10 rounded-xl p-3 text-white placeholder-slate-500 focus:outline-none focus:border-teal-500/50 transition-all resize-none",
                                ),
                                class_name="mb-6",
                            ),
                            # Actions
                            rx.el.div(
                                rx.radix.primitives.dialog.close(
                                    rx.el.button(
                                        "Cancel",
                                        class_name=GlassStyles.BUTTON_SECONDARY,
                                    ),
                                ),
                                rx.el.button(
                                    "Submit Suggestion",
                                    on_click=HealthDashboardState.submit_integration_suggestion,
                                    class_name=GlassStyles.BUTTON_PRIMARY,
                                ),
                                class_name="flex justify-end gap-3",
                            ),
                        ),
                    ),
                    class_name="p-6",
                ),
                class_name=f"fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md {GlassStyles.MODAL} z-50",
            ),
        ),
        open=HealthDashboardState.show_suggest_integration_modal,
        on_open_change=HealthDashboardState.set_show_suggest_integration_modal,
    )
