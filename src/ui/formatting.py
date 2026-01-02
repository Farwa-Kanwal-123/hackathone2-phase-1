"""
UI formatting helpers and constants

Provides color schemes, status badges, and text formatting utilities for Rich library.
"""

from datetime import date
from typing import Optional, List
from rich.table import Table
from rich.box import ROUNDED
from src.todo import TodoItem

# Priority colors
PRIORITY_COLORS = {
    "High": "red",
    "Medium": "yellow",
    "Low": "green",
    None: "dim"
}

# Status icons
STATUS_ICONS = {
    True: "✓",   # Completed
    False: "[ ]"  # Incomplete
}

# Due date colors
DUE_DATE_COLORS = {
    "overdue": "red",
    "today": "#FFA500",  # Orange
    "upcoming": "white",
    "no_date": "dim"
}


def format_priority(priority: Optional[str]) -> str:
    """
    Format priority with color markup.

    Args:
        priority: "High", "Medium", "Low", or None

    Returns:
        Rich markup string (e.g., "[red]High[/red]")

    Example:
        >>> format_priority("High")
        "[red]High[/red]"
    """
    if priority is None:
        return "[dim]-[/dim]"

    color = PRIORITY_COLORS.get(priority, "white")
    return f"[{color}]{priority}[/{color}]"


def format_due_date(due_date: Optional[date]) -> tuple[str, str]:
    """
    Format due date with appropriate color.

    Args:
        due_date: date object or None

    Returns:
        Tuple of (formatted_text, color)
        e.g., ("Today", "#FFA500") or ("2025-12-31", "white")

    Example:
        >>> from datetime import date
        >>> format_due_date(date(2025, 12, 31))
        ("2025-12-31", "white")
    """
    if due_date is None:
        return ("-", "dim")

    today = date.today()

    if due_date < today:
        # Overdue
        return (due_date.isoformat(), "red")
    elif due_date == today:
        # Due today
        return ("Today", "#FFA500")
    else:
        # Future date
        return (due_date.isoformat(), "white")


def get_due_date_status(due_date: Optional[date]) -> str:
    """
    Get due date status for filtering/sorting.

    Args:
        due_date: date object or None

    Returns:
        "overdue", "today", "upcoming", or "no_date"
    """
    if due_date is None:
        return "no_date"

    today = date.today()

    if due_date < today:
        return "overdue"
    elif due_date == today:
        return "today"
    else:
        return "upcoming"


def days_until_due(due_date: Optional[date]) -> Optional[int]:
    """
    Calculate days until due date.

    Args:
        due_date: date object or None

    Returns:
        Number of days until due (negative if overdue, None if no date)
    """
    if due_date is None:
        return None

    return (due_date - date.today()).days


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to max length with suffix.

    Args:
        text: Text to truncate
        max_length: Maximum length (including suffix)
        suffix: Suffix for truncated text (default: "...")

    Returns:
        Truncated text

    Example:
        >>> truncate_text("Very long title here", 15)
        "Very long ti..."
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def render_task_table(todos: List[TodoItem]) -> Table:
    """
    Render todos as a Rich Table with formatting.

    Args:
        todos: List of TodoItem objects to render

    Returns:
        Rich Table object ready for console display

    Example:
        >>> from rich.console import Console
        >>> console = Console()
        >>> table = render_task_table(todos)
        >>> console.print(table)
    """
    # Create table with rounded box style
    table = Table(
        box=ROUNDED,
        border_style="blue",
        header_style="bold cyan"
    )

    # Add columns
    table.add_column("ID", justify="right", style="dim", width=4)
    table.add_column("✓", justify="center", width=3)
    table.add_column("Title", style="white", no_wrap=False, width=40)
    table.add_column("Priority", justify="center", width=10)
    table.add_column("Due Date", justify="center", width=12)
    table.add_column("Category", justify="center", width=12)

    # Add rows
    for todo in todos:
        # Format status icon
        status_icon = STATUS_ICONS[todo.completed]
        status_style = "green" if todo.completed else "white"

        # Format title (truncate if needed)
        title = truncate_text(todo.title, 40)
        title_style = "dim strike" if todo.completed else "white"

        # Format priority
        priority_text = format_priority(todo.priority)

        # Format due date
        due_text, due_color = format_due_date(todo.due_date)
        due_formatted = f"[{due_color}]{due_text}[/{due_color}]"

        # Format category
        category_text = todo.category if todo.category else "[dim]-[/dim]"

        # Add row to table
        table.add_row(
            str(todo.id),
            f"[{status_style}]{status_icon}[/{status_style}]",
            f"[{title_style}]{title}[/{title_style}]",
            priority_text,
            due_formatted,
            category_text
        )

    return table
