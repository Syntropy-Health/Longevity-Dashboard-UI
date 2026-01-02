"""Account registration page.

This module contains the registration form for new patient accounts.
"""

import reflex as rx

from ....states import AuthState
from ....styles.constants import GlassStyles


def register_form() -> rx.Component:
    """Registration form component with username, password, name, phone, and optional email.

    Returns:
        The styled registration form component
    """
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "user-plus",
                class_name="w-16 h-16 text-teal-400 mb-8 mx-auto drop-shadow-[0_0_20px_rgba(45,212,191,0.4)]",
            ),
            rx.el.h2(
                "Create Account",
                class_name="text-4xl font-extralight text-white text-center mb-3 tracking-tight",
            ),
            rx.el.p(
                "Join your personalized health portal",
                class_name="text-slate-400 text-center mb-10 font-light tracking-wide",
            ),
            rx.el.form(
                rx.cond(
                    AuthState.register_error != "",
                    rx.el.div(
                        rx.icon("badge-alert", class_name="w-5 h-5 text-red-400 mr-2"),
                        rx.el.span(
                            AuthState.register_error,
                            class_name="text-sm text-red-300 font-medium",
                        ),
                        class_name="bg-red-500/10 backdrop-blur-md border border-red-500/20 p-4 rounded-2xl flex items-center mb-6",
                    ),
                ),
                # Username field (required)
                rx.el.div(
                    rx.el.label(
                        "Username",
                        rx.el.span(" *", class_name="text-teal-400"),
                        class_name="block text-[10px] font-bold text-slate-400 mb-2 ml-2 uppercase tracking-widest",
                    ),
                    rx.el.input(
                        type="text",
                        name="username",
                        placeholder="sarah_chen",
                        required=True,
                        min_length=3,
                        class_name=GlassStyles.INPUT,
                    ),
                    rx.el.p(
                        "At least 3 characters, used for login",
                        class_name="text-slate-500 text-xs mt-1 ml-2",
                    ),
                    class_name="mb-4",
                ),
                # Password field (required)
                rx.el.div(
                    rx.el.label(
                        "Password",
                        rx.el.span(" *", class_name="text-teal-400"),
                        class_name="block text-[10px] font-bold text-slate-400 mb-2 ml-2 uppercase tracking-widest",
                    ),
                    rx.el.input(
                        type="password",
                        name="password",
                        placeholder="••••••••",
                        required=True,
                        min_length=6,
                        class_name=GlassStyles.INPUT,
                    ),
                    rx.el.p(
                        "At least 6 characters",
                        class_name="text-slate-500 text-xs mt-1 ml-2",
                    ),
                    class_name="mb-4",
                ),
                # Confirm Password field (required)
                rx.el.div(
                    rx.el.label(
                        "Confirm Password",
                        rx.el.span(" *", class_name="text-teal-400"),
                        class_name="block text-[10px] font-bold text-slate-400 mb-2 ml-2 uppercase tracking-widest",
                    ),
                    rx.el.input(
                        type="password",
                        name="confirm_password",
                        placeholder="••••••••",
                        required=True,
                        class_name=GlassStyles.INPUT,
                    ),
                    class_name="mb-4",
                ),
                # Name field (required)
                rx.el.div(
                    rx.el.label(
                        "Full Name",
                        rx.el.span(" *", class_name="text-teal-400"),
                        class_name="block text-[10px] font-bold text-slate-400 mb-2 ml-2 uppercase tracking-widest",
                    ),
                    rx.el.input(
                        type="text",
                        name="name",
                        placeholder="Sarah Chen",
                        required=True,
                        class_name=GlassStyles.INPUT,
                    ),
                    class_name="mb-4",
                ),
                # Phone field (required)
                rx.el.div(
                    rx.el.label(
                        "Phone Number",
                        rx.el.span(" *", class_name="text-teal-400"),
                        class_name="block text-[10px] font-bold text-slate-400 mb-2 ml-2 uppercase tracking-widest",
                    ),
                    rx.el.input(
                        type="tel",
                        name="phone",
                        placeholder="[+1] [555] [123-4567]",
                        required=True,
                        class_name=GlassStyles.INPUT,
                    ),
                    rx.el.p(
                        "Used for voice check-ins",
                        class_name="text-slate-500 text-xs mt-1 ml-2",
                    ),
                    class_name="mb-4",
                ),
                # Email field (optional)
                rx.el.div(
                    rx.el.label(
                        "Email",
                        rx.el.span(
                            " (optional)", class_name="text-slate-500 font-normal"
                        ),
                        class_name="block text-[10px] font-bold text-slate-400 mb-2 ml-2 uppercase tracking-widest",
                    ),
                    rx.el.input(
                        type="email",
                        name="email",
                        placeholder="sarah@example.com",
                        class_name=GlassStyles.INPUT,
                    ),
                    class_name="mb-8",
                ),
                rx.el.button(
                    rx.cond(
                        AuthState.is_loading,
                        rx.el.div(
                            class_name="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"
                        ),
                        "Create Account",
                    ),
                    type="submit",
                    disabled=AuthState.is_loading,
                    class_name=f"w-full flex justify-center py-4 px-6 text-sm font-semibold {GlassStyles.BUTTON_PRIMARY} disabled:opacity-70 disabled:cursor-not-allowed shadow-xl",
                ),
                # Link to login
                rx.el.div(
                    rx.el.p(
                        "Already have an account?",
                        class_name="text-slate-400 text-sm",
                    ),
                    rx.link(
                        "Sign in here",
                        href="/login",
                        class_name="text-teal-400 hover:text-teal-300 text-sm font-medium underline underline-offset-2",
                    ),
                    class_name="mt-6 flex flex-col items-center gap-2",
                ),
                on_submit=AuthState.register,
            ),
            class_name="bg-slate-800/40 backdrop-blur-[40px] py-12 px-8 sm:px-12 shadow-[0_20px_60px_rgba(0,0,0,0.3)] rounded-[3rem] w-full max-w-md border border-slate-600/30",
        ),
        class_name=f"min-h-screen {GlassStyles.PAGE_BG} flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8 font-['Open_Sans']",
    )


def register_page() -> rx.Component:
    """Registration page component.

    Returns:
        The registration form page
    """
    return register_form()
