"""
Utility functions, such as timezone conversion.
"""
from datetime import datetime
import pytz

def convert_to_timezone(dt_str: str, target_tz_str: str) -> datetime:
    """
    Converts a datetime string (expected in ISO format with timezone)
    to a target timezone.
    """
    try:
        target_tz = pytz.timezone(target_tz_str)
    except pytz.UnknownTimeZoneError:
        # Default to UTC if the provided timezone is invalid
        target_tz = pytz.utc

    
    source_dt_aware = datetime.fromisoformat(dt_str)

    return source_dt_aware.astimezone(target_tz)