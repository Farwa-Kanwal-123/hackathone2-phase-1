# Filter Service Contract

**Feature**: 004-rich-ui-enhanced
**Module**: `src/services/search_filter.py`
**Purpose**: Define interfaces for search, filter, and sort operations

## Overview

The `SearchFilterService` class provides search, filter, and sort operations on TodoItem collections. All methods are stateless and return new lists (do not modify storage).

---

## Class: `SearchFilterService`

### Constructor

**Signature**:
```python
from src.storage import TodoStorage

class SearchFilterService:
    def __init__(self, storage: TodoStorage):
        """
        Initialize search/filter service with storage reference.

        Args:
            storage: TodoStorage instance (read-only access)
        """
        self.storage = storage
```

**Invariants**:
- Service never modifies storage (read-only operations)
- All methods return new lists (do not modify input)
- Empty results return `[]`, never `None`

---

## Search Methods

### `search`

**Purpose**: Search todos by keyword in title (case-insensitive)

**Signature**:
```python
from typing import List
from src.todo import TodoItem

def search(self, query: str) -> List[TodoItem]:
    """
    Search todos by title keyword (case-insensitive).

    Args:
        query: Search keyword (partial match allowed)

    Returns:
        List of matching TodoItem objects (empty if no matches)

    Raises:
        ValueError: If query is empty or whitespace-only

    Example:
        >>> service.search("bug")
        [TodoItem(id=1, title="Fix bug in auth"), TodoItem(id=5, title="Debug API")]

    Contract:
        - Case-insensitive: "Bug" matches "bug fix"
        - Partial match: "auth" matches "authentication"
        - Empty query raises ValueError
        - No matches returns []
        - Results maintain storage order (sorted by ID)
    """
```

**Edge Cases**:
| Input | Behavior | Output |
|-------|----------|--------|
| Empty string `""` | Raise ValueError | `ValueError("Search query cannot be empty")` |
| Whitespace `"   "` | Raise ValueError | `ValueError("Search query cannot be empty")` |
| No matches | Return empty list | `[]` |
| All todos match | Return all todos | `[todo1, todo2, ...]` |
| Special characters `"bug!"` | Treat literally (escape regex) | Match "bug!" exactly |

---

## Filter Methods

### `filter_by_priority`

**Purpose**: Filter todos by priority level

**Signature**:
```python
def filter_by_priority(self, priority: str) -> List[TodoItem]:
    """
    Filter todos by priority level.

    Args:
        priority: "High", "Medium", "Low", or "None"

    Returns:
        List of TodoItem objects with matching priority

    Raises:
        ValueError: If priority is not valid

    Example:
        >>> service.filter_by_priority("High")
        [TodoItem(id=1, priority="High"), TodoItem(id=3, priority="High")]

    Contract:
        - Valid priorities: "High", "Medium", "Low", "None"
        - "None" matches todos with priority=None
        - Invalid priority raises ValueError
        - No matches returns []
    """
```

---

### `filter_by_category`

**Purpose**: Filter todos by category

**Signature**:
```python
def filter_by_category(self, category: str) -> List[TodoItem]:
    """
    Filter todos by category.

    Args:
        category: Category name (exact match, case-sensitive)

    Returns:
        List of TodoItem objects in specified category

    Example:
        >>> service.filter_by_category("Work")
        [TodoItem(id=1, category="Work"), TodoItem(id=2, category="Work")]

    Contract:
        - Exact match (case-sensitive): "Work" ≠ "work"
        - Empty category raises ValueError
        - No matches returns []
    """
```

---

### `filter_by_tag`

**Purpose**: Filter todos containing specified tag

**Signature**:
```python
def filter_by_tag(self, tag: str) -> List[TodoItem]:
    """
    Filter todos containing specified tag.

    Args:
        tag: Tag name (exact match, case-sensitive)

    Returns:
        List of TodoItem objects containing the tag

    Example:
        >>> service.filter_by_tag("urgent")
        [TodoItem(id=1, tags=["urgent", "bug"]), TodoItem(id=3, tags=["urgent"])]

    Contract:
        - Exact match within tags list
        - Empty tag raises ValueError
        - No matches returns []
    """
```

---

### `filter_by_status`

**Purpose**: Filter todos by completion status

**Signature**:
```python
def filter_by_status(self, status: str) -> List[TodoItem]:
    """
    Filter todos by completion status.

    Args:
        status: "completed", "incomplete", or "all"

    Returns:
        List of TodoItem objects matching status

    Raises:
        ValueError: If status is not valid

    Example:
        >>> service.filter_by_status("completed")
        [TodoItem(id=1, completed=True), TodoItem(id=3, completed=True)]

    Contract:
        - Valid statuses: "completed", "incomplete", "all"
        - "all" returns all todos (no filtering)
        - Invalid status raises ValueError
    """
```

