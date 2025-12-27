"""Authentication state management."""

from __future__ import annotations

import uuid

# Standard library
# Third-party
import reflex as rx
from sqlmodel import or_, select

# Local application
from longevity_clinic.app.data.schemas.db.models import User as UserDB
from longevity_clinic.app.data.schemas.state import User
from longevity_clinic.app.functions.auth_utils import hash_password, verify_password
from longevity_clinic.app.functions.utils import format_phone_display, normalize_phone


class AuthState(rx.State):
    user: User | None = None
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
        """Authenticate user with username/password.

        Checks demo credentials first, then database users.
        """
        self.is_loading = True
        self.login_error = ""
        username = form_data.get("username", "").strip()
        password = form_data.get("password", "")

        if not username or not password:
            self.login_error = "Username and password are required."
            self.is_loading = False
            return

        from longevity_clinic.app.config import (
            DEMO_ADMIN_PASSWORD,
            DEMO_ADMIN_USERNAME,
            DEMO_PATIENT_PASSWORD,
            DEMO_PATIENT_USERNAME,
            current_config,
        )

        demo = current_config.demo_user

        # Check demo admin credentials
        if username == DEMO_ADMIN_USERNAME and password == DEMO_ADMIN_PASSWORD:
            self.user = {
                "id": str(demo.admin_id),
                "username": DEMO_ADMIN_USERNAME,
                "email": "admin@longevityclinic.com",
                "role": "admin",
                "full_name": "Dr. Admin",
            }
            self.is_loading = False
            return rx.redirect("/admin/dashboard")

        # Check demo patient credentials
        if username == DEMO_PATIENT_USERNAME and password == DEMO_PATIENT_PASSWORD:
            self.user = {
                "id": str(demo.patient_id),
                "username": DEMO_PATIENT_USERNAME,
                "email": demo.email,
                "role": "patient",
                "full_name": demo.full_name,
                "phone": demo.phone.strip(),
            }
            self.is_loading = False
            return rx.redirect("/patient/portal")

        # Check database for registered users
        try:
            with rx.session() as session:
                # Find user by username or email
                db_user = session.exec(
                    select(UserDB).where(
                        or_(UserDB.username == username, UserDB.email == username)
                    )
                ).first()

                if db_user and db_user.password_hash:
                    if verify_password(password, db_user.password_hash):
                        self.user = {
                            "id": str(db_user.id),
                            "username": db_user.username or db_user.external_id.lower(),
                            "email": db_user.email,
                            "role": db_user.role,
                            "full_name": db_user.name,
                            "phone": db_user.phone or "",
                        }
                        self.is_loading = False
                        # Redirect based on role
                        if db_user.role in ["admin", "staff", "provider"]:
                            return rx.redirect("/admin/dashboard")
                        return rx.redirect("/patient/portal")

            # No valid credentials found
            self.login_error = "Invalid username or password."
            self.is_loading = False

        except Exception as e:
            self.login_error = f"Login failed: {e!s}"
            self.is_loading = False

    @rx.event
    async def register(self, form_data: dict):
        """Register a new patient account with username and password."""
        self.is_loading = True
        self.register_error = ""

        username = form_data.get("username", "").strip().lower()
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")
        name = form_data.get("name", "").strip()
        phone = form_data.get("phone", "").strip()
        email = form_data.get("email", "").strip() or None

        # Import demo credentials to prevent collision
        from longevity_clinic.app.config import (
            DEMO_ADMIN_USERNAME,
            DEMO_PATIENT_USERNAME,
        )

        # Validation
        if not username:
            self.register_error = "Username is required."
            self.is_loading = False
            return

        if len(username) < 3:
            self.register_error = "Username must be at least 3 characters."
            self.is_loading = False
            return

        # Prevent using demo usernames
        if username in [DEMO_ADMIN_USERNAME, DEMO_PATIENT_USERNAME]:
            self.register_error = "This username is reserved. Please choose another."
            self.is_loading = False
            return

        if not password:
            self.register_error = "Password is required."
            self.is_loading = False
            return

        if len(password) < 6:
            self.register_error = "Password must be at least 6 characters."
            self.is_loading = False
            return

        if password != confirm_password:
            self.register_error = "Passwords do not match."
            self.is_loading = False
            return

        if not name:
            self.register_error = "Full name is required."
            self.is_loading = False
            return

        if not phone:
            self.register_error = "Phone number is required."
            self.is_loading = False
            return

        # Normalize phone to E.164 format
        normalized_phone = normalize_phone(phone)
        if not normalized_phone:
            self.register_error = (
                "Invalid phone number format. Use +1XXXXXXXXXX or similar."
            )
            self.is_loading = False
            return

        try:
            with rx.session() as session:
                # Check if username already exists
                existing_username = session.exec(
                    select(UserDB).where(UserDB.username == username)
                ).first()
                if existing_username:
                    self.register_error = "This username is already taken."
                    self.is_loading = False
                    return

                # Check if phone already exists
                existing_phone = session.exec(
                    select(UserDB).where(UserDB.phone == normalized_phone)
                ).first()
                if existing_phone:
                    self.register_error = (
                        "An account with this phone number already exists."
                    )
                    self.is_loading = False
                    return

                # Check email uniqueness if provided
                if email:
                    existing_email = session.exec(
                        select(UserDB).where(UserDB.email == email)
                    ).first()
                    if existing_email:
                        self.register_error = (
                            "An account with this email already exists."
                        )
                        self.is_loading = False
                        return

                # Generate external_id (P + next available number)
                last_patient = session.exec(
                    select(UserDB)
                    .where(UserDB.role == "patient")
                    .where(UserDB.external_id.startswith("P"))
                    .order_by(UserDB.id.desc())
                ).first()

                if last_patient and last_patient.external_id.startswith("P"):
                    try:
                        last_num = int(last_patient.external_id[1:])
                        external_id = f"P{last_num + 1:03d}"
                    except ValueError:
                        external_id = f"P{uuid.uuid4().hex[:6].upper()}"
                else:
                    external_id = "P001"

                # Hash password
                password_hash = hash_password(password)

                # Create user in DB
                new_user = UserDB(
                    external_id=external_id,
                    username=username,
                    password_hash=password_hash,
                    name=name,
                    email=email or f"{username}@placeholder.local",
                    phone=normalized_phone,
                    role="patient",
                )
                session.add(new_user)
                session.commit()
                session.refresh(new_user)

                # Set session state and redirect
                self.user = {
                    "id": str(new_user.id),
                    "username": username,
                    "email": new_user.email,
                    "role": "patient",
                    "full_name": name,
                    "phone": normalized_phone,
                }
                self.is_loading = False
                return rx.redirect("/patient/portal")

        except Exception as e:
            self.register_error = f"Registration failed: {e!s}"
            self.is_loading = False

    @rx.event
    def logout(self):
        self.user = None
        self.show_mobile_menu = False
        return rx.redirect("/")

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
    def user_id(self) -> int:
        """Get user's database ID as integer."""
        if not self.user:
            return 0
        try:
            return int(self.user.get("id", "0"))
        except (ValueError, TypeError):
            return 0

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

    @rx.var
    def user_phone(self) -> str:
        """Get user's phone number for API calls."""
        if not self.user:
            return ""
        return self.user.get("phone", "")

    @rx.var
    def user_phone_formatted(self) -> str:
        """Get user's phone number formatted for display (e.g., +1 (123) 456-7890)."""
        phone = self.user_phone
        if not phone:
            return ""
        return format_phone_display(phone)
