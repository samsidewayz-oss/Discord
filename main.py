"""
Sam Sidewayz Daily Assistant - Main Entry Point

This module orchestrates the daily briefing workflow:
1. Load and validate configuration
2. Retrieve today's calendar events
3. Get content recommendation for the day
4. Generate priority for today
5. Fetch weather information for Sydney and Melbourne
6. Format message
7. Send to Discord

Runs via GitHub Actions every morning at 7:45 AM EDT.
"""

import logging
import sys
from typing import Optional, List, Dict, Any

from config import load_config, ConfigError
from modules.calendar import get_today_events
from modules.content_calendar import get_content_plan
from modules.priority import get_priority
from modules.weather import get_weather
from modules.formatter import format_message
from modules.discord_sender import send, DiscordSendError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> int:
    """
    Main execution flow for the daily assistant.
    
    Returns:
        0 on success, 1 on failure
    """
    try:
        logger.info("Starting Sam Sidewayz Daily Assistant")
        
        # Load configuration
        config = load_config()
        
        # Get calendar events
        logger.info("Fetching today's calendar events")
        calendar_events = get_today_events(config)
        logger.info(f"Retrieved {len(calendar_events)} events")
        
        # Get content plan
        logger.info("Generating content plan for today")
        content_plan = get_content_plan()
        logger.info(f"Content plan: {content_plan['title']}")
        
        # Get priority
        logger.info("Generating priority recommendation")
        priority = get_priority(calendar_events)
        logger.info(f"Priority: {priority}")
        
        # Get weather for multiple locations
        logger.info("Fetching weather information")
        weather_data = {}
        for location_name, coords in config.weather_locations.items():
            weather = get_weather(
                location_name,
                coords["latitude"],
                coords["longitude"]
            )
            if weather:
                weather_data[location_name] = weather
                logger.info(f"Weather for {location_name}: {weather['temperature']}°C")
            else:
                logger.warning(f"Weather fetch failed for {location_name}")
        
        # Format message
        logger.info("Formatting Discord message")
        message = format_message(calendar_events, content_plan, priority, weather_data)
        
        # Send to Discord
        logger.info("Sending message to Discord")
        send(message, config)
        logger.info("Message sent successfully")
        
        logger.info("Daily assistant completed successfully")
        return 0
        
    except ConfigError as e:
        logger.error(f"Configuration error dumb ass: {e}")
        return 1
    except DiscordSendError as e:
        logger.error(f"Discord send error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
