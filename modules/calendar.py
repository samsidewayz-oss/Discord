"""
Google Calendar Module

Handles retrieval of calendar events for the current day.
"""

import logging
from datetime import datetime
from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class CalendarService:
    """Manages Google Calendar API interactions."""
    
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    
    def __init__(self, config):
        """Initialize calendar service with credentials.
        
        Args:
            config: Config object with Google credentials
        """
        self.config = config
        self._service = None
    
    @property
    def service(self):
        """Lazy-load and cache the Google Calendar service."""
        if self._service is None:
            creds = Credentials(
                token=None,
                refresh_token=self.config.google_refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.config.google_client_id,
                client_secret=self.config.google_client_secret,
                scopes=self.SCOPES
            )
            self._service = build("calendar", "v3", credentials=creds)
        return self._service
    
    def get_today_events(self) -> List[Dict[str, Any]]:
        """Retrieve calendar events for today.
        
        Returns:
            List of calendar event dictionaries
        """
        try:
            today = datetime.utcnow().date()
            start = datetime.combine(today, datetime.min.time()).isoformat() + "Z"
            end = datetime.combine(today, datetime.max.time()).isoformat() + "Z"
            
            events = self.service.events().list(
                calendarId="primary",
                timeMin=start,
                timeMax=end,
                singleEvents=True,
                orderBy="startTime"
            ).execute()
            
            items = events.get("items", [])
            logger.info(f"Retrieved {len(items)} calendar events for today")
            return items
            
        except Exception as e:
            logger.error(f"Error retrieving calendar events: {e}", exc_info=True)
            raise


def get_today_events(config) -> List[Dict[str, Any]]:
    """Get today's calendar events.
    
    Args:
        config: Config object with Google credentials
        
    Returns:
        List of calendar event dictionaries
    """
    service = CalendarService(config)
    return service.get_today_events()
