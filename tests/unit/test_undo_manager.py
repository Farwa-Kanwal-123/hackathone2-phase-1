"""
Unit tests for UndoManager

Tests undo functionality for add/delete/update/complete actions:
- record_action() - captures state before action
- undo() - restores previous state
- can_undo() - checks if undo available
- get_undo_description() - describes undo operation
"""

import pytest
from datetime import datetime
from copy import deepcopy
from src.services.undo_manager import UndoManager, ActionSnapshot
from src.storage import TodoStorage
from src.todo import TodoItem


class TestRecordAction:
    """Test record_action() method"""

    def setup_method(self):
        """Set up test storage and undo manager"""
        self.storage = TodoStorage()
        self.undo_mgr = UndoManager()

    def test_record_action_add_stores_none_previous_state(self):
        """Should store None as previous_state for add action"""
        self.undo_mgr.record_action("add", 1, self.storage)

        assert self.undo_mgr.last_action is not None
        assert self.undo_mgr.last_action.action_type == "add"
        assert self.undo_mgr.last_action.todo_id == 1
        assert self.undo_mgr.last_action.previous_state is None

    def test_record_action_delete_stores_deep_copy(self):
        """Should store deep copy of todo for delete action"""
        self.storage.add("Test todo")
        todo = self.storage.todos[1]
        todo.priority = "High"

        self.undo_mgr.record_action("delete", 1, self.storage)

        assert self.undo_mgr.last_action.previous_state is not None
        assert self.undo_mgr.last_action.previous_state.title == "Test todo"
        assert self.undo_mgr.last_action.previous_state.priority == "High"
        # Verify deep copy (not same object)
        assert self.undo_mgr.last_action.previous_state is not todo

    def test_record_action_update_stores_deep_copy(self):
        """Should store deep copy of todo for update action"""
        self.storage.add("Old title")
        self.undo_mgr.record_action("update", 1, self.storage)

        assert self.undo_mgr.last_action.previous_state is not None
        assert self.undo_mgr.last_action.previous_state.title == "Old title"

    def test_record_action_complete_stores_deep_copy(self):
        """Should store deep copy of todo for complete action"""
        self.storage.add("Task")
        self.undo_mgr.record_action("complete", 1, self.storage)

        assert self.undo_mgr.last_action.previous_state is not None
        assert self.undo_mgr.last_action.previous_state.completed is False

    def test_record_action_overwrites_previous_action(self):
        """Should overwrite previous action (single-level undo)"""
        self.storage.add("First")
        self.undo_mgr.record_action("add", 1, self.storage)

        self.storage.add("Second")
        self.undo_mgr.record_action("add", 2, self.storage)

        assert self.undo_mgr.last_action.todo_id == 2  # First action lost

    def test_record_action_invalid_type_raises_error(self):
        """Should raise ValueError for invalid action type"""
        with pytest.raises(ValueError) as exc_info:
            self.undo_mgr.record_action("invalid", 1, self.storage)

        assert "action_type must be one of" in str(exc_info.value)
        assert "invalid" in str(exc_info.value)

    def test_record_action_captures_timestamp(self):
        """Should capture timestamp of action"""
        before = datetime.now()
        self.undo_mgr.record_action("add", 1, self.storage)
        after = datetime.now()

        assert before <= self.undo_mgr.last_action.timestamp <= after


class TestUndoAdd:
    """Test undo() for add action"""

    def setup_method(self):
        """Set up test storage and undo manager"""
        self.storage = TodoStorage()
        self.undo_mgr = UndoManager()

    def test_undo_add_deletes_todo(self):
        """Should delete the added todo"""
        # Record and execute add
        self.undo_mgr.record_action("add", self.storage.next_id, self.storage)
        self.storage.add("New todo")

        # Undo add
        message = self.undo_mgr.undo(self.storage)

        assert 1 not in self.storage.todos
        assert "Removed todo" in message
        assert "ID: 1" in message

    def test_undo_add_clears_history(self):
        """Should clear undo history after undo"""
        self.undo_mgr.record_action("add", self.storage.next_id, self.storage)
        self.storage.add("Todo")

        self.undo_mgr.undo(self.storage)

        assert self.undo_mgr.last_action is None
        assert not self.undo_mgr.can_undo()

    def test_undo_add_cannot_undo_twice(self):
        """Should not allow undoing the same action twice"""
        self.undo_mgr.record_action("add", self.storage.next_id, self.storage)
        self.storage.add("Todo")

        self.undo_mgr.undo(self.storage)

        with pytest.raises(ValueError) as exc_info:
            self.undo_mgr.undo(self.storage)

        assert "No action to undo" in str(exc_info.value)


