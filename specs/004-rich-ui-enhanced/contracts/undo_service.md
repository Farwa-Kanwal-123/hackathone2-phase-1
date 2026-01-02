# Undo Service Contract

**Feature**: 004-rich-ui-enhanced
**Module**: `src/services/undo_manager.py`
**Purpose**: Define interfaces for single-level undo functionality

## Overview

The `UndoManager` class provides single-level undo functionality by recording action snapshots and restoring previous states. Only the most recent action can be undone (no multi-level undo stack).

---

## Class: `UndoManager`

### Constructor

**Signature**:
```python
from typing import Optional
from src.services.undo_manager import ActionSnapshot

class UndoManager:
    def __init__(self):
        """
        Initialize undo manager with no action history.

        Attributes:
            last_action: The most recent action snapshot (None if no actions)
        """
        self.last_action: Optional[ActionSnapshot] = None
```

**Invariants**:
- Only one action is stored at a time (single-level undo)
- After successful undo, `last_action` is cleared (cannot undo twice)
- Recording new action overwrites previous action (no undo stack)

---

## ActionSnapshot Entity

**Purpose**: Capture state before an action for undo

**Structure**:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from copy import deepcopy
from src.todo import TodoItem

@dataclass
class ActionSnapshot:
    """
    Snapshot of a single action for undo.

    Attributes:
        action_type: Type of action ("add", "delete", "update", "complete")
        todo_id: ID of the todo affected
        previous_state: Deep copy of todo before action (None for "add")
        timestamp: When the action occurred
    """
    action_type: str
    todo_id: int
    previous_state: Optional[TodoItem]
    timestamp: datetime

    def __post_init__(self):
        """Validate action_type"""
        valid_types = ["add", "delete", "update", "complete"]
        if self.action_type not in valid_types:
            raise ValueError(
                f"action_type must be one of {valid_types}. Got: {self.action_type}"
            )
```

**Contract**:
- `action_type` must be "add", "delete", "update", or "complete"
- `previous_state` is `None` for "add" (todo didn't exist before)
- `previous_state` is a deep copy for other actions (prevents mutation)
- `timestamp` records when action occurred (for debugging/logging)

---

## Methods

### `record_action`

**Purpose**: Record an action before it's executed (for future undo)

**Signature**:
```python
from src.storage import TodoStorage
from datetime import datetime

def record_action(
    self,
    action_type: str,
    todo_id: int,
    storage: TodoStorage
) -> None:
    """
    Record an action snapshot before executing the action.

    Args:
        action_type: "add", "delete", "update", or "complete"
        todo_id: ID of the todo being modified
        storage: TodoStorage instance (to capture current state)

    Returns:
        None (stores snapshot in self.last_action)

    Raises:
        ValueError: If action_type is invalid

    Example:
        >>> undo_mgr = UndoManager()
        >>> # Before deleting todo ID 5:
        >>> undo_mgr.record_action("delete", 5, storage)
        >>> storage.delete(5)
        >>> # Later: can undo the delete

    Contract:
        - Must be called BEFORE the action is executed
        - Captures current state of todo (before modification)
        - Overwrites previous snapshot (single-level undo)
        - "add" action: previous_state=None (todo doesn't exist yet)
        - Other actions: previous_state=deepcopy(todo)
    """
```

**Recording Logic by Action Type**:

| Action Type | Previous State | Example |
|-------------|----------------|---------|
| `"add"` | `None` (todo doesn't exist) | About to add new todo |
| `"delete"` | `deepcopy(storage.todos[todo_id])` | Capture todo before deletion |
| `"update"` | `deepcopy(storage.todos[todo_id])` | Capture old title/priority/etc. |
| `"complete"` | `deepcopy(storage.todos[todo_id])` | Capture completed=False state |

**Important**: Must capture state BEFORE executing the action:
```python
# CORRECT:
undo_mgr.record_action("delete", 5, storage)  # Capture state
storage.delete(5)                              # Then execute

# INCORRECT:
storage.delete(5)                              # Execute first
undo_mgr.record_action("delete", 5, storage)  # Too late! Todo already gone
```

---

### `can_undo`

**Purpose**: Check if undo is available

**Signature**:
```python
def can_undo(self) -> bool:
    """
    Check if undo is available.

    Returns:
        True if last_action is not None, False otherwise

    Example:
        >>> undo_mgr = UndoManager()
        >>> undo_mgr.can_undo()
        False
        >>> undo_mgr.record_action("add", 1, storage)
        >>> undo_mgr.can_undo()
        True
    """
