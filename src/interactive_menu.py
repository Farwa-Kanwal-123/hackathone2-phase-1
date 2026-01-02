"""
Interactive Menu Module

Provides menu display and interactive prompt functions for the todo application.
Wraps existing CLI handlers with user-friendly prompts and input validation.

Functions:
- display_menu(): Show numbered menu options
- get_menu_choice(): Get and validate menu selection (1-6)
- prompt_for_input(msg): Get string input from user
- prompt_for_id(msg): Get and validate numeric ID
- interactive_add(storage): Interactive add workflow
- interactive_list(storage): Interactive list workflow
- interactive_complete(storage): Interactive complete workflow
- interactive_update(storage): Interactive update workflow
- interactive_delete(storage): Interactive delete workflow
"""

from src.storage import TodoStorage


def display_menu():
    """Display the interactive menu with numbered options."""
    print("\n1. Add todo")
    print("2. List all todos")
    print("3. Complete todo")
    print("4. Update todo")
    print("5. Delete todo")
    print("6. Exit")
    print("\nEnter your choice (1-6): ", end="")


def get_menu_choice():
    """Get and validate user's menu choice (1-6)."""
    while True:
        try:
            choice_str = input().strip()
            if not choice_str:
                print("Error: Please enter a number between 1 and 6.")
                print("Enter your choice (1-6): ", end="")
                continue

            choice = int(choice_str)
            if 1 <= choice <= 6:
                return choice
            else:
                print("Error: Invalid choice. Please enter a number between 1 and 6.")
                print("Enter your choice (1-6): ", end="")
        except ValueError:
            print("Error: Please enter a number between 1 and 6.")
            print("Enter your choice (1-6): ", end="")


def prompt_for_input(prompt_message: str) -> str:
    """
    Prompt user for string input with validation.

    Args:
        prompt_message: Message to display to user

    Returns:
        User's input string (stripped of whitespace)
    """
    while True:
        user_input = input(prompt_message).strip()
        if user_input:
            return user_input
        print("Error: Title cannot be empty or whitespace.")


def prompt_for_id(prompt_message: str) -> int:
    """
    Prompt user for numeric ID input with validation.

    Args:
        prompt_message: Message to display to user

    Returns:
        User's input as integer
    """
    while True:
        try:
            id_str = input(prompt_message).strip()
            if not id_str:
                print("Error: Please enter a valid numeric ID.")
                continue
            return int(id_str)
        except ValueError:
            print("Error: Please enter a valid numeric ID.")


def interactive_add(storage: TodoStorage):
    """Interactive workflow for adding a todo."""
    from src.cli import handle_add
    from src.exceptions import TodoError

    title = prompt_for_input("Enter todo title: ")

    try:
        result = handle_add(storage, title)
        print(result)
    except TodoError as e:
        print(f"Error: {e}")


def interactive_list(storage: TodoStorage):
    """Interactive workflow for listing todos."""
    from src.cli import handle_list

    result = handle_list(storage)

    if result == "No todos found":
        print("No todos found. Start by adding one!")
    else:
        print("\nYour todos:\n")
        print(result)
        # Count total and completed
        todos = storage.list_all()
        completed_count = sum(1 for t in todos if t.completed)
        print(f"\nTotal: {len(todos)} todos ({completed_count} completed)")


def interactive_complete(storage: TodoStorage):
    """Interactive workflow for completing a todo."""
    from src.cli import handle_complete
    from src.exceptions import NotFoundError

    todo_id = prompt_for_id("Enter the ID of the todo to complete: ")

    try:
        result = handle_complete(storage, todo_id)
        print(result)
    except NotFoundError as e:
        print(f"Error: {e}")


def interactive_update(storage: TodoStorage):
    """Interactive workflow for updating a todo."""
    from src.cli import handle_update
    from src.exceptions import TodoError

    todo_id = prompt_for_id("Enter the ID of the todo to update: ")
    new_title = prompt_for_input("Enter the new title: ")

    try:
        result = handle_update(storage, todo_id, new_title)
        print(result)
    except TodoError as e:
        print(f"Error: {e}")


def interactive_delete(storage: TodoStorage):
    """Interactive workflow for deleting a todo."""
    from src.cli import handle_delete
    from src.exceptions import NotFoundError

    todo_id = prompt_for_id("Enter the ID of the todo to delete: ")

    try:
        result = handle_delete(storage, todo_id)
        print(result)
    except NotFoundError as e:
        print(f"Error: {e}")