class TestUndoDelete:
    """Test undo() for delete action"""

    def setup_method(self):
        """Set up test storage and undo manager"""
        self.storage = TodoStorage()
        self.undo_mgr = UndoManager()

    def test_undo_delete_restores_todo(self):
        """Should restore deleted todo with exact state"""
        self.storage.add("Test todo")
        todo = self.storage.todos[1]
        todo.priority = "High"

        # Record and execute delete
        self.undo_mgr.record_action("delete", 1, self.storage)
        self.storage.delete(1)

        assert 1 not in self.storage.todos

        # Undo delete
        message = self.undo_mgr.undo(self.storage)

        assert 1 in self.storage.todos
        assert self.storage.todos[1].title == "Test todo"
        assert self.storage.todos[1].priority == "High"
        assert "Restored 'Test todo'" in message

    def test_undo_delete_restores_with_original_id(self):
        """Should restore todo with original ID"""
        self.storage.add("Todo 1")
        self.storage.add("Todo 2")

        self.undo_mgr.record_action("delete", 1, self.storage)
        self.storage.delete(1)

        self.undo_mgr.undo(self.storage)

        assert 1 in self.storage.todos
        assert 2 in self.storage.todos
        assert self.storage.todos[1].title == "Todo 1"

    def test_undo_delete_without_previous_state_raises_error(self):
        """Should raise error if previous_state is None"""
        # Manually create snapshot with None previous_state (edge case)
        self.undo_mgr.last_action = ActionSnapshot(
            action_type="delete",
            todo_id=999,
            previous_state=None,
            timestamp=datetime.now()
        )

        with pytest.raises(ValueError) as exc_info:
            self.undo_mgr.undo(self.storage)

        assert "Cannot undo delete: no previous state" in str(exc_info.value)


class TestUndoUpdate:
    """Test undo() for update action"""

    def setup_method(self):
        """Set up test storage and undo manager"""
        self.storage = TodoStorage()
        self.undo_mgr = UndoManager()

    def test_undo_update_restores_title(self):
        """Should restore previous title"""
        self.storage.add("Old title")

        # Record and execute update
        self.undo_mgr.record_action("update", 1, self.storage)
        self.storage.update(1, "New title")

        assert self.storage.todos[1].title == "New title"

        # Undo update
        message = self.undo_mgr.undo(self.storage)

        assert self.storage.todos[1].title == "Old title"
        assert "Reverted 'Old title'" in message

    def test_undo_update_restores_priority(self):
        """Should restore all todo fields (not just title)"""
        self.storage.add("Task")
        todo = self.storage.todos[1]
        todo.priority = "Low"

        # Record and execute update (change priority)
        self.undo_mgr.record_action("update", 1, self.storage)
        todo.priority = "High"

        assert todo.priority == "High"

        # Undo update
        self.undo_mgr.undo(self.storage)

        assert self.storage.todos[1].priority == "Low"

    def test_undo_update_without_previous_state_raises_error(self):
        """Should raise error if previous_state is None"""
        self.undo_mgr.last_action = ActionSnapshot(
            action_type="update",
            todo_id=999,
            previous_state=None,
            timestamp=datetime.now()
        )

        with pytest.raises(ValueError) as exc_info:
            self.undo_mgr.undo(self.storage)

        assert "Cannot undo update: no previous state" in str(exc_info.value)