```

---

### `undo`

**Purpose**: Undo the last recorded action

**Signature**:
```python
def undo(self, storage: TodoStorage) -> str:
    """
    Undo the last recorded action.

    Args:
        storage: TodoStorage instance (to restore state)

    Returns:
        Success message describing what was undone

    Raises:
        ValueError: If no action to undo (last_action is None)

    Example:
        >>> undo_mgr.record_action("delete", 5, storage)
        >>> storage.delete(5)
        >>> message = undo_mgr.undo(storage)
        "Undone: Restored 'Fix bug' (ID: 5)"

    Contract:
        - Restores previous state based on action_type
        - Clears last_action after successful undo (cannot undo twice)
        - Raises ValueError if no action to undo
        - Returns descriptive message
    """
```

**Undo Logic by Action Type**:

| Action Type | Undo Operation | Example |
|-------------|----------------|---------|
| `"add"` | Delete the added todo | User added todo #10 → undo deletes #10 |
| `"delete"` | Restore deleted todo | User deleted todo #5 → undo restores #5 |
| `"update"` | Restore previous state | User changed title → undo restores old title |
| `"complete"` | Set completed=False | User marked complete → undo marks incomplete |

**Implementation**:
```python
def undo(self, storage: TodoStorage) -> str:
    if self.last_action is None:
        raise ValueError("No action to undo")

    snapshot = self.last_action
    action_type = snapshot.action_type
    todo_id = snapshot.todo_id
    previous_state = snapshot.previous_state

    try:
        if action_type == "add":
            # Undo add → delete the todo
            storage.delete(todo_id)
            message = f"Undone: Removed todo (ID: {todo_id})"

        elif action_type == "delete":
            # Undo delete → restore the todo
            if previous_state is None:
                raise ValueError("Cannot undo delete: no previous state")
            storage._restore_todo(previous_state)
            message = f"Undone: Restored '{previous_state.title}' (ID: {todo_id})"

        elif action_type == "update":
            # Undo update → restore previous state
            if previous_state is None:
                raise ValueError("Cannot undo update: no previous state")
            storage._restore_todo(previous_state)
            message = f"Undone: Reverted '{storage.todos[todo_id].title}' (ID: {todo_id})"

        elif action_type == "complete":
            # Undo complete → mark incomplete
            if todo_id not in storage.todos:
                raise ValueError(f"Cannot undo: todo {todo_id} not found")
            storage.todos[todo_id].completed = False
            message = f"Undone: Marked incomplete (ID: {todo_id})"

        else:
            raise ValueError(f"Unknown action type: {action_type}")

        # Clear undo history after successful undo
        self.last_action = None
        return message

    except Exception as e:
        # On error, keep undo history (allow retry)
        raise ValueError(f"Undo failed: {e}") from e
```

---

### `get_undo_description`

**Purpose**: Get description of what undo will do (for confirmation)

**Signature**:
```python
def get_undo_description(self) -> Optional[str]:
    """
    Get description of what undo will do.

    Returns:
        Human-readable description, or None if no action to undo

    Example:
        >>> undo_mgr.record_action("delete", 5, storage)
        >>> storage.delete(5)
        >>> undo_mgr.get_undo_description()
        "Undo delete of 'Fix bug' (ID: 5)"

    Contract:
        - Returns None if last_action is None
        - Returns descriptive text for confirmation prompts
    """
```

**Description Format**:
| Action Type | Description |
|-------------|-------------|
| `"add"` | `"Undo add of 'Task title' (ID: 5)"` |
| `"delete"` | `"Undo delete of 'Task title' (ID: 5)"` |
| `"update"` | `"Undo update of 'Task title' (ID: 5)"` |
| `"complete"` | `"Undo completion of 'Task title' (ID: 5)"` |

---

## Storage Extension Required

### `_restore_todo` Method

The undo functionality requires a new storage method to restore todos with exact state (including ID):

**Signature**:
```python
# Add to TodoStorage class
from copy import deepcopy

def _restore_todo(self, todo: TodoItem) -> None:
    """
    Restore a todo with its exact state (including ID).
    Used for undo operations.

    Args:
        todo: TodoItem to restore (with original ID)

    Contract:
        - Overwrites any existing todo with same ID
        - Does not update next_id (IDs are never reused)
        - Makes deep copy to prevent external mutation

    Example:
        >>> old_todo = TodoItem(id=5, title="Old", completed=False)
        >>> storage._restore_todo(old_todo)
        >>> storage.todos[5].title
        "Old"
    """
    self.todos[todo.id] = deepcopy(todo)
    # Do NOT update next_id - IDs are never reused
```

---

## Usage Workflow

### Standard Workflow

```python
from src.services.undo_manager import UndoManager
from src.storage import TodoStorage

storage = TodoStorage()
undo_mgr = UndoManager()

