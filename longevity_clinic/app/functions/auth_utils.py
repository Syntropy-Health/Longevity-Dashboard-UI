"""Authentication utilities for password hashing and verification.

Uses bcrypt for secure password hashing with an additional pepper for defense in depth.
"""

import bcrypt

from longevity_clinic.app.config import PASSWORD_PEPPER


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with pepper.

    Args:
        password: Plain text password

    Returns:
        Bcrypt hashed password string
    """
    # Add pepper to password before hashing
    peppered = f"{password}{PASSWORD_PEPPER}"
    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(peppered.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash.

    Args:
        password: Plain text password to verify
        password_hash: Stored bcrypt hash

    Returns:
        True if password matches, False otherwise
    """
    if not password_hash:
        return False
    try:
        peppered = f"{password}{PASSWORD_PEPPER}"
        return bcrypt.checkpw(peppered.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False
