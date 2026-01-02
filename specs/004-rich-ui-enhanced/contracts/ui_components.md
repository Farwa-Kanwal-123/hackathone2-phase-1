# UI Components Contract

**Feature**: 004-rich-ui-enhanced
**Module**: `src/ui/`
**Purpose**: Define interfaces for Rich library UI components

## Overview

This contract defines the rendering interfaces for visual UI components using the Rich library. All components are pure functions that take data and return rendered output via Rich Console.

---

## Module: `src/ui/tables.py`

### `render_task_table`

**Purpose**: Render todos in a Rich table with colored status, priority, and dates

**Signature**:
```python
from rich.console import Console
from typing import List, Optional
from src.todo import TodoItem

def render_task_table(
    todos: List[TodoItem],
    console: Console,
    title: str = "Your Tasks",
    show_stats: bool = True
) -> None:
    """
    Render todos in a rich table format.

    Args:
        todos: List of TodoItem objects to display
        console: Rich Console instance for output
        title: Table title (default: "Your Tasks")
        show_stats: Whether to show statistics below table (default: True)

    Returns:
        None (output printed to console)

    Example:
        >>> from rich.console import Console
        >>> console = Console()
        >>> todos = [TodoItem(id=1, title="Test", priority="High")]
        >>> render_task_table(todos, console)
        # Outputs:
        # ┌─────┬─────────┬──────────┬───────────┬──────────┬──────────┐
        # │  ID │ Status  │ Priority │   Title   │ Due Date │ Category │
        # ├─────┼─────────┼──────────┼───────────┼──────────┼──────────┤
        # │  1  │  [ ]    │   High   │   Test    │    -     │    -     │
        # └─────┴─────────┴──────────┴───────────┴──────────┴──────────┘
    """
```

**Column Specifications**:
| Column | Width | Alignment | Content | Color |
|--------|-------|-----------|---------|-------|
| ID | Auto | Right | todo.id | Cyan |
| Status | 9 | Center | ✓ or [ ] | Green (complete) / White (incomplete) |
| Priority | 10 | Center | High/Med/Low/- | Red/Yellow/Green/Dim |
| Title | 40 | Left | todo.title (truncate if >40) | White |
| Due Date | 12 | Center | YYYY-MM-DD or "Today" or "-" | Red (overdue) / Orange (today) / White (future) / Dim (none) |
| Category | 15 | Left | todo.category or "-" | Blue |

**Table Styling**:
- Box style: `rich.box.ROUNDED`
- Title style: `bold cyan`
- Header style: `bold white on blue`
- Border style: `blue`

**Statistics Footer** (if `show_stats=True`):
```
Total: 10 | Completed: 3 (30%) | Overdue: 2
```

---

### `render_task_detail`

**Purpose**: Render single todo with full details (no truncation)

**Signature**:
```python
def render_task_detail(
    todo: TodoItem,
    console: Console
) -> None:
    """
    Render a single todo with full details.

    Args:
        todo: TodoItem to display
        console: Rich Console instance

    Example:
        >>> render_task_detail(todo, console)
        # Outputs:
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #  Task #5
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        #  Title:     Fix authentication bug
        #  Status:    [ ] Incomplete
        #  Priority:  🔴 High
        #  Due:       2025-12-31 (2 days)
        #  Category:  Work
        #  Tags:      urgent, security
        #  Created:   2025-12-29 10:30
        #  Updated:   2025-12-29 14:45
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
```

---

## Module: `src/ui/panels.py`

### `render_statistics_panel`

**Purpose**: Render statistics panel with progress bar and breakdowns

**Signature**:
```python
from src.services.statistics import StatisticsService

def render_statistics_panel(
    stats_service: StatisticsService,
    console: Console
) -> None:
    """
    Render statistics panel with visual progress bar.

    Args:
        stats_service: StatisticsService instance (calculates stats)
        console: Rich Console instance

    Example:
        >>> from src.services.statistics import StatisticsService
        >>> stats = StatisticsService(storage)
        >>> render_statistics_panel(stats, console)
        # Outputs:
        # ╭─────────────────── Statistics ────────────────────╮
        # │                                                    │
        # │  Progress:  ━━━━━━━━━━░░░░░░░░░░  40% (4/10)     │
        # │                                                    │
        # │  By Priority:                                      │
        # │    🔴 High:    2 tasks                            │
        # │    🟡 Medium:  5 tasks                            │
        # │    🟢 Low:     3 tasks                            │
        # │                                                    │
        # │  By Status:                                        │
        # │    ✅ Complete:    4 tasks                        │
        # │    ⏳ Incomplete:  6 tasks                        │
        # │    🔥 Overdue:     2 tasks                        │
        # │                                                    │
        # ╰────────────────────────────────────────────────────╯
    """
```

**Panel Styling**:
- Box style: `rich.box.ROUNDED`
- Border color: `blue`
- Title style: `bold white on blue`
- Progress bar: Green (completed) / Dim (remaining)

---

### `render_alert_panel`

**Purpose**: Render colored alert panels (success, error, warning, info)

**Signature**:
```python
def render_alert_panel(
    message: str,
    alert_type: str,
    console: Console,
    title: Optional[str] = None
) -> None:
    """
    Render colored alert panel.

    Args:
        message: Alert message text
        alert_type: "success", "error", "warning", or "info"
        console: Rich Console instance
        title: Optional title (default: auto-generated from type)

    Example:
        >>> render_alert_panel("Task deleted successfully", "success", console)
        # Outputs:
        # ╭───────────── ✅ Success ─────────────╮
        # │  Task deleted successfully            │
        # ╰───────────────────────────────────────╯
    """
```

