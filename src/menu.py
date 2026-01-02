"""
Rich Interactive Menu Module

Enhanced interactive menu using Rich library for beautiful tables
and Questionary for arrow key navigation.

This module provides the main menu loop with:
- Arrow key navigation (Up/Down)
- Enter to select
- Esc/Ctrl+C for graceful exit
- Rich table rendering for todos
- Interactive prompts for all operations
"""

import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from src.storage import TodoStorage
from src.ui.formatting import render_task_table
from src.ui.prompts import (
    prompt_task_selection,
    prompt_priority_selection,
    prompt_confirmation,
    prompt_text_input,
)
from src.exceptions import TodoError, ValidationError, NotFoundError
from src.services.date_parser import parse_due_date, DateParseError
from src.services.undo_manager import UndoManager

# Initialize Rich console
console = Console()


def display_todos_table(todos, empty_message="No todos found"):
    """
    Helper function to display todos in a Rich table.

    Args:
        todos: List of TodoItem objects to display
        empty_message: Message to show if list is empty

    Returns:
        True if todos were displayed, False if empty
    """
    if not todos:
        console.print(f"[yellow]{empty_message}[/yellow]")
        return False

    table = render_task_table(todos)
    console.print(table)
    console.print()
    return True


def handle_operation_error(error):
    """
    Helper function to handle and display operation errors consistently.

    Args:
        error: The exception to handle and display
    """
    console.print(f"[red]Error: {error}[/red]")


def show_success_message(message):
    """
    Helper function to display success messages consistently.

    Args:
        message: Success message to display
    """
    console.print(f"[green]✓ {message}[/green]")


def show_cancelled_message():
    """Helper function to display cancellation message consistently."""
    console.print("[yellow]Cancelled[/yellow]")


def show_welcome():
    """Display welcome message with Rich formatting."""
    welcome_text = Text("Todo App -Interactive Cli Application", style="bold cyan")
    console.print(Panel(welcome_text, border_style="cyan"))


def show_main_menu() -> Optional[str]:
    """
    Display main menu and get user selection using arrow keys.

    Returns:
        Selected menu option, or None if user cancelled (Esc)
    """
    import questionary

    choices = [
        "Add todo",
        "List all todos",
        "View statistics",
        "Search todos",
        "Filter by category",
        "Filter by tag",
        "Advanced filter",
        "Complete todo",
        "Update todo",
        "Delete todo",
        "Undo last action",
        "Help",
        "Exit"
    ]

    answer = questionary.select(
        "What would you like to do?",
        choices=choices
    ).ask()

    return answer


def rich_add_workflow(storage: TodoStorage, undo_mgr: UndoManager):
    """Interactive workflow for adding a todo with Rich UI."""
    console.print("\n[bold cyan]Add New Todo[/bold cyan]")

    # Get title
    title = prompt_text_input("Enter todo title:")
    if title is None:
        show_cancelled_message()
        return

    # Get priority (optional)
    priority = prompt_priority_selection("Select priority (optional):")

    # Get due date (optional)
    due_date_str = prompt_text_input("Enter due date (optional, e.g., 'tomorrow', '2024-12-31'):")
    due_date = None
    if due_date_str:
        try:
            due_date = parse_due_date(due_date_str)
        except DateParseError as e:
            console.print(f"[yellow]Warning: {e}. Skipping due date.[/yellow]")

    # Get category (optional)
    category = prompt_text_input("Enter category (optional):")
    if category is not None and category.strip() == "":
        category = None

    # Get tags (optional)
    tags_str = prompt_text_input("Enter tags (comma-separated, optional):")
    tags = []
    if tags_str:
        # Split by comma and clean up whitespace
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

    # Record undo action before adding
    undo_mgr.record_action("add", storage.next_id, storage)

    # Add todo
    try:
        from src.cli import handle_add
        result = handle_add(storage, title)

        # Update with optional fields
        todo_id = storage.next_id - 1  # Last added ID
        if todo_id in storage.todos:
            todo = storage.todos[todo_id]
            if priority:
                todo.priority = priority
            if due_date:
                todo.due_date = due_date
            if category:
                todo.category = category
            if tags:
                todo.tags = tags

        show_success_message(result)
    except (TodoError, ValidationError) as e:
        handle_operation_error(e)


def rich_list_workflow(storage: TodoStorage):
    """Interactive workflow for listing todos with Rich table."""
    console.print("\n[bold cyan]All Todos[/bold cyan]\n")

    todos = storage.list_all()

    if not display_todos_table(todos, "No todos found. Start by adding one!"):
        return

    # Summary
    completed_count = sum(1 for t in todos if t.completed)
    console.print(f"[dim]Total: {len(todos)} todos ({completed_count} completed)[/dim]")


