"""
Central configuration for the application.
"""
from pytz import timezone

# Database configuration
DATABASE_URL = "fitness.db"

# Timezone configuration for creating new classes
DEFAULT_TIMEZONE = timezone("Asia/Kolkata")