"""
Configuration Management

Handles environment variable validation and configuration loading.
"""

import os
import sys
import logging

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


class Config:
    """Application configuration from environment variables."""
    
    REQUIRED_VARS = {
        'GOOGLE_REFRESH_TOKEN': 'Google Refresh Token',
        'GOOGLE_CLIENT_ID': 'Google Client ID',
        'GOOGLE_CLIENT_SECRET': 'Google Client Secret',
        'DISCORD_WEBHOOK': 'Discord Webhook URL'
    }
    
    def __init__(self):
        self.google_refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN')
        self.google_client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.discord_webhook = os.getenv('DISCORD_WEBHOOK')
    
    def validate(self) -> bool:
        """Validate that all required environment variables are set.
        
        Returns:
            True if valid, raises ConfigError if invalid
            
        Raises:
            ConfigError: If required variables are missing or invalid
        """
        missing = [name for name in self.REQUIRED_VARS.keys() if not os.getenv(name)]
        if missing:
            raise ConfigError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
        
        if not self.discord_webhook.startswith('https://'):
            raise ConfigError(
                "DISCORD_WEBHOOK must be a valid HTTPS URL"
            )
        
        logger.info("Configuration validated successfully")
        return True


def load_config() -> Config:
    """Load and validate configuration.
    
    Returns:
        Config object with validated settings
        
    Raises:
        ConfigError: If configuration is invalid
    """
    try:
        config = Config()
        config.validate()
        return config
    except ConfigError as e:
        logger.error(f"Configuration error: {e}")
        raise
