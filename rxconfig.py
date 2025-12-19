import reflex as rx
import os
from pathlib import Path

# =============================================================================
# Hierarchical Environment Loading
# =============================================================================
# Load order:
#   1. .env.base (shared config)
#   2. .env.{APP_ENV} (environment-specific: dev, test, prod)
#   3. .env.secrets (API keys - gitignored)
#
# Set APP_ENV to control which environment config is loaded:
#   - APP_ENV=dev (default) - local development, backend on localhost
#   - APP_ENV=prod - production deployment on Railway
# =============================================================================


def load_hierarchical_env():
    """Load environment variables from hierarchical env files.

    IMPORTANT: We preserve any environment variables that were set BEFORE this
    script runs (e.g., by Railway, Docker, or the shell). The .env files only
    provide defaults for vars that aren't already set.

    For local development: env files work as expected (base → env-specific → secrets)
    For Railway deployment: Railway sets vars which take precedence over env files
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("python-dotenv not installed, skipping .env loading")
        return

    # Capture deployment-critical env vars BEFORE loading any .env files
    # These should not be overridden by .env file loading
    critical_vars = [
        "APP_ENV",
        "IS_DEMO",
        "REFLEX_API_URL",
        "REFLEX_DEPLOY_URL",
        "CORS_ALLOWED_ORIGINS",
        "REFLEX_DB_URL",
        "OPENAI_API_KEY",
        "CALL_API_TOKEN",
    ]
    pre_existing = {k: os.environ[k] for k in critical_vars if k in os.environ}

    base_path = Path(__file__).parent
    envs_path = base_path / "envs"

    # Determine environment (default to dev, but respect if already set)
    app_env = pre_existing.get("APP_ENV", os.getenv("APP_ENV", "dev")).lower()
    print(f"🔧 Loading environment: {app_env}")

    # Load in order (later files override earlier ones within the hierarchy)
    env_files = [
        envs_path / ".env.base",  # Shared config
        envs_path / f".env.{app_env}",  # Environment-specific
        envs_path / ".env.secrets",  # Secrets (gitignored)
    ]

    for env_file in env_files:
        if env_file.exists():
            # Load with override=True so env files can build on each other
            load_dotenv(env_file, override=True)
            print(f"  ✓ Loaded: {env_file.name}")
        else:
            print(f"  ○ Skipped (not found): {env_file.name}")

    # CRITICAL: Restore pre-existing environment variables
    # This ensures Railway/Docker/shell vars take precedence over .env files
    for key, value in pre_existing.items():
        os.environ[key] = value
        if key != "OPENAI_API_KEY" and key != "CALL_API_TOKEN":  # Don't log secrets
            print(f"  ↩ Restored pre-existing: {key}={value}")


# Load environment variables
load_hierarchical_env()

# =============================================================================
# Deployment URL Configuration
# =============================================================================
# Single Source of Truth:
#   - REFLEX_API_URL: Backend's public URL (frontend uses this for API/WebSocket)
#   - REFLEX_DEPLOY_URL: This service's own public URL
#   - CORS_ALLOWED_ORIGINS: Frontend URL (backend uses for CORS)
# =============================================================================

# Get deployment URLs from environment
backend_url = os.getenv("REFLEX_API_URL", "")
deploy_url = os.getenv("REFLEX_DEPLOY_URL", "")

# Log the effective URLs
if backend_url:
    print(f"📡 Backend URL (REFLEX_API_URL): {backend_url}")
else:
    print("📡 Backend URL: http://localhost:8000 (default)")

if deploy_url:
    print(f"🌐 Deploy URL (REFLEX_DEPLOY_URL): {deploy_url}")
else:
    print("🌐 Deploy URL: http://localhost:3000 (default)")

# Build CORS origins list from CORS_ALLOWED_ORIGINS env var (comma-separated)
# Include: backend URL, frontend URL, localhost for dev
cors_env = os.getenv("CORS_ALLOWED_ORIGINS", "")
cors_origins = (
    [origin.strip() for origin in cors_env.split(",") if origin.strip()]
    if cors_env
    else []
)
# Always add localhost for dev and the backend/deploy URLs if set
cors_origins.extend(
    [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
)
if backend_url:
    cors_origins.append(backend_url)
if deploy_url:
    cors_origins.append(deploy_url)
# Remove duplicates and empty strings
cors_origins = list(set(filter(None, cors_origins)))
print(f"🔒 CORS allowed origins: {cors_origins}")

config = rx.Config(
    app_name="longevity_clinic",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    # Deployment URLs - set per-service at deploy time
    # - Frontend: api_url=backend URL, deploy_url=frontend URL
    # - Backend: deploy_url=backend address (api_url leave empty to default to localhost)
    **({"api_url": backend_url} if backend_url else {}),
    **({"deploy_url": deploy_url} if deploy_url else {}),
    # Backend host/port - Railway requires 0.0.0.0 and uses PORT env var
    backend_host="0.0.0.0",
    backend_port=int(os.getenv("BACKEND_PORT", "8000")),
    # Frontend port - Railway sets PORT env var
    frontend_port=int(os.getenv("FRONTEND_PORT", "3000")),
    # Database - use REFLEX_DB_URL (Railway sets this from Postgres service)
    db_url=os.getenv("REFLEX_DB_URL", "sqlite:///reflex.db"),
    # Additional frontend packages
    frontend_packages=["react-icons"],
    show_built_with_reflex=False,
    # CORS settings for production
    cors_allowed_origins=cors_origins,
)
