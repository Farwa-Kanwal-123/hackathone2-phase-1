# Data Model: Update Todo Titles

**Feature**: `002-update-todo`
**Created**: 2025-12-25
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md)

## Overview

This document specifies the data model changes required to support updating todo titles. The update operation extends the existing Phase 1 architecture with minimal modifications to the storage layer.

## Entities

### TodoItem (No Changes)

The `TodoItem` dataclass remains unchanged. All validation logic is preserved and reused.

**Existing Structure**:
```python
@dataclass
class TodoItem:
    id: int
    title: str
    completed: bool = False
```

**Validation Rules** (unchanged):
- Title must be 1-200 characters
- Title cannot be empty or whitespace-only
- ID is immutable once assigned
- Completed status defaults to False

**Why No Changes**: The update operation creates a new `TodoItem` instance with the updated title, leveraging existing validation in `__post_init__`.

---

## Storage Layer

### TodoStorage.update() Method (NEW)

**Purpose**: Update an existing todo's title while preserving its ID and completion status.

**Method Signature**:
```python
def update(self, todo_id: int, new_title: str) -> TodoItem:
    """
    Update the title of an existing todo.

    Args:
        todo_id: The ID of the todo to update
        new_title: The new title (must pass TodoItem validation)

    Returns:
        The updated TodoItem

    Raises:
        NotFoundError: If todo_id does not exist
        ValidationError: If new_title fails validation
    """
```

**Implementation Strategy**:
```python
# Pseudocode for update operation
1. Check if todo_id exists in self.todos
   - If not found → raise NotFoundError(f"Todo with ID {todo_id} not found")

2. Retrieve the existing TodoItem
   old_todo = self.todos[todo_id]

3. Create a new TodoItem with updated title
   updated_todo = TodoItem(
       id=old_todo.id,           # Preserve ID
       title=new_title,          # New title (validated in __post_init__)
       completed=old_todo.completed  # Preserve status
   )
   # Note: If new_title is invalid, TodoItem.__post_init__ raises ValidationError

4. Replace the old todo in storage
   self.todos[todo_id] = updated_todo

5. Return the updated TodoItem
   return updated_todo
```

**Data Flow**:
```
Input: todo_id=1, new_title="Buy groceries"

self.todos BEFORE:
{
    1: TodoItem(id=1, title="Buy grocreies", completed=False),
    2: TodoItem(id=2, title="Write report", completed=True)
}

Operation: update(1, "Buy groceries")
    ↓
Retrieve: old_todo = TodoItem(id=1, title="Buy grocreies", completed=False)
    ↓
Create: new_todo = TodoItem(id=1, title="Buy groceries", completed=False)
    ↓
Replace: self.todos[1] = new_todo

self.todos AFTER:
{
    1: TodoItem(id=1, title="Buy groceries", completed=False),  # Title updated
    2: TodoItem(id=2, title="Write report", completed=True)     # Unchanged
}

Return: TodoItem(id=1, title="Buy groceries", completed=False)
```

---

## Error Handling

### NotFoundError

**When Raised**: Todo with the specified ID does not exist in storage.

**Example**:
```python
# Storage contains IDs: [1, 2, 3]
storage.update(99, "New title")
# Raises: NotFoundError("Todo with ID 99 not found")
```

**User-Facing Message**: "Error: Todo with ID 99 not found"

---

### ValidationError

**When Raised**: New title fails TodoItem validation rules.

**Example 1 - Empty Title**:
```python
storage.update(1, "")
# Raises: ValidationError("Title cannot be empty or whitespace")
```

**Example 2 - Title Too Long**:
```python
storage.update(1, "A" * 201)
# Raises: ValidationError("Title cannot exceed 200 characters")
```

**Example 3 - Whitespace Only**:
```python
storage.update(1, "   ")
# Raises: ValidationError("Title cannot be empty or whitespace")
```

**User-Facing Messages**: Same as add command validation errors (consistency).

---

## Invariants

**Data Integrity Guarantees**:

1. **ID Immutability**: Todo IDs NEVER change during update operations
   - Enforced by: Creating new TodoItem with `id=old_todo.id`

