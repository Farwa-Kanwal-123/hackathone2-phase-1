# Data Model: Enhanced Todo Console with Rich UI

**Feature**: 004-rich-ui-enhanced
**Date**: 2025-12-29
**Purpose**: Define extended entities, relationships, validation rules, and state transitions

## Entity Overview

This feature extends the existing `TodoItem` entity and introduces new entities for undo functionality:

| Entity | Purpose | Persistence |
|--------|---------|-------------|
| **TodoItem** (extended) | Core task entity with priority, dates, categories | In-memory (dict) |
| **ActionSnapshot** (new) | Undo history record | In-memory (single instance) |

---

## TodoItem Entity (Extended)

### Current State (Phase 1 + Feature 003)

```python
@dataclass
class TodoItem:
    id: int
    title: str
    completed: bool = False
```

**Validation**:
- `title`: 1-200 characters, non-empty, non-whitespace

---

### Extended State (Feature 004)

```python
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from src.exceptions import ValidationError

@dataclass
class TodoItem:
    """
    Extended TodoItem with priority, due dates, categories, and tags.

    Attributes:
        id: Unique identifier (assigned by storage)
        title: Todo description (1-200 characters, non-empty)
        completed: Whether the todo is done (defaults to False)
        priority: Priority level (High, Medium, Low, or None)
        due_date: Optional due date (datetime.date object)
        category: Optional category name (e.g., "Work", "Personal")
        tags: Optional list of tags (e.g., ["urgent", "bug-fix"])
        created_date: Timestamp when todo was created
        updated_date: Timestamp when todo was last updated
    """
    id: int
    title: str
    completed: bool = False
    priority: Optional[str] = None  # "High", "Medium", "Low", or None
    due_date: Optional[date] = None
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """
        Validate fields after initialization.

        Raises:
            ValidationError: If any field fails validation
        """
        # Existing validation: title
        stripped_title = self.title.strip()
        if not stripped_title:
            raise ValidationError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")

        # New validation: priority
        if self.priority is not None:
            if self.priority not in ["High", "Medium", "Low"]:
                raise ValidationError(
                    f"Priority must be 'High', 'Medium', 'Low', or None. Got: {self.priority}"
                )

        # New validation: due_date
        if self.due_date is not None:
            if not isinstance(self.due_date, date):
                raise ValidationError(
                    f"due_date must be a datetime.date object. Got: {type(self.due_date)}"
                )

        # New validation: category
        if self.category is not None:
            if not isinstance(self.category, str):
                raise ValidationError("category must be a string")
            if len(self.category) > 50:
                raise ValidationError("category cannot exceed 50 characters")

        # New validation: tags
        if not isinstance(self.tags, list):
            raise ValidationError("tags must be a list")
        for tag in self.tags:
            if not isinstance(tag, str):
                raise ValidationError(f"All tags must be strings. Got: {type(tag)}")
            if len(tag) > 30:
                raise ValidationError(f"Tag '{tag}' exceeds 30 characters")
```

---

### Field Specifications

| Field | Type | Required | Default | Validation | Example |
|-------|------|----------|---------|------------|---------|
| `id` | int | Yes | N/A (assigned by storage) | Must be unique | `1` |
| `title` | str | Yes | N/A | 1-200 chars, non-empty | `"Fix authentication bug"` |
| `completed` | bool | No | `False` | Must be boolean | `True` |
| `priority` | Optional[str] | No | `None` | "High", "Medium", "Low", or None | `"High"` |
| `due_date` | Optional[date] | No | `None` | Must be date object | `date(2025, 12, 31)` |
| `category` | Optional[str] | No | `None` | Max 50 chars | `"Work"` |
| `tags` | List[str] | No | `[]` | Each tag max 30 chars | `["urgent", "bug"]` |
| `created_date` | datetime | No | `datetime.now()` | Auto-set on creation | `datetime(2025, 12, 29, 10, 30)` |
| `updated_date` | datetime | No | `datetime.now()` | Auto-update on modification | `datetime(2025, 12, 29, 14, 45)` |

