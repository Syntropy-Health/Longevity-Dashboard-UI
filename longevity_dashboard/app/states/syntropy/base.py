"""Base state with admin configuration loading capabilities."""

import logging
from typing import Any, Dict, Optional

import reflex as rx
from sqlmodel import select

from ...data.schemas.db.syntropy import AdminConfig

logger = logging.getLogger(__name__)


class ConfigurableState(rx.State, mixin=True):
    """Base state mixin that can load configuration from AdminConfig.

    This is a mixin that provides configuration loading capabilities
    to any state that inherits from it. Mark with mixin=True to indicate
    it should not be instantiated directly.
    """

    _config_loaded: bool = False
    _admin_config: Optional[Dict[str, Any]] = None

    @rx.event
    async def load_admin_config(self, config_name: str = "syntropy_config") -> Optional[Dict[str, Any]]:
        """Load admin configuration from database.

        Args:
            config_name: Name of the configuration to load (defaults to "syntropy_config")

        Returns:
            Configuration dictionary if found, None otherwise
        """
        try:
            with rx.session() as session:
                try:
                    stmt = select(AdminConfig).where(
                        AdminConfig.name == config_name,
                        AdminConfig.is_latest == True
                    )
                    config = session.exec(stmt).first()

                    if config and config.configuration:
                        self._admin_config = config.configuration
                        self._config_loaded = True
                        logger.info("Loaded admin config '%s' v%s", config_name, config.version)
                        return config.configuration
                except (AttributeError, ValueError, TypeError):
                    logger.debug("is_latest column not available, using fallback")

                stmt = select(AdminConfig).where(
                    AdminConfig.name == config_name
                )
                configs = session.exec(stmt).all()

                if configs:
                    latest_config = max(configs, key=lambda c: c.version)
                    if latest_config.configuration:
                        self._admin_config = latest_config.configuration
                        self._config_loaded = True
                        logger.info("Loaded admin config '%s' v%s", config_name, latest_config.version)
                        return latest_config.configuration

                logger.warning("Admin config '%s' not found", config_name)
                return None

        except (AttributeError, ValueError, TypeError) as e:
            logger.error("Error loading admin config: %s", e)
            return None

    def get_config_value(self, path: str, default: Any = None) -> Any:
        """Get a configuration value by dot-notation path.

        Args:
            path: Dot-notation path to the config value (e.g., "syntropy.landing.logo_tagline")
            default: Default value if path not found

        Returns:
            Configuration value or default
        """
        if not self._admin_config:
            return default

        try:
            value = self._admin_config
            for key in path.split('.'):
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
