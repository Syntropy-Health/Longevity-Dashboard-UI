"""Pytest configuration and shared fixtures."""

import os
from pathlib import Path

import pytest

# Load environment variables using hierarchical env loading
try:
    from dotenv import load_dotenv

    base_dir = Path(__file__).parent.parent
    envs_dir = base_dir / "envs"

    # Load in order: .env.base -> .env.dev -> .env.secrets
    for env_file in [".env.base", ".env.dev", ".env.secrets"]:
        env_path = envs_dir / env_file
        if env_path.exists():
            load_dotenv(env_path, override=True)
            print(f"Loaded environment from {env_path}")

    # Also check for legacy .env in root
    legacy_env = base_dir / ".env"
    if legacy_env.exists():
        load_dotenv(legacy_env, override=True)
except ImportError:
    pass


@pytest.fixture(scope="session")
def db_url():
    """Get the database URL from environment."""
    return os.getenv(
        "REFLEX_DB_URL",
        "sqlite:///reflex.db",
    )


@pytest.fixture(scope="session")
def call_api_token():
    """Get the call API token from environment."""
    return os.getenv("CALL_API_TOKEN", "")


@pytest.fixture(scope="session")
def call_logs_api_base():
    """Get the call logs API base URL."""
    return "https://directus-staging-ee94.up.railway.app/items/call_logs"


@pytest.fixture(scope="session")
def demo_phone_number():
    """Get the demo phone number for testing call logs."""
    from longevity_clinic.app.data.seed import DEMO_PHONE_NUMBER

    return DEMO_PHONE_NUMBER
