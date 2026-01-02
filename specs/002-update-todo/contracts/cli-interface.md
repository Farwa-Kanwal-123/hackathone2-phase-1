# CLI Interface Contract: Update Command

**Feature**: `002-update-todo`
**Created**: 2025-12-25
**Related**: [spec.md](../spec.md) | [plan.md](../plan.md) | [data-model.md](../data-model.md)

## Overview

This document specifies the command-line interface contract for the `update` command. It defines syntax, arguments, output formats, exit codes, and error messages.

---

## Command Syntax

### Basic Form

```bash
python -m src.main update <id> <new-title>
```

**Positional Arguments**:
1. `id` (integer, required): The ID of the todo to update
2. `new-title` (string, required): The new title for the todo

**Examples**:
```bash
# Update todo with ID 1
python -m src.main update 1 "Buy groceries"

# Update completed todo
python -m src.main update 3 "Submit final report"

# Update with quoted string (handles spaces)
python -m src.main update 2 "Review pull request #42"
```

---

## Argument Specifications

### `<id>` Argument

**Type**: Integer (positive)
**Required**: Yes
**Validation**:
- Must be a valid integer
- Must correspond to an existing todo ID

**Valid Examples**:
```bash
update 1 "New title"
update 42 "New title"
update 999 "New title"
```

**Invalid Examples**:
```bash
update abc "New title"       # Non-integer → argparse error
update -5 "New title"         # Negative integer (caught by argparse type=int)
update 99 "New title"         # Valid integer, but ID doesn't exist → NotFoundError
```

---

### `<new-title>` Argument

**Type**: String
**Required**: Yes
**Validation**:
- Length: 1-200 characters
- Cannot be empty after stripping whitespace
- Cannot be whitespace-only

**Valid Examples**:
```bash
update 1 "Buy groceries"
update 1 "A"                                    # Single character
update 1 "$(python -c 'print("A"*200)')"       # Exactly 200 characters
update 1 "Review PR #123 and merge if tests pass"  # Special characters allowed
```

**Invalid Examples**:
```bash
update 1 ""                                     # Empty string → ValidationError
update 1 "   "                                  # Whitespace-only → ValidationError
update 1 "$(python -c 'print("A"*201)')"       # 201 characters → ValidationError
```

---

## Success Output

### Format

```
Updated: '<old-title>' → '<new-title>' (ID: <id>)
```

**Components**:
- `Updated:` - Status indicator
- `'<old-title>'` - Original title (single-quoted for clarity)
- `→` - Visual separator showing transition
- `'<new-title>'` - New title (single-quoted for clarity)
- `(ID: <id>)` - Todo identifier for reference

**Exit Code**: `0`

---

### Success Examples

**Example 1: Typo Correction**
```bash
$ python -m src.main update 1 "Buy groceries"
Updated: 'Buy grocreies' → 'Buy groceries' (ID: 1)
```

**Example 2: Completed Todo Update**
```bash
$ python -m src.main update 2 "Submit final quarterly report"
Updated: 'Submit report' → 'Submit final quarterly report' (ID: 2)
```

**Example 3: Special Characters**
```bash
$ python -m src.main update 3 "Review PR #42 & merge"
Updated: 'Review PR' → 'Review PR #42 & merge' (ID: 3)
```

---

## Error Output

### Error 1: Todo Not Found

**Condition**: ID does not exist in storage

**Output Format**:
```
Error: Todo with ID <id> not found
```

**Exit Code**: `1`

**Example**:
```bash
$ python -m src.main update 99 "New title"
Error: Todo with ID 99 not found
$ echo $?
1
```

---

### Error 2: Empty or Whitespace-Only Title

**Condition**: New title is empty or contains only whitespace

**Output Format**:
```
Error: Title cannot be empty or whitespace
```

**Exit Code**: `1`

**Examples**:
```bash
$ python -m src.main update 1 ""
Error: Title cannot be empty or whitespace
$ echo $?
1

$ python -m src.main update 1 "   "
Error: Title cannot be empty or whitespace
$ echo $?
1
```

---

### Error 3: Title Exceeds Maximum Length

**Condition**: New title exceeds 200 characters

**Output Format**:
```
Error: Title cannot exceed 200 characters
```

**Exit Code**: `1`

**Example**:
```bash
$ python -m src.main update 1 "$(python -c 'print("A"*201)')"
Error: Title cannot exceed 200 characters
$ echo $?
1
```

---

### Error 4: Invalid ID Argument

**Condition**: ID argument is not a valid integer

**Output Format**: (argparse standard error)
```
usage: todo update [-h] id new_title
todo update: error: argument id: invalid int value: '<value>'
```

**Exit Code**: `2` (argparse standard)

**Example**:
```bash
$ python -m src.main update abc "New title"
usage: todo update [-h] id new_title
todo update: error: argument id: invalid int value: 'abc'
$ echo $?
2
```

---

## Argparse Configuration

### Subcommand Definition

```python
update_parser = subparsers.add_parser(
    'update',
    help='Update the title of an existing todo'
)
update_parser.add_argument(
    'id',
    type=int,
    help='ID of the todo to update'
)
update_parser.add_argument(
    'new_title',
    type=str,
    help='New title for the todo (1-200 characters)'
)
```