---

### Priority Levels

| Priority | Color (Rich) | Use Case | Sort Order |
|----------|-------------|----------|------------|
| `"High"` | Red | Critical, urgent tasks | 1 |
| `"Medium"` | Yellow | Important but not urgent | 2 |
| `"Low"` | Green | Nice-to-have tasks | 3 |
| `None` | Gray | Unprioritized tasks | 4 |

**Default Priority**: When priority is not specified, it remains `None` (not auto-set to "Medium")

---

### Due Date States

| State | Condition | Color (Rich) | Example |
|-------|-----------|-------------|---------|
| **Overdue** | `due_date < date.today()` | Red | Due yesterday |
| **Today** | `due_date == date.today()` | Orange | Due today |
| **Upcoming** | `due_date > date.today()` | Normal | Due tomorrow |
| **No Date** | `due_date is None` | Dim | No deadline |

**Calculation Helpers**:
```python
from datetime import date

def get_due_date_status(todo: TodoItem) -> str:
    """Return 'overdue', 'today', 'upcoming', or 'no_date'"""
    if todo.due_date is None:
        return "no_date"
    today = date.today()
    if todo.due_date < today:
        return "overdue"
    elif todo.due_date == today:
        return "today"
    else:
        return "upcoming"

def days_until_due(todo: TodoItem) -> Optional[int]:
    """Return number of days until due (negative if overdue, None if no date)"""
    if todo.due_date is None:
        return None
    return (todo.due_date - date.today()).days
```

---

### State Transitions

```
┌─────────────┐
│  Created    │  priority=None, completed=False, due_date=None
│ (New Todo)  │
└──────┬──────┘
       │
       ├─── Set Priority ────→ priority="High"/"Medium"/"Low"
       ├─── Set Due Date ────→ due_date=date(...)
       ├─── Add Category ────→ category="Work"
       ├─── Add Tags ────────→ tags=["urgent"]
       │
       ├─── Update Title ────→ title="new title", updated_date=now()
       ├─── Mark Complete ───→ completed=True, updated_date=now()
       │
       └─── Delete ──────────→ Removed from storage
```

**Invariants**:
- `id` never changes after creation
- `created_date` never changes after creation
- `updated_date` updates on any modification (title, priority, due_date, category, tags, completed)
- `completed` can transition True → False (undo) or False → True (complete)

---

## ActionSnapshot Entity (New)

### Purpose
Track the last action for single-level undo functionality.

### Structure

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from copy import deepcopy

@dataclass
class ActionSnapshot:
    """
    Snapshot of a single action for undo functionality.

    Attributes:
        action_type: Type of action ("add", "delete", "update", "complete")
        todo_id: ID of the todo affected
        previous_state: Deep copy of todo before action (None for "add")
        timestamp: When the action occurred
    """
    action_type: str  # "add", "delete", "update", "complete"
    todo_id: int
    previous_state: Optional[TodoItem]  # None for "add", TodoItem copy for others
    timestamp: datetime