def rich_statistics_workflow(storage: TodoStorage):
    """Interactive workflow for viewing statistics dashboard."""
    from src.ui.panels import render_statistics_panel

    console.print("\n[bold cyan]Statistics Dashboard[/bold cyan]\n")

    # Render statistics panel
    panel = render_statistics_panel(storage)
    console.print(panel)
    console.print()


def rich_complete_workflow(storage: TodoStorage, undo_mgr: UndoManager):
    """Interactive workflow for completing a todo."""
    console.print("\n[bold cyan]Complete Todo[/bold cyan]")

    # Get incomplete todos
    todos = [t for t in storage.list_all() if not t.completed]

    if not display_todos_table(todos, "No incomplete todos found!"):
        return

    # Prompt for selection
    todo_id = prompt_task_selection(todos, "Select todo to complete:")
    if todo_id is None:
        show_cancelled_message()
        return

    # Record undo action before completing
    undo_mgr.record_action("complete", todo_id, storage)

    # Complete the todo
    try:
        from src.cli import handle_complete
        result = handle_complete(storage, todo_id)
        show_success_message(result)
    except NotFoundError as e:
        handle_operation_error(e)


def rich_update_workflow(storage: TodoStorage, undo_mgr: UndoManager):
    """Interactive workflow for updating a todo."""
    console.print("\n[bold cyan]Update Todo[/bold cyan]")

    todos = storage.list_all()

    if not display_todos_table(todos, "No todos found!"):
        return

    # Prompt for selection
    todo_id = prompt_task_selection(todos, "Select todo to update:")
    if todo_id is None:
        show_cancelled_message()
        return

    # Get new title
    new_title = prompt_text_input("Enter new title:")
    if new_title is None:
        show_cancelled_message()
        return

    # Record undo action before updating
    undo_mgr.record_action("update", todo_id, storage)

    # Update the todo
    try:
        from src.cli import handle_update
        result = handle_update(storage, todo_id, new_title)
        show_success_message(result)
    except (NotFoundError, ValidationError) as e:
        handle_operation_error(e)


def rich_delete_workflow(storage: TodoStorage, undo_mgr: UndoManager):
    """Interactive workflow for deleting a todo."""
    console.print("\n[bold cyan]Delete Todo[/bold cyan]")

    todos = storage.list_all()

    if not display_todos_table(todos, "No todos found!"):
        return

    # Prompt for selection
    todo_id = prompt_task_selection(todos, "Select todo to delete:")
    if todo_id is None:
        show_cancelled_message()
        return

    # Confirm deletion
    if not prompt_confirmation("Are you sure you want to delete this todo?"):
        show_cancelled_message()
        return

    # Record undo action before deleting
    undo_mgr.record_action("delete", todo_id, storage)

    # Delete the todo
    try:
        from src.cli import handle_delete
        result = handle_delete(storage, todo_id)
        show_success_message(result)
    except NotFoundError as e:
        handle_operation_error(e)


def rich_undo_workflow(storage: TodoStorage, undo_mgr: UndoManager):
    """Interactive workflow for undoing the last action."""
    console.print("\n[bold cyan]Undo Last Action[/bold cyan]")

    # Check if undo is available
    if not undo_mgr.can_undo():
        console.print("[yellow]No action to undo[/yellow]")
        return

    # Show what will be undone
    description = undo_mgr.get_undo_description()
    console.print(f"\n[dim]{description}[/dim]")

    # Confirm undo
    if not prompt_confirmation("Do you want to undo this action?"):
        show_cancelled_message()
        return

    # Perform undo
    try:
        message = undo_mgr.undo(storage)
        show_success_message(message)
    except ValueError as e:
        handle_operation_error(e)


