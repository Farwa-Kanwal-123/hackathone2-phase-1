# Implementation Plan: Interactive Menu-Based Todo Console

**Branch**: `003-interactive-menu` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-interactive-menu/spec.md`

## Summary

Transform the existing CLI todo application into a beginner-friendly, interactive, menu-based console app that launches via `uv run main.py`. Add a main menu loop that displays numbered options, prompts users for input interactively, and automatically returns to the menu after each operation. Reuse existing storage, validation, and CLI handler logic while adding a thin interactive layer on top.

**Technical Approach**: Create a new `main.py` entry point at repository root that implements a menu loop pattern. Add an `interactive_menu.py` module in the `src/` directory for menu display and input prompting logic. Configure `uv` project with `pyproject.toml` to support `uv run main.py`. Reuse all existing CLI handlers (`handle_add`, `handle_list`, etc.) by wrapping them with interactive prompts.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Python stdlib (existing: argparse, dataclasses), pytest 7.4.0+, pytest-cov 4.1.0+ (existing)
**Package Manager**: `uv` (Python package installer and resolver)
**Entry Point**: `main.py` at repository root (NEW - runs via `uv run main.py`)
**Storage**: In-memory dict (existing - no changes)
**Testing**: pytest with TDD workflow (existing infrastructure)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux terminals)
**Project Type**: Single project (CLI application with interactive mode)
**Performance Goals**: Menu displays instantly (<100ms), operations complete <5 seconds
**Constraints**: Phase 1 boundaries (no databases, no file I/O, no TUI libraries), text-based menu only
**Scale/Scope**: Single user CLI session, in-memory only, extends existing 5-command CLI

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Initial Check (Pre-Design)

**I. Specification is the Source of Truth**
- ✅ PASS: Specification exists at `specs/003-interactive-menu/spec.md`
- ✅ PASS: All requirements documented with acceptance criteria
- ✅ PASS: No ambiguities (0 NEEDS CLARIFICATION markers)

**II. Agents, Not Prompts**
- ✅ PASS: Planning executed via `/sp.plan` command
- ✅ PASS: Will use existing QA agents for validation
- ✅ PASS: Skills defined for reusable procedures

**III. Quality Gates Over Speed**
- ✅ PASS: TDD workflow required (write tests first)
- ✅ PASS: Coverage target: 80% overall, 100% on interactive menu logic
- ✅ PASS: Test failures block implementation

**IV. Deterministic Behavior**
- ✅ PASS: No randomness in menu display or input handling
- ✅ PASS: Same user input produces same menu navigation
- ✅ PASS: Predictable menu loop behavior

**V. Phase 1 Scope Boundaries**
- ✅ PASS: CLI-only (text-based menu, no TUI libraries)
- ✅ PASS: In-memory storage (reuses existing TodoStorage)
- ✅ PASS: Python stdlib only (no new external dependencies beyond uv tooling)
- ✅ PASS: No database, no file I/O (except uv project configuration)

**VI. Agent Architecture**
- ✅ PASS: QA agents will validate interactive menu functionality
- ✅ PASS: Follows existing agent patterns from Phase 1

**VII. Test-First Development**
- ✅ PASS: TDD workflow enforced (RED → GREEN → REFACTOR)
- ✅ PASS: Tests written before implementation
- ✅ PASS: Unit tests for menu logic, integration tests for user workflows

**INITIAL GATE RESULT**: ✅ PASS - All constitutional requirements met

## Project Structure

### Documentation (this feature)

```text
specs/003-interactive-menu/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── data-model.md        # No changes to entities (existing TodoItem, TodoStorage)
├── quickstart.md        # Usage examples for interactive menu
├── contracts/           # Menu interface contract
│   └── menu-interface.md # Menu display and input prompt specifications
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (already created)
└── tasks.md             # Task breakdown (created by /sp.tasks)
```

### Source Code (repository root)

```text
main.py                  # NEW: Entry point for uv run main.py (interactive mode)
pyproject.toml           # NEW: uv project configuration