---

### `filter_by_due_date_range`

**Purpose**: Filter todos by due date range

**Signature**:
```python
from datetime import date

def filter_by_due_date_range(self, date_range: str) -> List[TodoItem]:
    """
    Filter todos by due date range.

    Args:
        date_range: "overdue", "today", "this_week", "this_month", "no_date"

    Returns:
        List of TodoItem objects matching date range

    Raises:
        ValueError: If date_range is not valid

    Example:
        >>> service.filter_by_due_date_range("overdue")
        [TodoItem(id=1, due_date=date(2025, 12, 20)), ...]

    Contract:
        - "overdue": due_date < today
        - "today": due_date == today
        - "this_week": today <= due_date < today + 7 days
        - "this_month": due_date in current month
        - "no_date": due_date is None
        - Invalid range raises ValueError
    """
```

**Date Range Definitions**:
| Range | Condition | Example (today = 2025-12-29) |
|-------|-----------|------------------------------|
| `"overdue"` | `due_date < today` | due_date = 2025-12-28 |
| `"today"` | `due_date == today` | due_date = 2025-12-29 |
| `"this_week"` | `today <= due_date < today + 7 days` | due_date = 2026-01-04 |
| `"this_month"` | `due_date.year == today.year and due_date.month == today.month` | due_date = 2025-12-31 |
| `"no_date"` | `due_date is None` | due_date = None |

---

### `apply_combined_filters`

**Purpose**: Apply multiple filters simultaneously (AND logic)

**Signature**:
```python
def apply_combined_filters(
    self,
    priorities: Optional[List[str]] = None,
    categories: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    status: Optional[str] = None,
    date_range: Optional[str] = None
) -> List[TodoItem]:
    """
    Apply multiple filters with AND logic.

    Args:
        priorities: List of priority levels (OR within, AND across)
        categories: List of categories (OR within, AND across)
        tags: List of tags (OR within, AND across)
        status: Completion status filter
        date_range: Due date range filter

    Returns:
        List of TodoItem objects matching ALL filter criteria

    Example:
        >>> service.apply_combined_filters(
        ...     priorities=["High", "Medium"],
        ...     status="incomplete",
        ...     date_range="overdue"
        ... )
        # Returns todos that are:
        # - (High OR Medium priority) AND
        # - (incomplete) AND
        # - (overdue)

    Contract:
        - None/empty lists for a filter type = no filtering on that criterion
        - Multiple values within a criterion use OR logic
        - Different criteria use AND logic
        - Empty result returns []
    """
```

**Filter Logic Example**:
```python
# User selects:
priorities = ["High", "Medium"]
categories = ["Work"]
status = "incomplete"

# SQL-like logic:
# WHERE (priority IN ("High", "Medium"))
#   AND (category IN ("Work"))
#   AND (completed = False)
```

---

## Sort Methods

### `sort_by_due_date`

**Purpose**: Sort todos by due date (overdue first)

**Signature**:
```python
def sort_by_due_date(self, todos: List[TodoItem]) -> List[TodoItem]:
    """
    Sort todos by due date.

    Args:
        todos: List of TodoItem objects to sort

    Returns:
        New list sorted by due date (original list unchanged)

    Sort Order:
        1. Overdue (oldest to newest)
        2. Today
        3. Upcoming (soonest to latest)
        4. No date

    Example:
        >>> todos = [todo_future, todo_overdue, todo_today, todo_no_date]
        >>> sorted_todos = service.sort_by_due_date(todos)
        [todo_overdue, todo_today, todo_future, todo_no_date]

    Contract:
        - Does not modify input list
        - Stable sort (preserves order for equal dates)
        - None dates always last
    """
```

---

### `sort_by_priority`

**Purpose**: Sort todos by priority (High first)

**Signature**:
```python
def sort_by_priority(self, todos: List[TodoItem]) -> List[TodoItem]:
    """
    Sort todos by priority.

    Args:
        todos: List of TodoItem objects to sort

    Returns:
        New list sorted by priority (original list unchanged)

    Sort Order:
        1. High
        2. Medium
        3. Low
        4. None

    Example:
        >>> todos = [todo_low, todo_high, todo_none, todo_medium]
        >>> sorted_todos = service.sort_by_priority(todos)
        [todo_high, todo_medium, todo_low, todo_none]

    Contract:
        - Does not modify input list
        - Stable sort (preserves order for equal priorities)
        - None priorities always last
    """
```

---

### `sort_by_created_date`

**Purpose**: Sort todos by creation date (newest first)

**Signature**:
```python
def sort_by_created_date(self, todos: List[TodoItem], reverse: bool = True) -> List[TodoItem]:
    """
    Sort todos by created_date.

    Args:
        todos: List of TodoItem objects to sort
        reverse: If True, newest first (default). If False, oldest first.

    Returns:
        New list sorted by created_date

    Example:
        >>> sorted_todos = service.sort_by_created_date(todos)
        [newest_todo, ..., oldest_todo]

    Contract:
        - Does not modify input list
        - Stable sort
    """
```

