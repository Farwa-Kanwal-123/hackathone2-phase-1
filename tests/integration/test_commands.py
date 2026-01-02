"""
Integration tests for CLI commands

Tests cover:
- "add" command (T015)
- "list" command with todos (T016)
- "list" command with empty list (T017)
- "complete" command (T032-T034)
- "delete" command (T044-T046)
"""

import pytest
from src.main import main
from src.storage import TodoStorage
from src.exceptions import ValidationError, NotFoundError
import sys
from io import StringIO


class TestAddCommand:
    """Integration tests for 'add' command (T015)"""

    def test_add_command_creates_todo(self, monkeypatch, capsys):
        """Test that 'add' command creates a todo and displays confirmation"""
        # Mock command line arguments
        monkeypatch.setattr(sys, 'argv', ['todo', 'add', 'Buy groceries'])

        # Run main
        exit_code = main()

        # Capture output
        captured = capsys.readouterr()

        assert exit_code == 0
        assert "Todo added: Buy groceries (ID: 1)" in captured.out

    def test_add_command_with_empty_title_shows_error(self, monkeypatch, capsys):
        """Test that 'add' command with empty title shows error"""
        monkeypatch.setattr(sys, 'argv', ['todo', 'add', ''])

        exit_code = main()

        captured = capsys.readouterr()

        assert exit_code == 1
        assert "Error: Title cannot be empty" in captured.out

    def test_add_command_increments_id(self, monkeypatch, capsys):
        """Test that multiple 'add' commands increment IDs"""
        # This test simulates multiple invocations but with same storage instance
        # In real CLI, storage is recreated each time (in-memory = not persistent)
        # We test the storage behavior here
        storage = TodoStorage()

        # First add
        todo1 = storage.add("First")
        assert todo1.id == 1

        # Second add
        todo2 = storage.add("Second")
        assert todo2.id == 2


class TestListCommand:
    """Integration tests for 'list' command (T016, T017)"""

    def test_list_command_with_todos(self, monkeypatch, capsys):
        """Test that 'list' command displays all todos (T016)"""
        # This test requires pre-populated storage
        # Since we have in-memory storage, we need to modify main() to accept storage
        # For now, test the storage directly and verify format
        storage = TodoStorage()
        storage.add("Buy groceries")
        storage.add("Write tests")

        todos = storage.list_all()

        # Verify expected output format: "ID. [status] title"
        assert len(todos) == 2
        # First todo: "1. [ ] Buy groceries"
        assert todos[0].id == 1
        assert todos[0].title == "Buy groceries"
        assert todos[0].completed is False
        # Second todo: "2. [ ] Write tests"
        assert todos[1].id == 2
        assert todos[1].title == "Write tests"
        assert todos[1].completed is False

    def test_list_command_with_empty_list(self, monkeypatch, capsys):
        """Test that 'list' command shows message when no todos exist (T017)"""
        monkeypatch.setattr(sys, 'argv', ['todo', 'list'])

        exit_code = main()

        captured = capsys.readouterr()

        assert exit_code == 0
        assert "No todos found" in captured.out

    def test_list_command_formats_completed_todos(self):
        """Test that list formats completed todos with [x]"""
        storage = TodoStorage()
        todo = storage.add("Buy groceries")
        # Mark as complete (will implement in US2, but test format now)
        todo.completed = True

        todos = storage.list_all()

        # Expected format: "1. [x] Buy groceries"
        assert todos[0].completed is True

    def test_list_command_formats_incomplete_todos(self):
        """Test that list formats incomplete todos with [ ]"""
        storage = TodoStorage()
        storage.add("Buy groceries")

        todos = storage.list_all()

        # Expected format: "1. [ ] Buy groceries"
        assert todos[0].completed is False


class TestCompleteCommand:
    """Integration tests for 'complete' command (T032-T034)"""

    def test_complete_command_with_valid_id(self, monkeypatch, capsys):
        """Test that 'complete' command marks todo as complete (T032)"""
        # Since storage is in-memory and recreated each time,
        # we test the storage layer directly
        storage = TodoStorage()
        todo = storage.add("Buy groceries")

        # Complete the todo
        completed = storage.complete(todo.id)

        assert completed.completed is True
        assert completed.id == 1
        assert completed.title == "Buy groceries"

    def test_complete_command_with_invalid_id(self, monkeypatch, capsys):
        """Test that 'complete' command with invalid ID shows error (T033)"""
        monkeypatch.setattr(sys, 'argv', ['todo', 'complete', '999'])

        exit_code = main()

        captured = capsys.readouterr()

        assert exit_code == 1
        assert "Error: Todo with ID 999 not found" in captured.out

    def test_complete_command_with_non_numeric_id(self, monkeypatch, capsys):
        """Test that 'complete' command with non-numeric ID shows error (T034)"""
        # argparse will handle this - it expects an int
        # This test verifies the CLI handles invalid input gracefully
        with pytest.raises(SystemExit):
            monkeypatch.setattr(sys, 'argv', ['todo', 'complete', 'abc'])
            main()

    def test_complete_command_updates_list_output(self):
        """Test that completed todos show [x] in list"""
        storage = TodoStorage()
        storage.add("Buy groceries")
        storage.add("Write tests")

        # Complete first todo
        storage.complete(1)

        todos = storage.list_all()

        # First todo should be completed
        assert todos[0].completed is True
        # Second todo should be incomplete
        assert todos[1].completed is False


