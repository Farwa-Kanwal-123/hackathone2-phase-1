# Implementation Plan: Todo CLI Core

**Branch**: `001-todo-cli-core` | **Date**: 2025-12-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-core/spec.md`

## Summary

Build a command-line todo application that supports CRUD operations (add, list, complete, delete) with in-memory storage. The application will use Python 3.11+ with argparse for CLI parsing, store todos in a dictionary data structure, and provide user-friendly error messages for all operations. Phase 1 focuses exclusively on core CLI functionality without persistence, web interfaces, or databases.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: argparse (stdlib), pytest (testing), pytest-cov (coverage)
**Storage**: In-memory dictionary (Phase 1 constraint - no persistence)
**Testing**: pytest with coverage reporting
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project (CLI application)
**Performance Goals**: <5s for add operations, <2s for list operations, instant feedback
**Constraints**: In-memory only (no file I/O), CLI only (no GUI/web), Python stdlib preferred
**Scale/Scope**: Single user, process lifetime, <1000 todos expected

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase 1 Scope Boundaries

**✅ ALLOWED (Compliant)**:
- ✅ CLI-based interaction (using argparse from Python stdlib)
- ✅ In-memory data structures (dict for storage, int for IDs)
- ✅ Python standard library (argparse, sys)
- ✅ CRUD operations (add, list, complete, delete)
- ✅ Testing frameworks (pytest, pytest-cov)
- ✅ Code quality tools (pylint, flake8, black - optional)

**❌ PROHIBITED (None Used)**:
- ❌ Databases - NOT USED
- ❌ File persistence - NOT USED
- ❌ Web frameworks - NOT USED
- ❌ GUI libraries - NOT USED
- ❌ External APIs - NOT USED
- ❌ Background services - NOT USED
- ❌ Network calls - NOT USED

### Principle Compliance

**I. Specification is the Source of Truth**: ✅ PASS
- Spec created first, approved before planning
- All requirements traced to spec.md

**II. Agents, Not Prompts**: ✅ PASS
- Implementation will follow SDD workflow
- QA Agent skills will validate quality gates

**III. Quality Gates Over Speed**: ✅ PASS
- Test-first development planned
- Coverage targets: 80% overall, 100% critical paths
- QA validation before merge

**IV. Deterministic Behavior**: ✅ PASS
- Sequential ID generation (no UUIDs)
- No random elements
- Predictable CLI output format
- No timestamps in business logic

**V. Phase 1 Scope Boundaries**: ✅ PASS
- All constraints respected (see above)

**VI. Agent Architecture**: ✅ PASS
- Planning uses specialized agents
- Implementation will follow task-based workflow

**VII. Test-First Development**: ✅ PASS
- TDD planned for all features
- Tests before implementation
- Red-Green-Refactor cycle

**Constitution Compliance**: ✅ **FULL COMPLIANCE** - No violations, no complexity justification needed

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-core/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (to be generated)
│   └── cli-interface.md # CLI command specifications
├── checklists/          # Quality checklists
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── todo.py          # Todo entity and business logic
├── storage.py       # In-memory storage management
├── cli.py           # CLI command parsing and routing
└── main.py          # Entry point and orchestration

tests/
├── unit/
│   ├── test_todo.py       # Todo entity tests
│   ├── test_storage.py    # Storage layer tests
│   └── test_cli.py        # CLI parsing tests
└── integration/
    └── test_commands.py   # End-to-end command tests

requirements.txt     # Python dependencies (pytest, pytest-cov)
README.md           # User documentation and quickstart
```

**Structure Decision**: Single project structure selected. This is a standalone CLI application with no web/mobile components. The `src/` directory contains production code with clear separation of concerns (entity, storage, CLI, orchestration). The `tests/` directory mirrors the structure with unit tests for each module and integration tests for end-to-end workflows.

## Complexity Tracking

**No complexity justification needed** - All constitution checks pass with zero violations.

---

## Phase 0: Research & Technology Decisions

All technical decisions are resolved based on Phase 1 constraints and Python best practices. No research phase required as all choices are predetermined by constitution:

- **CLI Framework**: argparse (Python stdlib) - no external dependencies needed
- **Storage**: Python dict - simple, fast, in-memory
- **Testing**: pytest - industry standard for Python
- **ID Generation**: Sequential integers starting from 1
- **Error Handling**: Custom exception classes with user-friendly messages

**Rationale**: Phase 1 constraints eliminate technology choices. Python stdlib provides all necessary functionality (argparse for CLI, dict for storage). No research needed for well-established Python patterns.

**Status**: ✅ **Phase 0 skipped** - All decisions predetermined by constitution and Python conventions.

