"""
Message Formatter Module

Formats the daily briefing message for Discord.
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from modules.weather import weather_code_to_emoji, weather_code_to_description

logger = logging.getLogger(__name__)


def format_message(
    calendar_events: List[Dict[str, Any]],
    content_plan: Optional[Dict[str, Any]] = None,
    priority: Optional[str] = None,
    weather_data: Optional[Dict[str, Dict[str, Any]]] = None
) -> str:
    """Format the daily briefing message.
    
    Args:
        calendar_events: List of calendar events
        content_plan: Optional content plan for the day
        priority: Optional priority recommendation
        weather_data: Optional dictionary with weather for multiple locations
        
    Returns:
        Formatted message string for Discord
    """
    today = datetime.now().strftime("%A %d %B")
    message = f"☀️ **SIDEWAYZ Daily Assistant**\n\n📅 {today}\n\n"
    
    # Add weather for multiple locations if provided
    if weather_data:
        for location_name, weather in weather_data.items():
            temp = weather.get("temperature", "N/A")
            code = weather.get("weather_code")
            emoji = weather_code_to_emoji(code) if code is not None else "🌡️"
            description = weather_code_to_description(code) if code is not None else "Unknown"
            wind = weather.get("wind_speed", "N/A")
            message += f"{emoji} **{location_name}:** {temp}°C, {description} (Wind: {wind} km/h)\n"
        message += "\n"
    
    # Add priority if provided
    if priority:
        message += f"🎯 **Priority:** {priority}\n\n"
    
    # Add content plan if provided
    if content_plan:
        message += f"📝 **Content Plan:** {content_plan.get('title', 'N/A')}\n\n"
    
    # Add calendar events
    if not calendar_events:
        message += "No calendar events today. Clear schedule 🔥"
    else:
        message += "**Today's Schedule:**\n"
        for event in calendar_events:
            start = event["start"].get("dateTime", "All day")
            summary = event.get("summary", "Untitled")
            message += f"• {start} — {summary}\n"
    
    logger.debug(f"Formatted message ({len(message)} chars)")
    return message
