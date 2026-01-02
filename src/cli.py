"""
CLI argument parsing and command handling

Defines command-line interface using argparse and handler functions.
"""

import argparse
from src.storage import TodoStorage
from src.exceptions import TodoError


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the CLI argument parser.

    Returns:
        Configured ArgumentParser with subcommands
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Todo CLI - Manage your tasks from the command line",
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command: todo add <title>
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("title", type=str, help="Todo description")

    # List command: todo list
    subparsers.add_parser("list", help="List all todos")

    # Complete command: todo complete <id>
    complete_parser = subparsers.add_parser("complete", help="Mark a todo as complete")
    complete_parser.add_argument("id", type=int, help="Todo ID to complete")

    # Delete command: todo delete <id>
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("id", type=int, help="Todo ID to delete")

    # Update command: todo update <id> <new_title>
    update_parser = subparsers.add_parser("update", help="Update the title of an existing todo")
    update_parser.add_argument("id", type=int, help="ID of the todo to update")
    update_parser.add_argument("new_title", type=str, help="New title for the todo (1-200 characters)")

    return parser


def handle_add(storage: TodoStorage, title: str) -> str:
    """
    Handle the 'add' command.

    Args:
        storage: TodoStorage instance
        title: Todo title to add

    Returns:
        Success message with todo details

    Raises:
        TodoError: If validation fails
    """
    todo = storage.add(title)
    return f"Todo added: {todo.title} (ID: {todo.id})"


def handle_list(storage: TodoStorage) -> str:
    """
    Handle the 'list' command.

    Args:
        storage: TodoStorage instance

    Returns:
        Formatted list of todos or "No todos found" message
    """
    todos = storage.list_all()

    if not todos:
        return "No todos found"

    # Format: "ID. [status] title"
    # Status: [x] for completed, [ ] for incomplete
    lines = []
    for todo in todos:
        status = "[x]" if todo.completed else "[ ]"
        lines.append(f"{todo.id}. {status} {todo.title}")

    return "\n".join(lines)


def handle_complete(storage: TodoStorage, todo_id: int) -> str:
    """
    Handle the 'complete' command.

    Args:
        storage: TodoStorage instance
        todo_id: ID of todo to complete

    Returns:
        Success message

    Raises:
        NotFoundError: If todo doesn't exist
    """
    todo = storage.complete(todo_id)
    return f"Completed: {todo.title} (ID: {todo.id})"


def handle_delete(storage: TodoStorage, todo_id: int) -> str:
    """
    Handle the 'delete' command.

    Args:
        storage: TodoStorage instance
        todo_id: ID of todo to delete

    Returns:
        Success message

    Raises:
        NotFoundError: If todo doesn't exist (raised by storage.delete)
    """
    # Get todo title before deleting (for confirmation message)
    # This will raise NotFoundError if todo doesn't exist
    title = storage.todos.get(todo_id)
    if title is None:
        from src.exceptions import NotFoundError
        raise NotFoundError(f"Todo with ID {todo_id} not found")

    title_text = title.title
    storage.delete(todo_id)
    return f"Deleted: {title_text} (ID: {todo_id})"


def handle_update(storage: TodoStorage, todo_id: int, new_title: str) -> str:
    """
    Handle the 'update' command.

    Args:
        storage: TodoStorage instance
        todo_id: ID of todo to update
        new_title: New title for the todo

    Returns:
        Success message showing old and new titles

    Raises:
        NotFoundError: If todo doesn't exist
        ValidationError: If new_title is invalid
    """
    # Get old title before updating (for confirmation message)
    old_todo = storage.todos.get(todo_id)
    if old_todo is None:
        from src.exceptions import NotFoundError
        raise NotFoundError(f"Todo with ID {todo_id} not found")

    old_title = old_todo.title

    # Update the todo
    updated_todo = storage.update(todo_id, new_title)

    # Return confirmation message with old and new titles
    return f"Updated: '{old_title}' → '{updated_todo.title}' (ID: {todo_id})"
