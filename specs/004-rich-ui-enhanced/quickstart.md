# Quickstart: Enhanced Todo Console with Rich UI

**Feature**: 004-rich-ui-enhanced
**Date**: 2025-12-29
**Purpose**: Practical integration guide for implementing the rich UI feature

## Prerequisites

Before starting implementation, ensure:
- [ ] Feature 003 (Interactive Menu) is complete and tested
- [ ] All 84 existing tests pass
- [ ] Python 3.11+ is installed
- [ ] UV package manager is installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

---

## Quick Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
# Add dependencies to requirements.txt
cat >> requirements.txt << EOF

# Feature 004: Rich UI Dependencies
rich>=13.0,<14.0
questionary>=2.0,<3.0
python-dateutil>=2.8,<3.0
EOF

# Install with UV
uv pip install -r requirements.txt
```

**Verify Installation**:
```bash
python -c "import rich; print(rich.__version__)"  # Should print 13.x.x
python -c "import questionary; print(questionary.__version__)"  # Should print 2.x.x
python -c "import dateutil; print(dateutil.__version__)"  # Should print 2.x.x
```

---

### Step 2: Extend TodoItem Entity

**File**: `src/todo.py`

Add new fields to the TodoItem dataclass:

```python
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from src.exceptions import ValidationError

@dataclass
class TodoItem:
    id: int
    title: str
    completed: bool = False

    # NEW FIELDS (Feature 004)
    priority: Optional[str] = None  # "High", "Medium", "Low", or None
    due_date: Optional[date] = None
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        # Existing validation (title)
        stripped_title = self.title.strip()
        if not stripped_title:
            raise ValidationError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")

        # NEW VALIDATION (Feature 004)
        if self.priority is not None and self.priority not in ["High", "Medium", "Low"]:
            raise ValidationError(
                f"Priority must be 'High', 'Medium', 'Low', or None. Got: {self.priority}"
            )

        if self.due_date is not None and not isinstance(self.due_date, date):
            raise ValidationError("due_date must be a datetime.date object")

        if self.category is not None and len(self.category) > 50:
            raise ValidationError("category cannot exceed 50 characters")

        if not isinstance(self.tags, list):
            raise ValidationError("tags must be a list")
        for tag in self.tags:
            if not isinstance(tag, str) or len(tag) > 30:
                raise ValidationError("Each tag must be a string <= 30 characters")
```

**Test**:
```bash
pytest tests/unit/test_todo.py -v  # Existing tests should still pass
```

---

### Step 3: Create Service Layer Structure

```bash
# Create service directories
mkdir -p src/services
mkdir -p src/ui
mkdir -p tests/contract

# Create __init__.py files
touch src/services/__init__.py
touch src/ui/__init__.py

# Create placeholder files
touch src/services/search_filter.py
touch src/services/undo_manager.py
touch src/services/date_parser.py
touch src/services/statistics.py

touch src/ui/tables.py
touch src/ui/panels.py
touch src/ui/prompts.py
touch src/ui/formatting.py
```

---

### Step 4: Verify Backward Compatibility

Run existing test suite to ensure changes don't break anything:

```bash
pytest tests/ -v

# Expected output:
# ===== 84 passed in X.XXs =====
# (63 Phase 1 tests + 21 interactive menu tests)
```

If tests fail:
1. Check that all new TodoItem fields have default values
2. Ensure validation only triggers for invalid values (not None)
3. Verify existing TodoItem usage still works

---

## Implementation Roadmap

### Phase 1: Foundation (Days 1-2)

**Goal**: Extend data model and create service stubs

**Tasks**:
1. ✅ Extend TodoItem with new fields
2. ⬜ Add `DateParseError` exception to `src/exceptions.py`
3. ⬜ Implement `date_parser.py` service
4. ⬜ Implement `statistics.py` service
5. ⬜ Write unit tests for new services

**Test**:
```bash
pytest tests/unit/test_date_parser.py -v
pytest tests/unit/test_statistics.py -v
```

---

### Phase 2: Search & Filter (Days 3-4)

**Goal**: Implement SearchFilterService with all filter/sort methods

**Tasks**:
1. ⬜ Implement `search_filter.py` service
2. ⬜ Add filter methods to TodoStorage
3. ⬜ Write unit tests for search/filter/sort
4. ⬜ Write contract tests

**Test**:
```bash
pytest tests/unit/test_search_filter.py -v
pytest tests/contract/test_filter_contracts.py -v
```

---

### Phase 3: Undo Functionality (Day 5)

**Goal**: Implement UndoManager with single-level undo

**Tasks**:
1. ⬜ Implement `undo_manager.py` service
2. ⬜ Add `_restore_todo` method to TodoStorage
3. ⬜ Write unit tests for undo operations
4. ⬜ Write contract tests

**Test**:
```bash
pytest tests/unit/test_undo_manager.py -v
pytest tests/contract/test_undo_contracts.py -v
```

---

### Phase 4: Rich UI Components (Days 6-8)

**Goal**: Implement visual UI components using Rich library

**Tasks**:
1. ⬜ Implement `formatting.py` (colors, badges, helpers)
2. ⬜ Implement `tables.py` (task table rendering)
3. ⬜ Implement `panels.py` (statistics, alerts)
4. ⬜ Implement `prompts.py` (questionary wrappers)
5. ⬜ Write unit tests for UI components

**Test**:
```bash
pytest tests/unit/test_ui_components.py -v
pytest tests/contract/test_ui_contracts.py -v
```

---

### Phase 5: Integration (Days 9-10)

**Goal**: Create rich_menu.py entry point and integrate all components

**Tasks**:
1. ⬜ Create `src/rich_menu.py` (enhanced interactive menu)
2. ⬜ Integrate all services and UI components
3. ⬜ Write integration tests for rich UI workflows
4. ⬜ Manual testing with `python -m src.rich_menu`

**Test**:
```bash
pytest tests/integration/test_rich_workflows.py -v
python -m src.rich_menu  # Manual testing
```

---

## Example: Implementing SearchFilterService

### TDD Workflow (RED → GREEN → REFACTOR)

**Step 1: RED - Write Failing Tests**

`tests/unit/test_search_filter.py`:
```python
import pytest
from src.services.search_filter import SearchFilterService
from src.storage import TodoStorage
from src.todo import TodoItem

