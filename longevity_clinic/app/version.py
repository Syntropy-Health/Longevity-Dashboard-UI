"""Version information for Longevity Clinic app.

Reads version from pyproject.toml and provides feature tag support.
"""

import tomllib
from pathlib import Path

# Cache for version info
_version_info: dict | None = None


def _load_version_info() -> dict:
    """Load version info from pyproject.toml."""
    global _version_info
    if _version_info is not None:
        return _version_info

    # Find pyproject.toml (traverse up from this file)
    current = Path(__file__).resolve()
    for parent in [current.parent, *list(current.parents)]:
        pyproject = parent / "pyproject.toml"
        if pyproject.exists():
            with open(pyproject, "rb") as f:
                data = tomllib.load(f)
                _version_info = {
                    "version": data.get("project", {}).get("version", "0.0.0"),
                    "name": data.get("project", {}).get("name", "longclinic"),
                }
                return _version_info

    # Fallback
    _version_info = {"version": "0.0.0", "name": "longclinic"}
    return _version_info


def get_version() -> str:
    """Get the current version string (e.g., '0.2.1')."""
    return _load_version_info()["version"]


def get_version_display() -> str:
    """Get display version with 'v' prefix (e.g., 'v0.2.1')."""
    return f"v{get_version()}"


# Feature tag - updated manually or via CI when features are added
# Format: short description of latest feature(s)
FEATURE_TAG = "profile-edit-seq-fix"


def get_full_version() -> str:
    """Get full version with feature tag (e.g., 'v0.2.1 • profile-editing')."""
    version = get_version_display()
    if FEATURE_TAG:
        return f"{version} • {FEATURE_TAG}"
    return version


# Expose at module level
__version__ = get_version()
