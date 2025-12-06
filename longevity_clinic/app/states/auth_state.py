import reflex as rx
import asyncio
from typing import Optional

from ..data.state_schemas import User


class AuthState(rx.State):
    user: Optional[User] = None
    is_authenticated: bool = False
    login_error: str = ""
    register_error: str = ""
    is_loading: bool = False
    show_mobile_menu: bool = False

    @rx.event
    def toggle_mobile_menu(self):
        self.show_mobile_menu = not self.show_mobile_menu

    @rx.event
    def close_mobile_menu(self):
        self.show_mobile_menu = False

    @rx.event
    async def login(self, form_data: dict):
        self.is_loading = True
        self.login_error = ""
        await asyncio.sleep(1)
        username = form_data.get("username", "")
        password = form_data.get("password", "")
        if username == "admin" and password == "admin":
            self.user = {
                "id": "1",
                "username": "admin",
                "email": "admin@clinic.com",
                "role": "admin",
                "full_name": "Dr. Sarah Administrator",
            }
            self.is_authenticated = True
            self.is_loading = False
            return rx.redirect("/admin/dashboard")
        elif username == "patient" and password == "patient":
            self.user = {
                "id": "2",
                "username": "patient",
                "email": "patient@example.com",
                "role": "patient",
                "full_name": "John Doe",
            }
            self.is_authenticated = True
            self.is_loading = False
            return rx.redirect("/patient/portal")
        else:
            self.login_error = "Invalid username or password. Try 'admin'/'admin' or 'patient'/'patient'."
            self.is_loading = False

    @rx.event
    def logout(self):
        self.user = None
        self.is_authenticated = False
        self.show_mobile_menu = False
        return rx.redirect("/")

    @rx.event
    def check_auth(self):
        """Check if user is authenticated and redirect to login if not."""
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.event
    async def register(self, form_data: dict):
        self.is_loading = True
        self.register_error = ""
        await asyncio.sleep(1)
        self.register_error = (
            "Registration is closed for this demo. Please use the login form."
        )
        self.is_loading = False

    @rx.var
    def user_initials(self) -> str:
        if not self.user:
            return "??"
        name_parts = self.user["full_name"].split(" ")
        if len(name_parts) >= 2:
            return f"{name_parts[0][0]}{name_parts[1][0]}".upper()
        return self.user["full_name"][:2].upper()

    @rx.var
    def user_first_name(self) -> str:
        if not self.user:
            return "Guest"
        name_parts = self.user["full_name"].split(" ")
        return name_parts[0] if name_parts else "Guest"

    @rx.var
    def is_admin(self) -> bool:
        return self.user is not None and self.user["role"] in ["admin", "staff"]

    @rx.var
    def role_label(self) -> str:
        if not self.user:
            return ""
        return self.user["role"].capitalize()

    @rx.var
    def user_full_name(self) -> str:
        """Get user's full name safely."""
        if not self.user:
            return ""
        return self.user.get("full_name", "")
