# Quickstart: Interactive Menu-Based Todo Console

**Feature**: `003-interactive-menu`
**Created**: 2025-12-28
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md)

## Overview

This guide provides practical examples of using the interactive menu to manage todos. The interactive mode launches via `uv run main.py` and guides you through operations with numbered menus and prompts - no command memorization required!

---

## Prerequisites

### Install uv (if not already installed)

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify installation**:
```bash
uv --version
```

---

## Quick Start

### Launch the Interactive Menu

```bash
$ uv run main.py
```

**Expected Output**:
```text
=== Todo App - Interactive Menu ===

Welcome! Manage your todos with ease.

1. Add todo
2. List all todos
3. Complete todo
4. Update todo
5. Delete todo
6. Exit

Enter your choice (1-6): _
```

**What You See**:
- Welcome message (displayed once)
- Numbered menu with 6 options
- Prompt waiting for your choice

---

## Basic Workflows

### Workflow 1: Add Your First Todo

**Step 1: Select "Add todo"**
```text
Enter your choice (1-6): 1
```

**Step 2: Enter the todo title**
```text
Enter todo title: Buy groceries
```

**Step 3: See confirmation**
```text
Todo added: Buy groceries (ID: 1)

1. Add todo
2. List all todos
3. Complete todo
4. Update todo
5. Delete todo
6. Exit

Enter your choice (1-6): _
```

**Result**: Todo created, menu redisplays automatically

---

### Workflow 2: View Your Todos

**Step 1: Select "List all todos"**
```text
Enter your choice (1-6): 2
```

**Step 2: See your todos**
```text
Your todos:

1. [ ] Buy groceries

Total: 1 todos (0 completed)

1. Add todo
2. List all todos
...
Enter your choice (1-6): _
```

**Result**: All todos displayed, menu redisplays

---

### Workflow 3: Complete a Todo

**Step 1: Select "Complete todo"**
```text
Enter your choice (1-6): 3
```

**Step 2: Enter the todo ID**
```text
Enter the ID of the todo to complete: 1
```

**Step 3: See confirmation**
```text
Completed: Buy groceries (ID: 1)

1. Add todo
...
Enter your choice (1-6): _
```

**Step 4: Verify in list**
```text
Enter your choice (1-6): 2

Your todos:

1. [x] Buy groceries

Total: 1 todos (1 completed)
```

**Result**: Todo marked complete with `[x]`

---

### Workflow 4: Update a Todo

**Step 1: Select "Update todo"**
```text
Enter your choice (1-6): 4
```

**Step 2: Enter the todo ID**
```text
Enter the ID of the todo to update: 1
```

**Step 3: Enter new title**
```text
Enter the new title: Buy groceries and milk
```

**Step 4: See confirmation**
```text
Updated: 'Buy groceries' → 'Buy groceries and milk' (ID: 1)
```

**Result**: Todo title updated, ID and status preserved

---

### Workflow 5: Delete a Todo

**Step 1: Select "Delete todo"**
```text
Enter your choice (1-6): 5
```

**Step 2: Enter the todo ID**
```text
Enter the ID of the todo to delete: 1
```

**Step 3: See confirmation**
```text
Deleted: Buy groceries and milk (ID: 1)
```

**Result**: Todo removed from list

---

### Workflow 6: Exit the Application

**Step 1: Select "Exit"**
```text
Enter your choice (1-6): 6
```

**Step 2: See goodbye message**
```text
Goodbye! Your todos will be cleared (in-memory only).
```

**Result**: Application exits, all todos lost (in-memory only)

---

## Common Scenarios

### Scenario 1: Managing Daily Tasks

