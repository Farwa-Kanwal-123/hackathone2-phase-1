# Implementation Plan: Update Todo Titles

**Branch**: `002-update-todo` | **Date**: 2025-12-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-update-todo/spec.md`

## Summary

Add ability to update/edit existing todo titles via CLI command while preserving ID and completion status. Extends existing Phase 1 todo CLI with an `update` command that validates titles using the same rules as creation, provides clear error messages, and maintains data integrity.

**Technical Approach**: Extend existing `TodoStorage` class with `update()` method, add `update` subcommand to CLI parser, create `handle_update()` handler function, and route command in main.py. Follow established patterns from Phase 1 (TDD, in-memory storage, argparse CLI).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Python stdlib (argparse, dataclasses), pytest 7.4.0+, pytest-cov 4.1.0+
**Storage**: In-memory dict (Phase 1 constraint - no persistence)
**Testing**: pytest with TDD workflow (RED → GREEN → REFACTOR)
**Target Platform**: CLI (Windows, macOS, Linux terminals)
**Project Type**: Single project (CLI application)
**Performance Goals**: Update operation completes in <5 seconds (instant CLI response)
**Constraints**: Phase 1 boundaries (no databases, no file I/O, no web frameworks), <200 character title limit, deterministic behavior
**Scale/Scope**: Single user CLI session, in-memory only, extends existing 4-command CLI to 5 commands

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Initial Check (Pre-Design)

**I. Specification is the Source of Truth**
- ✅ PASS: Specification exists at `specs/002-update-todo/spec.md`
- ✅ PASS: All requirements documented with acceptance criteria
- ✅ PASS: No ambiguities (0 NEEDS CLARIFICATION markers)

**II. Agents, Not Prompts**
- ✅ PASS: Planning executed via `/sp.plan` command
- ✅ PASS: Will use existing QA agents (qa.test-execution, qa.requirement-verification, qa.quality-audit)
- ✅ PASS: Skills defined for reusable validation procedures

**III. Quality Gates Over Speed**
- ✅ PASS: TDD workflow required (write tests first)
- ✅ PASS: Coverage target: 80% overall, 100% on CRUD operations (storage.py)
- ✅ PASS: Test failures block implementation

**IV. Deterministic Behavior**
- ✅ PASS: No randomness in update operation
- ✅ PASS: Same input (ID, new title) produces same output
- ✅ PASS: Validation uses existing deterministic rules

**V. Phase 1 Scope Boundaries**
- ✅ PASS: CLI-only (argparse)
- ✅ PASS: In-memory storage (extends existing dict-based TodoStorage)
- ✅ PASS: Python stdlib only (no new dependencies)
- ✅ PASS: No database, no file I/O, no web framework

**VI. Agent Architecture**
- ✅ PASS: QA agents will validate update functionality
- ✅ PASS: Follows existing agent patterns from Phase 1

**VII. Test-First Development**
- ✅ PASS: TDD workflow enforced (RED → GREEN → REFACTOR)
- ✅ PASS: Tests written before implementation
- ✅ PASS: Unit tests for storage layer, integration tests for CLI

**INITIAL GATE RESULT**: ✅ PASS - All constitutional requirements met

## Project Structure

### Documentation (this feature)

```text
specs/002-update-todo/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── data-model.md        # Entity changes (TodoItem - no changes, TodoStorage - add update method)
├── quickstart.md        # Usage examples for update command
├── contracts/           # CLI command contract
│   └── cli-interface.md # Update command specification
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (already created)
└── tasks.md             # Task breakdown (created by /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker (no changes)
├── exceptions.py        # Custom exceptions (no changes - reuse existing ValidationError, NotFoundError)
├── todo.py              # TodoItem entity (no changes)
├── storage.py           # TodoStorage class (ADD: update() method)
├── cli.py               # CLI handlers (ADD: handle_update() function, update subcommand to parser)
└── main.py              # Entry point (ADD: route update command)

tests/
├── unit/
│   ├── __init__.py      # Unit test marker (no changes)
│   ├── test_todo.py     # TodoItem tests (no changes)
│   └── test_storage.py  # TodoStorage tests (ADD: update() method tests)
└── integration/
    ├── __init__.py      # Integration test marker (no changes)
    └── test_commands.py # CLI tests (ADD: update command integration tests)
