# Quickstart: Update Todo Titles

**Feature**: `002-update-todo`
**Created**: 2025-12-25
**Related**: [spec.md](./spec.md) | [plan.md](./plan.md)

## Overview

This guide provides practical examples of using the `update` command to edit todo titles. The update command allows you to correct typos, clarify tasks, or update descriptions without deleting and re-creating todos.

---

## Basic Usage

### Update a Todo Title

**Command**:
```bash
python -m src.main update <id> "<new-title>"
```

**Example**:
```bash
$ python -m src.main update 1 "Buy groceries"
Updated: 'Buy grocreies' → 'Buy groceries' (ID: 1)
```

---

## Common Scenarios

### Scenario 1: Fix a Typo

**Problem**: You added a todo with a spelling mistake.

**Solution**:
```bash
# Step 1: Add a todo with a typo
$ python -m src.main add "Buy grocreies"
Todo added: Buy grocreies (ID: 1)

# Step 2: Fix the typo
$ python -m src.main update 1 "Buy groceries"
Updated: 'Buy grocreies' → 'Buy groceries' (ID: 1)

# Step 3: Verify the fix
$ python -m src.main list
1. [ ] Buy groceries
```

**Result**: The typo is corrected, and the todo retains its original ID.

---

### Scenario 2: Clarify a Task

**Problem**: Your todo is too vague and needs more detail.

**Solution**:
```bash
# Step 1: Add a vague todo
$ python -m src.main add "Submit report"
Todo added: Submit report (ID: 2)

# Step 2: Add more detail
$ python -m src.main update 2 "Submit quarterly sales report to management"
Updated: 'Submit report' → 'Submit quarterly sales report to management' (ID: 2)

# Step 3: Check the updated list
$ python -m src.main list
1. [ ] Buy groceries
2. [ ] Submit quarterly sales report to management
```

**Result**: The task description is now clear and actionable.

---

### Scenario 3: Update a Completed Todo

**Problem**: You completed a todo but realized the title needs updating.

**Solution**:
```bash
# Step 1: Add and complete a todo
$ python -m src.main add "Review PR"
Todo added: Review PR (ID: 3)

$ python -m src.main complete 3
Completed: Review PR (ID: 3)

# Step 2: Update the completed todo
$ python -m src.main update 3 "Review PR #42 and provide feedback"
Updated: 'Review PR' → 'Review PR #42 and provide feedback' (ID: 3)

# Step 3: Verify the update
$ python -m src.main list
1. [ ] Buy groceries
2. [ ] Submit quarterly sales report to management
3. [x] Review PR #42 and provide feedback    # Still marked as completed
```

**Result**: The title is updated, and the completion status is preserved.

---

### Scenario 4: Update Multiple Todos

**Problem**: You need to update several todos in a workflow.

**Solution**:
```bash
# Initial state
$ python -m src.main list
1. [ ] Task A
2. [ ] Task B
3. [x] Task C

# Update each todo
$ python -m src.main update 1 "Complete project proposal"
Updated: 'Task A' → 'Complete project proposal' (ID: 1)

$ python -m src.main update 2 "Schedule team meeting"
Updated: 'Task B' → 'Schedule team meeting' (ID: 2)

$ python -m src.main update 3 "Finalize budget presentation"
Updated: 'Task C' → 'Finalize budget presentation' (ID: 3)

# Verify all updates
$ python -m src.main list
1. [ ] Complete project proposal
2. [ ] Schedule team meeting
3. [x] Finalize budget presentation
```

**Result**: All todos have clear, descriptive titles.

---

## Error Handling

### Error 1: Todo Not Found

**Problem**: You try to update a todo that doesn't exist.

**Example**:
```bash
$ python -m src.main update 99 "New title"
Error: Todo with ID 99 not found
```

**Solution**: Use `list` to check existing todo IDs:
```bash
$ python -m src.main list
1. [ ] Buy groceries
2. [ ] Submit quarterly sales report to management
3. [x] Review PR #42 and provide feedback

# Update an existing todo
$ python -m src.main update 2 "Submit annual sales report to management"
Updated: 'Submit quarterly sales report to management' → 'Submit annual sales report to management' (ID: 2)
```

---

### Error 2: Empty Title

**Problem**: You accidentally provide an empty title.

**Example**:
```bash
$ python -m src.main update 1 ""
Error: Title cannot be empty or whitespace
```

