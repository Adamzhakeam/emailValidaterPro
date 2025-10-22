"""
Utility module for date and time operations
Replacement for kisa_utils dependency
"""

from datetime import datetime


class DateUtils:
    """Date utility functions"""
    
    @staticmethod
    def currentTimestamp():
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()


# Create a dates instance for backward compatibility
dates = DateUtils()


