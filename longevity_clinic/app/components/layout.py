import reflex as rx
from .sidebar import sidebar, mobile_menu
from .header import header
from ..config import current_config


def authenticated_layout(content: rx.Component) -> rx.Component:
    """
    Wrapper for authenticated pages.
    Includes the Sidebar, Header, and Mobile Menu.
    Uses a glassmorphism design system with a gradient background.
    """
    return rx.el.div(
        mobile_menu(),
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                content,
                class_name="flex-1 overflow-y-auto p-4 sm:p-6 md:p-8 scroll-smooth scrollbar-thin scrollbar-track-transparent scrollbar-thumb-gray-200/30",
            ),
            class_name="flex-1 flex flex-col min-w-0 h-screen overflow-hidden relative",
        ),
        class_name=f"flex h-screen w-full font-['Open_Sans'] {current_config.glass_bg_gradient} text-gray-800 antialiased selection:bg-emerald-100/50 selection:text-emerald-900 bg-fixed",
    )