"""
UI panels for rich displays

Provides panel-based displays using Rich library components.
"""

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.text import Text
from src.storage import TodoStorage
from src.services.statistics import StatisticsService


def render_alert_panel(message: str, alert_type: str = "info") -> Panel:
    """
    Render alert panel with icon and colored border.

    Args:
        message: Alert message to display
        alert_type: Type of alert ("success", "error", "warning", "info")

    Returns:
        Rich Panel with formatted alert

    Raises:
        ValueError: If alert_type is invalid

    Example:
        >>> panel = render_alert_panel("Task completed!", alert_type="success")
        >>> console.print(panel)
    """
    valid_types = ["success", "error", "warning", "info"]
    if alert_type not in valid_types:
        raise ValueError(
            f"alert_type must be one of {valid_types}. Got: {alert_type}"
        )

    # Map alert types to icons and colors
    alert_config = {
        "success": {"icon": "✓", "color": "green", "title": "Success"},
        "error": {"icon": "✗", "color": "red", "title": "Error"},
        "warning": {"icon": "⚠", "color": "yellow", "title": "Warning"},
        "info": {"icon": "ℹ", "color": "blue", "title": "Info"}
    }

    config = alert_config[alert_type]
    icon = config["icon"]
    color = config["color"]
    title = config["title"]

    # Create formatted message with icon
    formatted_message = f"{icon}  {message}"

    return Panel(
        formatted_message,
        title=title,
        border_style=color,
        padding=(0, 1)
    )


def render_statistics_panel(storage: TodoStorage) -> Panel:
    """
    Render statistics dashboard panel with progress bars and breakdowns.

    Args:
        storage: TodoStorage instance

    Returns:
        Rich Panel with formatted statistics

    Example:
        >>> panel = render_statistics_panel(storage)
        >>> console.print(panel)
    """
    console = Console()
    service = StatisticsService(storage)

    # Get statistics
    completion_stats = service.get_completion_stats()
    priority_breakdown = service.get_priority_breakdown()
    category_breakdown = service.get_category_breakdown()
    overdue_count = service.get_overdue_count()

    # Create layout
    content = []

    # Completion progress bar
    content.append(Text("Completion Progress", style="bold cyan"))
    content.append("")

    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        expand=False
    )

    total = completion_stats["total"]
    completed = completion_stats["completed"]
    incomplete = completion_stats["incomplete"]
    percentage = completion_stats["percentage"]

    # Manually create progress bar representation
    bar_width = 40
    filled = int(bar_width * percentage / 100)
    bar = "█" * filled + "░" * (bar_width - filled)

    content.append(Text(f"Progress: {bar} {percentage:.0f}%", style="green"))
    content.append(Text(f"Total: {total} | Completed: {completed} | Incomplete: {incomplete}", style="dim"))
    content.append("")

    # Priority breakdown
    content.append(Text("Priority Breakdown", style="bold cyan"))
    content.append("")

    priority_table = Table(show_header=False, box=None, padding=(0, 2))
    priority_table.add_column("Priority", style="cyan")
    priority_table.add_column("Count", justify="right")

    for priority, count in priority_breakdown.items():
        priority_style = {
            "High": "red",
            "Medium": "yellow",
            "Low": "green",
            "None": "dim"
        }.get(priority, "white")

        priority_table.add_row(
            Text(priority, style=priority_style),
            str(count)
        )

    content.append(priority_table)
    content.append("")

    # Category breakdown
    if category_breakdown:
        content.append(Text("Category Breakdown", style="bold cyan"))
        content.append("")

        category_table = Table(show_header=False, box=None, padding=(0, 2))
        category_table.add_column("Category", style="cyan")
        category_table.add_column("Count", justify="right")

        for category, count in category_breakdown.items():
            category_style = "dim" if category == "Uncategorized" else "white"
            category_table.add_row(
                Text(category, style=category_style),
                str(count)
            )

        content.append(category_table)
        content.append("")

    # Overdue count
    if overdue_count > 0:
        content.append(Text(f"⚠️  Overdue Tasks: {overdue_count}", style="bold red"))
    else:
        content.append(Text("✓ No overdue tasks", style="green"))

    # Create panel
    from rich.console import Group
    panel_content = Group(*content)

    return Panel(
        panel_content,
        title="📊 Todo Statistics Dashboard",
        border_style="cyan",
        padding=(1, 2)
    )