**Alert Types**:
| Type | Icon | Border Color | Title Color |
|------|------|--------------|-------------|
| success | ✅ | green | bold green |
| error | ❌ | red | bold red |
| warning | ⚠️ | yellow | bold yellow |
| info | ℹ️ | blue | bold blue |

---

## Module: `src/ui/prompts.py`

### `prompt_task_selection`

**Purpose**: Interactive task selection with arrow keys

**Signature**:
```python
import questionary

def prompt_task_selection(
    todos: List[TodoItem],
    prompt_text: str = "Select a task:"
) -> Optional[int]:
    """
    Prompt user to select a task using arrow keys.

    Args:
        todos: List of TodoItem objects to choose from
        prompt_text: Prompt message (default: "Select a task:")

    Returns:
        Selected todo ID, or None if cancelled (Ctrl+C / Esc)

    Example:
        >>> todos = storage.list_all()
        >>> selected_id = prompt_task_selection(todos)
        # User sees:
        # ? Select a task: (Use arrow keys)
        #   1. [ ] Buy milk (Medium)
        # ❯ 2. [x] Fix bug (High) - Due: Today
        #   3. [ ] Write report (Low)
    """
```

**Choice Format**:
```
{id}. [{status}] {title} ({priority}) - Due: {due_date_text}
```

---

### `prompt_priority_selection`

**Purpose**: Select priority level with arrow keys

**Signature**:
```python
def prompt_priority_selection() -> Optional[str]:
    """
    Prompt user to select priority level.

    Returns:
        "High", "Medium", "Low", or None if cancelled

    Example:
        >>> priority = prompt_priority_selection()
        # User sees:
        # ? Select priority: (Use arrow keys)
        #   🔴 High
        # ❯ 🟡 Medium
        #   🟢 Low
        #   ⚪ No Priority
    """
```

---

### `prompt_filter_criteria`

**Purpose**: Multi-select checkboxes for filter criteria

**Signature**:
```python
def prompt_filter_criteria() -> dict:
    """
    Prompt user to select filter criteria (checkbox multi-select).

    Returns:
        Dictionary with filter settings:
        {
            "priorities": ["High", "Medium"],  # Selected priorities
            "statuses": ["Incomplete"],         # Selected statuses
            "categories": ["Work"],             # Selected categories
            "date_range": "overdue"             # Date filter
        }

    Example:
        >>> filters = prompt_filter_criteria()
        # User sees:
        # ? Filter by: (Use arrow keys and space to select)
        #   ◯ High Priority
        #   ◉ Medium Priority
        #   ◯ Low Priority
        #   ◉ Incomplete
        #   ◯ Completed
        #   ◯ Overdue
    """
```

---

## Module: `src/ui/formatting.py`

### Constants and Helpers

**Purpose**: Color schemes, status badges, and formatting utilities

**Constants**:
```python
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
    "today": "orange",
    "upcoming": "white",
    "no_date": "dim"
}
```

**Functions**:
```python
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

def format_due_date(due_date: Optional[date]) -> tuple[str, str]:
    """
    Format due date with appropriate color.

    Args:
        due_date: date object or None

    Returns:
        Tuple of (formatted_text, color)
        e.g., ("Today", "orange") or ("2025-12-31", "white")

    Example:
        >>> format_due_date(date(2025, 12, 31))
        ("2025-12-31", "white")
    """

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
```

---

## Contract Tests

**Location**: `tests/contract/test_ui_contracts.py`

**Purpose**: Verify all UI functions adhere to their contracts

**Test Cases**:
1. `test_render_task_table_contract` - Verify table renders without errors
2. `test_render_statistics_panel_contract` - Verify panel renders with stats
3. `test_prompt_task_selection_contract` - Verify prompts return expected types
4. `test_format_priority_contract` - Verify color markup is valid Rich syntax
5. `test_truncate_text_contract` - Verify truncation respects max_length

**Example Test**:
```python
import pytest
from rich.console import Console
from io import StringIO
from src.ui.tables import render_task_table
from src.todo import TodoItem

def test_render_task_table_contract():
    """Verify render_task_table adheres to contract"""
    # Arrange
    todos = [
        TodoItem(id=1, title="Test", priority="High"),
        TodoItem(id=2, title="Test 2", priority="Low")
    ]
    output = StringIO()
    console = Console(file=output, force_terminal=True)

    # Act
    render_task_table(todos, console, show_stats=False)

    # Assert
    result = output.getvalue()
    assert "ID" in result
    assert "Status" in result
    assert "Priority" in result
    assert "Test" in result
    assert "High" in result
```

---

## Summary

**UI Component Contracts**:
- ✅ `tables.py` - Task table and detail rendering
- ✅ `panels.py` - Statistics and alert panels
- ✅ `prompts.py` - Interactive selection prompts
- ✅ `formatting.py` - Color schemes and text formatting

**Key Principles**:
- Pure functions (no side effects beyond console output)
- Rich Console dependency injection (testable with StringIO)
- Consistent color scheme across all components
- Clear separation: data (TodoItem) → formatting (ui/) → output (console)

**Next**: `filter_service.md` contract for search/filter/sort operations