```text
$ uv run main.py

Enter your choice (1-6): 1
Enter todo title: Check emails
Todo added: Check emails (ID: 1)

Enter your choice (1-6): 1
Enter todo title: Review project proposal
Todo added: Review project proposal (ID: 2)

Enter your choice (1-6): 1
Enter todo title: Call team meeting at 2pm
Todo added: Call team meeting at 2pm (ID: 3)

Enter your choice (1-6): 2
Your todos:

1. [ ] Check emails
2. [ ] Review project proposal
3. [ ] Call team meeting at 2pm

Total: 3 todos (0 completed)

Enter your choice (1-6): 3
Enter the ID of the todo to complete: 1
Completed: Check emails (ID: 1)

Enter your choice (1-6): 2
Your todos:

1. [x] Check emails
2. [ ] Review project proposal
3. [ ] Call team meeting at 2pm

Total: 3 todos (1 completed)

Enter your choice (1-6): 6
Goodbye! Your todos will be cleared (in-memory only).
```

---

### Scenario 2: Fixing Typos

```text
Enter your choice (1-6): 1
Enter todo title: Buy grocreies
Todo added: Buy grocreies (ID: 1)

Enter your choice (1-6): 2
Your todos:

1. [ ] Buy grocreies   # Typo spotted!

Enter your choice (1-6): 4
Enter the ID of the todo to update: 1
Enter the new title: Buy groceries
Updated: 'Buy grocreies' → 'Buy groceries' (ID: 1)

Enter your choice (1-6): 2
Your todos:

1. [ ] Buy groceries   # Fixed!
```

---

### Scenario 3: Starting with Empty List

```text
$ uv run main.py

Enter your choice (1-6): 2
No todos found. Start by adding one!

Enter your choice (1-6): 1
Enter todo title: My first todo
Todo added: My first todo (ID: 1)

Enter your choice (1-6): 2
Your todos:

1. [ ] My first todo

Total: 1 todos (0 completed)
```

---

## Error Handling

### Error 1: Invalid Menu Choice

**Input**:
```text
Enter your choice (1-6): 9
```

**Response**:
```text
Error: Invalid choice. Please enter a number between 1 and 6.

1. Add todo
2. List all todos
...
Enter your choice (1-6): _
```

**Solution**: Enter a number from 1 to 6

---

### Error 2: Non-Numeric Menu Choice

**Input**:
```text
Enter your choice (1-6): abc
```

**Response**:
```text
Error: Please enter a number between 1 and 6.

1. Add todo
...
Enter your choice (1-6): _
```

**Solution**: Enter a number, not text

---

### Error 3: Empty Todo Title

**Input**:
```text
Enter your choice (1-6): 1
Enter todo title:
```
(Press Enter without typing)

**Response**:
```text
Error: Title cannot be empty or whitespace.
Enter todo title: _
```

**Solution**: Type a title before pressing Enter

---

### Error 4: Todo Not Found

**Input**:
```text
Enter your choice (1-6): 3
Enter the ID of the todo to complete: 999
```

**Response**:
```text
Error: Todo with ID 999 not found.
Enter the ID of the todo to complete: _
```

**Solution**: Use `List all todos` to see valid IDs, then enter a valid ID

---

### Error 5: Non-Numeric ID

**Input**:
```text
Enter your choice (1-6): 3
Enter the ID of the todo to complete: abc
```

**Response**:
```text
Error: Please enter a valid numeric ID.
Enter the ID of the todo to complete: _
```

**Solution**: Enter a number (the todo ID)

---

## Advanced Usage

### Using Ctrl+C to Exit

**At any time, press Ctrl+C**:
```text
Enter your choice (1-6): ^C

Goodbye! Your todos will be cleared (in-memory only).
```

**Result**: Graceful exit, same as selecting option 6

---

### Long Todo Titles

**Example**:
```text
Enter todo title: Review quarterly sales report and prepare presentation for stakeholder meeting on Friday
Todo added: Review quarterly sales report and prepare presentation for stakeholder meeting on Friday (ID: 1)
```

**Limit**: Up to 200 characters allowed

---

### Special Characters in Titles

**Example**:
```text
Enter todo title: Review PR #42 & merge if tests pass ✓
Todo added: Review PR #42 & merge if tests pass ✓ (ID: 1)
```

**Result**: All printable characters allowed

---

### Completing Already-Completed Todos

**Example**:
```text
Enter your choice (1-6): 3
Enter the ID of the todo to complete: 1
Completed: Buy groceries (ID: 1)

Enter your choice (1-6): 3
Enter the ID of the todo to complete: 1
Completed: Buy groceries (ID: 1)   # Idempotent - no error
```