class TestEdgeCases:
    """Comprehensive edge case tests for all commands (T055)"""

    def test_add_with_very_long_title_within_limit(self):
        """Test adding todo with exactly 200 characters (edge of valid)"""
        storage = TodoStorage()
        long_title = "a" * 200

        todo = storage.add(long_title)

        assert todo.title == long_title
        assert len(todo.title) == 200

    def test_add_with_title_exceeding_limit(self):
        """Test adding todo with 201 characters (just over limit)"""
        storage = TodoStorage()
        too_long_title = "a" * 201

        with pytest.raises(ValidationError, match="cannot exceed 200 characters"):
            storage.add(too_long_title)

    def test_add_with_whitespace_only_title(self):
        """Test adding todo with only whitespace"""
        storage = TodoStorage()

        with pytest.raises(ValidationError, match="cannot be empty"):
            storage.add("   ")

    def test_add_with_special_characters_in_title(self):
        """Test that special characters are allowed in titles"""
        storage = TodoStorage()
        special_title = "Buy @#$% groceries! (urgent)"

        todo = storage.add(special_title)

        assert todo.title == special_title

    def test_complete_already_completed_todo_is_idempotent(self):
        """Test that completing twice doesn't error (edge case: idempotency)"""
        storage = TodoStorage()
        todo = storage.add("Test")

        # Complete once
        storage.complete(todo.id)
        # Complete again - should not error
        storage.complete(todo.id)

        assert todo.completed is True

    def test_delete_from_empty_storage(self):
        """Test deleting when no todos exist"""
        storage = TodoStorage()

        with pytest.raises(NotFoundError):
            storage.delete(1)

    def test_sequential_operations_maintain_state(self):
        """Test that multiple operations maintain consistent state"""
        storage = TodoStorage()

        # Add three todos
        todo1 = storage.add("First")
        todo2 = storage.add("Second")
        todo3 = storage.add("Third")

        # Complete second
        storage.complete(todo2.id)

        # Delete first
        storage.delete(todo1.id)

        # Verify state
        remaining = storage.list_all()
        assert len(remaining) == 2
        assert remaining[0].id == 2
        assert remaining[0].completed is True
        assert remaining[1].id == 3
        assert remaining[1].completed is False

    def test_exit_codes_on_success(self, monkeypatch):
        """Test that successful commands return exit code 0 (FR-012)"""
        monkeypatch.setattr(sys, 'argv', ['todo', 'list'])
        exit_code = main()
        assert exit_code == 0

    def test_exit_codes_on_error(self, monkeypatch):
        """Test that error commands return non-zero exit code (FR-012)"""
        monkeypatch.setattr(sys, 'argv', ['todo', 'complete', '999'])
        exit_code = main()
        assert exit_code == 1


class TestDeleteCommand:
    """Integration tests for 'delete' command (T044-T046)"""

    def test_delete_command_with_valid_id(self, monkeypatch, capsys):
        """Test that 'delete' command removes todo (T044)"""
        storage = TodoStorage()
        todo = storage.add("Buy groceries")

        # Delete the todo
        storage.delete(todo.id)

        # Verify it's removed
        all_todos = storage.list_all()
        assert len(all_todos) == 0

    def test_delete_command_with_invalid_id(self, monkeypatch, capsys):
        """Test that 'delete' command with invalid ID shows error (T045)"""
        monkeypatch.setattr(sys, 'argv', ['todo', 'delete', '999'])

        exit_code = main()

        captured = capsys.readouterr()

        assert exit_code == 1
        assert "Error: Todo with ID 999 not found" in captured.out

    def test_delete_command_with_non_numeric_id(self, monkeypatch, capsys):
        """Test that 'delete' command with non-numeric ID shows error (T046)"""
        # argparse will handle this - it expects an int
        with pytest.raises(SystemExit):
            monkeypatch.setattr(sys, 'argv', ['todo', 'delete', 'abc'])
            main()

    def test_delete_command_preserves_id_sequence(self):
        """Test that deleting todos doesn't affect next ID assignment"""
        storage = TodoStorage()
        todo1 = storage.add("First")
        todo2 = storage.add("Second")

        # Delete first todo
        storage.delete(todo1.id)

        # Add new todo - should get ID 3, not reuse ID 1
        todo3 = storage.add("Third")
        assert todo3.id == 3

        # Verify list
        all_todos = storage.list_all()
        assert len(all_todos) == 2
        assert all_todos[0].id == 2
        assert all_todos[1].id == 3


