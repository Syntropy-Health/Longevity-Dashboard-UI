"""Auth page module.

This module provides the authentication interface with:
- Login form
- Registration form
- Credential display
"""

from .page import auth_page, login_form
from .register import register_page

__all__ = [
    "auth_page",
    "login_form",
    "register_page",
]
