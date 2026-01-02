"""
Interactive Menu-Based Todo Console Application

Entry point for interactive mode: uv run main.py

This module provides a beginner-friendly, menu-based interface for managing todos.
Users are guided through numbered menu options and prompts, eliminating the need
to memorize command syntax.
"""

from src.storage import TodoStorage
from src.interactive_menu import (
    display_menu,
    get_menu_choice,
    interactive_add,
    interactive_list,
    interactive_complete,
    interactive_update,
    interactive_delete
)


def main():
    """Main entry point for interactive menu mode."""
    storage = TodoStorage()

    # Display welcome message
    print("=== Todo App - Interactive Menu ===")
    print("\nWelcome! Manage your todos with ease.")

    try:
        while True:
            # Display menu and get choice
            display_menu()
            choice = get_menu_choice()

            # Dispatch to appropriate handler
            if choice == 1:
                interactive_add(storage)
            elif choice == 2:
                interactive_list(storage)
            elif choice == 3:
                interactive_complete(storage)
            elif choice == 4:
                interactive_update(storage)
            elif choice == 5:
                interactive_delete(storage)
            elif choice == 6:
                print("\nGoodbye! Your todos will be cleared (in-memory only).")
                break

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nGoodbye! Your todos will be cleared (in-memory only).")


if __name__ == "__main__":
    main()