class TestUndoComplete:
    """Test undo() for complete action"""

    def setup_method(self):
        """Set up test storage and undo manager"""
        self.storage = TodoStorage()
        self.undo_mgr = UndoManager()

    def test_undo_complete_marks_incomplete(self):
        """Should set completed=False"""
        self.storage.add("Task")

        # Record and execute complete
        self.undo_mgr.record_action("complete", 1, self.storage)
        self.storage.complete(1)

        assert self.storage.todos[1].completed is True

        # Undo complete
        message = self.undo_mgr.undo(self.storage)

        assert self.storage.todos[1].completed is False
        assert "Marked incomplete" in message

    def test_undo_complete_with_missing_todo_raises_error(self):
        """Should raise error if todo no longer exists"""
        self.storage.add("Task")
        self.undo_mgr.record_action("complete", 1, self.storage)
        self.storage.complete(1)
        self.storage.delete(1)  # Delete after completing

        with pytest.raises(ValueError) as exc_info:
            self.undo_mgr.undo(self.storage)

        assert "Cannot undo: todo 1 not found" in str(exc_info.value)


class TestCanUndo:
    """Test can_undo() method"""

    def setup_method(self):
        """Set up test storage and undo manager"""
        self.storage = TodoStorage()
        self.undo_mgr = UndoManager()

    def test_can_undo_false_when_no_action(self):
        """Should return False when no action recorded"""
        assert not self.undo_mgr.can_undo()

    def test_can_undo_true_after_recording_action(self):
        """Should return True after recording action"""
        self.undo_mgr.record_action("add", 1, self.storage)
        assert self.undo_mgr.can_undo()

    def test_can_undo_false_after_undo(self):
        """Should return False after undo (history cleared)"""
        self.undo_mgr.record_action("add", self.storage.next_id, self.storage)
        self.storage.add("Todo")

        self.undo_mgr.undo(self.storage)

        assert not self.undo_mgr.can_undo()


class TestGetUndoDescription:
    """Test get_undo_description() method"""

    def setup_method(self):
        """Set up test storage and undo manager"""
        self.storage = TodoStorage()
        self.undo_mgr = UndoManager()

    def test_get_undo_description_returns_none_when_no_action(self):
        """Should return None when no action recorded"""
        assert self.undo_mgr.get_undo_description() is None

    def test_get_undo_description_add(self):
        """Should describe add undo"""
        self.undo_mgr.record_action("add", 5, self.storage)
        desc = self.undo_mgr.get_undo_description()

        assert desc == "Undo add of todo (ID: 5)"

    def test_get_undo_description_delete(self):
        """Should describe delete undo with title"""
        self.storage.add("Fix bug")
        self.undo_mgr.record_action("delete", 1, self.storage)

        desc = self.undo_mgr.get_undo_description()

        assert desc == "Undo delete of 'Fix bug' (ID: 1)"

    def test_get_undo_description_update(self):
        """Should describe update undo with title"""
        self.storage.add("Old title")
        self.undo_mgr.record_action("update", 1, self.storage)

        desc = self.undo_mgr.get_undo_description()

        assert desc == "Undo update of 'Old title' (ID: 1)"

    def test_get_undo_description_complete(self):
        """Should describe complete undo with title"""
        self.storage.add("Task name")
        self.undo_mgr.record_action("complete", 1, self.storage)

        desc = self.undo_mgr.get_undo_description()

        assert desc == "Undo completion of 'Task name' (ID: 1)"


class TestUndoWithNoAction:
    """Test undo() error handling"""

    def setup_method(self):
        """Set up test storage and undo manager"""
        self.storage = TodoStorage()
        self.undo_mgr = UndoManager()

    def test_undo_without_action_raises_error(self):
        """Should raise ValueError when no action to undo"""
        with pytest.raises(ValueError) as exc_info:
            self.undo_mgr.undo(self.storage)

        assert "No action to undo" in str(exc_info.value)


class TestActionSnapshotValidation:
    """Test ActionSnapshot validation in __post_init__"""

    def test_action_snapshot_valid_types(self):
        """Should accept valid action types"""
        valid_types = ["add", "delete", "update", "complete"]

        for action_type in valid_types:
            snapshot = ActionSnapshot(
                action_type=action_type,
                todo_id=1,
                previous_state=None,
                timestamp=datetime.now()
            )
            assert snapshot.action_type == action_type

    def test_action_snapshot_invalid_type_raises_error(self):
        """Should raise ValueError for invalid action type"""
        with pytest.raises(ValueError) as exc_info:
            ActionSnapshot(
                action_type="invalid",
                todo_id=1,
                previous_state=None,
                timestamp=datetime.now()
            )

        assert "action_type must be one of" in str(exc_info.value)
        assert "invalid" in str(exc_info.value)
