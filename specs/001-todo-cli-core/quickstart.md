# Quickstart Guide: Todo CLI

**Version**: 1.0
**Date**: 2025-12-24
**Target Users**: Command-line users comfortable with basic terminal operations

## Overview

Todo CLI is a simple command-line application for managing your daily tasks. Add todos, mark them complete, and delete them when done - all from your terminal.

**Key Features**:
- ✅ Add todos with descriptive titles
- ✅ View all your todos at a glance
- ✅ Mark todos as complete when finished
- ✅ Delete todos you no longer need
- ✅ Simple, intuitive commands

**Phase 1 Limitations**:
- 📝 Data is stored in-memory only (lost when program exits)
- 📝 No editing of todo titles (delete and re-add instead)
- 📝 No filtering, searching, or sorting
- 📝 No due dates or priorities

---

## Installation

### Prerequisites

- Python 3.11 or higher
- Terminal/Command Prompt access

### Install

```bash
# Clone the repository
git clone https://github.com/your-org/todo-app.git
cd todo-app

# Install dependencies
pip install -r requirements.txt

# Run the todo CLI
python src/main.py --help
```

**Optional**: Create an alias for convenience:

```bash
# Linux/macOS (~/.bashrc or ~/.zshrc)
alias todo="python /path/to/todo-app/src/main.py"

# Windows (PowerShell profile)
function todo { python C:\path\to\todo-app\src\main.py $args }
```

After setting up the alias, you can use `todo` instead of `python src/main.py`.

---

## Quick Start (5-Minute Tutorial)

### Step 1: Add Your First Todo

```bash
$ todo add "Buy groceries"
Todo added: Buy groceries (ID: 1)
```

**What happened?**
- Todo CLI created a new task with the title "Buy groceries"
- It assigned a unique ID (1) to your todo
- You can now track this task

### Step 2: Add More Todos

```bash
$ todo add "Read Python book"
Todo added: Read Python book (ID: 2)

$ todo add "Call mom"
Todo added: Call mom (ID: 3)
```

**Tip**: Use quotes around titles with spaces. Without quotes, only the first word is captured.

### Step 3: View All Your Todos

```bash
$ todo list
1. [ ] Buy groceries
2. [ ] Read Python book
3. [ ] Call mom
```

**What you see**:
- `1.`, `2.`, `3.` = Todo IDs
- `[ ]` = Pending (not completed yet)
- Todos are listed in the order they were created

### Step 4: Complete a Todo

```bash
$ todo complete 1
Todo #1 marked as complete
```

### Step 5: Check Your Progress

```bash
$ todo list
1. [x] Buy groceries
2. [ ] Read Python book
3. [ ] Call mom
```

**Notice**: Todo #1 now shows `[x]` (completed) instead of `[ ]` (pending).

### Step 6: Delete a Todo

```bash
$ todo delete 2
Todo #2 deleted
```

### Step 7: Final List

```bash
$ todo list
1. [x] Buy groceries
3. [ ] Call mom
```

**Notice**: Todo #2 is gone. The IDs of remaining todos don't change.

---

## Command Reference

### Add a Todo

```bash
todo add "<title>"
```

**Examples**:
```bash
todo add "Exercise for 30 minutes"
todo add "Prepare presentation slides"
```

**Requirements**:
- Title must be 1-200 characters
- Title cannot be empty

**Common Errors**:
```bash
$ todo add ""
Error: Title cannot be empty
```

---

### List All Todos

```bash
todo list
```

**Output**:
- Shows all todos with IDs, status, and titles
- `[ ]` = pending, `[x]` = completed
- If no todos exist: "No todos found"

**Examples**:
```bash
$ todo list
1. [ ] Buy groceries
2. [x] Read book
3. [ ] Call mom

$ todo list  # empty list
No todos found
```

---

### Complete a Todo

```bash
todo complete <id>
```

**Examples**:
```bash
todo complete 1
todo complete 5
```

**Requirements**:
- ID must be a number
- ID must exist in your todo list

**Common Errors**:
```bash
$ todo complete 999
Error: Todo #999 not found

$ todo complete abc
Error: Invalid ID 'abc' - ID must be a number
```

**Note**: You can complete an already-completed todo (no error, just confirmation).

---

### Delete a Todo

```bash
todo delete <id>
```

**Examples**:
```bash
todo delete 1
todo delete 5
```

**Requirements**:
- ID must be a number
- ID must exist in your todo list

**Common Errors**:
```bash
$ todo delete 999
Error: Todo #999 not found

$ todo delete abc
Error: Invalid ID 'abc' - ID must be a number
```

