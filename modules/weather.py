"""
Weather Module

Fetches weather information for the current day.
"""

import logging
import requests
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class WeatherError(Exception):
    """Raised when weather fetch fails."""
    pass


def get_weather(location_name: str, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """Fetch current weather data using Open-Meteo API (no API key required).
    
    Args:
        location_name: Name of the location (for logging)
        latitude: Location latitude
        longitude: Location longitude
        
    Returns:
        Dictionary with weather information or None if fetch fails
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        current = data.get("current", {})
        
        weather_info = {
            "location": location_name,
            "temperature": current.get("temperature_2m"),
            "weather_code": current.get("weather_code"),
            "wind_speed": current.get("wind_speed_10m"),
            "timezone": data.get("timezone")
        }
        
        logger.info(f"Weather fetched for {location_name}: {weather_info['temperature']}°C")
        return weather_info
        
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to fetch weather for {location_name}: {e}")
        return None
    except Exception as e:
        logger.warning(f"Error processing weather data for {location_name}: {e}")
        return None


def weather_code_to_emoji(code: int) -> str:
    """Convert WMO weather code to emoji.
    
    Args:
        code: WMO weather code
        
    Returns:
        Appropriate emoji for weather condition
    """
    # WMO Weather interpretation codes
    if code == 0:
        return "☀️"  # Clear sky
    elif code == 1 or code == 2:
        return "🌤️"  # Mainly clear
    elif code == 3:
        return "☁️"  # Overcast
    elif code == 45 or code == 48:
        return "🌫️"  # Foggy
    elif code in [51, 53, 55, 61, 63, 65]:
        return "🌧️"  # Drizzle or rain
    elif code in [71, 73, 75, 77]:
        return "❄️"  # Snow
    elif code in [80, 81, 82]:
        return "⛈️"  # Rain showers
    elif code in [85, 86]:
        return "🌨️"  # Snow showers
    elif code in [95, 96, 99]:
        return "⚡"  # Thunderstorm
    else:
        return "🌡️"  # Default


def weather_code_to_description(code: int) -> str:
    """Convert WMO weather code to description.
    
    Args:
        code: WMO weather code
        
    Returns:
        Human-readable weather description
    """
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return descriptions.get(code, "Unknown")