```

### Field Specifications

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `action_type` | str | Action performed | `"delete"` |
| `todo_id` | int | ID of affected todo | `5` |
| `previous_state` | Optional[TodoItem] | Todo state before action | `TodoItem(id=5, title="old", ...)` |
| `timestamp` | datetime | When action occurred | `datetime(2025, 12, 29, 15, 30)` |

### Action Types and Undo Logic

| Action Type | Previous State | Undo Operation |
|-------------|----------------|----------------|
| `"add"` | `None` (todo didn't exist) | Delete the added todo |
| `"delete"` | `TodoItem(...)` (full copy) | Re-add the deleted todo |
| `"update"` | `TodoItem(...)` (old state) | Restore old title/priority/etc. |
| `"complete"` | `TodoItem(completed=False, ...)` | Set completed=False |

**Undo Implementation**:
```python
def undo_action(snapshot: ActionSnapshot, storage: TodoStorage) -> str:
    """
    Undo the last action.

    Args:
        snapshot: The action to undo
        storage: TodoStorage instance

    Returns:
        Success message describing what was undone

    Raises:
        ValueError: If undo is not possible
    """
    if snapshot.action_type == "add":
        # Undo add → delete the todo
        storage.delete(snapshot.todo_id)
        return f"Undone: Removed todo (ID: {snapshot.todo_id})"

    elif snapshot.action_type == "delete":
        # Undo delete → restore the todo
        if snapshot.previous_state is None:
            raise ValueError("Cannot undo delete: no previous state")
        # Re-add with original ID (requires storage support)
        storage._restore_todo(snapshot.previous_state)
        return f"Undone: Restored '{snapshot.previous_state.title}' (ID: {snapshot.todo_id})"

    elif snapshot.action_type == "update":
        # Undo update → restore previous state
        if snapshot.previous_state is None:
            raise ValueError("Cannot undo update: no previous state")
        storage._restore_todo(snapshot.previous_state)
        return f"Undone: Reverted to '{snapshot.previous_state.title}' (ID: {snapshot.todo_id})"

    elif snapshot.action_type == "complete":
        # Undo complete → mark incomplete
        storage.todos[snapshot.todo_id].completed = False
        return f"Undone: Marked incomplete (ID: {snapshot.todo_id})"
```

**Storage Extension Required**:
```python
# Add to TodoStorage class
def _restore_todo(self, todo: TodoItem) -> None:
    """
    Restore a todo with its exact state (including ID).
    Used for undo operations.

    Args:
        todo: TodoItem to restore (with original ID)
    """
    self.todos[todo.id] = deepcopy(todo)
    # Don't update next_id - IDs are never reused
```

---

## Relationships and Indexes

### TodoStorage Extensions

**Current Storage** (Phase 1):
```python
class TodoStorage:
    def __init__(self):
        self.todos: dict[int, TodoItem] = {}
        self.next_id: int = 1
```

**Extended Storage** (Feature 004):
```python
class TodoStorage:
    def __init__(self):
        self.todos: dict[int, TodoItem] = {}
        self.next_id: int = 1

    # New methods for extended TodoItem
    def list_all(self) -> List[TodoItem]:
        """Return all todos sorted by ID (existing method - no changes)"""
        return sorted(self.todos.values(), key=lambda todo: todo.id)

    def filter_by_priority(self, priority: str) -> List[TodoItem]:
        """Return todos with specified priority"""
        return [t for t in self.todos.values() if t.priority == priority]

    def filter_by_category(self, category: str) -> List[TodoItem]:
        """Return todos in specified category"""
        return [t for t in self.todos.values() if t.category == category]

    def filter_by_tag(self, tag: str) -> List[TodoItem]:
        """Return todos with specified tag"""
        return [t for t in self.todos.values() if tag in t.tags]

    def filter_by_status(self, completed: bool) -> List[TodoItem]:
        """Return todos by completion status"""
        return [t for t in self.todos.values() if t.completed == completed]

    def search(self, query: str) -> List[TodoItem]:
        """Search todos by title (case-insensitive)"""
        query_lower = query.lower()
        return [t for t in self.todos.values() if query_lower in t.title.lower()]

    def sort_by_due_date(self, todos: List[TodoItem]) -> List[TodoItem]:
        """
        Sort todos by due date.
        Order: Overdue → Today → Upcoming → No date
        """
        def due_date_key(todo: TodoItem):
            if todo.due_date is None:
                return (3, date.max)  # No date last
            today = date.today()
            if todo.due_date < today:
                return (0, todo.due_date)  # Overdue first
            elif todo.due_date == today:
                return (1, todo.due_date)  # Today second
            else:
                return (2, todo.due_date)  # Upcoming third

        return sorted(todos, key=due_date_key)

    def sort_by_priority(self, todos: List[TodoItem]) -> List[TodoItem]:
        """
        Sort todos by priority.
        Order: High → Medium → Low → None
        """
        priority_order = {"High": 1, "Medium": 2, "Low": 3, None: 4}
        return sorted(todos, key=lambda t: priority_order.get(t.priority, 4))