def rich_help_workflow():
    """Display help information with available commands and shortcuts."""
    from rich.table import Table
    from rich.panel import Panel
    from rich.console import Group

    console.print("\n[bold cyan]Help - Available Commands[/bold cyan]\n")

    # Create help table
    help_table = Table(show_header=True, box=None, padding=(0, 2))
    help_table.add_column("Command", style="cyan", no_wrap=True)
    help_table.add_column("Description", style="white")

    # Add commands
    help_table.add_row("Add todo", "Create a new todo with title, priority, due date, category, and tags")
    help_table.add_row("List all todos", "Display all todos in a formatted table")
    help_table.add_row("View statistics", "Show completion stats, priority breakdown, and overdue count")
    help_table.add_row("Search todos", "Search todos by keyword (case-insensitive)")
    help_table.add_row("Filter by category", "Filter todos by category name")
    help_table.add_row("Filter by tag", "Filter todos by tag name")
    help_table.add_row("Advanced filter", "Apply multiple filters (status, priority, category, tag, due date)")
    help_table.add_row("Complete todo", "Mark a todo as completed")
    help_table.add_row("Update todo", "Change the title of a todo")
    help_table.add_row("Delete todo", "Remove a todo permanently")
    help_table.add_row("Undo last action", "Undo the last add/delete/update/complete operation")
    help_table.add_row("Help", "Show this help screen")
    help_table.add_row("Exit", "Exit the application")

    # Add keyboard shortcuts
    shortcuts = Table(show_header=True, box=None, padding=(0, 2))
    shortcuts.add_column("Key", style="cyan", no_wrap=True)
    shortcuts.add_column("Action", style="white")

    shortcuts.add_row("Up/Down Arrow", "Navigate menu options")
    shortcuts.add_row("Enter", "Select highlighted option")
    shortcuts.add_row("Esc", "Cancel current operation and return to menu")
    shortcuts.add_row("Ctrl+C", "Exit application")

    # Group tables
    content = Group(
        help_table,
        "",
        Text("Keyboard Shortcuts", style="bold cyan"),
        "",
        shortcuts,
        "",
        Text("Tip: You can cancel any operation by pressing Esc", style="dim italic")
    )

    # Display in panel
    panel = Panel(content, title="📖 Help Guide", border_style="cyan", padding=(1, 2))
    console.print(panel)
    console.print()


def rich_filter_by_category_workflow(storage: TodoStorage):
    """Interactive workflow for filtering todos by category."""
    console.print("\n[bold cyan]Filter by Category[/bold cyan]")

    # Get category input
    category = prompt_text_input("Enter category to filter (or press Esc to cancel):")
    if category is None:
        show_cancelled_message()
        return

    # Filter todos
    from src.services.search_filter import SearchFilterService
    try:
        service = SearchFilterService(storage)
        filtered_todos = service.filter_by_category(category)

        if not filtered_todos:
            console.print(f"\n[yellow]No todos found with category '{category}'[/yellow]")
            return

        # Display filtered results
        console.print(f"\n[bold]Todos in category '{category}':[/bold]\n")
        if not display_todos_table(filtered_todos):
            return

        console.print(f"[dim]Found {len(filtered_todos)} todo(s) in category '{category}'[/dim]")
    except ValueError as e:
        handle_operation_error(e)


def rich_filter_by_tag_workflow(storage: TodoStorage):
    """Interactive workflow for filtering todos by tag."""
    console.print("\n[bold cyan]Filter by Tag[/bold cyan]")

    # Get tag input
    tag = prompt_text_input("Enter tag to filter (or press Esc to cancel):")
    if tag is None:
        show_cancelled_message()
        return

    # Filter todos
    from src.services.search_filter import SearchFilterService
    try:
        service = SearchFilterService(storage)
        filtered_todos = service.filter_by_tag(tag)

        if not filtered_todos:
            console.print(f"\n[yellow]No todos found with tag '{tag}'[/yellow]")
            return

        # Display filtered results
        console.print(f"\n[bold]Todos with tag '{tag}':[/bold]\n")
        if not display_todos_table(filtered_todos):
            return

        console.print(f"[dim]Found {len(filtered_todos)} todo(s) with tag '{tag}'[/dim]")
    except ValueError as e:
        handle_operation_error(e)


def rich_search_workflow(storage: TodoStorage):
    """Interactive workflow for searching todos by keyword."""
    console.print("\n[bold cyan]Search Todos[/bold cyan]")

    # Get search query
    query = prompt_text_input("Enter search keyword (or press Esc to cancel):")
    if query is None:
        show_cancelled_message()
        return

    # Search todos
    from src.services.search_filter import SearchFilterService
    try:
        service = SearchFilterService(storage)
        results = service.search(query)

        if not results:
            console.print(f"\n[yellow]No todos found matching '{query}'[/yellow]")
            return

        # Display search results
        console.print(f"\n[bold]Search results for '{query}':[/bold]\n")
        if not display_todos_table(results):
            return

        console.print(f"[dim]Found {len(results)} todo(s) matching '{query}'[/dim]")
    except ValueError as e:
        handle_operation_error(e)


