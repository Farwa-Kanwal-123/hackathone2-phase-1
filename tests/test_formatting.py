"""
Unit tests for UI formatting helpers

Tests cover priority formatting, due date formatting, status display,
and text truncation utilities.
"""

import pytest
from datetime import date, timedelta
from src.ui.formatting import (
    format_priority,
    format_due_date,
    get_due_date_status,
    days_until_due,
    truncate_text,
    PRIORITY_COLORS,
    STATUS_ICONS,
    DUE_DATE_COLORS
)


class TestFormatPriority:
    """Test priority color formatting with Rich markup"""

    def test_format_priority_high(self):
        """High priority should be formatted with red color"""
        result = format_priority("High")
        assert result == "[red]High[/red]"

    def test_format_priority_medium(self):
        """Medium priority should be formatted with yellow color"""
        result = format_priority("Medium")
        assert result == "[yellow]Medium[/yellow]"

    def test_format_priority_low(self):
        """Low priority should be formatted with green color"""
        result = format_priority("Low")
        assert result == "[green]Low[/green]"

    def test_format_priority_none(self):
        """None priority should be formatted with dim dash"""
        result = format_priority(None)
        assert result == "[dim]-[/dim]"

    def test_format_priority_invalid(self):
        """Invalid priority should default to white"""
        result = format_priority("Invalid")
        assert result == "[white]Invalid[/white]"


class TestFormatDueDate:
    """Test due date formatting with color coding"""

    def test_format_due_date_overdue(self):
        """Overdue dates should be formatted in red"""
        yesterday = date.today() - timedelta(days=1)
        text, color = format_due_date(yesterday)
        assert text == yesterday.isoformat()
        assert color == "red"

    def test_format_due_date_today(self):
        """Today's date should be formatted in orange with 'Today' text"""
        today = date.today()
        text, color = format_due_date(today)
        assert text == "Today"
        assert color == "#FFA500"  # Orange

    def test_format_due_date_upcoming(self):
        """Future dates should be formatted in white"""
        tomorrow = date.today() + timedelta(days=1)
        text, color = format_due_date(tomorrow)
        assert text == tomorrow.isoformat()
        assert color == "white"

    def test_format_due_date_none(self):
        """None due date should show dash in dim color"""
        text, color = format_due_date(None)
        assert text == "-"
        assert color == "dim"


class TestGetDueDateStatus:
    """Test due date status categorization"""

    def test_get_due_date_status_overdue(self):
        """Overdue dates should return 'overdue' status"""
        yesterday = date.today() - timedelta(days=1)
        status = get_due_date_status(yesterday)
        assert status == "overdue"

    def test_get_due_date_status_today(self):
        """Today's date should return 'today' status"""
        today = date.today()
        status = get_due_date_status(today)
        assert status == "today"

    def test_get_due_date_status_upcoming(self):
        """Future dates should return 'upcoming' status"""
        tomorrow = date.today() + timedelta(days=1)
        status = get_due_date_status(tomorrow)
        assert status == "upcoming"

    def test_get_due_date_status_none(self):
        """None due date should return 'no_date' status"""
        status = get_due_date_status(None)
        assert status == "no_date"


class TestDaysUntilDue:
    """Test days until due calculation"""

    def test_days_until_due_overdue(self):
        """Overdue dates should return negative days"""
        yesterday = date.today() - timedelta(days=1)
        days = days_until_due(yesterday)
        assert days == -1

    def test_days_until_due_today(self):
        """Today's date should return 0 days"""
        today = date.today()
        days = days_until_due(today)
        assert days == 0

    def test_days_until_due_upcoming(self):
        """Future dates should return positive days"""
        next_week = date.today() + timedelta(days=7)
        days = days_until_due(next_week)
        assert days == 7

    def test_days_until_due_none(self):
        """None due date should return None"""
        days = days_until_due(None)
        assert days is None


class TestTruncateText:
    """Test text truncation utility"""

    def test_truncate_text_short(self):
        """Short text should not be truncated"""
        result = truncate_text("Hello", 10)
        assert result == "Hello"

    def test_truncate_text_exact_length(self):
        """Text exactly at max_length should not be truncated"""
        result = truncate_text("Hello", 5)
        assert result == "Hello"

    def test_truncate_text_long(self):
        """Long text should be truncated with ellipsis"""
        result = truncate_text("Hello World", 8)
        assert result == "Hello..."
        assert len(result) == 8

    def test_truncate_text_very_long(self):
        """Very long text should be truncated properly"""
        long_text = "This is a very long todo item that needs truncation"
        result = truncate_text(long_text, 20)
        assert result == "This is a very lo..."
        assert len(result) == 20

    def test_truncate_text_edge_case_small_max(self):
        """Max length smaller than ellipsis should still work"""
        result = truncate_text("Hello", 3)
        assert result == "..."
        assert len(result) == 3


class TestConstants:
    """Test that color constants are properly defined"""

    def test_priority_colors_defined(self):
        """PRIORITY_COLORS should have all priority levels"""
        assert "High" in PRIORITY_COLORS
        assert "Medium" in PRIORITY_COLORS
        assert "Low" in PRIORITY_COLORS
        assert None in PRIORITY_COLORS

    def test_status_icons_defined(self):
        """STATUS_ICONS should have completed and incomplete"""
        assert True in STATUS_ICONS
        assert False in STATUS_ICONS

    def test_due_date_colors_defined(self):
        """DUE_DATE_COLORS should have all status types"""
        assert "overdue" in DUE_DATE_COLORS
        assert "today" in DUE_DATE_COLORS
        assert "upcoming" in DUE_DATE_COLORS
        assert "no_date" in DUE_DATE_COLORS
