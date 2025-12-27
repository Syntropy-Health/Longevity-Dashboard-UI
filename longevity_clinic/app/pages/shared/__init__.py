"""Shared pages module - pages used by both admin and patient roles."""

from .appointments import appointments_page
from .auth import auth_page, register_page
from .notifications import notifications_page

__all__ = ["appointments_page", "auth_page", "notifications_page", "register_page"]