2. **Status Preservation**: Completion status NEVER changes during title updates
   - Enforced by: Creating new TodoItem with `completed=old_todo.completed`

3. **Validation Consistency**: Update validation rules IDENTICAL to add validation
   - Enforced by: Reusing `TodoItem.__post_init__` validation

4. **Atomicity**: Update operation is all-or-nothing
   - If validation fails → no changes to storage
   - If ID not found → no changes to storage
   - Only successful updates modify `self.todos`

5. **Determinism**: Same input produces same output
   - update(1, "New title") always produces the same result
   - No randomness, timestamps, or non-deterministic behavior

---

## State Transitions

**Incomplete Todo Update**:
```
BEFORE: TodoItem(id=1, title="Old title", completed=False)
ACTION: update(1, "New title")
AFTER:  TodoItem(id=1, title="New title", completed=False)
```
**Status**: Remains incomplete (False → False)

---

**Completed Todo Update**:
```
BEFORE: TodoItem(id=2, title="Old title", completed=True)
ACTION: update(2, "New title")
AFTER:  TodoItem(id=2, title="New title", completed=True)
```
**Status**: Remains completed (True → True)

---

**Invalid Update (ID Not Found)**:
```
BEFORE: self.todos = {1: TodoItem(...), 2: TodoItem(...)}
ACTION: update(99, "New title")
RESULT: NotFoundError raised, self.todos unchanged
AFTER:  self.todos = {1: TodoItem(...), 2: TodoItem(...)}  # No changes
```

---

**Invalid Update (Validation Failure)**:
```
BEFORE: TodoItem(id=1, title="Valid title", completed=False)
ACTION: update(1, "")
RESULT: ValidationError raised, self.todos unchanged
AFTER:  TodoItem(id=1, title="Valid title", completed=False)  # No changes
```

---

## Testing Considerations

**Unit Tests Required** (in `tests/unit/test_storage.py`):

1. **Happy Path**:
   - Update incomplete todo's title
   - Update completed todo's title
   - Verify ID preserved
   - Verify status preserved

2. **Error Cases**:
   - Update non-existent ID (NotFoundError)
   - Update with empty title (ValidationError)
   - Update with whitespace-only title (ValidationError)
   - Update with title > 200 chars (ValidationError)

3. **Edge Cases**:
   - Update title to same value (idempotent)
   - Update to duplicate another todo's title (allowed)
   - Update with title exactly 200 chars (valid boundary)

**Integration Tests Required** (in `tests/integration/test_commands.py`):

1. **CLI Command**:
   - `update <id> "<new-title>"` executes successfully
   - Confirmation message shows old and new titles
   - List command shows updated title

2. **Error Messages**:
   - Clear error for non-existent ID
   - Clear error for invalid title

---

## Compatibility

**Phase 1 Constraints Maintained**:
- ✅ In-memory storage only (no persistence)
- ✅ Python stdlib only (no new dependencies)
- ✅ CLI-only interface
- ✅ Deterministic behavior

**Backward Compatibility**:
- ✅ Existing methods unchanged (add, list, complete, delete)
- ✅ Existing tests remain valid
- ✅ No breaking changes to TodoItem or TodoStorage API

**Forward Compatibility**:
- Update method signature allows future enhancements:
  - Phase 2 could add persistence after update
  - Could add optional parameters (e.g., `preserve_timestamp`)
  - Could extend to batch updates in future phases

---

## Summary

**Changes**:
- ✅ Add `TodoStorage.update(todo_id, new_title)` method
- ❌ No changes to `TodoItem` dataclass
- ❌ No changes to `exceptions.py`

**Key Design Decisions**:
1. **Immutable Pattern**: Replace entire TodoItem rather than mutating
2. **Validation Reuse**: Leverage existing TodoItem validation
3. **Minimal Surface Area**: Single method addition, no API changes

**Traceability**:
- Implements: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006
- Supports: SC-005 (data integrity)
- Aligns with: Constitution Principle IV (Deterministic Behavior)
