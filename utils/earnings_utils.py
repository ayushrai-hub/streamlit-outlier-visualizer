"""
Utility functions for earnings analysis and formatting.
"""
import re

def parse_duration(duration_str):
    """Parse a duration string (e.g., '1h 30m 20s') to total seconds."""
    if duration_str == '-':
        return 0
    total_seconds = 0
    parts = re.findall(r'(\d+)([hms])', duration_str)
    for value, unit in parts:
        value = int(value)
        if unit == 'h':
            total_seconds += value * 3600
        elif unit == 'm':
            total_seconds += value * 60
        elif unit == 's':
            total_seconds += value
    return total_seconds

def format_seconds(seconds):
    """Format seconds into 'HHh MMm SSs' string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}h {minutes:02d}m {secs:02d}s"
