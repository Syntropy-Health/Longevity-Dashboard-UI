import reflex as rx
from ..states.auth_state import AuthState
from ..config import current_config


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "activity",
                class_name="w-16 h-16 text-emerald-500 mb-8 mx-auto drop-shadow-xl opacity-90",
            ),
            rx.el.h2(
                "Vitality Clinic",
                class_name="text-4xl font-extralight text-gray-800 text-center mb-3 tracking-tight",
            ),
            rx.el.p(
                "Sign in to your personalized health portal",
                class_name="text-gray-500 text-center mb-12 font-light tracking-wide",
            ),
            rx.el.form(
                rx.cond(
                    AuthState.login_error != "",
                    rx.el.div(
                        rx.icon("badge_alert", class_name="w-5 h-5 text-red-500 mr-2"),
                        rx.el.span(
                            AuthState.login_error,
                            class_name="text-sm text-red-700 font-medium",
                        ),
                        class_name="bg-red-50/60 backdrop-blur-md border border-red-100/60 p-4 rounded-2xl flex items-center mb-8",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Username",
                        class_name="block text-[10px] font-bold text-gray-400 mb-2 ml-2 uppercase tracking-widest",
                    ),
                    rx.el.input(
                        type="text",
                        name="username",
                        placeholder="admin or patient",
                        required=True,
                        class_name=f"w-full px-6 py-4 {current_config.glass_input_style}",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password",
                        class_name="block text-[10px] font-bold text-gray-400 mb-2 ml-2 uppercase tracking-widest",
                    ),
                    rx.el.input(
                        type="password",
                        name="password",
                        placeholder="••••••••",
                        required=True,
                        class_name=f"w-full px-6 py-4 {current_config.glass_input_style}",
                    ),
                    class_name="mb-10",
                ),
                rx.el.button(
                    rx.cond(
                        AuthState.is_loading,
                        rx.el.div(
                            class_name="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"
                        ),
                        "Access Portal",
                    ),
                    type="submit",
                    disabled=AuthState.is_loading,
                    class_name=f"w-full flex justify-center py-4 px-6 text-sm font-semibold {current_config.glass_button_primary} disabled:opacity-70 disabled:cursor-not-allowed shadow-xl",
                ),
                rx.el.div(
                    rx.el.p(
                        "Access Credentials",
                        class_name="text-[10px] font-bold text-gray-400 uppercase mb-4 tracking-widest text-center",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Admin",
                                class_name="font-bold text-gray-600 block text-xs mb-1",
                            ),
                            rx.el.span(
                                "admin / admin",
                                class_name="text-gray-400 font-mono text-[10px]",
                            ),
                            class_name="text-center",
                        ),
                        rx.el.div(class_name="w-px h-8 bg-gray-300/40 mx-6"),
                        rx.el.div(
                            rx.el.span(
                                "Patient",
                                class_name="font-bold text-gray-600 block text-xs mb-1",
                            ),
                            rx.el.span(
                                "patient / patient",
                                class_name="text-gray-400 font-mono text-[10px]",
                            ),
                            class_name="text-center",
                        ),
                        class_name="flex justify-center items-center",
                    ),
                    class_name="mt-12 p-6 bg-white/30 rounded-[2rem] border border-white/40 backdrop-blur-lg",
                ),
                on_submit=AuthState.login,
            ),
            class_name="bg-white/30 backdrop-blur-[40px] py-16 px-8 sm:px-12 shadow-[0_20px_60px_rgba(0,0,0,0.03)] rounded-[3rem] w-full max-w-md border border-white/50",
        ),
        class_name=f"min-h-screen {current_config.glass_bg_gradient} flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8 font-['Open_Sans']",
    )


def auth_page() -> rx.Component:
    return login_form()