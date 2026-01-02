"""
Undo manager service

Provides single-level undo functionality for todo operations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from copy import deepcopy
from src.todo import TodoItem
from src.storage import TodoStorage


@dataclass
class ActionSnapshot:
    """
    Snapshot of a single action for undo.

    Attributes:
        action_type: Type of action ("add", "delete", "update", "complete")
        todo_id: ID of the todo affected
        previous_state: Deep copy of todo before action (None for "add")
        timestamp: When the action occurred
    """
    action_type: str
    todo_id: int
    previous_state: Optional[TodoItem]
    timestamp: datetime

    def __post_init__(self):
        """Validate action_type"""
        valid_types = ["add", "delete", "update", "complete"]
        if self.action_type not in valid_types:
            raise ValueError(
                f"action_type must be one of {valid_types}. Got: {self.action_type}"
            )


class UndoManager:
    """
    Manager for single-level undo functionality.

    Only the most recent action can be undone (no multi-level undo stack).
    """

    def __init__(self):
        """
        Initialize undo manager with no action history.

        Attributes:
            last_action: The most recent action snapshot (None if no actions)
        """
        self.last_action: Optional[ActionSnapshot] = None

    def record_action(self, action_type: str, todo_id: int, storage: TodoStorage) -> None:
        """
        Record an action snapshot before executing the action.

        Args:
            action_type: "add", "delete", "update", or "complete"
            todo_id: ID of the todo being modified
            storage: TodoStorage instance (to capture current state)

        Returns:
            None (stores snapshot in self.last_action)

        Raises:
            ValueError: If action_type is invalid

        Example:
            >>> undo_mgr = UndoManager()
            >>> # Before deleting todo ID 5:
            >>> undo_mgr.record_action("delete", 5, storage)
            >>> storage.delete(5)
            >>> # Later: can undo the delete
        """
        # Capture previous state
        if action_type == "add":
            previous_state = None  # Todo doesn't exist yet
        else:
            # Get current state before modification
            if todo_id in storage.todos:
                previous_state = deepcopy(storage.todos[todo_id])
            else:
                previous_state = None

        # Create and store snapshot
        self.last_action = ActionSnapshot(
            action_type=action_type,
            todo_id=todo_id,
            previous_state=previous_state,
            timestamp=datetime.now()
        )

    def can_undo(self) -> bool:
        """
        Check if undo is available.

        Returns:
            True if last_action is not None, False otherwise

        Example:
            >>> undo_mgr = UndoManager()
            >>> undo_mgr.can_undo()
            False
            >>> undo_mgr.record_action("add", 1, storage)
            >>> undo_mgr.can_undo()
            True
        """
        return self.last_action is not None

    def get_undo_description(self) -> Optional[str]:
        """
        Get description of what undo will do.

        Returns:
            Human-readable description, or None if no action to undo

        Example:
            >>> undo_mgr.record_action("delete", 5, storage)
            >>> storage.delete(5)
            >>> undo_mgr.get_undo_description()
            "Undo delete of 'Fix bug' (ID: 5)"
        """
        if self.last_action is None:
            return None

        action_type = self.last_action.action_type
        todo_id = self.last_action.todo_id
        previous_state = self.last_action.previous_state

        if action_type == "add":
            return f"Undo add of todo (ID: {todo_id})"
        elif previous_state:
            title = previous_state.title
            if action_type == "delete":
                return f"Undo delete of '{title}' (ID: {todo_id})"
            elif action_type == "update":
                return f"Undo update of '{title}' (ID: {todo_id})"
            elif action_type == "complete":
                return f"Undo completion of '{title}' (ID: {todo_id})"

        return f"Undo {action_type} (ID: {todo_id})"

    def undo(self, storage: TodoStorage) -> str:
        """
        Undo the last recorded action.

        Args:
            storage: TodoStorage instance (to restore state)

        Returns:
            Success message describing what was undone

        Raises:
            ValueError: If no action to undo (last_action is None)

        Example:
            >>> undo_mgr.record_action("delete", 5, storage)
            >>> storage.delete(5)
            >>> message = undo_mgr.undo(storage)
            "Undone: Restored 'Fix bug' (ID: 5)"
        """
        if self.last_action is None:
            raise ValueError("No action to undo")

        snapshot = self.last_action
        action_type = snapshot.action_type
        todo_id = snapshot.todo_id
        previous_state = snapshot.previous_state

        try:
            if action_type == "add":
                # Undo add → delete the todo
                storage.delete(todo_id)
                message = f"Undone: Removed todo (ID: {todo_id})"

            elif action_type == "delete":
                # Undo delete → restore the todo
                if previous_state is None:
                    raise ValueError("Cannot undo delete: no previous state")
                storage._restore_todo(previous_state)
                message = f"Undone: Restored '{previous_state.title}' (ID: {todo_id})"

            elif action_type == "update":
                # Undo update → restore previous state
                if previous_state is None:
                    raise ValueError("Cannot undo update: no previous state")
                storage._restore_todo(previous_state)
                message = f"Undone: Reverted '{previous_state.title}' (ID: {todo_id})"

            elif action_type == "complete":
                # Undo complete → mark incomplete
                if todo_id not in storage.todos:
                    raise ValueError(f"Cannot undo: todo {todo_id} not found")
                storage.todos[todo_id].completed = False
                message = f"Undone: Marked incomplete (ID: {todo_id})"

            else:
                raise ValueError(f"Unknown action type: {action_type}")

            # Clear undo history after successful undo
            self.last_action = None
            return message

        except Exception as e:
            # On error, keep undo history (allow retry)
            raise ValueError(f"Undo failed: {e}") from e
