"""Pytest configuration and shared fixtures."""

import pytest
import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


@pytest.fixture(scope="session")
def db_url():
    """Get the database URL from environment."""
    return os.getenv(
        "DB_URL",
        os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/longevity_clinic",
        ),
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
    from longevity_clinic.app.data.demo import DEMO_PHONE_NUMBER

    return DEMO_PHONE_NUMBER
