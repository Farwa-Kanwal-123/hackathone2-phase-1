# CLI Interface Contract: Todo CLI Core

**Feature**: Todo CLI Core
**Date**: 2025-12-24
**Status**: Design
**Interface Type**: Command-Line Interface (CLI)

## Overview

This document specifies the exact CLI command structure, arguments, outputs, and error messages for the Todo CLI application. All commands follow consistent patterns for usability and determinism.

## Command Format

```
todo <command> [arguments] [options]
```

**Global Options**:
- `--help`, `-h`: Display help information

**Exit Codes**:
- `0`: Success
- `1`: Error (validation, not found, invalid input)

## Commands

### 1. Add Todo

**Purpose**: Create a new todo item with a given title

**Syntax**:
```bash
todo add <title>
```

**Arguments**:
| Argument | Type   | Required | Constraints | Description |
|----------|--------|----------|-------------|-------------|
| title    | string | Yes      | 1-200 chars | The todo task description |

**Examples**:
```bash
$ todo add "Buy groceries"
$ todo add "Read Python book"
$ todo add "Call mom"
```

**Success Output**:
```
Todo added: {title} (ID: {id})
```

Example:
```
$ todo add "Buy groceries"
Todo added: Buy groceries (ID: 1)
```

**Error Cases**:

| Error | Condition | Output | Exit Code |
|-------|-----------|--------|-----------|
| Empty title | Title is empty string | `Error: Title cannot be empty` | 1 |
| Title too long | Title > 200 chars | `Error: Title too long (max 200 characters)` | 1 |
| No title | No argument provided | `Error: Title is required` | 1 |

**Error Examples**:
```bash
$ todo add ""
Error: Title cannot be empty

$ todo add "A very long title exceeding 200 characters..."
Error: Title too long (max 200 characters)

$ todo add
Error: Title is required
```

---

### 2. List Todos

**Purpose**: Display all todo items with their IDs, titles, and completion status

**Syntax**:
```bash
todo list
```

**Arguments**: None

**Examples**:
```bash
$ todo list
```

**Success Output** (with todos):
```
{id}. [{status}] {title}
{id}. [{status}] {title}
...
```

Where:
- `{id}`: Todo ID (integer)
- `{status}`: `[x]` for completed, `[ ]` for pending
- `{title}`: Todo title

Example:
```
$ todo list
1. [ ] Buy groceries
2. [x] Read Python book
3. [ ] Call mom
```

**Success Output** (empty list):
```
No todos found
```

Example:
```
$ todo list
No todos found
```

**Error Cases**: None (always succeeds, even with empty list)

**Exit Code**: Always 0

**Ordering**: Todos listed in ascending ID order (1, 2, 3, ...)

---

### 3. Complete Todo

**Purpose**: Mark a todo item as completed

**Syntax**:
```bash
todo complete <id>
```

**Arguments**:
| Argument | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| id       | int  | Yes      | > 0, exists | The ID of the todo to complete |

**Examples**:
```bash
$ todo complete 1
$ todo complete 42
```

**Success Output**:
```
Todo #{id} marked as complete
```

Example:
```
$ todo complete 1
Todo #1 marked as complete
```

**Error Cases**:

| Error | Condition | Output | Exit Code |
|-------|-----------|--------|-----------|
| Non-existent ID | ID not in storage | `Error: Todo #{id} not found` | 1 |
| Invalid ID | ID is not a number | `Error: Invalid ID '{id}' - ID must be a number` | 1 |
| No ID | No argument provided | `Error: ID is required` | 1 |

**Error Examples**:
```bash
$ todo complete 999
Error: Todo #999 not found

$ todo complete abc
Error: Invalid ID 'abc' - ID must be a number

$ todo complete
Error: ID is required
```

**Idempotency**: Marking an already-completed todo as complete is allowed and succeeds (no error).

---

### 4. Delete Todo

**Purpose**: Remove a todo item from the list

**Syntax**:
```bash
todo delete <id>
```

**Arguments**:
| Argument | Type | Required | Constraints | Description |
|----------|------|----------|-------------|-------------|
| id       | int  | Yes      | > 0, exists | The ID of the todo to delete |

**Examples**:
```bash
$ todo delete 1
$ todo delete 42
```

**Success Output**:
```
Todo #{id} deleted
```

Example:
```
$ todo delete 1
Todo #1 deleted
```

**Error Cases**:

| Error | Condition | Output | Exit Code |
|-------|-----------|--------|-----------|
| Non-existent ID | ID not in storage | `Error: Todo #{id} not found` | 1 |
| Invalid ID | ID is not a number | `Error: Invalid ID '{id}' - ID must be a number` | 1 |
| No ID | No argument provided | `Error: ID is required` | 1 |

