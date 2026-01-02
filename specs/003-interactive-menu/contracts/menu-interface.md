# Menu Interface Contract

**Feature**: `003-interactive-menu`
**Created**: 2025-12-28
**Related**: [spec.md](../spec.md) | [plan.md](../plan.md)

## Overview

This contract specifies the exact behavior, display format, and interaction patterns for the interactive menu interface. All implementations must conform to these specifications.

---

## Menu Display Format

### Welcome Message

**When Displayed**: On application startup (before first menu display)

**Format**:
```text
=== Todo App - Interactive Menu ===

Welcome! Manage your todos with ease.
```

**Requirements**:
- Display once per session (not repeated on menu loop)
- Blank line after welcome message before menu

---

### Main Menu

**When Displayed**:
- After welcome message (first time)
- After each operation completes (loop)
- After invalid input (re-display)

**Format**:
```text
1. Add todo
2. List all todos
3. Complete todo
4. Update todo
5. Delete todo
6. Exit

Enter your choice (1-6): _
```

**Requirements**:
- Numbered list (1-6) with clear action descriptions
- Blank line before menu
- Prompt on same line as cursor (no newline after colon)
- Cursor position indicated by `_` (user types here)

**Validation**:
- Accept only numeric input (1-6)
- Invalid input: Display error + re-display menu
- Empty input: Display error + re-display menu

---

## Input Prompts

### General Prompt Pattern

**Format**:
```text
{Prompt message}: _
```

**Requirements**:
- Clear, specific prompt message
- Colon followed by space
- Cursor on same line as prompt
- No newline after prompt text

---

### Add Todo Prompt

**When Displayed**: User selects menu option 1

**Format**:
```text
Enter todo title: _
```

**Validation**:
- Title length: 1-200 characters
- Cannot be empty string
- Cannot be whitespace-only
- Strip leading/trailing whitespace before validation

**Error Handling**:
```text
Error: Title cannot be empty or whitespace.
Enter todo title: _
```

**Success Response**:
```text
Todo added: Buy groceries (ID: 1)
```

---

### List Todos Display

**When Displayed**: User selects menu option 2

**Format (with todos)**:
```text
Your todos:

1. [ ] Buy groceries
2. [x] Read Python book
3. [ ] Call mom

Total: 3 todos (1 completed)
```

**Format (no todos)**:
```text
No todos found. Start by adding one!
```

**Requirements**:
- Header line: "Your todos:"
- Blank line after header
- Each todo: `{ID}. [{status}] {title}`
- Status: `[ ]` for incomplete, `[x]` for completed
- Sorted by ID (ascending)
- Footer line: Total count + completed count
- Blank line before returning to menu

---

### Complete Todo Prompt

**When Displayed**: User selects menu option 3

**Format**:
```text
Enter the ID of the todo to complete: _
```

**Validation**:
- Must be numeric
- Must be existing todo ID
- Accept already-completed todos (idempotent)

**Error Handling**:
```text
Error: Todo with ID 99 not found.
Enter the ID of the todo to complete: _
```

**Success Response**:
```text
Completed: Buy groceries (ID: 1)
```

---

### Update Todo Prompts

**When Displayed**: User selects menu option 4

**Format (ID prompt)**:
```text
Enter the ID of the todo to update: _
```

**Format (title prompt)**:
```text
Enter the new title: _
```

**Validation**:
- ID: Must be numeric, must exist
- Title: Same rules as Add todo (1-200 chars, not empty)

**Error Handling (invalid ID)**:
```text
Error: Todo with ID 99 not found.
Enter the ID of the todo to update: _
```

**Error Handling (invalid title)**:
```text
Error: Title cannot be empty or whitespace.
Enter the new title: _
```

**Success Response**:
```text
Updated: 'Buy milk' → 'Buy groceries' (ID: 1)
```

---

### Delete Todo Prompt

**When Displayed**: User selects menu option 5

**Format**:
```text
Enter the ID of the todo to delete: _
```

**Validation**:
- Must be numeric
- Must be existing todo ID

**Error Handling**:
```text
Error: Todo with ID 99 not found.
Enter the ID of the todo to delete: _
```

**Success Response**:
```text
Deleted: Buy groceries (ID: 1)
```

---

## Exit Behavior

### Normal Exit (Menu Option 6)

**When Triggered**: User selects menu option 6

**Format**:
```text
Goodbye! Your todos will be cleared (in-memory only).
```

**Behavior**:
- Display goodbye message
- Exit program with code 0
- No error/exception raised

---

### Ctrl+C Exit

**When Triggered**: User presses Ctrl+C at any time

**Format**:
```text

Goodbye! Your todos will be cleared (in-memory only).
```

**Behavior**:
- Catch KeyboardInterrupt exception
- Display goodbye message (with blank line before)
- Exit program with code 0
- No traceback displayed

---

## Error Message Format

### General Error Pattern

**Format**:
```text
Error: {specific error description}.
```

**Requirements**:
- Prefix: "Error: " (capital E, colon, space)
- Error description: Specific, actionable
- Period at end
- Blank line after error before re-prompting

