"""User model for patients and admins."""

from datetime import datetime

import reflex as rx
from sqlmodel import Field

from .base import utc_now


class User(rx.Model, table=True):
    """User account for patients and admins."""

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    external_id: str = Field(index=True, unique=True)  # e.g., "P001"
    username: str | None = Field(
        default=None, index=True, unique=True
    )  # Login username
    password_hash: str | None = Field(default=None)  # bcrypt hashed password
    name: str
    email: str = Field(index=True, unique=True)
    phone: str | None = Field(default=None, index=True)
    role: str = Field(default="patient")  # "patient" | "admin" | "provider"
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