---

### `sort_by_title`

**Purpose**: Sort todos alphabetically by title

**Signature**:
```python
def sort_by_title(self, todos: List[TodoItem], case_sensitive: bool = False) -> List[TodoItem]:
    """
    Sort todos alphabetically by title.

    Args:
        todos: List of TodoItem objects to sort
        case_sensitive: If True, case-sensitive sort (default: False)

    Returns:
        New list sorted by title

    Example:
        >>> sorted_todos = service.sort_by_title(todos)
        ["Buy milk", "Fix bug", "Write report"]

    Contract:
        - Does not modify input list
        - Default: case-insensitive ("Buy" before "buy")
        - Stable sort
    """
```

---

## Performance Contracts

### Complexity Guarantees

| Method | Time Complexity | Space Complexity | Notes |
|--------|----------------|------------------|-------|
| `search(query)` | O(n * m) | O(k) | n=todos, m=avg title length, k=matches |
| `filter_by_*` | O(n) | O(k) | n=todos, k=matches |
| `apply_combined_filters` | O(n * f) | O(k) | f=number of filter types |
| `sort_by_due_date` | O(n log n) | O(n) | Stable sort (Python Timsort) |
| `sort_by_priority` | O(n log n) | O(n) | Stable sort |
| `sort_by_title` | O(n log n) | O(n) | Stable sort |

**Acceptable for Phase 1**: All methods perform well with <100 tasks (typical usage: 20-50 tasks).

**Future Optimization** (out of scope): For 1000+ tasks, consider indexing (priority index, category index, date index).

---

## Error Handling

### Exception Types

| Exception | Raised When | Example |
|-----------|-------------|---------|
| `ValueError` | Invalid filter parameter | `filter_by_priority("invalid")` |
| `ValueError` | Empty search query | `search("")` |
| `TypeError` | Invalid argument type | `sort_by_due_date("not a list")` |

**Error Messages**:
```python
# Invalid priority
ValueError("Priority must be 'High', 'Medium', 'Low', or 'None'. Got: 'invalid'")

# Empty query
ValueError("Search query cannot be empty")

# Invalid status
ValueError("Status must be 'completed', 'incomplete', or 'all'. Got: 'done'")

# Invalid date range
ValueError("Date range must be 'overdue', 'today', 'this_week', 'this_month', or 'no_date'. Got: 'yesterday'")
```

---

## Contract Tests

**Location**: `tests/contract/test_filter_contracts.py`

**Test Cases**:
1. `test_search_contract` - Verify search adheres to case-insensitive partial match
2. `test_filter_by_priority_contract` - Verify only valid priorities accepted
3. `test_filter_by_due_date_range_contract` - Verify date ranges calculated correctly
4. `test_apply_combined_filters_contract` - Verify AND logic across filters
5. `test_sort_by_due_date_contract` - Verify overdue first, None last
6. `test_sort_methods_immutable_contract` - Verify sorts don't modify input

**Example Test**:
```python
import pytest
from datetime import date, timedelta
from src.services.search_filter import SearchFilterService
from src.storage import TodoStorage
from src.todo import TodoItem

def test_filter_by_due_date_range_contract():
    """Verify filter_by_due_date_range calculates ranges correctly"""
    # Arrange
    storage = TodoStorage()
    service = SearchFilterService(storage)

    today = date.today()
    storage.add("Overdue task")
    storage.todos[1].due_date = today - timedelta(days=1)

    storage.add("Today task")
    storage.todos[2].due_date = today

    storage.add("Future task")
    storage.todos[3].due_date = today + timedelta(days=5)

    # Act
    overdue = service.filter_by_due_date_range("overdue")
    today_tasks = service.filter_by_due_date_range("today")

    # Assert
    assert len(overdue) == 1
    assert overdue[0].id == 1
    assert len(today_tasks) == 1
    assert today_tasks[0].id == 2
```

---

## Summary

**Search/Filter/Sort Service Contract**:
- ✅ Search by keyword (case-insensitive, partial match)
- ✅ Filter by priority, category, tag, status, date range
- ✅ Combined filters with AND logic
- ✅ Sort by due_date, priority, created_date, title
- ✅ All methods return new lists (immutable operations)
- ✅ O(n) filter, O(n log n) sort complexity
- ✅ Clear error messages for invalid inputs

**Key Principles**:
- Read-only operations (never modify storage)
- Immutable results (always return new lists)
- Fail fast with clear error messages
- Efficient for <100 tasks (Phase 1 scope)

**Next**: `undo_service.md` contract for undo/action history
