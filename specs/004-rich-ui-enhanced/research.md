# Research: Enhanced Todo Console with Rich UI

**Feature**: 004-rich-ui-enhanced
**Date**: 2025-12-29
**Purpose**: Document technology decisions, best practices, and design patterns for rich UI implementation

## Technology Decisions

### 1. Rich Library for Terminal UI

**Decision**: Use `rich 13.0+` for all visual UI components

**Rationale**:
- **Industry Standard**: Most popular Python terminal UI library (40k+ GitHub stars)
- **Comprehensive Features**: Tables, panels, progress bars, syntax highlighting, live updates, spinners
- **ANSI/Unicode Support**: Built-in color schemes, emoji support, box drawing characters
- **Performance**: Efficient rendering with minimal overhead
- **Cross-platform**: Works on Windows/macOS/Linux terminals
- **Well-documented**: Extensive docs, examples, active community
- **No Breaking Changes**: Stable API since v10, backward compatible

**Alternatives Considered**:
- **blessed** - Lower-level, more complex API, requires manual layout management
- **urwid** - More powerful but overly complex for CLI tables/panels, steeper learning curve
- **colorama** - Only handles colors, would need additional libraries for tables/panels
- **tabulate** - Only handles tables, no progress bars, panels, or interactive features

**Best Practices** (from Rich documentation):
- Use `Console()` instance for all output (thread-safe, buffered)
- Use `Table()` with box styles (SIMPLE, ROUNDED, HEAVY) for task display
- Use `Panel()` with borders for statistics sections
- Use `Progress()` for loading animations (not multi-threaded for Phase 1)
- Use `Text()` with markup for colored status badges: `[red]High[/red]`, `[green]✓ Complete[/green]`
- Use `rich.prompt.Prompt` for simple text input (fallback if questionary unavailable)

**Implementation Patterns**:
```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

console = Console()

# Task table with colors
table = Table(title="Your Tasks", box=ROUNDED)
table.add_column("ID", style="cyan")
table.add_column("Status", style="magenta")
table.add_column("Priority", style="bold")
table.add_column("Title")
table.add_row("1", "[green]✓[/green]", "[red]High[/red]", "Fix bug")
console.print(table)

# Statistics panel
stats_panel = Panel(
    "[green]5 completed[/green] | [yellow]3 in progress[/yellow] | [red]2 overdue[/red]",
    title="Statistics",
    border_style="blue"
)
console.print(stats_panel)
```

**Integration Strategy**:
- Create `src/ui/formatting.py` - Color scheme constants, status badge mappings
- Create `src/ui/tables.py` - Task table rendering functions
- Create `src/ui/panels.py` - Statistics panel, progress bar rendering
- Isolate Rich imports to `ui/` module - makes testing easier (mock console output)

---

### 2. Questionary for Interactive Prompts

**Decision**: Use `questionary 2.0+` for arrow-key navigation menus

**Rationale**:
- **Interactive UX**: Built-in arrow key support, highlight current selection, Enter to confirm
- **Rich Integration**: Compatible with rich library (shares ANSI terminal capabilities)
- **Multiple Input Types**: Select, checkbox, confirm, text, password, autocomplete
- **Validation**: Built-in validators, custom validation functions
- **Keyboard Shortcuts**: Ctrl+C graceful exit, Esc to cancel
- **Styling**: Customizable colors, prompts, instructions

**Alternatives Considered**:
- **PyInquirer** - Unmaintained, last update 2019, dependency issues
- **inquirer** - Less polished UX, fewer prompt types
- **rich.prompt.Prompt** - Basic text input only, no arrow navigation
- **prompt_toolkit** - Lower-level library (questionary is built on this), more complex

**Best Practices** (from questionary documentation):
- Use `questionary.select()` for menu navigation (replaces numbered menu from feature 003)
- Use `questionary.checkbox()` for multi-select filters
- Use `questionary.autocomplete()` for category/tag selection
- Use `questionary.confirm()` for delete confirmations
- Use `questionary.text()` with validators for title/date input
- Style with `questionary.Style()` for consistent colors

**Implementation Patterns**:
```python
import questionary

# Menu selection with arrow keys
action = questionary.select(
    "What do you want to do?",
    choices=[
        "Add todo",
        "List todos",
        "Search todos",
        "Statistics",
        "Exit"
    ],
    instruction="(Use arrow keys)"
).ask()

# Multi-select for filters
filters = questionary.checkbox(
    "Filter by priority:",
    choices=["High", "Medium", "Low"]
).ask()

# Confirmation prompt
confirmed = questionary.confirm(
    "Delete this todo? This cannot be undone.",
    default=False
).ask()
```

