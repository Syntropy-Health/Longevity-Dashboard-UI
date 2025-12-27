import logging
import os
from typing import Any, Literal

from pydantic import BaseModel, Field, computed_field

# =============================================================================
# Centralized Logging Configuration
# =============================================================================

# LOG_FILE_PATH = Path(__file__).parent.parent.parent / "dev.logs"

# Read LOGLEVEL from environment variable (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# Defaults to DEBUG for development. Use INFO for production to reduce log verbosity.
_LOGLEVEL_STR = os.getenv("LOGLEVEL", "DEBUG").upper()
_LOGLEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "WARN": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
DEFAULT_LOG_LEVEL = _LOGLEVEL_MAP.get(_LOGLEVEL_STR, logging.DEBUG)


def get_logger(name: str, level: int | None = None) -> logging.Logger:
    """
    Get a configured logger instance with console output.

    Args:
        name: Logger name (e.g., 'longevity_clinic.call_logs')
        level: Logging level (default: from LOGLEVEL env var, or DEBUG)

    Returns:
        Configured logger instance
    """
    if level is None:
        level = DEFAULT_LOG_LEVEL
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Only add handlers if not already present to avoid duplicate logs
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console handler only (file handler disabled to prevent Reflex hot-reload loops)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# Create config logger (before any other code that might log)
_config_logger = get_logger("longevity_clinic.config")

# Ensure OpenAI API key is loaded from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CALL_API_TOKEN = os.getenv("CALL_API_TOKEN", "")
PASSWORD_PEPPER = os.getenv("PASSWORD_PEPPER", "default-pepper-change-in-production")

# Validate required API keys on startup
if not OPENAI_API_KEY:
    _config_logger.warning(
        "OPENAI_API_KEY not set. Voice transcription and AI features will not work."
    )

if not CALL_API_TOKEN:
    _config_logger.warning("CALL_API_TOKEN not set. Call log fetching will not work.")


# =============================================================================
# Demo Credentials (for testing/demo purposes only)
# =============================================================================
DEMO_ADMIN_USERNAME = "admin"
DEMO_ADMIN_PASSWORD = "admin"
DEMO_PATIENT_USERNAME = "patient"
DEMO_PATIENT_PASSWORD = "patient"


class DemoUserConfig(BaseModel):
    """Demo user profile configuration for sidebar and UI display."""

    full_name: str = "Sarah Chen"
    email: str = "sarah.chen@longevityclinic.com"
    phone: str = "+14087585046"  # Demo phone for call logs
    role: Literal["admin", "patient"] = "patient"

    # User IDs for seeding and auth
    patient_id: int = 1
    admin_id: int = 2

    @computed_field
    @property
    def initials(self) -> str:
        """Generate initials from full name."""
        parts = self.full_name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[-1][0]}".upper()
        return self.full_name[:2].upper() if self.full_name else "?"

    @computed_field
    @property
    def role_label(self) -> str:
        """Human-readable role label."""
        return "Administrator" if self.role == "admin" else "Patient"

    @computed_field
    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == "admin"


class GlassStyleConfig(BaseModel):
    """Glassmorphism UI style configuration.

    Apple Glass aesthetic with transparency, blur effects, and subtle gradients.
    These are legacy styles - prefer GlassStyles from styles/constants.py for new code.
    """

    bg_gradient: str = (
        "bg-[radial-gradient(circle_at_top_left,_var(--tw-gradient-stops))] "
        "from-blue-50/30 via-white to-emerald-50/30"
    )
    panel_style: str = (
        "bg-white/60 backdrop-blur-3xl border border-white/40 "
        "shadow-[0_8px_30px_rgb(0,0,0,0.04)] rounded-[2rem] "
        "hover:bg-white/80 transition-all duration-500"
    )
    header_style: str = (
        "bg-white/30 backdrop-blur-xl border-b border-white/20 "
        "sticky top-0 z-50 supports-[backdrop-filter]:bg-white/10"
    )
    sidebar_style: str = (
        "bg-white/20 backdrop-blur-2xl border-r border-white/20 "
        "supports-[backdrop-filter]:bg-white/10"
    )
    card_hover: str = (
        "hover:bg-white/80 hover:shadow-[0_20px_40px_rgb(0,0,0,0.06)] "
        "hover:-translate-y-1 transition-all duration-500 ease-out border-white/50"
    )
    input_style: str = (
        "bg-white/30 backdrop-blur-lg border border-white/40 "
        "focus:bg-white/60 focus:ring-2 focus:ring-emerald-500/5 "
        "focus:border-emerald-500/10 rounded-2xl placeholder-gray-400/60 "
        "transition-all duration-300 outline-none text-gray-700 "
        "font-light tracking-wide shadow-[inset_0_2px_4px_rgba(0,0,0,0.01)]"
    )
    button_primary: str = (
        "bg-emerald-500/80 hover:bg-emerald-500/90 text-white "
        "shadow-lg shadow-emerald-500/10 backdrop-blur-md border border-white/20 "
        "rounded-2xl transition-all duration-300 active:scale-[0.98] "
        "font-medium tracking-wide hover:shadow-emerald-500/20"
    )
    button_secondary: str = (
        "bg-white/40 hover:bg-white/70 text-gray-600 border border-white/40 "
        "shadow-sm backdrop-blur-md rounded-2xl transition-all duration-300 "
        "active:scale-[0.98] font-medium hover:text-gray-900"
    )