src/
├── __init__.py          # Package marker (no changes)
├── exceptions.py        # Custom exceptions (no changes)
├── todo.py              # TodoItem entity (no changes)
├── storage.py           # TodoStorage class (no changes)
├── cli.py               # CLI handlers (no changes - reused)
├── main.py              # Existing CLI entry point (no changes - preserved for python -m src.main)
└── interactive_menu.py  # NEW: Menu display and interactive prompt logic

tests/
├── unit/
│   ├── __init__.py      # Unit test marker (no changes)
│   ├── test_todo.py     # TodoItem tests (no changes)
│   ├── test_storage.py  # TodoStorage tests (no changes)
│   └── test_menu.py     # NEW: Interactive menu tests
└── integration/
    ├── __init__.py      # Integration test marker (no changes)
    └── test_interactive.py # NEW: Interactive workflow tests
```

## Architecture

### Layered Design

```text
┌──────────────────────────────────────────┐
│   Entry Point (main.py at root)         │  ← NEW: uv run main.py
│   - Interactive menu loop                │
│   - Display menu, get choice             │
│   - Dispatch to interactive handlers     │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│   Interactive Layer (interactive_menu.py)│  ← NEW: Menu & prompt logic
│   - display_menu() → show options        │
│   - get_menu_choice() → validate input   │
│   - prompt_for_input(msg) → get user text│
│   - Interactive handlers wrapping CLI    │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│   CLI Layer (cli.py - EXISTING)         │  ← NO CHANGES: Reused handlers
│   - handle_add(), handle_list(), etc.   │
│   - Command routing                     │
│   - User feedback                       │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│   Business Logic (storage.py - EXISTING)│  ← NO CHANGES
│   - CRUD operations                     │
│   - ID management                       │
│   - State management                    │
└──────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────┐
│   Entity Layer (todo.py - EXISTING)     │  ← NO CHANGES
│   - TodoItem dataclass                  │
│   - Validation logic                    │
└──────────────────────────────────────────┘
```

### Component Responsibilities

**1. main.py (NEW - Root Entry Point)**
- **Purpose**: Entry point for `uv run main.py` interactive mode
- **Responsibilities**:
  - Initialize TodoStorage instance
  - Display welcome message
  - Enter menu loop (while True)
  - Display menu → get choice → execute → repeat
  - Handle exit gracefully (goodbye message)
  - Handle Ctrl+C interrupts
- **Pattern**: Main loop with try/except for clean exit

**2. interactive_menu.py (NEW - Interactive Layer)**
- **Core Functions**:
  - `display_menu()` → Print numbered menu options
  - `get_menu_choice()` → Get and validate numeric menu selection
  - `prompt_for_input(prompt_message)` → Get string input from user
  - `prompt_for_id(prompt_message)` → Get and validate numeric ID
  - `interactive_add(storage)` → Prompt for title, call handle_add()
  - `interactive_list(storage)` → Call handle_list(), display results
  - `interactive_complete(storage)` → Prompt for ID, call handle_complete()
  - `interactive_update(storage)` → Prompt for ID and title, call handle_update()
  - `interactive_delete(storage)` → Prompt for ID, call handle_delete()

**3. Existing CLI Handlers (cli.py - REUSED)**
- **No Changes**: All existing handlers (`handle_add`, `handle_list`, etc.) are reused
- **Integration**: Interactive functions wrap these handlers with prompts

**4. uv Configuration (pyproject.toml - NEW)**
- **Purpose**: Configure `uv` to run `main.py` as entry point
- **Contents**:
  ```toml
  [project]
  name = "todo-app"
  version = "1.5.0"
  description = "Interactive in-memory todo console app"
  requires-python = ">=3.11"
  dependencies = []

  [build-system]
  requires = ["hatchling"]
  build-backend = "hatchling.build"
  ```

### Data Flow: Interactive Add Example

```text
User runs: uv run main.py
    ↓
main.py: Display welcome + menu
    ↓
User: Selects option "1" (Add todo)
    ↓
main.py: Calls interactive_add(storage)
    ↓
