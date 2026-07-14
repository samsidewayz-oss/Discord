"""
Message Formatter Module

Formats the daily briefing message for Discord.
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def format_message(
    calendar_events: List[Dict[str, Any]],
    content_plan: Optional[Dict[str, Any]] = None,
    priority: Optional[str] = None
) -> str:
    """Format the daily briefing message.
    
    Args:
        calendar_events: List of calendar events
        content_plan: Optional content plan for the day
        priority: Optional priority recommendation
        
    Returns:
        Formatted message string for Discord
    """
    today = datetime.now().strftime("%A %d %B")
    message = f"☀️ **SIDEWAYZ Daily Assistant**\n\n📅 {today}\n\n"
    
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
