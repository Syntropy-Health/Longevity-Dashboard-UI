"""Alembic migrations environment configuration.

Supports both local SQLite and remote PostgreSQL (Supabase) databases.
Database URL is read from REFLEX_DB_URL environment variable.
"""

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import create_engine, pool

from alembic import context

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables (same hierarchy as rxconfig.py)
try:
    from dotenv import load_dotenv

    envs_path = Path(__file__).parent.parent / "envs"
    app_env = os.getenv("APP_ENV", "dev").lower()

    # Load in order: base → env-specific → secrets
    for env_file in [
        envs_path / ".env.base",
        envs_path / f".env.{app_env}",
        envs_path / ".env.secrets",
    ]:
        if env_file.exists():
            load_dotenv(env_file, override=True)
except ImportError:
    pass  # dotenv not available, rely on environment variables

# Import SQLModel metadata from our models
# This enables autogenerate to detect model changes
from sqlmodel import SQLModel

from longevity_clinic.app.data.schemas.db.enums import (  # noqa: F401
    BiomarkerCategory,
    CheckInType,
    TreatmentCategory,
    TreatmentStatus,
    UrgencyLevel,
)

# Import all models to register them with SQLModel.metadata
# This MUST happen before accessing SQLModel.metadata for autogenerate to work
from longevity_clinic.app.data.schemas.db.models import (  # noqa: F401
    Appointment,
    BiomarkerAggregate,
    BiomarkerDefinition,
    BiomarkerReading,
    CallLog,
    CallTranscript,
    CheckIn,
    ClinicDailyMetrics,
    FoodLogEntry,
    MedicationEntry,
    Notification,
    PatientTreatment,
    PatientVisit,
    ProviderMetrics,
    SymptomEntry,
    Treatment,
    TreatmentProtocolMetric,
    User,
)

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate support
target_metadata = SQLModel.metadata


def get_database_url() -> str:
    """Get database URL from environment or alembic.ini.

    Priority:
    1. REFLEX_DB_URL environment variable (production/test)
    2. sqlalchemy.url from alembic.ini (fallback)

    For Supabase PostgreSQL, use the pooler URL on port 6543.
    """
    db_url = os.getenv("REFLEX_DB_URL")
    if db_url:
        print(
            f"📦 Using database from REFLEX_DB_URL: {db_url.split('@')[1] if '@' in db_url else db_url}"
        )
        return db_url

    # Fallback to alembic.ini config
    url = config.get_main_option("sqlalchemy.url")
    if url and url != "driver://user:pass@localhost/dbname":
        return url

    # Default to local SQLite
    return "sqlite:///reflex.db"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Generates SQL scripts without connecting to the database.
    Useful for reviewing migration SQL before applying.
    """
    url = get_database_url()
    is_sqlite = url.startswith("sqlite")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Enable batch mode for SQLite (required for ALTER TABLE operations)
        render_as_batch=is_sqlite,
        # Don't compare types for SQLite - TEXT/VARCHAR are equivalent
        compare_type=not is_sqlite,
        # Don't compare server defaults - causes false positives with datetime
        compare_server_default=False,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Creates an engine and runs migrations against the live database.
    """
    url = get_database_url()
    is_sqlite = url.startswith("sqlite")

    # Create engine directly with the URL (not from config section)
    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
        # PostgreSQL-specific settings for Supabase
        **(
            {"connect_args": {"sslmode": "require"}}
            if url.startswith("postgresql")
            else {}
        ),
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Enable batch mode for SQLite (required for ALTER TABLE operations)
            render_as_batch=is_sqlite,
            # Don't compare types for SQLite - TEXT/VARCHAR are equivalent
            compare_type=not is_sqlite,
            # Don't compare server defaults - causes false positives with datetime
            compare_server_default=False,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
