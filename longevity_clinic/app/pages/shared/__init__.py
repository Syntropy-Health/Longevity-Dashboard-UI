"""Shared pages module - pages used by both admin and patient roles."""

from .auth import auth_page
from .appointments import appointments_page
from .notifications import notifications_page

__all__ = ["auth_page", "appointments_page", "notifications_page"]
