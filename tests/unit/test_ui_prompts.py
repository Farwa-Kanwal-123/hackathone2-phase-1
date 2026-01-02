"""
Unit tests for UI prompts module

Tests cover prompt_task_selection(), prompt_priority_selection(),
and prompt_confirmation() using questionary.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.storage import TodoStorage
from src.todo import TodoItem


# Note: These tests will be implemented when src/ui/prompts.py is created
class TestPromptTaskSelection:
    """Test task selection prompt with arrow key navigation"""

    def setup_method(self):
        """Set up test storage with todos"""
        self.storage = TodoStorage()
        self.storage.add("Task 1")
        self.storage.add("Task 2")
        self.storage.add("Task 3")

    @patch('questionary.select')
    def test_prompt_task_selection_returns_selected_id(self, mock_select):
        """Should return the ID of the selected task"""
        # Import will happen after implementation
        from src.ui.prompts import prompt_task_selection

        # Mock questionary.select to return "1. Task 1"
        mock_question = MagicMock()
        mock_question.ask.return_value = "1. Task 1"
        mock_select.return_value = mock_question

        todos = self.storage.list_all()
        result = prompt_task_selection(todos, "Select a task")

        assert result == 1
        mock_select.assert_called_once()

    @patch('questionary.select')
    def test_prompt_task_selection_with_empty_list(self, mock_select):
        """Should return None when todo list is empty"""
        from src.ui.prompts import prompt_task_selection

        result = prompt_task_selection([], "Select a task")

        assert result is None
        mock_select.assert_not_called()

    @patch('questionary.select')
    def test_prompt_task_selection_formats_choices(self, mock_select):
        """Should format todo choices with ID and title"""
        from src.ui.prompts import prompt_task_selection

        mock_question = MagicMock()
        mock_question.ask.return_value = "2. Task 2"
        mock_select.return_value = mock_question

        todos = self.storage.list_all()
        result = prompt_task_selection(todos, "Select a task")

        # Verify questionary.select was called with formatted choices
        call_args = mock_select.call_args
        choices = call_args[1]['choices']
        assert "1. Task 1" in choices
        assert "2. Task 2" in choices
        assert "3. Task 3" in choices

    @patch('questionary.select')
    def test_prompt_task_selection_cancellation(self, mock_select):
        """Should return None when user cancels (Esc)"""
        from src.ui.prompts import prompt_task_selection

        # Mock Esc key press (returns None)
        mock_question = MagicMock()
        mock_question.ask.return_value = None
        mock_select.return_value = mock_question

        todos = self.storage.list_all()
        result = prompt_task_selection(todos, "Select a task")

        assert result is None

    @patch('questionary.select')
    def test_prompt_task_selection_with_completed_todos(self, mock_select):
        """Should display completed todos with strikethrough"""
        from src.ui.prompts import prompt_task_selection

        self.storage.complete(2)  # Complete Task 2

        mock_question = MagicMock()
        mock_question.ask.return_value = "2. Task 2"
        mock_select.return_value = mock_question

        todos = self.storage.list_all()
        result = prompt_task_selection(todos, "Select a task")

        assert result == 2


class TestPromptPrioritySelection:
    """Test priority selection prompt"""

    @patch('questionary.select')
    def test_prompt_priority_selection_high(self, mock_select):
        """Should return 'High' when High is selected"""
        from src.ui.prompts import prompt_priority_selection

        mock_question = MagicMock()
        mock_question.ask.return_value = "High"
        mock_select.return_value = mock_question

        result = prompt_priority_selection()

        assert result == "High"
        mock_select.assert_called_once()

    @patch('questionary.select')
    def test_prompt_priority_selection_medium(self, mock_select):
        """Should return 'Medium' when Medium is selected"""
        from src.ui.prompts import prompt_priority_selection

        mock_question = MagicMock()
        mock_question.ask.return_value = "Medium"
        mock_select.return_value = mock_question

        result = prompt_priority_selection()

        assert result == "Medium"

    @patch('questionary.select')
    def test_prompt_priority_selection_low(self, mock_select):
        """Should return 'Low' when Low is selected"""
        from src.ui.prompts import prompt_priority_selection

        mock_question = MagicMock()
        mock_question.ask.return_value = "Low"
        mock_select.return_value = mock_question

        result = prompt_priority_selection()

        assert result == "Low"

    @patch('questionary.select')
    def test_prompt_priority_selection_none(self, mock_select):
        """Should return None when 'None (no priority)' is selected"""
        from src.ui.prompts import prompt_priority_selection

        mock_question = MagicMock()
        mock_question.ask.return_value = "None (no priority)"
        mock_select.return_value = mock_question

        result = prompt_priority_selection()

        assert result is None

    @patch('questionary.select')
    def test_prompt_priority_selection_cancellation(self, mock_select):
        """Should return None when user cancels (Esc)"""
        from src.ui.prompts import prompt_priority_selection

        mock_question = MagicMock()
        mock_question.ask.return_value = None
        mock_select.return_value = mock_question

        result = prompt_priority_selection()

        assert result is None

    @patch('questionary.select')
    def test_prompt_priority_selection_choices(self, mock_select):
        """Should present all priority options"""
        from src.ui.prompts import prompt_priority_selection

        mock_question = MagicMock()
        mock_question.ask.return_value = "Medium"
        mock_select.return_value = mock_question

        result = prompt_priority_selection()

        # Verify questionary.select was called with correct choices
        call_args = mock_select.call_args
        choices = call_args[1]['choices']
        assert "High" in choices
        assert "Medium" in choices
        assert "Low" in choices
        assert "None (no priority)" in choices


class TestPromptConfirmation:
    """Test confirmation prompt"""

    @patch('questionary.confirm')
    def test_prompt_confirmation_yes(self, mock_confirm):
        """Should return True when user confirms"""
        from src.ui.prompts import prompt_confirmation

        mock_question = MagicMock()
        mock_question.ask.return_value = True
        mock_confirm.return_value = mock_question

        result = prompt_confirmation("Are you sure?")

        assert result is True
        mock_confirm.assert_called_once_with("Are you sure?")

    @patch('questionary.confirm')
    def test_prompt_confirmation_no(self, mock_confirm):
        """Should return False when user declines"""
        from src.ui.prompts import prompt_confirmation

        mock_question = MagicMock()
        mock_question.ask.return_value = False
        mock_confirm.return_value = mock_question

        result = prompt_confirmation("Delete this task?")

        assert result is False

    @patch('questionary.confirm')
    def test_prompt_confirmation_cancellation(self, mock_confirm):
        """Should return False when user cancels (Esc)"""
        from src.ui.prompts import prompt_confirmation

        mock_question = MagicMock()
        mock_question.ask.return_value = None
        mock_confirm.return_value = mock_question

        result = prompt_confirmation("Continue?")

        assert result is False


class TestPromptTextInput:
    """Test text input prompt"""

    @patch('questionary.text')
    def test_prompt_text_input_valid(self, mock_text):
        """Should return user input text"""
        from src.ui.prompts import prompt_text_input

        mock_question = MagicMock()
        mock_question.ask.return_value = "New task title"
        mock_text.return_value = mock_question

        result = prompt_text_input("Enter title")

        assert result == "New task title"
        mock_text.assert_called_once_with("Enter title")

    @patch('questionary.text')
    def test_prompt_text_input_empty(self, mock_text):
        """Should return empty string when user provides no input"""
        from src.ui.prompts import prompt_text_input

        mock_question = MagicMock()
        mock_question.ask.return_value = ""
        mock_text.return_value = mock_question

        result = prompt_text_input("Enter title")

        assert result == ""

    @patch('questionary.text')
    def test_prompt_text_input_cancellation(self, mock_text):
        """Should return None when user cancels (Esc)"""
        from src.ui.prompts import prompt_text_input

        mock_question = MagicMock()
        mock_question.ask.return_value = None
        mock_text.return_value = mock_question

        result = prompt_text_input("Enter title")

        assert result is None