**Integration Strategy**:
- Create `src/ui/prompts.py` - Questionary prompt wrappers
- Replace numbered menu in `src/interactive_menu.py` with questionary.select()
- Use for task selection (instead of typing IDs)
- Use for priority/category selection during add/update

**Fallback Strategy**:
- If questionary fails on a terminal (rare), fall back to `input()` with numbered options
- Maintain compatibility with basic terminals (no arrow key support)

---

### 3. Python-dateutil for Date Parsing

**Decision**: Use `python-dateutil 2.8+` for flexible date parsing

**Rationale**:
- **Natural Language Parsing**: Supports "tomorrow", "next week", "in 3 days"
- **Multiple Formats**: Parses YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, ISO 8601
- **Timezone Aware**: Handles timezones (not needed now, but future-proof)
- **Relative Dates**: `relativedelta` for date arithmetic
- **Robust**: Handles edge cases (leap years, month boundaries, invalid dates)
- **Standard Library Compatibility**: Works with `datetime.datetime` and `datetime.date`

**Alternatives Considered**:
- **datetime.strptime()** - Manual format parsing, no natural language, brittle
- **arrow** - More opinionated API, less flexible, additional dependency
- **pendulum** - Heavier library, timezone focus not needed
- **maya** - Unmaintained, last update 2019

**Best Practices** (from python-dateutil docs):
- Use `dateutil.parser.parse()` for flexible parsing (tries multiple formats)
- Use `parser.parse(fuzzy=True)` to extract dates from natural language text
- Validate with try/except and custom `DateParseError` exception
- Store dates as `datetime.date` (not datetime) for simplicity (no time component needed)
- Use `relativedelta` for "due in X days" calculations

**Implementation Patterns**:
```python
from dateutil import parser
from datetime import date, timedelta
from src.exceptions import DateParseError

def parse_due_date(user_input: str) -> date:
    """
    Parse user input into a date object.

    Accepts:
    - YYYY-MM-DD (2025-12-31)
    - MM/DD/YYYY (12/31/2025)
    - Natural language (tomorrow, next week, in 3 days)

    Returns:
        date object

    Raises:
        DateParseError: If parsing fails
    """
    try:
        # Try parsing with fuzzy=True (extracts date from natural language)
        parsed_dt = parser.parse(user_input, fuzzy=True)
        return parsed_dt.date()  # Extract date component
    except (ValueError, TypeError, parser.ParserError) as e:
        raise DateParseError(
            f"Could not parse '{user_input}' as a date. "
            f"Try: YYYY-MM-DD, 'tomorrow', 'next week', 'in 3 days'"
        ) from e

# Relative date shortcuts
def get_due_date_shortcuts():
    """Common date shortcuts for quick selection"""
    today = date.today()
    return {
        "today": today,
        "tomorrow": today + timedelta(days=1),
        "next week": today + timedelta(weeks=1),
        "next month": today + timedelta(days=30)
    }
```

**Integration Strategy**:
- Create `src/services/date_parser.py` - Date parsing logic
- Add `DateParseError` to `src/exceptions.py`
- Use in interactive prompts with validation
- Display date shortcuts in questionary autocomplete

**Error Handling**:
- Catch parsing errors and show clear examples
- Validate that parsed dates are not in the distant past (e.g., >1 year ago)
- Show formatted date back to user for confirmation

---

### 4. Design Patterns for Services Layer

**Decision**: Implement service layer with dependency injection pattern

**Rationale**:
- **Separation of Concerns**: Business logic (services/) separate from UI (ui/) and storage (storage.py)
- **Testability**: Services can be tested independently with mocked storage
- **Reusability**: Search/filter/sort logic used by both CLI and rich UI
- **Maintainability**: Single responsibility - each service has one purpose

**Service Patterns**:

**SearchFilterService** - Search, filter, sort operations
```python
class SearchFilterService:
    def __init__(self, storage: TodoStorage):
        self.storage = storage

    def search(self, query: str) -> List[TodoItem]:
        """Search titles for keyword (case-insensitive)"""
        todos = self.storage.list_all()
        return [t for t in todos if query.lower() in t.title.lower()]

    def filter_by_priority(self, priority: str) -> List[TodoItem]:
        """Filter by priority level"""
        todos = self.storage.list_all()
        return [t for t in todos if t.priority == priority]

    def sort_by_due_date(self, todos: List[TodoItem]) -> List[TodoItem]:
        """Sort by due date (overdue first, then soonest to latest, None last)"""
        # Implementation in data-model.md
```

