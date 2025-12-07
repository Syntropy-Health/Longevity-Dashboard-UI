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
    """Load environment variables from hierarchical env files."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("python-dotenv not installed, skipping .env loading")
        return
    
    base_path = Path(__file__).parent
    envs_path = base_path / "envs"
    
    # Determine environment (default to dev)
    app_env = os.getenv("APP_ENV", "dev").lower()
    print(f"🔧 Loading environment: {app_env}")
    
    # Load in order (later files override earlier ones)
    env_files = [
        envs_path / ".env.base",      # Shared config
        envs_path / f".env.{app_env}", # Environment-specific
        envs_path / ".env.secrets",    # Secrets (gitignored)
    ]
    
    for env_file in env_files:
        if env_file.exists():
            load_dotenv(env_file, override=True)
            print(f"  ✓ Loaded: {env_file.name}")
        else:
            print(f"  ○ Skipped (not found): {env_file.name}")

# Load environment variables
load_hierarchical_env()

# Get deployment URLs from environment
# Empty string means use Reflex defaults (localhost)
frontend_url = os.getenv("FRONTEND_DEPLOY_URL", "")
backend_url = os.getenv("REFLEX_API_URL", "")

# Log the effective URLs
if backend_url:
    print(f"📡 Backend URL: {backend_url}")
else:
    print("📡 Backend URL: http://localhost:8000 (default)")

if frontend_url:
    print(f"🌐 Frontend URL: {frontend_url}")
else:
    print("🌐 Frontend URL: http://localhost:3000 (default)")

# Build CORS origins list
cors_origins = [
    frontend_url,
    "http://localhost:3000",
    "https://longevity-clinic-test.up.railway.app",
    "https://longevity-clinic-backend-test.up.railway.app",
]
# Remove duplicates and empty strings
cors_origins = list(set(filter(None, cors_origins)))

config = rx.Config(
    app_name="longevity_clinic",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    # Database - use REFLEX_DB_URL (Railway sets this from Postgres service)
    db_url=os.getenv("REFLEX_DB_URL", "dev.db"),
    # Additional frontend packages
    frontend_packages=["react-icons"],
    show_built_with_reflex=False,
    # CORS settings for production
    cors_allowed_origins=cors_origins,
)