```

## Architecture

### Layered Design (Existing Pattern)

```text
┌─────────────────────────────────────┐
│   CLI Layer (cli.py, main.py)      │  ← ADD: update command handling
│   - Argument parsing (argparse)    │
│   - Command routing                │
│   - User feedback                  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Business Logic (storage.py)      │  ← ADD: update() method
│   - CRUD operations                │
│   - ID management                  │
│   - State management               │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Entity Layer (todo.py)           │  ← NO CHANGES
│   - TodoItem dataclass             │
│   - Validation logic               │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Storage (in-memory dict)         │  ← NO CHANGES
│   - {id: TodoItem}                 │
└─────────────────────────────────────┘
```

### Component Responsibilities

**1. TodoStorage.update() Method** (NEW)
- **Input**: todo_id (int), new_title (str)
- **Validation**:
  - Check todo exists (raise NotFoundError if not)
  - Validate new title using TodoItem validation (delegate to TodoItem)
- **Operation**:
  - Retrieve existing TodoItem from dict
  - Create new TodoItem with same ID, new title, same completed status
  - Replace old TodoItem in dict
- **Output**: Updated TodoItem
- **Errors**: NotFoundError, ValidationError

**2. CLI Parser** (EXTEND)
- **Add**: `update` subcommand to existing parser
- **Arguments**:
  - `id` (int, required): Todo ID to update
  - `title` (str, required): New title
- **Pattern**: Follows existing `complete` and `delete` subcommands

**3. handle_update() Function** (NEW)
- **Input**: storage (TodoStorage), todo_id (int), new_title (str)
- **Operation**:
  - Call storage.update(todo_id, new_title)
  - Format success message showing old and new titles
- **Output**: String message for user
- **Error Handling**: Propagate TodoError exceptions to main.py

**4. Main.py Routing** (EXTEND)
- **Add**: Route `update` command to handle_update()
- **Pattern**: Follows existing command routing

### Data Flow: Update Command

```text
User Input
    ↓
$ python -m src.main update 1 "New title"
    ↓
main.py: parse_args()
    ↓
main.py: route to handle_update(storage, 1, "New title")
    ↓
cli.py: handle_update() calls storage.update(1, "New title")
    ↓
storage.py: update()
    ├── Check ID exists (self.todos.get(1))
    │   ├── If not found → raise NotFoundError
    │   └── If found → continue
    ├── Get old TodoItem
    ├── Create new TodoItem with new title
    │   └── TodoItem validates title in __post_init__
    │       ├── Empty/whitespace → raise ValidationError
    │       ├── >200 chars → raise ValidationError
    │       └── Valid → continue
    ├── Replace in self.todos[1]
    └── Return updated TodoItem
    ↓
cli.py: Format message "Updated: '{old}' → '{new}' (ID: 1)"
    ↓
main.py: print(output), return 0
    ↓