---

### Common Error Messages

**Invalid Menu Choice**:
```text
Error: Invalid choice. Please enter a number between 1 and 6.
```

**Non-Numeric Input (Menu)**:
```text
Error: Please enter a number between 1 and 6.
```

**Non-Numeric ID**:
```text
Error: Please enter a valid numeric ID.
```

**Todo Not Found**:
```text
Error: Todo with ID {id} not found.
```

**Empty Title**:
```text
Error: Title cannot be empty or whitespace.
```

**Title Too Long**:
```text
Error: Title cannot exceed 200 characters.
```

---

## Control Flow

### Menu Loop Pattern

```text
1. Display menu
2. Get user choice (numeric 1-6)
3. Validate choice
   - Valid → Execute action
   - Invalid → Display error, go to step 1
4. Execute action
5. Display result/confirmation
6. If choice != 6, go to step 1
7. If choice == 6, display goodbye and exit
```

---

### Input Validation Pattern

```text
1. Display prompt
2. Get user input (string)
3. Validate input
   - Valid → Process and return result
   - Invalid → Display error, go to step 1
4. Return result to caller
```

---

## Testing Requirements

### Unit Tests (Menu Functions)

**display_menu()**:
- Verify exact menu text output
- Verify numbered list format (1-6)
- Verify prompt format

**get_menu_choice()**:
- Test valid inputs (1, 2, 3, 4, 5, 6)
- Test invalid numeric (0, 7, -1, 100)
- Test non-numeric ("abc", "", "1.5")
- Test whitespace handling (" 1 ", "\n")

**prompt_for_input()**:
- Test returns user input correctly
- Test whitespace stripping
- Test empty input handling

**prompt_for_id()**:
- Test valid numeric IDs
- Test non-numeric inputs
- Test empty input
- Test negative numbers

---

### Integration Tests (Full Workflows)

**Add Workflow**:
- Menu → Select 1 → Enter title → See confirmation → Return to menu

**List Workflow**:
- Menu → Select 2 → See todos or "No todos found" → Return to menu

**Complete Workflow**:
- Menu → Select 3 → Enter ID → See confirmation → Return to menu
- Test invalid ID path

**Update Workflow**:
- Menu → Select 4 → Enter ID → Enter title → See confirmation → Return to menu
- Test invalid ID path
- Test invalid title path

**Delete Workflow**:
- Menu → Select 5 → Enter ID → See confirmation → Return to menu
- Test invalid ID path

**Exit Workflow**:
- Menu → Select 6 → See goodbye message → Program exits

**Ctrl+C Workflow**:
- Press Ctrl+C → See goodbye message → Program exits

---

## Edge Cases

### Special Input Scenarios

**EOF (Ctrl+D / Ctrl+Z)**:
- Behavior: Catch EOFError, display goodbye, exit gracefully
- No traceback or crash

**Very Long Input (>10000 chars)**:
- Menu choice: Reject as invalid
- Title: Reject as >200 characters (validation catches)

**Special Characters in Title**:
- Allow: All printable characters (spaces, punctuation, Unicode)
- Example: "Buy @#$% groceries! (urgent)" is valid

**Repeated Invalid Input**:
- No limit: Keep re-prompting indefinitely
- No "maximum attempts exceeded" error

---

## Compatibility

### Terminal Compatibility

**Supported Terminals**:
- Windows: cmd.exe, PowerShell
- macOS: Terminal.app, iTerm2
- Linux: bash, zsh, any POSIX-compliant terminal

**Requirements**:
- Basic stdin/stdout support
- No ANSI color codes required
- No cursor positioning required
- ASCII-only menu text (titles can have Unicode)

---

### Backward Compatibility

**Existing CLI Preserved**:
```bash
# Existing CLI (unchanged)
python -m src.main add "Buy groceries"
python -m src.main list

# New Interactive Mode
uv run main.py
```

**Requirements**:
- Both modes must coexist
- No conflicts or breaking changes
- Same validation rules in both modes

---

## Performance Requirements

**Menu Display**: <100ms from last input to menu display
**Input Echo**: Immediate (standard terminal behavior)
**Operation Response**: <5 seconds from input to confirmation

---

## Security Considerations

**Input Sanitization**:
- Strip leading/trailing whitespace
- No SQL injection risk (no database)
- No command injection risk (no shell commands executed)

**Data Validation**:
- All inputs validated before processing
- Invalid inputs rejected, not processed

**Error Disclosure**:
- Error messages safe to display (no sensitive data)
- No stack traces in production mode

---

## Summary

This contract ensures:
- ✅ Consistent user experience across all operations
- ✅ Clear, beginner-friendly prompts and messages
- ✅ Robust error handling with helpful feedback
- ✅ Predictable control flow (menu loop pattern)
- ✅ Backward compatibility with existing CLI

**Implementation Compliance**:
All interactive menu code must conform to these specifications. Tests will validate exact message formats, prompt patterns, and control flow behavior.