**Result**: Operation succeeds, todo remains completed

---

### Updating Completed Todos

**Example**:
```text
# Todo 1 is completed
Enter your choice (1-6): 4
Enter the ID of the todo to update: 1
Enter the new title: Buy groceries (updated)
Updated: 'Buy groceries' → 'Buy groceries (updated)' (ID: 1)

Enter your choice (1-6): 2
Your todos:

1. [x] Buy groceries (updated)   # Status preserved
```

**Result**: Title updated, completion status preserved

---

## Tips and Best Practices

### Tip 1: Check Your List Before Operations

**Best Practice**:
```text
1. Select "List all todos" (option 2)
2. Note the ID of the todo you want to modify
3. Select the operation (complete/update/delete)
4. Enter the ID you noted
```

**Why**: Ensures you're operating on the correct todo

---

### Tip 2: Use Update Instead of Delete+Add

**Don't**:
```text
5. Delete todo (old title)
1. Add todo (new title)   # Gets new ID
```

**Do**:
```text
4. Update todo (keeps same ID)
```

**Why**: Preserves todo ID, cleaner workflow

---

### Tip 3: Review Confirmations

**After each operation**:
- Read the confirmation message carefully
- Verify the operation succeeded as expected
- Check the list if unsure

**Example**:
```text
Completed: Buy groceries (ID: 1)   # Confirmation shows what changed
```

---

### Tip 4: Exit Gracefully

**Option 1**: Select menu option 6
**Option 2**: Press Ctrl+C

**Don't**: Force-close terminal or kill process

**Why**: Ensures proper cleanup and goodbye message

---

## Troubleshooting

### Problem: "command not found: uv"

**Cause**: uv not installed or not in PATH

**Solution**:
1. Install uv (see Prerequisites)
2. Restart terminal
3. Verify: `uv --version`

---

### Problem: "No such file or directory: main.py"

**Cause**: Running command from wrong directory

**Solution**:
```bash
cd /path/to/todo-app
uv run main.py
```

---

### Problem: Application Won't Start

**Cause**: Missing dependencies or Python version

**Solution**:
1. Verify Python 3.11+: `python --version`
2. Run: `uv sync` to install dependencies
3. Try again: `uv run main.py`

---

### Problem: Todos Disappear After Restart

**Expected Behavior**: This is normal - in-memory storage only

**Explanation**: All todos are lost when the application exits (by design for Phase 1)

**Workaround**: None - file persistence coming in future phases

---

## Comparison: CLI vs Interactive Mode

### CLI Mode (Existing)

```bash
# Each command requires full syntax
$ python -m src.main add "Buy groceries"
Todo added: Buy groceries (ID: 1)

$ python -m src.main list
1. [ ] Buy groceries

$ python -m src.main complete 1
Completed: Buy groceries (ID: 1)
```

**Pros**: Fast for power users, scriptable
**Cons**: Requires memorizing commands

---

### Interactive Mode (New)

```text
$ uv run main.py

Enter your choice (1-6): 1    # Menu shows options
Enter todo title: Buy groceries
Todo added: Buy groceries (ID: 1)

Enter your choice (1-6): 2    # List
Your todos:
1. [ ] Buy groceries

Enter your choice (1-6): 3    # Complete
Enter the ID of the todo to complete: 1
Completed: Buy groceries (ID: 1)
```

**Pros**: Beginner-friendly, guided prompts
**Cons**: Requires more keypresses

**Recommendation**: Use interactive mode for learning, CLI mode for scripting

---

## Summary

**Key Takeaways**:
- Launch with `uv run main.py`
- Numbered menu shows all available operations
- Prompts guide you through each step
- Automatic return to menu after operations
- Exit with option 6 or Ctrl+C
- All data lost on exit (in-memory only)

**Next Steps**:
- Try the basic workflows above
- Experiment with error scenarios
- Compare with CLI mode (`python -m src.main`)
- Provide feedback on user experience

---

**Related Documentation**:
- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Menu Interface Contract](./contracts/menu-interface.md)
- [Data Model](./data-model.md)
