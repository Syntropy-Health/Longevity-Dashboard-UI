import reflex as rx
import os

# Get deployment URLs from environment
frontend_url = os.getenv("FRONTEND_DEPLOY_URL", "http://localhost:3000")
backend_url = os.getenv("REFLEX_API_URL", "http://localhost:8000")

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
    # Database - Railway provides DATABASE_URL, we also check DB_URL
    db_url=os.getenv("DB_URL", os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/longevity_clinic")),
    # Additional frontend packages
    frontend_packages=["react-icons"],
    # CORS settings for production
    cors_allowed_origins=cors_origins,
)
