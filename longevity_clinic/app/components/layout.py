import reflex as rx
from .sidebar import sidebar, mobile_menu
from .header import header
from ..styles.constants import GlassStyles


def authenticated_layout(content: rx.Component) -> rx.Component:
    """
    Wrapper for authenticated pages.
    Includes the Sidebar, Header, and Mobile Menu.
    Uses a glassmorphism design system with a gradient background.
    """
    return rx.el.div(
        # Ambient glow effects for depth
        rx.el.div(
            class_name="fixed top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top_left,_var(--tw-gradient-stops))] from-teal-900/20 via-slate-900/0 to-slate-900/0 pointer-events-none"
        ),
        rx.el.div(
            class_name="fixed bottom-0 right-0 w-[500px] h-[500px] bg-teal-500/10 rounded-full blur-[100px] pointer-events-none"
        ),
        mobile_menu(),
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                content,
                class_name="flex-1 overflow-y-auto p-4 sm:p-6 md:p-8 scroll-smooth scrollbar-thin scrollbar-track-transparent scrollbar-thumb-slate-600/30",
            ),
            class_name="flex-1 flex flex-col min-w-0 h-screen overflow-hidden relative md:ml-64",
        ),
        class_name=f"flex h-screen w-full font-['Open_Sans'] {GlassStyles.PAGE_BG} antialiased selection:bg-teal-500/20 selection:text-teal-100 bg-fixed",
    )