# 1. Add a todo (with undo support)
undo_mgr.record_action("add", storage.next_id, storage)
storage.add("Buy milk")  # ID: 1

# 2. Update a todo (with undo support)
undo_mgr.record_action("update", 1, storage)
storage.update(1, "Buy whole milk")

# 3. Undo the update
if undo_mgr.can_undo():
    print(undo_mgr.get_undo_description())  # "Undo update of 'Buy whole milk' (ID: 1)"
    message = undo_mgr.undo(storage)
    print(message)  # "Undone: Reverted 'Buy milk' (ID: 1)"

# 4. Cannot undo again (single-level)
undo_mgr.can_undo()  # False
```

### Error Handling

```python
# Attempting undo with no action
try:
    undo_mgr.undo(storage)
except ValueError as e:
    print(e)  # "No action to undo"

# Invalid action type
try:
    undo_mgr.record_action("invalid", 1, storage)
except ValueError as e:
    print(e)  # "action_type must be one of ['add', 'delete', 'update', 'complete']. Got: invalid"
```

---

## Limitations (By Design)

### Single-Level Undo Only

**Constraint**: Only the most recent action can be undone

**Rationale**:
- Simplifies implementation (no undo stack management)
- Matches spec requirement (FR-028: "Maintain a history of the last action")
- Sufficient for most use cases (prevent accidental deletes/updates)

**Out of Scope**:
- Multi-level undo (undo multiple actions)
- Redo functionality
- Undo persistence (undo history lost on app restart)

### No Undo for Certain Operations

**Cannot Undo**:
- List/view operations (read-only, nothing to undo)
- Search/filter operations (no state change)
- Operations that failed (only successful actions are recorded)

---

## Contract Tests

**Location**: `tests/contract/test_undo_contracts.py`

**Test Cases**:
1. `test_record_action_captures_state_contract` - Verify deep copy of previous state
2. `test_undo_add_contract` - Verify undo removes added todo
3. `test_undo_delete_contract` - Verify undo restores deleted todo
4. `test_undo_update_contract` - Verify undo restores previous title/priority
5. `test_undo_complete_contract` - Verify undo sets completed=False
6. `test_undo_clears_history_contract` - Verify cannot undo twice
7. `test_undo_without_action_raises_contract` - Verify ValueError when no action

**Example Test**:
```python
import pytest
from copy import deepcopy
from src.services.undo_manager import UndoManager, ActionSnapshot
from src.storage import TodoStorage
from src.todo import TodoItem

def test_undo_delete_contract():
    """Verify undo restores deleted todo with exact state"""
    # Arrange
    storage = TodoStorage()
    undo_mgr = UndoManager()

    storage.add("Test todo")
    todo = storage.todos[1]
    todo.priority = "High"  # Modify priority

    # Record and execute delete
    undo_mgr.record_action("delete", 1, storage)
    storage.delete(1)

    # Assert: todo is deleted
    assert 1 not in storage.todos

    # Act: undo delete
    message = undo_mgr.undo(storage)

    # Assert: todo is restored with exact state
    assert 1 in storage.todos
    assert storage.todos[1].title == "Test todo"
    assert storage.todos[1].priority == "High"
    assert "Restored 'Test todo'" in message

    # Assert: cannot undo again
    assert not undo_mgr.can_undo()
```

---

## Performance Considerations

### Memory Usage

| Operation | Memory Impact | Notes |
|-----------|---------------|-------|
| `record_action` | O(1) - single TodoItem deep copy | Acceptable (one todo is small) |
| `undo` | O(1) - restore one TodoItem | Minimal impact |

**Deep Copy Overhead**: TodoItem is small (< 1KB), so deep copy is fast.

### Time Complexity

| Method | Time Complexity | Notes |
|--------|----------------|-------|
| `record_action` | O(1) | Deep copy + assignment |
| `can_undo` | O(1) | Check if last_action is None |
| `undo` | O(1) | Restore state based on action_type |
| `get_undo_description` | O(1) | Format string |

**All operations are O(1)** - efficient for interactive use.

---

## Summary

**Undo Manager Contract**:
- ✅ Single-level undo (last action only)
- ✅ Supports add, delete, update, complete actions
- ✅ Deep copy ensures previous state is immutable
- ✅ Clear error messages when undo unavailable
- ✅ Storage extension required (`_restore_todo` method)
- ✅ O(1) time and space complexity

**Key Principles**:
- Record BEFORE executing action (capture state)
- Clear history after successful undo (cannot undo twice)
- Fail fast with descriptive errors
- Deep copy prevents mutation bugs

**Integration**: Works with TodoStorage without modifying core CRUD operations
