"""
Interactive prompts using questionary

Provides prompt functions for task selection, priority selection,
confirmations, and text input with arrow key navigation.
"""

from typing import List, Optional
import questionary
from src.todo import TodoItem


def prompt_task_selection(todos: List[TodoItem], message: str = "Select a task") -> Optional[int]:
    """
    Prompt user to select a task using arrow keys.

    Args:
        todos: List of TodoItem objects to choose from
        message: Prompt message to display

    Returns:
        Selected todo ID, or None if cancelled or empty list

    Example:
        >>> todos = storage.list_all()
        >>> todo_id = prompt_task_selection(todos, "Select task to complete")
        >>> if todo_id:
        >>>     storage.complete(todo_id)
    """
    if not todos:
        return None

    # Format choices as "ID. Title"
    choices = [f"{todo.id}. {todo.title}" for todo in todos]

    # Prompt with arrow key navigation
    answer = questionary.select(
        message,
        choices=choices
    ).ask()

    # Handle cancellation (Esc key)
    if answer is None:
        return None

    # Extract ID from choice (format: "ID. Title")
    todo_id = int(answer.split(". ")[0])
    return todo_id


def prompt_priority_selection(message: str = "Select priority") -> Optional[str]:
    """
    Prompt user to select a priority level using arrow keys.

    Args:
        message: Prompt message to display

    Returns:
        Selected priority ("High"/"Medium"/"Low"/None), or None if cancelled

    Example:
        >>> priority = prompt_priority_selection()
        >>> if priority:
        >>>     todo.priority = priority
    """
    choices = [
        "High",
        "Medium",
        "Low",
        "None (no priority)"
    ]

    answer = questionary.select(
        message,
        choices=choices
    ).ask()

    # Handle cancellation
    if answer is None:
        return None

    # Map "None (no priority)" to None
    if answer == "None (no priority)":
        return None

    return answer


def prompt_confirmation(message: str) -> bool:
    """
    Prompt user for yes/no confirmation.

    Args:
        message: Confirmation question to display

    Returns:
        True if confirmed, False if declined or cancelled

    Example:
        >>> if prompt_confirmation("Delete this task?"):
        >>>     storage.delete(todo_id)
    """
    answer = questionary.confirm(message).ask()

    # Treat cancellation (Esc) as No
    if answer is None:
        return False

    return answer


def prompt_text_input(message: str) -> Optional[str]:
    """
    Prompt user for text input.

    Args:
        message: Prompt message to display

    Returns:
        User input text, or None if cancelled

    Example:
        >>> title = prompt_text_input("Enter task title:")
        >>> if title:
        >>>     storage.add(title)
    """
    answer = questionary.text(message).ask()

    return answer
