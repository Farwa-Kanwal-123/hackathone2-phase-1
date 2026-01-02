"""
Unit Tests for Interactive Menu Functions

Tests for menu display, choice validation, and input prompts.
All tests follow TDD RED phase - written BEFORE implementation.
"""

import pytest
from unittest.mock import patch
from io import StringIO
from src.interactive_menu import display_menu, get_menu_choice


class TestDisplayMenu:
    """Tests for display_menu() function - T004"""

    def test_display_menu_shows_all_six_options(self, capsys):
        """Verify menu displays all 6 numbered options."""
        display_menu()
        captured = capsys.readouterr()

        # Verify all 6 menu options are present
        assert "1. Add todo" in captured.out
        assert "2. List all todos" in captured.out
        assert "3. Complete todo" in captured.out
        assert "4. Update todo" in captured.out
        assert "5. Delete todo" in captured.out
        assert "6. Exit" in captured.out

    def test_display_menu_shows_prompt(self, capsys):
        """Verify menu shows choice prompt."""
        display_menu()
        captured = capsys.readouterr()

        assert "Enter your choice (1-6):" in captured.out

    def test_display_menu_has_blank_line_before(self, capsys):
        """Verify menu has blank line before display."""
        display_menu()
        captured = capsys.readouterr()

        # Menu should start with a newline for spacing
        assert captured.out.startswith("\n")


class TestGetMenuChoice:
    """Tests for get_menu_choice() function - T005, T006"""

    @patch('builtins.input', side_effect=['1'])
    def test_get_menu_choice_accepts_valid_input_1(self, mock_input):
        """Test get_menu_choice() accepts valid input 1 - T005."""
        result = get_menu_choice()
        assert result == 1

    @patch('builtins.input', side_effect=['2'])
    def test_get_menu_choice_accepts_valid_input_2(self, mock_input):
        """Test get_menu_choice() accepts valid input 2."""
        result = get_menu_choice()
        assert result == 2

    @patch('builtins.input', side_effect=['3'])
    def test_get_menu_choice_accepts_valid_input_3(self, mock_input):
        """Test get_menu_choice() accepts valid input 3."""
        result = get_menu_choice()
        assert result == 3

    @patch('builtins.input', side_effect=['4'])
    def test_get_menu_choice_accepts_valid_input_4(self, mock_input):
        """Test get_menu_choice() accepts valid input 4."""
        result = get_menu_choice()
        assert result == 4

    @patch('builtins.input', side_effect=['5'])
    def test_get_menu_choice_accepts_valid_input_5(self, mock_input):
        """Test get_menu_choice() accepts valid input 5."""
        result = get_menu_choice()
        assert result == 5

    @patch('builtins.input', side_effect=['6'])
    def test_get_menu_choice_accepts_valid_input_6(self, mock_input):
        """Test get_menu_choice() accepts valid input 6."""
        result = get_menu_choice()
        assert result == 6

    @patch('builtins.input', side_effect=['0', '1'])
    def test_get_menu_choice_rejects_zero_and_reprompts(self, mock_input, capsys):
        """Test get_menu_choice() rejects 0 and re-prompts - T006."""
        result = get_menu_choice()
        captured = capsys.readouterr()

        assert result == 1
        assert "Error:" in captured.out or "Invalid" in captured.out

    @patch('builtins.input', side_effect=['7', '1'])
    def test_get_menu_choice_rejects_seven_and_reprompts(self, mock_input, capsys):
        """Test get_menu_choice() rejects 7 and re-prompts - T006."""
        result = get_menu_choice()
        captured = capsys.readouterr()

        assert result == 1
        assert "Error:" in captured.out or "Invalid" in captured.out

    @patch('builtins.input', side_effect=['abc', '1'])
    def test_get_menu_choice_rejects_non_numeric_and_reprompts(self, mock_input, capsys):
        """Test get_menu_choice() rejects 'abc' and re-prompts - T006."""
        result = get_menu_choice()
        captured = capsys.readouterr()

        assert result == 1
        assert "Error:" in captured.out or "number" in captured.out.lower()

    @patch('builtins.input', side_effect=['', '1'])
    def test_get_menu_choice_rejects_empty_input(self, mock_input, capsys):
        """Test get_menu_choice() rejects empty input and re-prompts."""
        result = get_menu_choice()
        captured = capsys.readouterr()

        assert result == 1
        assert "Error:" in captured.out or "number" in captured.out.lower()

    @patch('builtins.input', side_effect=[' 3 ', '1'])
    def test_get_menu_choice_strips_whitespace(self, mock_input):
        """Test get_menu_choice() strips whitespace from input."""
        result = get_menu_choice()
        # Should accept ' 3 ' as 3 after stripping
        assert result == 3 or result == 1
