"""AI Chat page for DietonAI health assistant."""

import reflex as rx

from ....states import SyntropyChatState


def _typing_indicator() -> rx.Component:
    """Animated typing indicator."""
    return rx.hstack(
        rx.box(class_name="w-2 h-2 bg-slate-400 rounded-full animate-bounce"),
        rx.box(
            class_name="w-2 h-2 bg-slate-400 rounded-full animate-bounce",
            style={"animation-delay": "0.1s"},
        ),
        rx.box(
            class_name="w-2 h-2 bg-slate-400 rounded-full animate-bounce",
            style={"animation-delay": "0.2s"},
        ),
        spacing="1",
    )


def _message_bubble(msg: dict) -> rx.Component:
    """Render a single chat message bubble."""
    is_ai = msg["is_ai"]
    content = msg["content"]

    return rx.box(
        rx.hstack(
            rx.cond(
                is_ai,
                rx.icon("bot", class_name="h-8 w-8 text-blue-500"),
                rx.icon("user", class_name="h-8 w-8 text-slate-500"),
            ),
            rx.box(
                rx.text(
                    rx.cond(is_ai, "DietonAI", "You"),
                    class_name="font-semibold text-xs text-slate-500 mb-1",
                ),
                rx.text(
                    content,
                    class_name=rx.cond(
                        is_ai,
                        "px-4 py-2 rounded-lg bg-blue-100 dark:bg-blue-900/30 text-slate-800 dark:text-slate-200",
                        "px-4 py-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200",
                    ),
                ),
                class_name="max-w-md",
            ),
            spacing="3",
            align="start",
            direction=rx.cond(is_ai, "row", "row-reverse"),
        ),
        class_name=rx.cond(
            is_ai,
            "w-full flex justify-start",
            "w-full flex justify-end",
        ),
    )


def _welcome_placeholder() -> rx.Component:
    """Welcome screen when no messages."""
    return rx.center(
        rx.vstack(
            rx.icon("bot", class_name="w-16 h-16 text-slate-300 dark:text-slate-600"),
            rx.heading("DietonAI", size="6", class_name="text-blue-600 dark:text-blue-400"),
            rx.text(
                "Your AI health assistant. Ask me anything about nutrition, wellness, and healthy living.",
                class_name="text-slate-500 text-center max-w-sm",
            ),
            spacing="4",
            align="center",
        ),
        class_name="flex-1 h-full",
    )


def _chat_messages() -> rx.Component:
    """Chat messages area."""
    return rx.cond(
        SyntropyChatState.has_messages,
        rx.box(
            rx.foreach(
                SyntropyChatState.active_session_messages,
                _message_bubble,
            ),
            rx.cond(
                SyntropyChatState.is_streaming,
                rx.box(
                    rx.hstack(
                        rx.icon("bot", class_name="h-8 w-8 text-blue-500"),
                        rx.box(
                            rx.text(
                                "DietonAI",
                                class_name="font-semibold text-xs text-slate-500 mb-1",
                            ),
                            rx.box(
                                _typing_indicator(),
                                class_name="px-4 py-3 rounded-lg bg-blue-100 dark:bg-blue-900/30",
                            ),
                            class_name="max-w-md",
                        ),
                        spacing="3",
                        align="start",
                    ),
                    class_name="w-full",
                ),
                rx.fragment(),
            ),
            class_name="space-y-4 p-4",
        ),
        _welcome_placeholder(),
    )


def _session_item(session: dict) -> rx.Component:
    """Single session item in sidebar."""
    is_active = SyntropyChatState.active_session_id == session["id"]
    return rx.box(
        rx.hstack(
            rx.icon("message-square", class_name="h-4 w-4"),
            rx.text(session["title"], class_name="truncate text-sm"),
            spacing="2",
            class_name="flex-1",
        ),
        on_click=lambda: SyntropyChatState.select_session(session["id"]),
        class_name=rx.cond(
            is_active,
            "p-3 rounded-lg cursor-pointer bg-blue-100 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800",
            "p-3 rounded-lg cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-800",
        ),
    )


def _chat_sidebar() -> rx.Component:
    """Chat history sidebar."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Chats", size="4"),
                rx.button(
                    rx.icon("plus", class_name="h-4 w-4"),
                    on_click=SyntropyChatState.create_new_session,
                    variant="ghost",
                    size="1",
                ),
                justify="between",
                align="center",
                class_name="w-full p-4 border-b border-slate-200 dark:border-slate-700",
            ),
            rx.box(
                rx.cond(
                    SyntropyChatState.is_loading_sessions,
                    rx.center(rx.spinner(), class_name="p-4"),
                    rx.vstack(
                        rx.foreach(SyntropyChatState.sessions, _session_item),
                        spacing="2",
                        class_name="w-full",
                    ),
                ),
                class_name="p-2 overflow-y-auto flex-1",
            ),
            spacing="0",
            class_name="h-full",
        ),
        class_name=rx.cond(
            SyntropyChatState.sidebar_collapsed,
            "hidden md:block w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-700",
            "w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-700",
        ),
    )


def _chat_input() -> rx.Component:
    """Chat input area."""
    return rx.box(
        rx.hstack(
            rx.input(
                placeholder="Ask DietonAI...",
                value=SyntropyChatState.user_input_text,
                on_change=SyntropyChatState.set_user_input,
                disabled=SyntropyChatState.is_streaming,
                class_name="flex-1",
                size="3",
            ),
            rx.button(
                rx.icon("send", class_name="h-4 w-4"),
                on_click=SyntropyChatState.send_message,
                disabled=SyntropyChatState.is_streaming,
                class_name="bg-blue-600 hover:bg-blue-700 text-white",
            ),
            spacing="2",
            class_name="w-full",
        ),
        class_name="p-4 border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900",
    )


def ai_chat_page() -> rx.Component:
    """Main AI chat page component."""
    return rx.box(
        rx.hstack(
            _chat_sidebar(),
            rx.vstack(
                rx.hstack(
                    rx.button(
                        rx.icon(
                            tag=rx.cond(
                                SyntropyChatState.sidebar_collapsed,
                                "panel-left-open",
                                "panel-left-close",
                            ),
                            class_name="h-5 w-5",
                        ),
                        on_click=SyntropyChatState.toggle_sidebar,
                        variant="ghost",
                        class_name="md:hidden",
                    ),
                    rx.heading("DietonAI Chat", size="5"),
                    spacing="2",
                    align="center",
                    class_name="p-4 border-b border-slate-200 dark:border-slate-700 w-full",
                ),
                rx.box(
                    _chat_messages(),
                    class_name="flex-1 overflow-y-auto",
                ),
                _chat_input(),
                spacing="0",
                class_name="flex-1 h-full",
            ),
            spacing="0",
            class_name="h-full w-full",
        ),
        on_mount=SyntropyChatState.on_load,
        class_name="h-[calc(100vh-8rem)] bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden",
    )