**Solution**: Provide a valid title:
```bash
$ python -m src.main update 1 "Buy groceries and household supplies"
Updated: 'Buy groceries' → 'Buy groceries and household supplies' (ID: 1)
```

---

### Error 3: Title Too Long

**Problem**: Your new title exceeds the 200-character limit.

**Example**:
```bash
$ python -m src.main update 1 "This is an extremely long title that goes on and on and on and exceeds the maximum allowed length of 200 characters which is enforced by the validation rules in the TodoItem dataclass and will result in a ValidationError being raised when attempting to create the new TodoItem instance during the update operation"
Error: Title cannot exceed 200 characters
```

**Solution**: Shorten the title to 200 characters or less:
```bash
$ python -m src.main update 1 "Buy groceries, household supplies, and toiletries for the month"
Updated: 'Buy groceries and household supplies' → 'Buy groceries, household supplies, and toiletries for the month' (ID: 1)
```

---

### Error 4: Invalid ID Format

**Problem**: You provide a non-numeric ID.

**Example**:
```bash
$ python -m src.main update abc "New title"
usage: todo update [-h] id new_title
todo update: error: argument id: invalid int value: 'abc'
```

**Solution**: Use a numeric ID:
```bash
$ python -m src.main update 1 "New title"
Updated: 'Buy groceries, household supplies, and toiletries for the month' → 'New title' (ID: 1)
```

---

## Advanced Usage

### Titles with Special Characters

**Example**:
```bash
# Special characters are allowed
$ python -m src.main update 1 "Review PR #42 & merge if tests pass ✓"
Updated: 'New title' → 'Review PR #42 & merge if tests pass ✓' (ID: 1)

# Quotes in titles (use escape or alternate quotes)
$ python -m src.main update 2 'Read "Clean Code" by Robert Martin'
Updated: 'Schedule team meeting' → 'Read "Clean Code" by Robert Martin' (ID: 2)
```

---

### Long Titles (Within Limit)

**Example**:
```bash
# Exactly 200 characters (valid)
$ python -m src.main update 3 "$(python -c 'print("A"*200)')"
Updated: 'Finalize budget presentation' → 'AAAAAAAAAA...' (ID: 3)

# 201 characters (invalid)
$ python -m src.main update 3 "$(python -c 'print("A"*201)')"
Error: Title cannot exceed 200 characters
```

---

### Idempotent Updates

**Example**:
```bash
# Update to the same title (no error, operation succeeds)
$ python -m src.main update 1 "Buy groceries"
Updated: 'Buy groceries' → 'Buy groceries' (ID: 1)
```

**Result**: Operation succeeds even though the title didn't change.

---

### Duplicate Titles

**Example**:
```bash
# Multiple todos can have the same title
$ python -m src.main list
1. [ ] Buy groceries
2. [ ] Submit report
3. [x] Review PR

$ python -m src.main update 2 "Buy groceries"
Updated: 'Submit report' → 'Buy groceries' (ID: 2)

$ python -m src.main list
1. [ ] Buy groceries
2. [ ] Buy groceries    # Duplicate title (allowed)
3. [x] Review PR
```

**Result**: Todos can have duplicate titles (no uniqueness constraint).

---

## Integration Workflows

### Workflow 1: Add → Update → Complete → Update

```bash
# Step 1: Add a todo
$ python -m src.main add "Draft email"
Todo added: Draft email (ID: 1)

# Step 2: Clarify the task
$ python -m src.main update 1 "Draft quarterly update email to stakeholders"
Updated: 'Draft email' → 'Draft quarterly update email to stakeholders' (ID: 1)

# Step 3: Complete the task
$ python -m src.main complete 1
Completed: Draft quarterly update email to stakeholders (ID: 1)

# Step 4: Update the completed task
$ python -m src.main update 1 "Draft and send quarterly update email to stakeholders"
Updated: 'Draft quarterly update email to stakeholders' → 'Draft and send quarterly update email to stakeholders' (ID: 1)

# Final state
$ python -m src.main list
1. [x] Draft and send quarterly update email to stakeholders
```

---

### Workflow 2: Batch Update and Reorganize

