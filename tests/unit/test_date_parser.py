"""
Unit tests for date parsing service

Tests parse_due_date() and get_due_date_shortcuts() functions.
"""

import pytest
from datetime import date, timedelta
from src.services.date_parser import parse_due_date, get_due_date_shortcuts, DateParseError


class TestParseDueDate:
    """Test parse_due_date() with various formats"""

    def test_parse_iso_format(self):
        """Should parse ISO format YYYY-MM-DD"""
        result = parse_due_date("2025-12-31")
        assert result == date(2025, 12, 31)

    def test_parse_us_format(self):
        """Should parse US format MM/DD/YYYY"""
        result = parse_due_date("12/31/2025")
        assert result == date(2025, 12, 31)

    def test_parse_shortcut_today(self):
        """Should parse 'today' shortcut"""
        result = parse_due_date("today")
        assert result == date.today()

    def test_parse_shortcut_tomorrow(self):
        """Should parse 'tomorrow' shortcut"""
        result = parse_due_date("tomorrow")
        assert result == date.today() + timedelta(days=1)

    def test_parse_shortcut_next_week(self):
        """Should parse 'next week' shortcut"""
        result = parse_due_date("next week")
        assert result == date.today() + timedelta(weeks=1)

    def test_parse_shortcut_next_month(self):
        """Should parse 'next month' shortcut"""
        result = parse_due_date("next month")
        assert result == date.today() + timedelta(days=30)

    def test_parse_relative_in_3_days(self):
        """Should parse relative date 'in 3 days'"""
        result = parse_due_date("in 3 days")
        # dateutil should handle this
        assert isinstance(result, date)

    def test_parse_case_insensitive(self):
        """Should handle uppercase input"""
        result = parse_due_date("TOMORROW")
        assert result == date.today() + timedelta(days=1)

    def test_parse_with_whitespace(self):
        """Should handle leading/trailing whitespace"""
        result = parse_due_date("  tomorrow  ")
        assert result == date.today() + timedelta(days=1)

    def test_parse_empty_string_raises_error(self):
        """Should raise DateParseError for empty string"""
        with pytest.raises(DateParseError, match="cannot be empty"):
            parse_due_date("")

    def test_parse_whitespace_only_raises_error(self):
        """Should raise DateParseError for whitespace-only string"""
        with pytest.raises(DateParseError, match="cannot be empty"):
            parse_due_date("   ")

    def test_parse_invalid_format_raises_error(self):
        """Should raise DateParseError for invalid format"""
        with pytest.raises(DateParseError, match="Could not parse"):
            parse_due_date("not-a-date-123xyz")

    def test_parse_none_raises_error(self):
        """Should raise DateParseError for None input"""
        with pytest.raises((DateParseError, TypeError)):
            parse_due_date(None)

    def test_parse_gibberish_raises_error(self):
        """Should raise DateParseError for complete gibberish"""
        # Use nonsense that dateutil cannot interpret
        with pytest.raises(DateParseError):
            parse_due_date("xyzabc nonsense")


class TestGetDueDateShortcuts:
    """Test get_due_date_shortcuts() helper"""

    def test_shortcuts_returns_dict(self):
        """Should return a dictionary"""
        shortcuts = get_due_date_shortcuts()
        assert isinstance(shortcuts, dict)

    def test_shortcuts_has_today(self):
        """Should include 'today' key"""
        shortcuts = get_due_date_shortcuts()
        assert "today" in shortcuts
        assert shortcuts["today"] == date.today()

    def test_shortcuts_has_tomorrow(self):
        """Should include 'tomorrow' key"""
        shortcuts = get_due_date_shortcuts()
        assert "tomorrow" in shortcuts
        assert shortcuts["tomorrow"] == date.today() + timedelta(days=1)

    def test_shortcuts_has_next_week(self):
        """Should include 'next week' key"""
        shortcuts = get_due_date_shortcuts()
        assert "next week" in shortcuts
        assert shortcuts["next week"] == date.today() + timedelta(weeks=1)

    def test_shortcuts_has_next_month(self):
        """Should include 'next month' key"""
        shortcuts = get_due_date_shortcuts()
        assert "next month" in shortcuts
        assert shortcuts["next month"] == date.today() + timedelta(days=30)

    def test_shortcuts_all_are_dates(self):
        """All values should be date objects"""
        shortcuts = get_due_date_shortcuts()
        for value in shortcuts.values():
            assert isinstance(value, date)