**UndoManager** - Single-level undo
```python
from dataclasses import dataclass
from typing import Optional
from copy import deepcopy

@dataclass
class ActionSnapshot:
    action_type: str  # "add", "delete", "update", "complete"
    todo_id: int
    previous_state: Optional[TodoItem]  # None for add, TodoItem for others
    timestamp: datetime

class UndoManager:
    def __init__(self):
        self.last_action: Optional[ActionSnapshot] = None

    def record_action(self, action_type: str, todo_id: int, previous_state: Optional[TodoItem]):
        """Record action for undo"""
        self.last_action = ActionSnapshot(
            action_type=action_type,
            todo_id=todo_id,
            previous_state=deepcopy(previous_state),  # Deep copy to preserve state
            timestamp=datetime.now()
        )

    def undo(self, storage: TodoStorage) -> str:
        """Undo last action, return message"""
        # Implementation in data-model.md
```

**StatisticsService** - Statistics calculations
```python
class StatisticsService:
    def __init__(self, storage: TodoStorage):
        self.storage = storage

    def get_completion_stats(self) -> dict:
        """Calculate completion percentage and counts"""
        todos = self.storage.list_all()
        total = len(todos)
        completed = sum(1 for t in todos if t.completed)
        return {
            "total": total,
            "completed": completed,
            "percentage": (completed / total * 100) if total > 0 else 0
        }

    def get_priority_breakdown(self) -> dict:
        """Count tasks by priority level"""
        # Implementation in data-model.md
```

---

## Integration Architecture

### Layered Dependency Flow

```
Entry Points (main.py, rich_menu.py)
         ↓
   UI Layer (ui/)
         ↓
Services Layer (services/)
         ↓
  Storage Layer (storage.py)
         ↓
  Entity Layer (todo.py)
```

**Dependency Rules**:
1. UI depends on Services (not Storage directly)
2. Services depend on Storage
3. Storage depends on Entities
4. No circular dependencies
5. All layers can raise Exceptions

**Testing Strategy**:
- **Unit Tests**: Each layer independently (mock dependencies)
- **Integration Tests**: UI → Services → Storage flow
- **Contract Tests**: Verify service interfaces match contracts

---

## Performance Considerations

### Rich Library Performance
- **Rendering**: Rich buffers output, prints once (efficient)
- **Large Lists**: Use pagination (20 tasks/page) for 100+ tasks
- **Live Updates**: Avoid `Live()` context manager (Phase 1 - no threading)

### Search/Filter Performance
- **In-memory**: All operations O(n) where n = number of tasks
- **100 tasks**: Search/filter <1ms (acceptable for Phase 1)
- **1000 tasks**: Would need indexing (out of scope for Phase 1)

### Date Parsing Performance
- **Caching**: Parse once, store as date object
- **Validation**: Front-load validation, fail fast

---

## Risk Mitigation

### Terminal Compatibility
- **Risk**: Some terminals may not support Rich/Questionary features
- **Mitigation**: Test on Windows CMD, PowerShell, Git Bash, macOS Terminal, Linux terminals
- **Fallback**: Maintain basic CLI mode (`python -m src.main`) for minimal terminals

### Dependency Versions
- **Risk**: Breaking changes in rich/questionary/python-dateutil
- **Mitigation**: Pin versions in requirements.txt (rich>=13.0,<14.0)
- **Testing**: Run tests on multiple Python versions (3.11, 3.12)

### Data Migration
- **Risk**: Existing TodoItem (id, title, completed) incompatible with extended model
- **Mitigation**: Make new fields optional with defaults (priority=None, due_date=None)
- **Testing**: Verify existing tests pass with extended model

---

## Summary

All technology decisions resolve initial uncertainties:
- ✅ Rich library for visual UI (tables, panels, progress bars)
- ✅ Questionary for interactive navigation (arrow keys, confirmations)
- ✅ Python-dateutil for flexible date parsing (natural language, multiple formats)
- ✅ Service layer pattern for business logic (search, filter, undo, statistics)
- ✅ Backward compatibility strategy (extend entities, add services, maintain existing CLI)

**Next Steps**: Phase 1 - Design (data-model.md, contracts/, quickstart.md)
