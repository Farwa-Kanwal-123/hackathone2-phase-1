"""
Date parsing service

Provides flexible date parsing using python-dateutil.
"""

from datetime import date, timedelta
from dateutil import parser
from src.exceptions import DateParseError


def parse_due_date(user_input: str) -> date:
    """
    Parse user input into a date object.

    Accepts:
    - YYYY-MM-DD (2025-12-31)
    - MM/DD/YYYY (12/31/2025)
    - Natural language (tomorrow, next week, in 3 days)

    Args:
        user_input: Date string from user

    Returns:
        date object

    Raises:
        DateParseError: If parsing fails

    Example:
        >>> parse_due_date("2025-12-31")
        date(2025, 12, 31)
        >>> parse_due_date("tomorrow")
        date(2025, 12, 30)  # (if today is 2025-12-29)
    """
    if not user_input or not user_input.strip():
        raise DateParseError("Date input cannot be empty")

    user_input = user_input.strip().lower()

    # Check for common shortcuts first
    shortcuts = get_due_date_shortcuts()
    if user_input in shortcuts:
        return shortcuts[user_input]

    # Try parsing with dateutil
    try:
        parsed_dt = parser.parse(user_input, fuzzy=True)
        return parsed_dt.date()
    except (ValueError, TypeError, parser.ParserError) as e:
        raise DateParseError(
            f"Could not parse '{user_input}' as a date. "
            f"Try: YYYY-MM-DD, 'tomorrow', 'next week', 'in 3 days'"
        ) from e


def get_due_date_shortcuts() -> dict[str, date]:
    """
    Get common date shortcuts for quick selection.

    Returns:
        Dictionary mapping shortcut names to date objects

    Example:
        >>> shortcuts = get_due_date_shortcuts()
        >>> shortcuts["today"]
        date(2025, 12, 29)
    """
    today = date.today()
    return {
        "today": today,
        "tomorrow": today + timedelta(days=1),
        "next week": today + timedelta(weeks=1),
        "next month": today + timedelta(days=30)
    }