def test_search_returns_matching_todos():
    """Test search returns todos with matching titles"""
    # Arrange
    storage = TodoStorage()
    storage.add("Buy milk")
    storage.add("Fix bug in auth")
    storage.add("Buy groceries")

    service = SearchFilterService(storage)

    # Act
    results = service.search("buy")

    # Assert
    assert len(results) == 2
    assert results[0].title == "Buy milk"
    assert results[1].title == "Buy groceries"

def test_search_is_case_insensitive():
    """Test search is case-insensitive"""
    storage = TodoStorage()
    storage.add("FIX BUG")

    service = SearchFilterService(storage)

    # Act
    results = service.search("fix")

    # Assert
    assert len(results) == 1
    assert results[0].title == "FIX BUG"

def test_search_empty_query_raises_error():
    """Test search with empty query raises ValueError"""
    storage = TodoStorage()
    service = SearchFilterService(storage)

    # Act & Assert
    with pytest.raises(ValueError, match="Search query cannot be empty"):
        service.search("")
```

Run tests (they should FAIL):
```bash
pytest tests/unit/test_search_filter.py -v
# Expected: ImportError or AttributeError (service doesn't exist yet)
```

---

**Step 2: GREEN - Implement Minimum Code**

`src/services/search_filter.py`:
```python
from typing import List
from src.storage import TodoStorage
from src.todo import TodoItem

class SearchFilterService:
    def __init__(self, storage: TodoStorage):
        self.storage = storage

    def search(self, query: str) -> List[TodoItem]:
        """Search todos by title keyword (case-insensitive)"""
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        query_lower = query.lower()
        todos = self.storage.list_all()

        return [t for t in todos if query_lower in t.title.lower()]
```

Run tests (they should PASS):
```bash
pytest tests/unit/test_search_filter.py -v
# Expected: 3 passed
```

---

**Step 3: REFACTOR - Improve Code Quality**

Add more tests for edge cases:
```python
def test_search_no_matches_returns_empty_list():
    """Test search with no matches returns empty list"""
    storage = TodoStorage()
    storage.add("Buy milk")

    service = SearchFilterService(storage)

    # Act
    results = service.search("xyz")

    # Assert
    assert results == []

def test_search_special_characters():
    """Test search handles special characters"""
    storage = TodoStorage()
    storage.add("Fix bug!")

    service = SearchFilterService(storage)

    # Act
    results = service.search("bug!")

    # Assert
    assert len(results) == 1
```

Refactor implementation (if needed):
- Add input validation
- Improve error messages
- Add type hints
- Add docstrings

---

## Example: Rendering Task Table

### Quick Integration Example

```python
from rich.console import Console
from src.ui.tables import render_task_table
from src.storage import TodoStorage

# Setup
storage = TodoStorage()
storage.add("Buy milk")
storage.todos[1].priority = "High"
storage.todos[1].due_date = date(2025, 12, 31)

storage.add("Fix bug")
storage.todos[2].priority = "Medium"
storage.todos[2].completed = True

# Render
console = Console()
render_task_table(storage.list_all(), console, title="My Tasks")
```

**Expected Output**:
```
┌────┬────────┬──────────┬──────────┬────────────┬──────────┐
│ ID │ Status │ Priority │  Title   │  Due Date  │ Category │
├────┼────────┼──────────┼──────────┼────────────┼──────────┤
│  1 │  [ ]   │   High   │ Buy milk │ 2025-12-31 │    -     │
│  2 │   ✓    │  Medium  │ Fix bug  │     -      │    -     │
└────┴────────┴──────────┴──────────┴────────────┴──────────┘