---

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` (to be generated) for detailed entity definitions.

**High-level overview**:

- **TodoItem**: Represents a single task
  - id (int): Unique sequential identifier (1, 2, 3...)
  - title (str): Task description (1-200 characters)
  - completed (bool): Completion status (False by default)

- **TodoStorage**: In-memory store
  - todos (dict[int, TodoItem]): Maps ID to TodoItem
  - next_id (int): Counter for generating sequential IDs

**Validation Rules**:
- Title: 1-200 characters, non-empty
- ID: Positive integer, must exist for operations
- Completed: Boolean, idempotent (can mark completed todo as completed)

**State Transitions**:
- pending → completed (via `complete` command)
- exists → deleted (via `delete` command, irreversible)
- No transition from completed → pending (not in Phase 1)

### CLI Interface Contracts

See `contracts/cli-interface.md` (to be generated) for detailed command specifications.

**Command Summary**:

1. **Add Todo**
   - Command: `todo add <title>`
   - Input: Title (string, 1-200 chars)
   - Output: "Todo added: {title} (ID: {id})"
   - Exit: 0 on success, 1 on validation error

2. **List Todos**
   - Command: `todo list`
   - Input: None
   - Output: Formatted list with IDs, titles, status
   - Exit: 0 (even if empty list)

3. **Complete Todo**
   - Command: `todo complete <id>`
   - Input: ID (integer)
   - Output: "Todo #{id} marked as complete"
   - Exit: 0 on success, 1 on error

4. **Delete Todo**
   - Command: `todo delete <id>`
   - Input: ID (integer)
   - Output: "Todo #{id} deleted"
   - Exit: 0 on success, 1 on error

5. **Help**
   - Command: `todo --help` or `todo -h`
   - Output: Usage information for all commands
   - Exit: 0

**Error Response Format**:
- Prefix: "Error: "
- Message: User-friendly description
- Examples:
  - "Error: Title cannot be empty"
  - "Error: Todo #42 not found"
  - "Error: Invalid ID '42' - ID must be a number"

### Implementation Modules

**src/todo.py** (Entity):
- `TodoItem` class (dataclass)
- Validation methods
- State management

**src/storage.py** (Storage):
- `TodoStorage` class
- CRUD operations (create, read, update, delete)
- ID generation
- In-memory dict management

**src/cli.py** (CLI):
- Argument parser setup (argparse)
- Command routing
- Output formatting
- Error message formatting

**src/main.py** (Entry Point):
- Initialize storage
- Parse arguments
- Route to command handlers
- Handle exceptions
- Exit with appropriate codes

### Error Handling Strategy

**Exception Hierarchy**:
- `TodoError` (base exception)
  - `ValidationError` (empty title, title too long)
  - `NotFoundError` (ID doesn't exist)
  - `InvalidInputError` (non-numeric ID, etc.)

**Error Flow**:
1. Validation errors caught at CLI layer
2. Business errors (not found) caught in storage
3. All errors converted to user-friendly messages
4. Exit with code 1 for errors, 0 for success
5. No stack traces shown to users (catch at top level)

### Testing Strategy

**Test Levels**:

1. **Unit Tests** (tests/unit/):
   - test_todo.py: TodoItem validation, state transitions
   - test_storage.py: CRUD operations, ID generation, edge cases
   - test_cli.py: Argument parsing, command routing, output formatting

2. **Integration Tests** (tests/integration/):
   - test_commands.py: End-to-end CLI workflows
   - Test scenarios from spec acceptance criteria
   - Verify output format and exit codes

**Coverage Targets**:
- Overall: ≥80%
- Critical paths (CRUD): 100%
- Error handlers: ≥90%
- Edge cases: Explicitly tested

**TDD Approach**:
1. Write test for new functionality (RED)
2. Run test - verify it fails
3. Implement minimum code to pass (GREEN)
4. Run test - verify it passes
5. Refactor while keeping tests green
6. Repeat for next functionality

### Quickstart Workflow

See `quickstart.md` (to be generated) for complete user guide.

**Basic User Journey**:

```bash
# 1. Add todos
$ todo add "Buy groceries"
Todo added: Buy groceries (ID: 1)

$ todo add "Read book"
Todo added: Read book (ID: 2)

# 2. List todos
$ todo list
1. [ ] Buy groceries
2. [ ] Read book

# 3. Complete a todo
$ todo complete 1
Todo #1 marked as complete

# 4. List again (see completed status)
$ todo list
1. [x] Buy groceries
2. [ ] Read book

# 5. Delete a todo
$ todo delete 2
Todo #2 deleted

# 6. Final list
$ todo list
1. [x] Buy groceries
```

### Constitution Re-Check (Post-Design)

**Phase 1 Scope Boundaries**: ✅ PASS
- Design uses only allowed technologies (argparse, dict)
- No prohibited technologies introduced

**Deterministic Behavior**: ✅ PASS
- Sequential ID generation (deterministic)
- No random elements in design
- Consistent output format

**Quality Gates**: ✅ PASS
- TDD strategy defined
- Coverage targets set
- Integration tests planned

**Overall Compliance**: ✅ **FULL COMPLIANCE MAINTAINED**

---

## Phase 2: Implementation

**Not executed by /sp.plan** - This phase is handled by `/sp.tasks` command.

The `/sp.tasks` command will:
1. Read this plan.md and spec.md
2. Generate tasks.md with specific implementation tasks
3. Break down work into testable units
4. Assign task IDs and priorities
5. Define acceptance criteria for each task

**Next Command**: `/sp.tasks` to generate implementation tasks

---

## Artifacts Generated

This planning phase produces:

1. **plan.md** (this file) - Implementation plan and architecture
2. **research.md** - Technology decisions (skipped - predetermined by constitution)
3. **data-model.md** - Entity and storage design
4. **contracts/cli-interface.md** - CLI command specifications
5. **quickstart.md** - User guide and workflow examples

All artifacts ready for task generation via `/sp.tasks`.