User sees confirmation
```

## Implementation Approach

### Phase 0: Research (No research needed)

**Decision**: No research required - feature extends existing Phase 1 architecture with established patterns.

**Rationale**:
- All components already exist (storage layer, CLI layer, validation)
- Update operation follows same patterns as complete/delete
- No new dependencies or technologies
- No ambiguities in requirements

**Alternatives considered**: None - straightforward extension of existing system.

### Phase 1: Design Artifacts

**To Generate**:
1. **data-model.md**: Document TodoStorage.update() method signature and behavior
2. **contracts/cli-interface.md**: Specify update command syntax and output format
3. **quickstart.md**: Usage examples for update command

**Design Decisions**:
- **Validation Strategy**: Reuse existing TodoItem validation by creating new instance
- **Update Method**: Replace entire TodoItem (immutable pattern) rather than modifying in place
- **Error Messages**: Show both old and new titles for clarity
- **ID Preservation**: Guaranteed by using same ID when creating new TodoItem
- **Status Preservation**: Guaranteed by copying `completed` field from old item

### Test-Driven Development (TDD) Workflow

**RED Phase** (Write Failing Tests):
1. Unit tests for TodoStorage.update()
   - Test updating valid todo
   - Test error for non-existent ID
   - Test validation for empty title
   - Test validation for >200 char title
   - Test preservation of ID and status
2. Integration tests for update command
   - Test successful update
   - Test error messages for invalid ID
   - Test error messages for invalid title
   - Test argparse validation for non-numeric ID

**GREEN Phase** (Implement Minimum Code):
1. Implement TodoStorage.update()
2. Add update subcommand to CLI parser
3. Implement handle_update()
4. Add routing in main.py

**REFACTOR Phase** (Improve Code Quality):
1. Extract common validation patterns
2. Improve error messages
3. Ensure consistency with existing commands

## Success Metrics

**From Specification (SC-001 to SC-006)**:
- ✅ Update completes in <5 seconds (instant CLI response)
- ✅ 100% valid commands succeed (tested via integration tests)
- ✅ Clear error messages (validated in tests)
- ✅ Eliminates delete-recreate workaround
- ✅ IDs and status never change (enforced by implementation)
- ✅ Consistent with existing commands (same patterns)

**Technical Metrics**:
- Test coverage: 80% overall, 100% on storage.update()
- All tests passing (RED → GREEN workflow)
- No Phase 1 constraint violations
- Zero new dependencies

## Risks and Mitigations

**Risk 1**: Inconsistent validation between add and update
- **Mitigation**: Reuse TodoItem.__post_init__ validation for both operations
- **Verification**: Integration tests verify same error messages

**Risk 2**: Breaking existing functionality
- **Mitigation**: No changes to existing methods (only additions)
- **Verification**: Run full Phase 1 test suite (49 tests) after implementation

**Risk 3**: Poor error messages for update-specific scenarios
- **Mitigation**: Explicitly test error message clarity in acceptance tests
- **Verification**: QA agent verifies error messages against spec

## Dependencies

**Technical Dependencies**:
- Python 3.11+ (existing)
- pytest 7.4.0+ (existing)
- argparse (stdlib, existing)

**Feature Dependencies**:
- Phase 1 todo CLI must be complete (already done - 60/60 tasks)
- TodoStorage class exists (yes)
- TodoItem validation exists (yes)
- CLI infrastructure exists (yes)

**Blockers**: None - all prerequisites met

## Rollout Strategy

**Phase 1 Extension** (This Feature):
1. Write tests for update operation (TDD RED)
2. Implement TodoStorage.update() (TDD GREEN)
3. Add CLI command and routing (TDD GREEN)
4. Refactor for quality (TDD REFACTOR)
5. Validate against spec (QA agents)
6. Update documentation (README, quickstart)

**Testing Strategy**:
- Unit tests: storage.update() with all edge cases
- Integration tests: CLI update command end-to-end
- Validation: Run existing Phase 1 tests (regression check)
- Manual: Test all acceptance scenarios from spec

**Release Criteria**:
- All new tests passing (100%)
- All existing tests passing (49 tests)
- Coverage ≥80% overall, 100% on storage.update()
- Constitution check passes
- All acceptance scenarios verified

## Constitution Re-Check (Post-Design)

**I. Specification is the Source of Truth**
- ✅ PASS: All design decisions traceable to spec requirements

**II. Agents, Not Prompts**
- ✅ PASS: QA agents ready for validation

**III. Quality Gates Over Speed**
- ✅ PASS: TDD workflow defined, coverage targets set

**IV. Deterministic Behavior**
- ✅ PASS: Update operation deterministic (same input → same output)

**V. Phase 1 Scope Boundaries**
- ✅ PASS: No database, no file I/O, CLI-only, in-memory storage

**VI. Agent Architecture**
- ✅ PASS: QA validation workflow defined

**VII. Test-First Development**
- ✅ PASS: TDD workflow (RED → GREEN → REFACTOR) enforced

**FINAL GATE RESULT**: ✅ PASS - Design maintains constitutional compliance

## Next Steps

1. **Phase 1 Complete**: Generate design artifacts
   - `data-model.md`: TodoStorage.update() specification
   - `contracts/cli-interface.md`: Update command contract
   - `quickstart.md`: Usage examples

2. **Ready for `/sp.tasks`**: Create task breakdown with TDD workflow

3. **Implementation Order**:
   - Tasks (RED): Write failing tests
   - Tasks (GREEN): Implement update functionality
   - Tasks (REFACTOR): Improve code quality
   - Tasks (Polish): Documentation and validation

**Estimated Scope**: ~10-15 tasks total
- Setup: 0 tasks (existing infrastructure)
- Tests (RED): 4-6 tasks
- Implementation (GREEN): 4-5 tasks
- Refactor: 1-2 tasks
- Polish: 1-2 tasks
