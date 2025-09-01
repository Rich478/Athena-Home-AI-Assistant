"""
Utility functions for managing real-time context information.
This module provides functions to get current time, date, and location information.
"""

from datetime import datetime
import requests
import json
from typing import Dict, Any

def get_current_time_and_date() -> Dict[str, Any]:
    """Get current time and date in a user-friendly format with contextual information."""
    now = datetime.now()
    
    return {
        "current_date": now.strftime("%A, %B %d, %Y"),
        "current_time": now.strftime("%I:%M %p"),
        "timezone": "Local Time",
        "day_of_week": now.strftime("%A"),
        "month": now.strftime("%B"),
        "year": now.strftime("%Y"),
        "is_weekend": now.weekday() >= 5,
        "is_weekday": now.weekday() < 5,
        "hour": now.hour,
        "is_morning": 5 <= now.hour < 12,
        "is_afternoon": 12 <= now.hour < 17,
        "is_evening": 17 <= now.hour < 21,
        "is_night": now.hour >= 21 or now.hour < 5,
        "is_holiday_season": _is_holiday_season(now),
        "season": _get_season(now),
        "is_school_year": _is_school_year(now)
    }

def get_location_context() -> Dict[str, Any]:
    """Get location information (IP-based, can be enhanced with user input)."""
    try:
        # Get location from IP address (basic implementation)
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get('city', 'Unknown'),
                "region": data.get('region', 'Unknown'),
                "country": data.get('country_name', 'Unknown'),
                "timezone": data.get('timezone', 'Unknown'),
                "latitude": data.get('latitude'),
                "longitude": data.get('longitude'),
                "detected": True
            }
    except Exception as e:
        print(f"[WARNING] Location detection failed: {e}")
    
    # Fallback if location detection fails
    return {
        "city": "Unknown",
        "region": "Unknown", 
        "country": "Unknown",
        "timezone": "Unknown",
        "latitude": None,
        "longitude": None,
        "detected": False
    }

def _is_holiday_season(date: datetime) -> bool:
    """Check if current date is during holiday season."""
    month = date.month
    day = date.day
    
    # Thanksgiving (4th Thursday in November) to New Year's
    if month == 11 and day >= 22:  # Approximate Thanksgiving
        return True
    elif month == 12:
        return True
    elif month == 1 and day <= 7:  # New Year's week
        return True
    
    return False

def _get_season(date: datetime) -> str:
    """Get the current season based on date."""
    month = date.month
    
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

def _is_school_year(date: datetime) -> bool:
    """Check if current date is during typical school year."""
    month = date.month
    
    # School year typically runs from September to June
    if month in [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]:
        return True
    else:
        return False

def create_context_summary() -> str:
    """Create a human-readable summary of current context."""
    time_info = get_current_time_and_date()
    location_info = get_location_context()
    
    summary = f"📅 {time_info['current_date']} at {time_info['current_time']}"
    summary += f"\n📍 {location_info['city']}, {location_info['region']}"
    summary += f"\n🌤️  {time_info['season']} season"
    
    if time_info['is_weekend']:
        summary += "\n🎉 Weekend - perfect for family activities!"
    else:
        summary += "\n📚 Weekday - time for school and work routines"
    
    if time_info['is_holiday_season']:
        summary += "\n🎄 Holiday season - special family time!"
    
    return summary

def get_context_aware_suggestions() -> Dict[str, list]:
    """Get context-aware activity suggestions based on current time and day."""
    time_info = get_current_time_and_date()
    
    suggestions = {
        "morning": [
            "Family breakfast planning",
            "School/work preparation",
            "Morning exercise routines",
            "Daily schedule review"
        ],
        "afternoon": [
            "Lunch planning",
            "After-school activities",
            "Homework time",
            "Family check-in"
        ],
        "evening": [
            "Dinner planning and preparation",
            "Family dinner time",
            "Evening activities",
            "Bedtime routines"
        ],
        "weekend": [
            "Family outings",
            "Relaxation activities",
            "Household projects",
            "Quality family time"
        ],
        "weekday": [
            "School/work routines",
            "Structured activities",
            "Homework and study time",
            "Family dinner planning"
        ]
    }
    
    # Return relevant suggestions based on current context
    relevant_suggestions = []
    
    if time_info['is_morning']:
        relevant_suggestions.extend(suggestions['morning'])
    elif time_info['is_afternoon']:
        relevant_suggestions.extend(suggestions['afternoon'])
    elif time_info['is_evening']:
        relevant_suggestions.extend(suggestions['evening'])
    
    if time_info['is_weekend']:
        relevant_suggestions.extend(suggestions['weekend'])
    else:
        relevant_suggestions.extend(suggestions['weekday'])
    
    return {
        "current_time_suggestions": relevant_suggestions[:4],  # Top 4 suggestions
        "all_suggestions": suggestions
    }