class AppConfig(BaseModel):
    """Main application configuration."""

    app_name: str = os.getenv("APP_NAME", "Vitality Clinic")
    clinic_name: str = os.getenv("CLINIC_NAME", "Vitality Health")
    admin_role_name: str = os.getenv("ADMIN_ROLE_NAME", "Administrator")
    patient_role_name: str = os.getenv("PATIENT_ROLE_NAME", "Patient")
    theme_color: str = os.getenv("THEME_COLOR", "emerald")

    # API Configuration
    openai_api_key: str = OPENAI_API_KEY
    call_api_token: str = CALL_API_TOKEN
    call_logs_api_base: str = (
        "https://directus-staging-ee94.up.railway.app/items/call_logs"
    )

    # VlogsAgent Configuration
    vlogs_process_with_llm: bool = True
    vlogs_llm_model: str = "gpt-4o-mini"
    vlogs_temperature: float = 0.3
    vlogs_fetch_limit: int = 50

    # Background processing configuration
    background_poll_interval: int = 15  # seconds between CDC processing cycles

    # Demo user for UI display
    demo_user: DemoUserConfig = DemoUserConfig()

    # Debug: reprocess all call logs regardless of processed_to_metrics status
    reprocess_call_logs_everytime: bool = False

    # Quick access patient count (admin dashboard)
    quick_access_patient_count: int = 5

    # Checkins pagination
    checkins_per_page: int = 10

    # Glass UI Styles (modularized)
    glass: GlassStyleConfig = GlassStyleConfig()

    # Legacy style properties (deprecated - use glass.* instead)
    # Note: glass_panel_style, glass_input_style, glass_button_secondary are still used
    @computed_field
    @property
    def glass_panel_style(self) -> str:
        return self.glass.panel_style

    @computed_field
    @property
    def glass_input_style(self) -> str:
        return self.glass.input_style

    @computed_field
    @property
    def glass_button_secondary(self) -> str:
        return self.glass.button_secondary


current_config = AppConfig()


# =============================================================================
# CDC Processing Configuration
# =============================================================================


class ProcessConfig(BaseModel):
    """Centralized CDC pipeline processing configuration."""

    model_config = {"arbitrary_types_allowed": True}

    # Polling/periodic settings
    poll_interval: int = Field(default=15, description="Seconds between poll cycles")
    refresh_interval: int = Field(
        default=30, description="Seconds for manual refresh periodic"
    )

    # Parallel processing
    max_parallel_llm: int = Field(default=3, description="Max concurrent LLM calls")
    max_parallel_db: int = Field(default=5, description="Max concurrent DB writes")

    # LLM settings
    llm_enabled: bool = Field(default=True)
    llm_model: str = Field(default="gpt-4o-mini")
    llm_temperature: float = Field(default=0.3)

    # Fetch limits
    fetch_limit: int = Field(default=50)
    checkins_limit: int = Field(default=200)

    # Ghost user ID for unknown phone numbers
    ghost_user_id: int = Field(
        default=-1, description="Fallback user_id for unmatched phones"
    )

    # Debug flags
    reprocess_all: bool = Field(default=False)
    verbose_logging: bool = Field(default=False)

    @classmethod
    def from_app(cls) -> "ProcessConfig":
        """Create from current_config defaults."""
        return cls(
            poll_interval=current_config.background_poll_interval,
            llm_enabled=current_config.vlogs_process_with_llm,
            llm_model=current_config.vlogs_llm_model,
            llm_temperature=current_config.vlogs_temperature,
            fetch_limit=current_config.vlogs_fetch_limit,
            reprocess_all=current_config.reprocess_call_logs_everytime,
        )


# Global process config instance
process_config = ProcessConfig.from_app()


class VlogsConfig(BaseModel):
    """Configuration for VlogsAgent (wraps ProcessConfig)."""

    model_config = {"arbitrary_types_allowed": True}

    extract_with_llm: bool = Field(default_factory=lambda: process_config.llm_enabled)
    llm_model: str = Field(default_factory=lambda: process_config.llm_model)
    temperature: float = Field(default_factory=lambda: process_config.llm_temperature)
    limit: int = Field(default_factory=lambda: process_config.fetch_limit)
    max_parallel: int = Field(default_factory=lambda: process_config.max_parallel_llm)
    output_schema: Any | None = None
    reprocess_all: bool = Field(default_factory=lambda: process_config.reprocess_all)