```bash
# Initial state: generic todos
$ python -m src.main add "Task 1"
Todo added: Task 1 (ID: 1)

$ python -m src.main add "Task 2"
Todo added: Task 2 (ID: 2)

$ python -m src.main add "Task 3"
Todo added: Task 3 (ID: 3)

# Update all todos with specific descriptions
$ python -m src.main update 1 "Morning: Review emails and prioritize tasks"
Updated: 'Task 1' → 'Morning: Review emails and prioritize tasks' (ID: 1)

$ python -m src.main update 2 "Afternoon: Attend project planning meeting"
Updated: 'Task 2' → 'Afternoon: Attend project planning meeting' (ID: 2)

$ python -m src.main update 3 "Evening: Complete code review for PR #123"
Updated: 'Task 3' → 'Evening: Complete code review for PR #123' (ID: 3)

# Final organized list
$ python -m src.main list
1. [ ] Morning: Review emails and prioritize tasks
2. [ ] Afternoon: Attend project planning meeting
3. [ ] Evening: Complete code review for PR #123
```

---

## Tips and Best Practices

### Tip 1: Use Quotes for Titles with Spaces

**Do**:
```bash
python -m src.main update 1 "Buy groceries"
```

**Don't**:
```bash
python -m src.main update 1 Buy groceries    # Error: too many arguments
```

---

### Tip 2: Check IDs Before Updating

**Best Practice**:
```bash
# Step 1: List todos to find the ID
$ python -m src.main list
1. [ ] Buy groceries
2. [ ] Submit report

# Step 2: Update the correct todo
$ python -m src.main update 2 "Submit final report"
Updated: 'Submit report' → 'Submit final report' (ID: 2)
```

---

### Tip 3: Update Completed Todos Safely

**Note**: Updating a completed todo preserves its completion status.

**Example**:
```bash
# Completed todo retains its status after update
$ python -m src.main list
3. [x] Review PR

$ python -m src.main update 3 "Review PR #42 and merge"
Updated: 'Review PR' → 'Review PR #42 and merge' (ID: 3)

$ python -m src.main list
3. [x] Review PR #42 and merge    # Still completed
```

---

### Tip 4: Keep Titles Concise

**Recommendation**: Aim for titles under 80 characters for readability.

**Good**:
```bash
python -m src.main update 1 "Buy groceries for the week"
```

**Acceptable but verbose**:
```bash
python -m src.main update 1 "Buy groceries including milk, bread, eggs, cheese, vegetables, fruits, and household cleaning supplies for the entire week"
```

---

## Command Reference

### Full Command

```bash
python -m src.main update <id> "<new-title>"
```

**Arguments**:
- `<id>`: Integer ID of the todo to update
- `<new-title>`: New title (1-200 characters, not empty)

**Exit Codes**:
- `0`: Success
- `1`: Application error (not found, validation error)
- `2`: Usage error (invalid arguments)

---

### Help

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

---

## Requirements and Constraints

**Title Requirements**:
- Length: 1-200 characters
- Cannot be empty
- Cannot be whitespace-only
- Special characters allowed
- Duplicate titles allowed

**ID Requirements**:
- Must be a valid integer
- Must correspond to an existing todo

**Behavior Guarantees**:
- Original ID is preserved
- Completion status is preserved
- Update operation is atomic (all-or-nothing)
- Same validation rules as `add` command

---

## Troubleshooting

### Problem: "Todo with ID X not found"

**Cause**: The ID doesn't exist in the current session.

**Solution**:
1. Run `python -m src.main list` to see available IDs
2. Use a valid ID from the list

---

### Problem: "Title cannot be empty or whitespace"

**Cause**: You provided an empty string or whitespace-only string.

**Solution**:
1. Provide a non-empty title with at least one non-whitespace character

---

### Problem: "Title cannot exceed 200 characters"

**Cause**: Your new title is too long.

**Solution**:
1. Shorten the title to 200 characters or less
2. Use abbreviations or more concise wording

---

### Problem: "argument id: invalid int value"

**Cause**: You provided a non-integer ID.

**Solution**:
1. Use a numeric ID (e.g., `1`, `2`, `42`)
2. Do not use letters or special characters in the ID

---

## Summary

**Key Takeaways**:
- Use `update <id> "<new-title>"` to change todo titles
- IDs and completion status are preserved
- Same validation rules as creating new todos
- Works on both completed and incomplete todos
- Clear error messages guide you when something goes wrong

**Next Steps**:
- Try updating a todo with `python -m src.main update 1 "Your new title"`
- Explore other commands: `add`, `list`, `complete`, `delete`
- Use `--help` for detailed command information

---

**Related Documentation**:
- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [CLI Interface Contract](./contracts/cli-interface.md)
- [Data Model](./data-model.md)
