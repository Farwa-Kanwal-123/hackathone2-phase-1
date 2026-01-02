"""
Integration Tests for Interactive Menu Workflows

Tests for complete user workflows through the interactive menu.
All tests follow TDD RED phase - written BEFORE implementation.
"""

import pytest
from unittest.mock import patch
from src.storage import TodoStorage


class TestMenuLoopWorkflow:
    """Tests for main menu loop - T007"""

    @patch('builtins.input', side_effect=['2', '6'])
    @patch('main.interactive_list')
    def test_menu_loop_executes_action_and_returns_to_menu(
        self, mock_interactive_list, mock_input
    ):
        """Test menu loop: select action → execute → return to menu → exit.

        Flow: User selects '2' (list) → action executes → menu redisplays → user selects '6' (exit)
        """
        from main import main

        # This test verifies the loop behavior
        # Should not raise exception, should exit cleanly
        main()  # Should exit gracefully when user selects 6

        # Verify list action was called
        assert mock_interactive_list.call_count == 1

    @patch('builtins.input', side_effect=['1', '2', '3', '6'])
    @patch('main.interactive_add')
    @patch('main.interactive_list')
    @patch('main.interactive_complete')
    def test_menu_loop_handles_multiple_actions_before_exit(
        self, mock_complete, mock_list, mock_add, mock_input
    ):
        """Test menu loop handles multiple actions before exit.

        Flow: Add → List → Complete → Exit
        """
        from main import main

        main()

        # Verify all actions were called once
        assert mock_add.call_count == 1
        assert mock_list.call_count == 1
        assert mock_complete.call_count == 1


class TestExitWorkflow:
    """Tests for exit workflow - T008"""

    @patch('builtins.input', side_effect=['6'])
    def test_exit_option_displays_goodbye_message(self, mock_input, capsys):
        """Test selecting option 6 displays goodbye message and exits."""
        from main import main

        main()
        captured = capsys.readouterr()

        # Verify goodbye message is displayed
        assert "Goodbye" in captured.out
        # Verify mention of in-memory data loss
        assert "in-memory" in captured.out.lower() or "cleared" in captured.out.lower()

    @patch('builtins.input', side_effect=['6'])
    def test_exit_option_terminates_cleanly(self, mock_input):
        """Test selecting option 6 terminates without exception."""
        from main import main

        # Should not raise any exception
        main()


class TestCtrlCExitHandling:
    """Tests for Ctrl+C exit handling - T009"""

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_ctrl_c_displays_goodbye_message(self, mock_input, capsys):
        """Test Ctrl+C displays goodbye message before exit."""
        from main import main

        main()
        captured = capsys.readouterr()

        # Verify goodbye message is displayed
        assert "Goodbye" in captured.out

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_ctrl_c_exits_cleanly_without_traceback(self, mock_input, capsys):
        """Test Ctrl+C exits without showing traceback."""
        from main import main

        main()
        captured = capsys.readouterr()

        # Should not show traceback
        assert "Traceback" not in captured.out
        assert "KeyboardInterrupt" not in captured.out

    @patch('builtins.input', side_effect=['2', KeyboardInterrupt()])
    @patch('main.interactive_list')
    def test_ctrl_c_during_menu_selection_exits_gracefully(
        self, mock_list, mock_input, capsys
    ):
        """Test Ctrl+C during menu selection exits gracefully after action."""
        from main import main

        main()
        captured = capsys.readouterr()

        # Verify goodbye message is displayed
        assert "Goodbye" in captured.out
        # Verify list was called before interrupt
        assert mock_list.call_count == 1