```

**No Indexes Required**: For Phase 1 (in-memory, <100 tasks), linear scans are acceptable (O(n) performance).

---

## Migration Strategy

### Backward Compatibility

**Challenge**: Existing code creates TodoItem with only `id`, `title`, `completed`.

**Solution**: All new fields have defaults:
```python
TodoItem(id=1, title="Old todo", completed=False)
# Equivalent to:
TodoItem(
    id=1,
    title="Old todo",
    completed=False,
    priority=None,           # Default
    due_date=None,           # Default
    category=None,           # Default
    tags=[],                 # Default
    created_date=datetime.now(),  # Default
    updated_date=datetime.now()   # Default
)
```

**Existing Tests**: All 84 tests should pass without modification:
- `TodoItem(id=1, title="test", completed=False)` still works
- New fields are ignored if not specified
- Validation only triggers if invalid values are provided

**Gradual Adoption**:
- Phase 1: Extend TodoItem with optional fields
- Phase 2: Add UI for priority/dates/categories
- Phase 3: Existing CLI remains unchanged (`python -m src.main`)
- Phase 4: Rich UI uses extended features (`python rich_menu.py`)

---

## Validation Rules Summary

| Field | Validation | Error Message |
|-------|------------|---------------|
| `title` | 1-200 chars, non-empty | "Title cannot be empty" |
| `title` | Non-whitespace | "Title cannot be empty" |
| `priority` | "High", "Medium", "Low", or None | "Priority must be 'High', 'Medium', 'Low', or None" |
| `due_date` | date object or None | "due_date must be a datetime.date object" |
| `category` | String, max 50 chars | "category cannot exceed 50 characters" |
| `tags` | List of strings | "tags must be a list" |
| `tags` | Each tag max 30 chars | "Tag 'X' exceeds 30 characters" |

All validation errors raise `ValidationError` (existing exception).

---

## Example Usage

### Creating Extended Todos

```python
from datetime import date
from src.todo import TodoItem

# Minimal todo (backward compatible)
todo1 = TodoItem(id=1, title="Buy milk")

# Todo with priority
todo2 = TodoItem(id=2, title="Fix bug", priority="High")

# Todo with all fields
todo3 = TodoItem(
    id=3,
    title="Write report",
    priority="Medium",
    due_date=date(2025, 12, 31),
    category="Work",
    tags=["quarterly", "urgent"]
)
```

### Filtering and Sorting

```python
storage = TodoStorage()
# ... add todos ...

# Filter by priority
high_priority = storage.filter_by_priority("High")

# Search by keyword
bug_tasks = storage.search("bug")

# Sort by due date
all_todos = storage.list_all()
sorted_todos = storage.sort_by_due_date(all_todos)
```

### Undo Operations

```python
undo_mgr = UndoManager()

# Record action before making change
old_todo = storage.todos.get(5)
undo_mgr.record_action("delete", 5, old_todo)
storage.delete(5)

# Later: undo
undo_mgr.undo(storage)  # Restores todo ID 5
```

---

## Summary

**Extended Entities**:
- ✅ TodoItem extended with 6 new fields (priority, due_date, category, tags, created_date, updated_date)
- ✅ ActionSnapshot entity for undo functionality
- ✅ Backward compatible with existing TodoItem usage
- ✅ All fields validated with clear error messages

**Storage Extensions**:
- ✅ Filter methods (priority, category, tag, status)
- ✅ Search method (title keyword search)
- ✅ Sort methods (due_date, priority)
- ✅ Restore method for undo operations

**Next Steps**: Generate contracts/ (service interfaces) and quickstart.md (integration guide)
