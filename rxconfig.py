import reflex as rx
import os

config = rx.Config(
    app_name="longevity_clinic",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    # Database
    db_url=os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/longevity_clinic"),
    # Additional frontend packages
    frontend_packages=["react-icons"],
    # CORS settings for production
    cors_allowed_origins=["https://longevity-clinic-platform-gold-moon.reflex.run/", "http://localhost:3000"],
)