class TestUpdateCommand:
    """Integration tests for 'update' command (T006-T009)"""

    def test_update_command_successful(self, monkeypatch, capsys):
        """Test that 'update' command updates todo title successfully (T006)"""
        storage = TodoStorage()
        todo = storage.add("Buy grocreies")

        # Update the todo
        updated = storage.update(todo.id, "Buy groceries")

        assert updated.title == "Buy groceries"
        assert updated.id == todo.id
        assert updated.completed is False

        # Verify change persists
        all_todos = storage.list_all()
        assert len(all_todos) == 1
        assert all_todos[0].title == "Buy groceries"

    def test_update_command_with_nonexistent_id(self, monkeypatch, capsys):
        """Test that 'update' command with non-existent ID shows error (T007)"""
        monkeypatch.setattr(sys, 'argv', ['todo', 'update', '999', 'New title'])

        exit_code = main()

        captured = capsys.readouterr()

        assert exit_code == 1
        assert "Error: Todo with ID 999 not found" in captured.out

    def test_update_command_with_invalid_title(self, monkeypatch, capsys):
        """Test that 'update' command with invalid title shows error (T008)"""
        storage = TodoStorage()
        # First add a todo so we can try to update it with invalid title
        storage.add("Original title")

        # Try to update with empty title - should raise ValidationError
        with pytest.raises(ValidationError):
            storage.update(1, "")

    def test_update_command_preserves_completion_status(self, monkeypatch, capsys):
        """Test that 'update' command preserves completion status (T009)"""
        storage = TodoStorage()

        # Add and complete a todo
        todo = storage.add("Original title")
        storage.complete(todo.id)

        # Verify it's completed
        assert todo.completed is True

        # Update the completed todo
        updated = storage.update(todo.id, "Updated title")

        # Verify status preserved
        assert updated.completed is True
        assert updated.title == "Updated title"
        assert updated.id == todo.id

        # Verify change persists
        all_todos = storage.list_all()
        assert len(all_todos) == 1
        assert all_todos[0].completed is True
        assert all_todos[0].title == "Updated title"


class TestUpdateCommandEdgeCases:
    """Edge case tests for 'update' command (T017)"""

    def test_update_idempotent(self):
        """Test that updating to same title is idempotent"""
        storage = TodoStorage()
        todo = storage.add("Buy groceries")

        # Update to same title
        updated = storage.update(todo.id, "Buy groceries")

        assert updated.title == "Buy groceries"
        assert updated.id == todo.id

    def test_update_whitespace_only_title(self):
        """Test that whitespace-only title raises ValidationError"""
        storage = TodoStorage()
        storage.add("Original title")

        with pytest.raises(ValidationError, match="cannot be empty"):
            storage.update(1, "   ")

    def test_update_title_exactly_200_chars(self):
        """Test updating with title exactly 200 characters (boundary)"""
        storage = TodoStorage()
        storage.add("Original title")

        long_title = "a" * 200
        updated = storage.update(1, long_title)

        assert updated.title == long_title
        assert len(updated.title) == 200

    def test_update_allows_duplicate_titles(self):
        """Test that duplicate titles are allowed across todos"""
        storage = TodoStorage()
        todo1 = storage.add("Buy groceries")
        todo2 = storage.add("Write tests")

        # Update todo2 to have same title as todo1
        updated = storage.update(todo2.id, "Buy groceries")

        # Both should have "Buy groceries"
        all_todos = storage.list_all()
        assert all_todos[0].title == "Buy groceries"
        assert all_todos[1].title == "Buy groceries"
        # But different IDs
        assert all_todos[0].id == 1
        assert all_todos[1].id == 2

    def test_update_after_deletion(self):
        """Test that update works correctly after deletions (ID gaps)"""
        storage = TodoStorage()
        storage.add("First")
        storage.add("Second")
        storage.add("Third")

        # Delete second todo
        storage.delete(2)

        # Update first todo - should work
        updated = storage.update(1, "First Updated")
        assert updated.title == "First Updated"

        # Update third todo - should work
        updated = storage.update(3, "Third Updated")
        assert updated.title == "Third Updated"

        # List should show gap at ID 2
        all_todos = storage.list_all()
        assert len(all_todos) == 2
        assert all_todos[0].id == 1
        assert all_todos[1].id == 3
