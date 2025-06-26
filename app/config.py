"""Application configuration management using Pydantic Settings.

This module provides centralized configuration management with environment
variable support and validation. All application settings are defined here
with sensible defaults and can be overridden via environment variables.
"""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support.

    Centralizes all application configuration with automatic environment variable
    loading and validation. Settings can be overridden using environment variables
    with the SHORTGIC_ prefix (e.g., SHORTGIC_DATABASE_PATH).

    Attributes:
        database_path: Path to the SQLite database file.
        app_name: Application name for branding and logging.
        debug: Enable debug mode for development.
        link_length: Length of generated short link identifiers.
        max_url_length: Maximum allowed length for target URLs.
    """

    # Database configuration
    database_path: str = "./shortgic.db"

    # Application configuration
    app_name: str = "ShortGic"
    debug: bool = False

    # Link generation configuration
    link_length: int = 5

    # URL validation
    max_url_length: int = 2048

    model_config = ConfigDict(env_file=".env", env_prefix="SHORTGIC_")


settings = Settings()