Total: 2 | Completed: 1 (50%) | Overdue: 0
```

---

## Testing Strategy

### Unit Tests

**Coverage Goals**:
- TodoItem validation: 100%
- Services (search, filter, undo, stats): 100%
- UI formatting helpers: 100%
- UI rendering: 80% (Rich output hard to test)

**Run Unit Tests**:
```bash
pytest tests/unit/ -v --cov=src --cov-report=term-missing
```

---

### Contract Tests

**Purpose**: Verify services adhere to documented contracts

**Run Contract Tests**:
```bash
pytest tests/contract/ -v
```

---

### Integration Tests

**Purpose**: Test end-to-end workflows with rich UI

**Run Integration Tests**:
```bash
pytest tests/integration/ -v
```

---

### Full Regression Suite

**Run All Tests**:
```bash
pytest tests/ -v --cov=src --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

---

## Manual Testing Checklist

### Basic Functionality
- [ ] Launch rich menu: `python -m src.rich_menu`
- [ ] Add todo with priority and due date
- [ ] View task table with colors
- [ ] Mark todo as complete (see checkmark)
- [ ] Update todo title/priority
- [ ] Delete todo (with confirmation)
- [ ] Undo delete (see todo restored)

### Search & Filter
- [ ] Search by keyword
- [ ] Filter by priority (High/Medium/Low)
- [ ] Filter by status (Complete/Incomplete)
- [ ] Filter by due date (Overdue/Today)
- [ ] Combine multiple filters
- [ ] Sort by due date
- [ ] Sort by priority

### Statistics
- [ ] View statistics panel
- [ ] See progress bar
- [ ] See priority breakdown
- [ ] See overdue count

### Edge Cases
- [ ] Add 100+ todos (test pagination)
- [ ] Search with no results
- [ ] Undo with no action
- [ ] Invalid date format (see error)
- [ ] Long title (see truncation in table, full in detail)

---

## Common Issues & Solutions

### Issue 1: Rich output doesn't show colors

**Symptom**: Plain text output, no colors

**Solution**:
```python
# Force color output
console = Console(force_terminal=True)
```

Or check terminal support:
```bash
python -c "from rich.console import Console; c = Console(); print(c.is_terminal)"
# Should print: True
```

---

### Issue 2: Questionary prompts don't work

**Symptom**: Keyboard interrupt or broken prompts

**Solution**: Ensure running in interactive terminal (not piped):
```bash
python -m src.rich_menu  # CORRECT
echo "1" | python -m src.rich_menu  # INCORRECT (piped input)
```

---

### Issue 3: Date parsing fails

**Symptom**: `DateParseError` for valid dates

**Solution**: Check date format:
```python
from src.services.date_parser import parse_due_date

# These should work:
parse_due_date("2025-12-31")  # ISO format
parse_due_date("12/31/2025")  # US format
parse_due_date("tomorrow")    # Natural language

# Invalid:
parse_due_date("invalid")  # Raises DateParseError
```

---

### Issue 4: Existing tests fail after extending TodoItem

**Symptom**: `TypeError: __init__() missing required keyword argument`

**Solution**: Ensure all new fields have defaults:
```python
# CORRECT
@dataclass
class TodoItem:
    id: int
    title: str
    completed: bool = False
    priority: Optional[str] = None  # Has default

# INCORRECT
@dataclass
class TodoItem:
    id: int
    title: str
    completed: bool = False
    priority: Optional[str]  # No default - breaks existing code
```

---

## Performance Tips

### For 100+ Tasks

If performance degrades with large task lists:

1. **Pagination**: Display 20 tasks per page
2. **Lazy Loading**: Only render visible tasks
3. **Debouncing**: Delay search until user stops typing

**Example Pagination**:
```python
def render_task_table_paginated(todos, console, page=1, per_page=20):
    start = (page - 1) * per_page
    end = start + per_page
    page_todos = todos[start:end]

    render_task_table(page_todos, console, title=f"Tasks (Page {page})")
    console.print(f"\nShowing {start+1}-{end} of {len(todos)}")
```

---

## Next Steps

After quickstart implementation:

1. **Run `/sp.tasks`** - Generate detailed task breakdown with test cases
2. **Follow TDD workflow** - RED → GREEN → REFACTOR for each task
3. **Incremental delivery** - Implement P1 user stories first, then P2, then P3
4. **Continuous testing** - Run tests after each change
5. **Manual testing** - Test rich UI workflows interactively

**Ready to start?** Begin with Phase 1 (Foundation) and follow the TDD workflow!
