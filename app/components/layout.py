import reflex as rx
from app.components.sidebar import sidebar
from app.components.navbar import navbar
from app.styles.glass_styles import GlassStyles


def dashboard_layout(content: rx.Component) -> rx.Component:
    """
    Wrapper for authenticated pages. Includes sidebar (desktop) and navbar.
    """
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(content, class_name="pt-24 px-6 pb-10"),
            class_name="md:pl-64 min-h-screen transition-all duration-300",
        ),
        class_name=GlassStyles.PAGE_BG,
    )