"""AI Medical Expert chat page for admin portal."""

import reflex as rx

from ...components.layout import authenticated_layout
from ...states import SyntropyChatState
from ..patient.chat.page import ai_chat_page as base_chat_page


def admin_chat_page() -> rx.Component:
    """Admin AI Medical Expert chat page."""
    return authenticated_layout(
        rx.box(
            rx.heading(
                "AI Medical Expert",
                size="6",
                class_name="mb-4 text-slate-800 dark:text-white",
            ),
            rx.text(
                "Get AI-assisted clinical insights and recommendations.",
                class_name="text-slate-500 mb-6",
            ),
            base_chat_page(),
            on_mount=SyntropyChatState.on_load,
            class_name="p-6",
        ),
    )
