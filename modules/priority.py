"""
Priority Module

Generates priority recommendations based on calendar events.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def get_priority(calendar_events: List[Dict[str, Any]]) -> str:
    """Generate a priority recommendation based on calendar events.
    
    Args:
        calendar_events: List of calendar events for today
        
    Returns:
        Priority recommendation string
    """
    if not calendar_events:
        priority = "🟢 Low - Clear day, focus on deep work"
    elif len(calendar_events) <= 2:
        priority = "🟡 Medium - Some meetings, maintain flexibility"
    else:
        priority = "🔴 High - Busy day, prioritize ruthlessly"
    
    logger.info(f"Generated priority: {priority}")
    return priority
