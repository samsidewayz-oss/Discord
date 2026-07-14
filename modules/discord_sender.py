"""
Discord Sender Module

Handles sending messages to Discord via webhook.
"""

import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)


class DiscordSendError(Exception):
    """Raised when Discord message sending fails."""
    pass


def send(message: str, config) -> bool:
    """Send a message to Discord webhook.
    
    Args:
        message: The message content to send
        config: Config object with Discord webhook URL
        
    Returns:
        True if message sent successfully
        
    Raises:
        DiscordSendError: If message sending fails
    """
    try:
        logger.debug(f"Sending message to Discord: {message[:100]}...")
        
        response = requests.post(
            config.discord_webhook,
            json={"content": message}
        )
        response.raise_for_status()
        
        logger.info("Message sent to Discord successfully")
        return True
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to send Discord message: {e}"
        logger.error(error_msg, exc_info=True)
        raise DiscordSendError(error_msg) from e