def rich_advanced_filter_workflow(storage: TodoStorage):
    """Interactive workflow for applying multiple filters with AND logic."""
    import questionary

    console.print("\n[bold cyan]Advanced Filter[/bold cyan]")
    console.print("[dim]Select multiple criteria (todos must match ALL selected criteria)[/dim]\n")

    criteria = {}

    # Filter by status
    status = questionary.select(
        "Filter by status:",
        choices=["all", "incomplete", "completed"]
    ).ask()
    if status is None:
        show_cancelled_message()
        return
    if status != "all":
        criteria["status"] = status

    # Filter by priority
    priority = questionary.select(
        "Filter by priority:",
        choices=["Any", "High", "Medium", "Low", "None"]
    ).ask()
    if priority is None:
        show_cancelled_message()
        return
    if priority != "Any":
        criteria["priority"] = priority

    # Filter by category
    category_input = prompt_text_input("Filter by category (leave empty to skip):")
    if category_input is None:
        show_cancelled_message()
        return
    if category_input.strip():
        criteria["category"] = category_input.strip()

    # Filter by tag
    tag_input = prompt_text_input("Filter by tag (leave empty to skip):")
    if tag_input is None:
        show_cancelled_message()
        return
    if tag_input.strip():
        criteria["tag"] = tag_input.strip()

    # Filter by due date range
    due_date_range = questionary.select(
        "Filter by due date:",
        choices=["Any", "Overdue", "Today", "This week", "This month", "No due date"]
    ).ask()
    if due_date_range is None:
        show_cancelled_message()
        return

    if due_date_range != "Any":
        range_map = {
            "Overdue": "overdue",
            "Today": "today",
            "This week": "week",
            "This month": "month",
            "No due date": "none"
        }
        criteria["due_date_range"] = range_map[due_date_range]

    # Apply filters
    from src.services.search_filter import SearchFilterService
    try:
        service = SearchFilterService(storage)
        results = service.apply_combined_filters(criteria)

        if not results:
            console.print(f"\n[yellow]No todos match the selected criteria[/yellow]")
            return

        # Display filtered results
        console.print(f"\n[bold]Filtered Results:[/bold]\n")
        if not display_todos_table(results):
            return

        # Show criteria summary
        console.print(f"\n[dim]Found {len(results)} todo(s) matching criteria:")
        for key, value in criteria.items():
            console.print(f"  • {key.replace('_', ' ').title()}: {value}")
        console.print("[/dim]")

    except ValueError as e:
        handle_operation_error(e)


def main_loop():
    """
    Main interactive menu loop.

    Runs until user selects Exit or presses Ctrl+C.
    Handles Esc key gracefully by returning to main menu.
    """
    storage = TodoStorage()
    undo_mgr = UndoManager()

    try:
        show_welcome()

        while True:
            try:
                # Show main menu
                choice = show_main_menu()

                # Handle cancellation (Esc key)
                if choice is None:
                    console.print("\n[yellow]Use arrow keys to navigate, Enter to select, or choose Exit to quit[/yellow]")
                    continue

                # Route to appropriate workflow
                if choice == "Add todo":
                    rich_add_workflow(storage, undo_mgr)
                elif choice == "List all todos":
                    rich_list_workflow(storage)
                elif choice == "View statistics":
                    rich_statistics_workflow(storage)
                elif choice == "Search todos":
                    rich_search_workflow(storage)
                elif choice == "Filter by category":
                    rich_filter_by_category_workflow(storage)
                elif choice == "Filter by tag":
                    rich_filter_by_tag_workflow(storage)
                elif choice == "Advanced filter":
                    rich_advanced_filter_workflow(storage)
                elif choice == "Complete todo":
                    rich_complete_workflow(storage, undo_mgr)
                elif choice == "Update todo":
                    rich_update_workflow(storage, undo_mgr)
                elif choice == "Delete todo":
                    rich_delete_workflow(storage, undo_mgr)
                elif choice == "Undo last action":
                    rich_undo_workflow(storage, undo_mgr)
                elif choice == "Help":
                    rich_help_workflow()
                elif choice == "Exit":
                    # Confirm exit
                    if prompt_confirmation("Are you sure you want to exit?"):
                        console.print("\n[cyan]Goodbye! 👋[/cyan]")
                        break
                    else:
                        continue

            except KeyboardInterrupt:
                # Handle Ctrl+C during menu selection
                console.print("\n[yellow]Operation cancelled. Returning to main menu...[/yellow]")
                continue

    except KeyboardInterrupt:
        # Handle Ctrl+C at top level
        console.print("\n\n[cyan]Goodbye! 👋[/cyan]")
        sys.exit(0)


if __name__ == "__main__":
    main_loop()