interactive_menu.py: interactive_add()
    ├── Display prompt: "Enter todo title:"
    ├── Get user input (title)
    ├── Validate input (not empty)
    │   ├── If invalid → show error, re-prompt
    │   └── If valid → continue
    ├── Call cli.handle_add(storage, title)
    ├── Print confirmation message
    └── Return to main.py loop
    ↓
main.py: Display menu again (loop continues)
```

### Menu Structure

```text
=== Todo App - Interactive Menu ===

1. Add todo
2. List all todos
3. Complete todo
4. Update todo
5. Delete todo
6. Exit

Enter your choice (1-6): _
```

## Implementation Approach

### Phase 0: Research

**No research needed** - Feature extends existing Phase 1 architecture with established patterns.

**Rationale**:
- All components already exist (storage, CLI handlers, validation)
- Interactive menu is straightforward stdin/stdout pattern
- No new dependencies (uv is tooling, not runtime dependency)
- No ambiguities in requirements

**uv Setup**:
- `uv` is a Python package installer (alternative to pip)
- `uv run main.py` executes main.py with project's Python environment
- Requires `pyproject.toml` at repository root (standard Python project file)
- No runtime dependency on uv (it's build/dev tooling)

### Phase 1: Design Artifacts

**To Generate**:
1. **data-model.md**: No changes (TodoItem and TodoStorage unchanged)
2. **contracts/menu-interface.md**: Specify menu display format, prompt patterns, input validation
3. **quickstart.md**: Usage examples for interactive menu workflows

**Design Decisions**:
- **Entry Point**: New `main.py` at root (vs modifying existing `src/main.py`)
  - Rationale: Preserves existing CLI for backward compatibility
  - Existing: `python -m src.main add "title"` still works
  - New: `uv run main.py` launches interactive mode
- **Menu Loop**: Infinite while loop with exit option
  - Rationale: Standard interactive CLI pattern
  - Clean exit on option "6" or Ctrl+C
- **Input Validation**: Re-prompt on invalid input (no crashes)
  - Rationale: Beginner-friendly (errors don't terminate session)
- **Handler Reuse**: Wrap existing CLI handlers with prompts
  - Rationale: DRY principle, minimal code duplication
  - Testing already validated handler logic

### Test-Driven Development (TDD) Workflow

**RED Phase** (Write Failing Tests):
1. Unit tests for interactive_menu.py
   - Test display_menu() output format
   - Test get_menu_choice() validation (valid/invalid inputs)
   - Test prompt_for_input() basic functionality
   - Test prompt_for_id() numeric validation
   - Test each interactive_* function with mocked input

2. Integration tests for main.py workflow
   - Test menu loop with simulated user input
   - Test add workflow (menu selection → prompt → add → menu)
   - Test list workflow
   - Test complete/update/delete workflows
   - Test exit workflow (option 6 and Ctrl+C)

**GREEN Phase** (Implement Minimum Code):
1. Create pyproject.toml with uv configuration
2. Create main.py with menu loop
3. Create interactive_menu.py with:
   - Menu display function
   - Input validation functions
   - Interactive handler wrappers
4. Verify `uv run main.py` launches successfully

**REFACTOR Phase** (Improve Code Quality):
1. Extract common prompt patterns
2. Improve error messages for clarity
3. Add input sanitization (strip whitespace)
4. Ensure consistent user experience

## Success Metrics

**From Specification (SC-001 to SC-006)**:
- ✅ Launch in <5 seconds via `uv run main.py`
- ✅ Complete add-list-complete workflow in <30 seconds
- ✅ 95% first-attempt success rate (clear menus and prompts)
- ✅ Zero crashes during normal operation
- ✅ Clear error messages (no external help needed)
- ✅ Eliminates command syntax memorization

**Technical Metrics**:
- Test coverage: 80% overall, 100% on interactive_menu.py
- All tests passing (RED → GREEN workflow)
- No Phase 1 constraint violations
- Zero new runtime dependencies (uv is dev/build tool only)
- Backward compatibility: existing CLI (`python -m src.main`) still works

## Risks and Mitigations

**Risk 1**: uv tooling not available on user's system
- **Mitigation**: Document uv installation in README, provide fallback instructions
- **Verification**: Test installation steps on clean system

**Risk 2**: Input handling edge cases (Ctrl+C, EOF, special characters)
- **Mitigation**: Comprehensive exception handling in menu loop
- **Verification**: Test with simulated edge case inputs

**Risk 3**: Menu display issues on different terminals
- **Mitigation**: Use only basic text (no ANSI codes, no cursor positioning)
- **Verification**: Test on Windows cmd, PowerShell, macOS terminal, Linux bash

**Risk 4**: Breaking existing CLI functionality
- **Mitigation**: No changes to existing `src/main.py` or handlers
- **Verification**: Run existing Phase 1 test suite (63 tests) after implementation

## Dependencies

**Technical Dependencies**:
- Python 3.11+ (existing)
- pytest 7.4.0+ (existing)
- uv package manager (NEW - dev/build tool, install separately)

**Feature Dependencies**:
- Phase 1 todo CLI must be complete (already done - all features implemented)
- TodoStorage class exists (yes)
- TodoItem validation exists (yes)
- CLI handlers exist (yes)

**Blockers**: None - all prerequisites met

## Rollout Strategy

**Phase 1.5 Implementation** (This Feature):
1. Create pyproject.toml (uv configuration)
2. Write tests for interactive menu (TDD RED)
3. Implement main.py and interactive_menu.py (TDD GREEN)
4. Refactor for quality (TDD REFACTOR)
5. Validate against spec (QA agents)
6. Update documentation (README, quickstart)

**Testing Strategy**:
- Unit tests: interactive_menu.py functions with mocked stdin
- Integration tests: main.py menu loop with simulated user sessions
- Validation: Run existing Phase 1 tests (regression check)
- Manual: Test all user stories from spec interactively

**Release Criteria**:
- All new tests passing (100%)
- All existing tests passing (63 tests from Phase 1)
- Coverage ≥80% overall, 100% on interactive_menu.py
- Constitution check passes
- All acceptance scenarios verified
- `uv run main.py` launches successfully

## Constitution Re-Check (Post-Design)

**I. Specification is the Source of Truth**
- ✅ PASS: All design decisions traceable to spec requirements

**II. Agents, Not Prompts**
- ✅ PASS: QA agents ready for validation

**III. Quality Gates Over Speed**
- ✅ PASS: TDD workflow defined, coverage targets set

**IV. Deterministic Behavior**
- ✅ PASS: Menu loop deterministic (same input → same behavior)

**V. Phase 1 Scope Boundaries**
- ✅ PASS: No database, no file I/O (except pyproject.toml config), CLI-only, in-memory storage

**VI. Agent Architecture**
- ✅ PASS: QA validation workflow defined

**VII. Test-First Development**
- ✅ PASS: TDD workflow (RED → GREEN → REFACTOR) enforced

**FINAL GATE RESULT**: ✅ PASS - Design maintains constitutional compliance

## Next Steps

1. **Phase 1 Complete**: Generate design artifacts
   - `contracts/menu-interface.md`: Menu display and prompt specifications
   - `quickstart.md`: Interactive usage examples

2. **Ready for `/sp.tasks`**: Create task breakdown with TDD workflow

3. **Implementation Order**:
   - Tasks (Setup): Create pyproject.toml, directory structure
   - Tasks (RED): Write failing tests for menu and workflows
   - Tasks (GREEN): Implement main.py and interactive_menu.py
   - Tasks (REFACTOR): Improve code quality
   - Tasks (Polish): Documentation and validation

**Estimated Scope**: ~20-25 tasks total
- Setup: 2-3 tasks (pyproject.toml, main.py stub, interactive_menu.py stub)
- Tests (RED): 8-10 tasks (unit tests for menu functions, integration tests for workflows)
- Implementation (GREEN): 5-7 tasks (menu loop, interactive handlers, uv configuration)
- Refactor: 2-3 tasks (error handling, input sanitization, user experience)
- Polish: 3-4 tasks (documentation, regression testing, manual validation)