**Warning**: Deletion is permanent! Deleted todos cannot be recovered.

---

### Get Help

```bash
todo --help
todo -h
```

**Output**: Shows usage information for all commands.

---

## Common Workflows

### Daily Task Management

```bash
# Morning: Add your tasks for the day
todo add "Review emails"
todo add "Team meeting at 10am"
todo add "Finish project report"

# Throughout the day: Check what's left
todo list

# As you finish tasks: Mark them complete
todo complete 1
todo complete 2

# Evening: Review your progress
todo list
1. [x] Review emails
2. [x] Team meeting at 10am
3. [ ] Finish project report
```

### Weekly Planning

```bash
# Monday: Add week's goals
todo add "Prepare Monday presentation"
todo add "Code review on Tuesday"
todo add "Client call on Wednesday"

# Complete as you go
todo complete 1  # After Monday presentation
todo complete 2  # After Tuesday code review

# Delete if plans change
todo delete 3  # Client call rescheduled
```

### Quick Capture

```bash
# Capture ideas quickly
todo add "Research Python decorators"
todo add "Buy birthday gift for Sarah"
todo add "Schedule dentist appointment"

# Review later
todo list

# Complete or delete as needed
todo complete 1
todo delete 2
```

---

## Tips & Best Practices

### ✅ DO

1. **Use descriptive titles**: "Buy milk" is better than "milk"
2. **Keep titles concise**: Aim for under 50 characters for readability
3. **Complete todos**: Feels good and helps track progress
4. **Review regularly**: Run `todo list` often to stay on track
5. **Delete finished tasks**: Keep your list clean and relevant

### ❌ DON'T

1. **Don't rely on persistence**: Remember, data is lost when you exit (Phase 1)
2. **Don't use very long titles**: Limit is 200 chars, but shorter is better
3. **Don't forget to quote titles**: `todo add Buy milk` only captures "Buy"
4. **Don't assume ID order**: After deletions, IDs may have gaps (1, 3, 5...)

---

## Troubleshooting

### Problem: "Command not found: todo"

**Solution**: Either:
1. Use full path: `python src/main.py add "Task"`
2. Set up alias (see Installation section)
3. Add to PATH

### Problem: Title only captures first word

**Example**:
```bash
$ todo add Buy groceries  # Wrong!
Todo added: Buy (ID: 1)
```

**Solution**: Use quotes:
```bash
$ todo add "Buy groceries"  # Correct!
Todo added: Buy groceries (ID: 1)
```

### Problem: Deleted todos leave gaps in IDs

**Example**:
```bash
$ todo list
1. [ ] Task A
2. [ ] Task B
3. [ ] Task C

$ todo delete 2
$ todo list
1. [ ] Task A
3. [ ] Task C  # ID 2 is missing
```

**This is expected behavior**: Deleted IDs are never reused. This is intentional to maintain data integrity.

### Problem: Can't edit a todo title

**Solution**: Delete and re-add:
```bash
$ todo delete 1
$ todo add "Corrected title"
```

**Note**: Editing is not available in Phase 1.

### Problem: Data lost after closing terminal

**This is expected**: Phase 1 stores data in memory only. Data is lost when the program exits. Future phases will add persistence.

---

## Keyboard Shortcuts

No keyboard shortcuts are built into the CLI itself, but you can use shell features:

**Bash/Zsh**:
- `Ctrl + R`: Search command history (find previous `todo` commands)
- `Up Arrow`: Cycle through previous commands
- `Tab`: Auto-complete file paths (not todo commands)

**Windows CMD/PowerShell**:
- `F7`: Show command history
- `Up Arrow`: Cycle through previous commands

---

## What's Next?

After mastering the basics:

1. **Experiment**: Try edge cases, learn the limits
2. **Build habits**: Use todo CLI for a week, see how it fits your workflow
3. **Provide feedback**: Report bugs or suggest features
4. **Stay tuned**: Phase 2 will add persistence, editing, and more!

---

## Getting Help

- **Command Help**: `todo --help`
- **Bug Reports**: [GitHub Issues](https://github.com/your-org/todo-app/issues)
- **Documentation**: See `specs/001-todo-cli-core/` for technical details

---

## Phase 1 Reminder

This is Phase 1 of the Todo CLI project. Current limitations:

- 📝 **No persistence**: Data lost on exit
- 📝 **No editing**: Can't change todo titles
- 📝 **No filtering**: Can't filter by status, search, or sort
- 📝 **No priorities**: All todos are equal
- 📝 **No due dates**: Can't set deadlines

Future phases will add these features. For now, enjoy a simple, fast, distraction-free todo experience!

---

**Happy task tracking!** 🎯
