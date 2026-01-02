"""
Contract tests for UndoManager

Validates the UndoManager interface contract:
- record_action() captures state before action
- undo() correctly restores state for all action types
- Single-level undo (cannot undo twice)
- Deep copy prevents mutation bugs
"""

import pytest
from copy import deepcopy
from datetime import datetime
from src.services.undo_manager import UndoManager, ActionSnapshot
from src.storage import TodoStorage
from src.todo import TodoItem


def test_record_action_captures_state_contract():
    """Verify deep copy of previous state (not same object reference)"""
    # Arrange
    storage = TodoStorage()
    undo_mgr = UndoManager()

    storage.add("Test todo")
    original_todo = storage.todos[1]

    # Act: record action
    undo_mgr.record_action("delete", 1, storage)

    # Assert: previous_state is deep copy (not same object)
    captured_state = undo_mgr.last_action.previous_state
    assert captured_state is not original_todo
    assert captured_state == original_todo  # Equal values
    assert captured_state is not None

    # Modify original - should not affect captured state
    original_todo.title = "Modified"
    assert captured_state.title == "Test todo"  # Still original value


def test_undo_add_contract():
    """Verify undo removes added todo and clears history"""
    # Arrange
    storage = TodoStorage()
    undo_mgr = UndoManager()

    # Act: add with undo support
    undo_mgr.record_action("add", storage.next_id, storage)
    storage.add("New todo")

    # Assert: todo exists
    assert 1 in storage.todos

    # Act: undo add
    message = undo_mgr.undo(storage)

    # Assert: todo removed, history cleared
    assert 1 not in storage.todos
    assert "Removed todo" in message
    assert undo_mgr.last_action is None
    assert not undo_mgr.can_undo()


def test_undo_delete_contract():
    """Verify undo restores deleted todo with exact state"""
    # Arrange
    storage = TodoStorage()
    undo_mgr = UndoManager()

    storage.add("Test todo")
    todo = storage.todos[1]
    todo.priority = "High"
    todo.category = "Work"
    original_created_date = todo.created_date

    # Act: delete with undo support
    undo_mgr.record_action("delete", 1, storage)
    storage.delete(1)

    # Assert: todo is deleted
    assert 1 not in storage.todos

    # Act: undo delete
    message = undo_mgr.undo(storage)

    # Assert: todo is restored with exact state
    assert 1 in storage.todos
    restored_todo = storage.todos[1]
    assert restored_todo.title == "Test todo"
    assert restored_todo.priority == "High"
    assert restored_todo.category == "Work"
    assert restored_todo.created_date == original_created_date
    assert "Restored 'Test todo'" in message
    assert not undo_mgr.can_undo()


def test_undo_update_contract():
    """Verify undo restores previous title/priority/category"""
    # Arrange
    storage = TodoStorage()
    undo_mgr = UndoManager()

    storage.add("Old title")
    todo = storage.todos[1]
    todo.priority = "Low"
    todo.category = "Personal"

    # Act: update with undo support
    undo_mgr.record_action("update", 1, storage)
    storage.update(1, "New title")
    # Get updated reference
    todo = storage.todos[1]
    todo.priority = "High"
    todo.category = "Work"

    # Assert: changes applied
    assert todo.title == "New title"
    assert todo.priority == "High"
    assert todo.category == "Work"

    # Act: undo update
    message = undo_mgr.undo(storage)

    # Assert: reverted to old state
    restored_todo = storage.todos[1]
    assert restored_todo.title == "Old title"
    assert restored_todo.priority == "Low"
    assert restored_todo.category == "Personal"
    assert "Reverted 'Old title'" in message
    assert not undo_mgr.can_undo()


def test_undo_complete_contract():
    """Verify undo sets completed=False"""
    # Arrange
    storage = TodoStorage()
    undo_mgr = UndoManager()

    storage.add("Task")

    # Act: complete with undo support
    undo_mgr.record_action("complete", 1, storage)
    storage.complete(1)

    # Assert: completed
    assert storage.todos[1].completed is True

    # Act: undo complete
    message = undo_mgr.undo(storage)

    # Assert: incomplete again
    assert storage.todos[1].completed is False
    assert "Marked incomplete" in message
    assert not undo_mgr.can_undo()


def test_undo_clears_history_contract():
    """Verify cannot undo twice (single-level undo)"""
    # Arrange
    storage = TodoStorage()
    undo_mgr = UndoManager()

    undo_mgr.record_action("add", storage.next_id, storage)
    storage.add("Todo")

    # Act: first undo
    undo_mgr.undo(storage)

    # Assert: cannot undo again
    assert not undo_mgr.can_undo()

    with pytest.raises(ValueError) as exc_info:
        undo_mgr.undo(storage)

    assert "No action to undo" in str(exc_info.value)


def test_undo_without_action_raises_contract():
    """Verify ValueError when no action recorded"""
    # Arrange
    storage = TodoStorage()
    undo_mgr = UndoManager()

    # Act & Assert: undo without action
    with pytest.raises(ValueError) as exc_info:
        undo_mgr.undo(storage)

    assert "No action to undo" in str(exc_info.value)
    assert not undo_mgr.can_undo()
