"""
In-memory storage for todo items

Provides CRUD operations using a dictionary-based storage system.
"""

from typing import List
from copy import deepcopy
from src.todo import TodoItem
from src.exceptions import NotFoundError


class TodoStorage:
    """
    In-memory storage for TodoItems using a dictionary.

    Attributes:
        todos: Dictionary mapping todo IDs to TodoItem objects
        next_id: Counter for generating sequential IDs (deterministic)
    """

    def __init__(self):
        """Initialize empty storage with ID counter starting at 1"""
        self.todos: dict[int, TodoItem] = {}
        self.next_id: int = 1

    def add(self, title: str) -> TodoItem:
        """
        Create and store a new todo item.

        Args:
            title: The todo description

        Returns:
            The created TodoItem with assigned ID

        Raises:
            ValidationError: If title is invalid (raised by TodoItem.__post_init__)
        """
        # Create TodoItem (validation happens in __post_init__)
        todo = TodoItem(id=self.next_id, title=title, completed=False)

        # Store in dictionary
        self.todos[todo.id] = todo

        # Increment ID counter (deterministic sequential IDs)
        self.next_id += 1

        return todo

    def list_all(self) -> List[TodoItem]:
        """
        Retrieve all todos sorted by ID.

        Returns:
            List of TodoItem objects sorted by ID (ascending)
        """
        # Return sorted list of todos by ID
        return sorted(self.todos.values(), key=lambda todo: todo.id)

    def complete(self, todo_id: int) -> TodoItem:
        """
        Mark a todo as complete.

        Args:
            todo_id: The ID of the todo to complete

        Returns:
            The updated TodoItem

        Raises:
            NotFoundError: If todo with given ID doesn't exist
        """
        if todo_id not in self.todos:
            raise NotFoundError(f"Todo with ID {todo_id} not found")

        # Mark as complete (idempotent - safe to call multiple times)
        self.todos[todo_id].completed = True

        return self.todos[todo_id]

    def delete(self, todo_id: int) -> None:
        """
        Delete a todo by ID.

        Args:
            todo_id: The ID of the todo to delete

        Raises:
            NotFoundError: If todo with given ID doesn't exist
        """
        if todo_id not in self.todos:
            raise NotFoundError(f"Todo with ID {todo_id} not found")

        # Remove from storage
        del self.todos[todo_id]

        # DO NOT decrement next_id - IDs are never reused (deterministic)

    def update(self, todo_id: int, new_title: str) -> TodoItem:
        """
        Update the title of an existing todo.

        Args:
            todo_id: The ID of the todo to update
            new_title: The new title (must pass TodoItem validation)

        Returns:
            The updated TodoItem

        Raises:
            NotFoundError: If todo_id does not exist
            ValidationError: If new_title fails validation
        """
        # Check if todo exists
        if todo_id not in self.todos:
            raise NotFoundError(f"Todo with ID {todo_id} not found")

        # Get the existing todo
        old_todo = self.todos[todo_id]

        # Create new TodoItem with updated title
        # (validation happens in __post_init__)
        updated_todo = TodoItem(
            id=old_todo.id,              # Preserve ID
            title=new_title,              # New title (validated)
            completed=old_todo.completed  # Preserve status
        )

        # Replace old todo in storage
        self.todos[todo_id] = updated_todo

        return updated_todo

    def _restore_todo(self, todo: TodoItem) -> None:
        """
        Restore a todo with its exact state (including ID).
        Used for undo operations.

        Args:
            todo: TodoItem to restore (with original ID)

        Contract:
            - Overwrites any existing todo with same ID
            - Does not update next_id (IDs are never reused)
            - Makes deep copy to prevent external mutation

        Example:
            >>> old_todo = TodoItem(id=5, title="Old", completed=False)
            >>> storage._restore_todo(old_todo)
            >>> storage.todos[5].title
            "Old"
        """
        self.todos[todo.id] = deepcopy(todo)
        # Do NOT update next_id - IDs are never reused