**Error Examples**:
```bash
$ todo delete 999
Error: Todo #999 not found

$ todo delete abc
Error: Invalid ID 'abc' - ID must be a number

$ todo delete
Error: ID is required
```

**Side Effects**: Deleted todo IDs are never reused. After deleting ID 2, the next created todo will still be ID 4 (if 3 exists), not 2.

---

### 5. Help

**Purpose**: Display usage information and command descriptions

**Syntax**:
```bash
todo --help
todo -h
todo help
```

**Arguments**: None

**Examples**:
```bash
$ todo --help
$ todo -h
$ todo help
```

**Output**:
```
Todo CLI - Simple command-line todo manager

Usage:
  todo add <title>        Add a new todo item
  todo list               List all todos
  todo complete <id>      Mark a todo as complete
  todo delete <id>        Delete a todo item
  todo --help             Show this help message

Examples:
  todo add "Buy groceries"
  todo list
  todo complete 1
  todo delete 2
```

**Exit Code**: 0

---

## Error Message Format

All error messages follow a consistent format:

```
Error: {description}
```

**Rules**:
- Prefix: Always start with "Error: "
- Description: User-friendly, actionable message
- No stack traces: Never expose Python stack traces to users
- Specific: Mention exact values when helpful (e.g., ID numbers)

**Examples of Good Error Messages**:
- `Error: Title cannot be empty`
- `Error: Todo #42 not found`
- `Error: Invalid ID 'abc' - ID must be a number`

**Examples of Bad Error Messages** (avoid these):
- `KeyError: 42` (too technical)
- `Error` (too vague)
- `An error occurred` (not actionable)

---

## Command Examples (Full Workflow)

```bash
# Start with empty list
$ todo list
No todos found

# Add some todos
$ todo add "Buy groceries"
Todo added: Buy groceries (ID: 1)

$ todo add "Read Python book"
Todo added: Read Python book (ID: 2)

$ todo add "Call mom"
Todo added: Call mom (ID: 3)

# List all todos
$ todo list
1. [ ] Buy groceries
2. [ ] Read Python book
3. [ ] Call mom

# Complete a todo
$ todo complete 2
Todo #2 marked as complete

# List again (see completed status)
$ todo list
1. [ ] Buy groceries
2. [x] Read Python book
3. [ ] Call mom

# Try to complete non-existent todo
$ todo complete 999
Error: Todo #999 not found

# Delete a todo
$ todo delete 1
Todo #1 deleted

# List after deletion (ID 1 is gone)
$ todo list
2. [x] Read Python book
3. [ ] Call mom

# Add another todo (ID continues from 4, not 1)
$ todo add "Exercise"
Todo added: Exercise (ID: 4)

$ todo list
2. [x] Read Python book
3. [ ] Call mom
4. [ ] Exercise

# Get help
$ todo --help
Todo CLI - Simple command-line todo manager
...
```

---

## Implementation Requirements

**Argument Parsing**:
- Use Python's `argparse` module
- Define subparsers for each command (add, list, complete, delete)
- Validate argument types and counts
- Provide custom error messages for missing/invalid arguments

**Output Formatting**:
- All output to stdout (except errors)
- Errors to stderr (optional, can use stdout)
- Consistent formatting (no extra newlines, spacing)
- Flush output after each operation

**Exit Codes**:
- Use `sys.exit(0)` for success
- Use `sys.exit(1)` for errors
- Catch all exceptions at top level

**Determinism**:
- Same command sequence always produces same output
- No timestamps in output (violates Phase 1 determinism)
- No random elements
- Consistent ordering (by ID ascending)

---

## Testing Requirements

**Contract Tests** (tests/integration/test_commands.py):

Each command must have tests for:
1. Success case (valid input, expected output)
2. All error cases (invalid input, expected error message)
3. Exit codes (0 for success, 1 for errors)
4. Output format (exact string matching)

**Example Test Cases**:

```python
def test_add_todo_success():
    output = run_command(["todo", "add", "Buy milk"])
    assert output == "Todo added: Buy milk (ID: 1)"
    assert exit_code == 0

def test_add_todo_empty_title():
    output = run_command(["todo", "add", ""])
    assert output == "Error: Title cannot be empty"
    assert exit_code == 1

def test_list_empty():
    output = run_command(["todo", "list"])
    assert output == "No todos found"
    assert exit_code == 0

# ... more tests for each command and error case
```

---

## Phase 1 Compliance

✅ **CLI-only interface** - No web, no GUI
✅ **Deterministic output** - Same input = same output
✅ **User-friendly errors** - Clear, actionable messages
✅ **No persistence** - In-memory only
✅ **Standard patterns** - Follows POSIX CLI conventions

**No constitution violations** - CLI interface fully compliant with Phase 1 constraints.