---

## Help Output

### Command-Specific Help

```bash
$ python -m src.main update --help
usage: todo update [-h] id new_title

Update the title of an existing todo

positional arguments:
  id          ID of the todo to update
  new_title   New title for the todo (1-200 characters)

options:
  -h, --help  show this help message and exit
```

### Main Help (Updated)

```bash
$ python -m src.main --help
usage: todo [-h] {add,list,complete,delete,update} ...

Todo CLI - Manage your tasks from the command line

positional arguments:
  {add,list,complete,delete,update}
                        Available commands
    add                 Add a new todo
    list                List all todos
    complete            Mark a todo as complete
    delete              Delete a todo
    update              Update the title of an existing todo

options:
  -h, --help            show this help message and exit
```

---

## Exit Codes

| Code | Meaning | Examples |
|------|---------|----------|
| `0` | Success | Todo updated successfully |
| `1` | Application error | Todo not found, validation error |
| `2` | Usage error | Invalid arguments (argparse) |

**Consistency**: Follows existing command exit code patterns (FR-012).

---

## Edge Cases and Behavior

### Idempotency

**Scenario**: Updating a todo to its current title

```bash
# Current state: ID 1, title "Buy groceries"
$ python -m src.main update 1 "Buy groceries"
Updated: 'Buy groceries' → 'Buy groceries' (ID: 1)
```

**Behavior**: Operation succeeds, no state change, confirmation shown.

---

### Duplicate Titles Allowed

**Scenario**: Updating a todo to match another todo's title

```bash
# Existing: ID 1 "Buy groceries", ID 2 "Write report"
$ python -m src.main update 2 "Buy groceries"
Updated: 'Write report' → 'Buy groceries' (ID: 2)

# Result: Both ID 1 and ID 2 now have title "Buy groceries"
```

**Behavior**: Operation succeeds. Duplicate titles are allowed (no uniqueness constraint).

---

### Status Preservation

**Scenario**: Updating a completed todo

```bash
# Before: ID 3, title "Old title", status: completed
$ python -m src.main update 3 "New title"
Updated: 'Old title' → 'New title' (ID: 3)

$ python -m src.main list
1. [ ] Buy groceries
2. [ ] Buy groceries
3. [x] New title    # Still marked as completed
```

**Behavior**: Completion status is preserved (completed → completed).

---

## Integration with Other Commands

### Workflow Example: Add → Update → List

```bash
# Step 1: Add a todo with a typo
$ python -m src.main add "Buy grocreies"
Todo added: Buy grocreies (ID: 1)

# Step 2: Update to fix typo
$ python -m src.main update 1 "Buy groceries"
Updated: 'Buy grocreies' → 'Buy groceries' (ID: 1)

# Step 3: Verify update
$ python -m src.main list
1. [ ] Buy groceries
```

---

### Workflow Example: Complete → Update → List

```bash
# Step 1: Add and complete a todo
$ python -m src.main add "Submit report"
Todo added: Submit report (ID: 2)

$ python -m src.main complete 2
Completed: Submit report (ID: 2)

# Step 2: Update the completed todo
$ python -m src.main update 2 "Submit final quarterly report"
Updated: 'Submit report' → 'Submit final quarterly report' (ID: 2)

# Step 3: Verify update (status preserved)
$ python -m src.main list
1. [ ] Buy groceries
2. [x] Submit final quarterly report    # Still completed
```

---

## Non-Functional Requirements

**Performance** (SC-001):
- Command execution completes in <5 seconds
- Instant CLI response (in-memory operation)

**Usability** (SC-003):
- Error messages are self-explanatory
- Users can correct errors without consulting documentation

**Consistency** (SC-006):
- Follows same patterns as existing commands (add, complete, delete)
- Same validation rules as add command
- Same error message style

---

## Testing Contract

**Integration Tests Required**:

1. **Successful Update**:
   - Input: `update 1 "New title"`
   - Verify: Success message contains old and new titles
   - Verify: Exit code 0
   - Verify: List command shows updated title

2. **Error: Not Found**:
   - Input: `update 99 "New title"`
   - Verify: Error message "Todo with ID 99 not found"
   - Verify: Exit code 1

3. **Error: Empty Title**:
   - Input: `update 1 ""`
   - Verify: Error message "Title cannot be empty or whitespace"
   - Verify: Exit code 1

4. **Error: Invalid ID**:
   - Input: `update abc "New title"`
   - Verify: Argparse error message
   - Verify: Exit code 2

5. **Edge: Completed Todo**:
   - Setup: Complete todo with ID 2
   - Input: `update 2 "New title"`
   - Verify: Title updated, status remains completed

---

## Traceability

**Implements**:
- FR-007: CLI command for updating todos
- FR-008: Confirmation with old and new titles
- FR-010: Exit codes (0 success, non-zero error)

**Supports**:
- SC-001: Update in <5 seconds
- SC-003: Clear error messages
- SC-006: Consistent with existing commands

**Aligns with**:
- Constitution Principle V: Phase 1 Scope Boundaries (CLI-only)
- Constitution Principle VI: Agent Architecture (deterministic output)
