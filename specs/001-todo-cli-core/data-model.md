# Data Model: Todo CLI Core

**Feature**: Todo CLI Core
**Date**: 2025-12-24
**Status**: Design

## Overview

This document defines the data entities and storage structures for the Todo CLI application. The design follows Phase 1 constraints: in-memory storage only, no persistence, simple data structures.

## Entities

### TodoItem

Represents a single task to be completed.

**Attributes**:

| Attribute   | Type | Required | Constraints | Default | Description |
|-------------|------|----------|-------------|---------|-------------|
| id          | int  | Yes      | > 0, unique | auto    | Unique sequential identifier |
| title       | str  | Yes      | 1-200 chars | -       | Task description |
| completed   | bool | Yes      | -           | False   | Completion status |

**Validation Rules**:

1. **Title Validation**:
   - MUST NOT be empty (minimum 1 character)
   - MUST NOT exceed 200 characters
   - Leading/trailing whitespace should be stripped
   - Empty strings after stripping are invalid

2. **ID Validation**:
   - MUST be a positive integer (> 0)
   - MUST be unique across all todos (even deleted ones)
   - Generated sequentially (1, 2, 3, ...)
   - Never reused after deletion

3. **Completed Validation**:
   - MUST be boolean (True or False)
   - Defaults to False on creation
   - Can be set to True (pending → completed)
   - Idempotent: marking completed todo as completed is allowed

**State Diagram**:

```
[Created] ---> [Pending (completed=False)]
                    |
                    | complete command
                    v
              [Completed (completed=True)]
                    |
                    | (no state change in Phase 1)
                    v
              [Completed (completed=True)]

[Any State] ---> [Deleted] (delete command, irreversible)
```

**Business Rules**:

- New todos start in Pending state (completed=False)
- Todos can transition from Pending to Completed
- Completed todos remain completed (no uncomplete in Phase 1)
- Deleted todos are removed from storage (no soft delete)
- IDs are never reused (monotonically increasing)

## Storage Structure

### TodoStorage

In-memory storage manager for all todos.

**Attributes**:

| Attribute | Type               | Description |
|-----------|--------------------|-------------|
| todos     | dict[int, TodoItem] | Maps todo ID to TodoItem instance |
| next_id   | int                | Counter for next available ID |

**Storage Invariants**:

1. **ID Uniqueness**: No two todos in `todos` dict have the same ID (enforced by dict key)
2. **Sequential IDs**: `next_id` always equals max(todos.keys()) + 1 (or 1 if empty)
3. **ID Persistence**: Once an ID is assigned, it's never reused (even after deletion)
4. **No Gaps**: After deletion, there may be gaps in ID sequence (e.g., 1, 2, 4, 5)

**Operations**:

### Create (Add Todo)

```
Input: title (str)
Process:
  1. Validate title (1-200 chars, non-empty)
  2. Generate new ID (current next_id)
  3. Create TodoItem(id=next_id, title=title, completed=False)
  4. Store in todos dict: todos[next_id] = new_todo
  5. Increment next_id by 1
Output: TodoItem with assigned ID
Errors: ValidationError if title invalid
```

### Read (Get Todo)

```
Input: id (int)
Process:
  1. Validate ID is positive integer
  2. Check if ID exists in todos dict
  3. Return todos[id]
Output: TodoItem
Errors: NotFoundError if ID doesn't exist
```

### Read All (List Todos)

```
Input: None
Process:
  1. Get all values from todos dict
  2. Sort by ID (ascending)
Output: List[TodoItem] (may be empty)
Errors: None (empty list if no todos)
```

### Update (Complete Todo)

```
Input: id (int)
Process:
  1. Validate ID is positive integer
  2. Check if ID exists in todos dict
  3. Set todos[id].completed = True
Output: Updated TodoItem
Errors: NotFoundError if ID doesn't exist
Note: Idempotent - can complete already-completed todo
```

### Delete (Remove Todo)

```
Input: id (int)
Process:
  1. Validate ID is positive integer
  2. Check if ID exists in todos dict
  3. Delete from dict: del todos[id]
  4. Do NOT decrement next_id (IDs never reused)
Output: None (or deleted TodoItem for confirmation)
Errors: NotFoundError if ID doesn't exist
```

## Data Relationships

**None** - TodoItem is a standalone entity with no relationships in Phase 1.

Potential future relationships (NOT in Phase 1):
- TodoItem → Category (many-to-one)
- TodoItem → Tags (many-to-many)
- TodoItem → User (many-to-one)

## Data Constraints Summary

| Constraint | Enforcement | Rationale |
|------------|-------------|-----------|
| Title 1-200 chars | Validation layer | User input sanity, display limits |
| Unique IDs | Storage layer (dict key) | Data integrity |
| Sequential IDs | Storage layer (counter) | Predictable, user-friendly |
| No ID reuse | Storage layer (never decrement) | Audit trail, referential integrity |
| In-memory only | Architecture | Phase 1 constraint |
| No persistence | Architecture | Phase 1 constraint |

## Implementation Guidance

**Python Data Structures**:

```python
from dataclasses import dataclass

@dataclass
class TodoItem:
    """Represents a single todo task."""
    id: int
    title: str
    completed: bool = False

    def __post_init__(self):
        """Validate todo attributes."""
        if not isinstance(self.title, str):
            raise ValidationError("Title must be a string")
        if len(self.title.strip()) == 0:
            raise ValidationError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValidationError("Title too long (max 200 characters)")
        self.title = self.title.strip()

class TodoStorage:
    """In-memory storage for todos."""

    def __init__(self):
        self.todos: dict[int, TodoItem] = {}
        self.next_id: int = 1

    # CRUD methods implementation...
```

**Memory Footprint**:

Estimated memory per todo:
- id (int): ~28 bytes
- title (str): ~50-250 bytes (avg ~100)
- completed (bool): ~28 bytes
- dict overhead: ~40 bytes

**Total per todo**: ~200 bytes

For 1000 todos: ~200 KB (well within memory limits)

## Testing Considerations

**Unit Tests Required**:

1. **TodoItem Validation**:
   - Empty title rejected
   - Title >200 chars rejected
   - Valid title accepted
   - Whitespace-only title rejected
   - Title trimmed properly

2. **Storage Operations**:
   - Add todo generates sequential IDs
   - Add multiple todos increments IDs correctly
   - Get existing todo succeeds
   - Get non-existent todo raises NotFoundError
   - List empty storage returns empty list
   - List populated storage returns all todos
   - Complete existing todo updates status
   - Complete non-existent todo raises NotFoundError
   - Delete existing todo removes from storage
   - Delete non-existent todo raises NotFoundError

3. **ID Management**:
   - IDs start at 1
   - IDs increment sequentially
   - Deleted IDs not reused
   - ID gaps handled correctly

## Phase 1 Compliance

✅ **In-memory only** - No file I/O, no databases
✅ **Simple structures** - Python dict and dataclass
✅ **No persistence** - Data lost on exit
✅ **Deterministic** - Sequential ID generation
✅ **Testable** - All operations have clear inputs/outputs

**No constitution violations** - Data model fully compliant with Phase 1 constraints.
