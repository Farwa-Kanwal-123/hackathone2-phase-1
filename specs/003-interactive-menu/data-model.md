# Data Model: Interactive Menu-Based Todo Console

**Feature**: `003-interactive-menu`
**Created**: 2025-12-28
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md)

## Overview

This document specifies the data model for the interactive menu feature. **No changes to existing entities** - the interactive menu is a presentation layer that reuses existing TodoItem and TodoStorage unchanged.

## Entities

### TodoItem (No Changes)

The `TodoItem` dataclass remains completely unchanged from Phase 1.

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

**Why No Changes**: The interactive menu operates at the presentation layer only. All todo data structures and validation logic remain identical.

---

### TodoStorage (No Changes)

The `TodoStorage` class remains completely unchanged from Phase 1.

**Existing Structure**:
- In-memory dictionary: `{id: TodoItem}`
- Sequential ID generation starting from 1
- Methods: `add()`, `list_all()`, `complete()`, `update()`, `delete()`

**Why No Changes**: Storage layer is unaware of how users interact with it (CLI args vs interactive menu). The interactive menu calls the same storage methods as the CLI.

---

## New Components (Presentation Layer Only)

### MenuChoice (Internal Type)

**Purpose**: Represent a user's menu selection (not a persistent entity).

**Structure**:
- Integer value (1-6 for menu options)
- Validation: Must be in valid range, numeric

**Usage**: Temporary value during menu loop - not stored, not passed to storage layer.

---

### InteractiveSession (Concept, Not a Class)

**Purpose**: Represent the runtime state during an interactive menu session.

**Characteristics**:
- Single TodoStorage instance for entire session
- Session starts when `uv run main.py` executes
- Session ends when user selects "Exit" or presses Ctrl+C
- All data lost when session ends (in-memory only)

**Not Implemented as a Class**: This is a conceptual model of the user session, not a concrete data structure. The session is managed by the `main.py` loop.

---

## Data Flow

### Add Todo (Interactive)

```text
User Input Flow:
  Menu Selection (1) → Prompt("Enter todo title:") → User Types "Buy milk" → Enter

Internal Data Flow:
  interactive_add(storage)
    ↓
  prompt_for_input("Enter todo title:") → returns "Buy milk"
    ↓
  handle_add(storage, "Buy milk")
    ↓
  storage.add("Buy milk")
    ↓
  Creates TodoItem(id=1, title="Buy milk", completed=False)
    ↓
  Stores in storage.todos[1]
    ↓
  Returns TodoItem to handler
    ↓
  Displays confirmation: "Todo added: Buy milk (ID: 1)"
```

**Key Point**: Same TodoItem creation as CLI mode - just input source differs (prompt vs argument).

---

### List Todos (Interactive)

```text
User Input Flow:
  Menu Selection (2) → Display List

Internal Data Flow:
  interactive_list(storage)
    ↓
  handle_list(storage)
    ↓
  storage.list_all()
    ↓
  Returns list of TodoItem objects sorted by ID
    ↓
  Formats and displays each todo
```

**Key Point**: Identical to CLI list operation - no data model differences.

---

### Complete/Update/Delete (Interactive)

```text
User Input Flow:
  Menu Selection (3/4/5) → Prompt("Enter todo ID:") → User Types "1" → Enter
  (For Update) → Prompt("Enter new title:") → User Types "Buy groceries" → Enter

Internal Data Flow:
  Same as CLI mode, but inputs come from prompts instead of arguments
```

**Key Point**: Data operations identical - only input mechanism differs.

---

## State Persistence

**Session Lifecycle**:
1. `uv run main.py` → TodoStorage() created (empty dict)
2. User adds/modifies todos → storage.todos dict updated in memory
3. User selects "Exit" or Ctrl+C → Python process terminates
4. All data lost (storage dict destroyed)

**No Changes from Phase 1**: In-memory only, no file persistence.

---

## Validation Rules

**Input Validation** (Interactive Layer - NEW):
- Menu choice: Must be 1-6 (numeric, in range)
- Todo ID: Must be numeric, must exist in storage
- Empty input: Re-prompt user (don't crash)
- Whitespace-only: Strip and validate

**Data Validation** (Storage Layer - UNCHANGED):
- Title: 1-200 characters, not empty, not whitespace-only
- ID: Positive integer, assigned by storage (user cannot set)
- Completed: Boolean only

**Error Handling**:
- Interactive layer: Catches exceptions, displays error, re-prompts
- Storage layer: Raises ValidationError, NotFoundError (unchanged)

---

## Invariants (Unchanged from Phase 1)

**Data Integrity Guarantees**:

1. **ID Immutability**: Todo IDs NEVER change
   - Enforced by: TodoStorage sequential ID generation

2. **ID Uniqueness**: No two todos have the same ID
   - Enforced by: Dictionary key uniqueness

3. **Sequential IDs**: IDs increment sequentially (no gaps reused)
   - Enforced by: `next_id` counter in TodoStorage

4. **Validation Consistency**: Same validation rules in CLI and interactive mode
   - Enforced by: Both modes call same `storage.add()` method

5. **Determinism**: Same operations produce same results
   - Enforced by: No randomness, no timestamps in business logic

---

## Integration with Existing Data Model

**Reuse Strategy**:
- ✅ **TodoItem**: Used directly, no wrapper classes
- ✅ **TodoStorage**: Called directly, no abstraction layer
- ✅ **Exceptions**: Caught and displayed interactively, not re-raised
- ✅ **Validation**: Delegated to TodoItem.__post_init__ (same as CLI)

**No Duplication**:
- ❌ No new entity classes
- ❌ No new validation logic
- ❌ No new storage mechanisms
- ✅ Only new presentation logic (menu display, prompts)

---

## Testing Considerations

**Unit Tests** (Interactive Layer):
- Test menu choice validation (1-6, numeric, invalid inputs)
- Test prompt functions return correct user input
- Test ID prompt validation (numeric, error handling)
- Test interactive handlers call correct storage methods

**Integration Tests** (End-to-End):
- Test full add workflow (menu → prompt → add → display → menu)
- Test full list workflow
- Test full complete/update/delete workflows
- Test error scenarios (invalid ID, empty title, etc.)

**Data Model Tests** (No Changes):
- All existing Phase 1 tests remain valid
- 63 tests from Phase 1 must still pass (regression check)

---

## Compatibility

**Phase 1 Constraints Maintained**:
- ✅ In-memory storage only (no persistence)
- ✅ Python stdlib only (no new dependencies)
- ✅ CLI-only interface (text-based menu)
- ✅ Deterministic behavior

**Backward Compatibility**:
- ✅ Existing CLI mode unchanged (`python -m src.main add "title"`)
- ✅ Existing data structures unchanged
- ✅ Existing tests remain valid
- ✅ No breaking changes to TodoItem or TodoStorage API

---

## Summary

**Data Model Changes**: **NONE**

**New Components**:
- Menu display logic (presentation only)
- Interactive prompt functions (input gathering only)
- Menu loop (control flow only)

**Key Design Decision**: Interactive menu is a **thin presentation layer** that wraps existing data structures and operations. No changes to core data model ensures:
- Minimal implementation complexity
- Reuse of validated logic
- Preservation of existing tests
- Easy rollback if needed

**Traceability**:
- Implements: All FR-* requirements (menu and interaction logic)
- Uses: Existing TodoItem and TodoStorage (no modifications)
- Maintains: Phase 1 constraints and principles
