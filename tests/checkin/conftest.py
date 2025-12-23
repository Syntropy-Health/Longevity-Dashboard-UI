"""Pytest fixtures for checkin integration tests.

Provides an isolated SQLite test database with proper schema setup.
"""

import contextlib
import os
import tempfile
from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

# Import all models to register them with SQLModel
from longevity_clinic.app.data.model import User


@pytest.fixture(scope="function")
def test_db_path() -> Generator[str]:
    """Create a temporary SQLite database for testing."""
    # Create temp file with proper cleanup
    fd, path = tempfile.mkstemp(suffix=".db", prefix="test_checkin_")
    os.close(fd)

    yield path

    # Cleanup after test
    with contextlib.suppress(OSError):
        os.unlink(path)


@pytest.fixture(scope="function")
def test_db_url(test_db_path: str) -> str:
    """Get the test database URL."""
    return f"sqlite:///{test_db_path}"


@pytest.fixture(scope="function")
def test_engine(test_db_url: str):
    """Create a test database engine and initialize schema."""
    engine = create_engine(test_db_url, echo=False)

    # Create all tables
    SQLModel.metadata.create_all(engine)

    return engine


@pytest.fixture(scope="function")
def test_session(test_engine) -> Generator[Session]:
    """Create a test database session."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="function")
def test_user(test_session: Session) -> User:
    """Create a test user in the database."""
    user = User(
        external_id="test_user_001",
        name="Test Patient",  # User model uses 'name' not 'full_name'
        email="test@example.com",
        phone="+11234567890",
        role="patient",
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user


@pytest.fixture
def sample_transcript() -> str:
    """Sample call transcript for testing health data extraction."""
    return """
    Hi, this is a check-in. I've been feeling pretty good today.
    I took my metformin 500mg this morning as usual.
    Also had my vitamin D supplement.
    For breakfast I had oatmeal with blueberries, about 300 calories.
    I've been having some mild headaches in the afternoon, maybe 3 out of 10 severity.
    Also a bit of fatigue but nothing too bad.
    Overall energy level is good, about 7 out of 10.
    """


@pytest.fixture
def sample_transcript_with_symptoms() -> str:
    """Sample transcript with detailed symptoms."""
    return """
    Good morning. I wanted to report that I've been experiencing some symptoms.
    I had joint pain in my knees, severity about 5 out of 10.
    Also some mild nausea after meals, started yesterday.
    I took ibuprofen 200mg for the pain, it helped a bit.
    Had a light lunch - chicken salad, probably 400 calories.
    Still taking my regular medications - lisinopril 10mg and aspirin 81mg daily.
    Sleep has been okay, about 6 hours last night.
    """


@pytest.fixture
def sample_transcript_minimal() -> str:
    """Minimal transcript for edge case testing."""
    return "Quick check-in, feeling fine today."
