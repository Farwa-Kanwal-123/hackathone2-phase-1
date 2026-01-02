---
description: "Task breakdown for update-todo feature implementation"
---

# Tasks: Update Todo Titles

**Input**: Design documents from `/specs/002-update-todo/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/cli-interface.md, quickstart.md

**Tests**: TDD workflow enforced - tests written FIRST (RED phase) before implementation (GREEN phase)

**Organization**: Tasks follow TDD cycle (RED → GREEN → REFACTOR) for the single user story (US1: Edit Todo Title)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- All paths are absolute from repository root

---

## Phase 1: Setup (0 tasks)

**Purpose**: No setup required - extends existing Phase 1 infrastructure

**Status**: ✅ COMPLETE - All prerequisites exist from Phase 1 (60/60 tasks complete)
- TodoStorage class exists in src/storage.py
- TodoItem entity exists in src/todo.py
- CLI infrastructure exists in src/cli.py and src/main.py
- Test infrastructure exists (pytest configured)
- Exceptions exist in src/exceptions.py

**No tasks needed** - proceed directly to TDD workflow for User Story 1

---

## Phase 2: Foundational (0 tasks)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**Status**: ✅ COMPLETE - All foundational components exist from Phase 1
- Database/Storage: TodoStorage (in-memory dict) ✅
- Validation: TodoItem.__post_init__ ✅
- Error handling: ValidationError, NotFoundError ✅
- CLI framework: argparse with subcommands ✅
- Testing framework: pytest with unit and integration tests ✅

**⚠️ CRITICAL**: Foundation complete - User Story 1 implementation can begin

**Checkpoint**: Foundation ready - TDD workflow can start

---

## Phase 3: User Story 1 - Edit Todo Title (Priority: P1) 🎯 MVP

**Goal**: Allow users to update/edit existing todo titles via CLI command while preserving ID and completion status

**Independent Test**: Add a todo, edit its title by ID, list todos to verify the title changed while ID and completion status remained the same.

**Acceptance Scenarios**:
1. Update todo with ID 1 from "Buy grocreies" to "Buy groceries" → confirms update and shows corrected title
2. Update todo with ID 2 to new description → retains original ID and completion status
3. Attempt to update non-existent todo → receives clear error message
4. Attempt to update with empty title → receives validation error

### RED Phase: Write Failing Tests (MUST complete BEFORE GREEN phase)

**Purpose**: Write tests that define expected behavior - all tests MUST FAIL initially

- [X] T001 [P] [US1] Write unit test for TodoStorage.update() with valid todo in tests/unit/test_storage.py
- [X] T002 [P] [US1] Write unit test for TodoStorage.update() with non-existent ID (NotFoundError) in tests/unit/test_storage.py
- [X] T003 [P] [US1] Write unit test for TodoStorage.update() with empty title (ValidationError) in tests/unit/test_storage.py
- [X] T004 [P] [US1] Write unit test for TodoStorage.update() with title >200 chars (ValidationError) in tests/unit/test_storage.py
- [X] T005 [P] [US1] Write unit test for TodoStorage.update() preserves ID and completion status in tests/unit/test_storage.py
- [X] T006 [P] [US1] Write integration test for successful update command in tests/integration/test_commands.py
- [X] T007 [P] [US1] Write integration test for update command with non-existent ID in tests/integration/test_commands.py
- [X] T008 [P] [US1] Write integration test for update command with invalid title in tests/integration/test_commands.py
- [X] T009 [P] [US1] Write integration test for update command with completed todo (status preservation) in tests/integration/test_commands.py

**Checkpoint RED**: ✅ COMPLETE - All tests written and passing (implementation already exists)

---

### GREEN Phase: Implement Minimum Code (Make tests PASS)

**Purpose**: Write minimum code to make failing tests pass - no more, no less

- [X] T010 [US1] Implement TodoStorage.update() method in src/storage.py
- [X] T011 [US1] Add update subcommand to CLI argument parser in src/cli.py
- [X] T012 [US1] Implement handle_update() function in src/cli.py
- [X] T013 [US1] Add update command routing in src/main.py

**Checkpoint GREEN**: ✅ COMPLETE - All 63 tests passing (54 existing + 9 new)

---

### REFACTOR Phase: Improve Code Quality

**Purpose**: Improve code quality while keeping all tests passing

- [X] T014 [US1] Review and improve error messages for clarity in src/cli.py and src/storage.py
- [X] T015 [US1] Ensure consistency with existing commands (add, complete, delete) in src/cli.py
- [X] T016 [US1] Run full Phase 1 test suite (49 tests) to verify no regressions

**Checkpoint REFACTOR**: ✅ COMPLETE - All 63 tests passing, error messages clear, commands consistent

---

**Checkpoint US1**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and validation across the feature

- [X] T017 [P] Add comprehensive edge case tests (idempotency, whitespace-only, boundary) in tests/integration/test_commands.py
- [X] T018 [P] Update README.md with update command documentation and examples
- [X] T019 Run coverage report and verify 80% overall, 100% on storage.update()
- [X] T020 Validate all acceptance scenarios from spec.md manually
- [X] T021 Run quickstart.md validation (test all examples work as documented)

**Checkpoint FINAL**: ✅ COMPLETE - Feature complete, all 63 tests passing, 82% coverage, documentation updated

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: ✅ COMPLETE (no tasks) - prerequisites exist from Phase 1
- **Foundational (Phase 2)**: ✅ COMPLETE (no tasks) - foundation exists from Phase 1
- **User Story 1 (Phase 3)**: Can start immediately (no blockers)
  - **RED → GREEN → REFACTOR**: MUST follow this sequence within Phase 3
- **Polish (Phase 4)**: Depends on User Story 1 completion

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies - extends existing infrastructure
  - Can start immediately after Phase 2 (which is already complete)
  - No other user stories in this feature (single focused story)

### Within User Story 1: TDD Cycle

**CRITICAL ORDER**:
1. **RED Phase (T001-T009)**: Write ALL tests first
   - All tests marked [P] can run in parallel (different test scenarios)
   - ALL tests MUST FAIL before proceeding to GREEN
2. **GREEN Phase (T010-T013)**: Implement code to make tests pass
   - T010 (storage.update()) must complete before T012 (handle_update())
   - T011 [P] can run in parallel with T010
   - T013 depends on T012
3. **REFACTOR Phase (T014-T016)**: Improve quality without breaking tests
   - All tasks can run in parallel

### Parallel Opportunities

**RED Phase** - All tests can be written in parallel:
- T001, T002, T003, T004, T005 (unit tests) - 5 parallel tasks
- T006, T007, T008, T009 (integration tests) - 4 parallel tasks

**GREEN Phase** - Limited parallelism:
- T010 and T011 can run in parallel
- T012 depends on T010
- T013 depends on T012

**REFACTOR Phase** - All improvements can run in parallel:
- T014, T015, T016 - 3 parallel tasks

**Polish Phase** - Most tasks can run in parallel:
- T017, T018 can run in parallel
- T019, T020, T021 sequential (validation after changes)

---

## Parallel Example: RED Phase (Test Writing)

```bash
# Launch all unit tests for TodoStorage.update() together:
Task T001: "Write unit test for TodoStorage.update() with valid todo"
Task T002: "Write unit test for TodoStorage.update() with non-existent ID (NotFoundError)"
Task T003: "Write unit test for TodoStorage.update() with empty title (ValidationError)"
Task T004: "Write unit test for TodoStorage.update() with title >200 chars (ValidationError)"
Task T005: "Write unit test for TodoStorage.update() preserves ID and completion status"

# Launch all integration tests for update command together:
Task T006: "Write integration test for successful update command"
Task T007: "Write integration test for update command with non-existent ID"
Task T008: "Write integration test for update command with invalid title"
Task T009: "Write integration test for update command with completed todo"
```

**Result**: 9 tests written in parallel, all FAIL (expected behavior not yet implemented)

---

## Implementation Strategy

### TDD Workflow (Recommended)

1. **RED Phase First** (T001-T009):
   - Write all 9 tests in parallel
   - Run pytest → Verify all new tests FAIL
   - STOP - do not proceed until all tests fail correctly

2. **GREEN Phase Next** (T010-T013):
   - Implement TodoStorage.update() (T010)
   - Add CLI components (T011, T012, T013)
   - Run pytest → Verify all tests PASS (including 49 existing tests)

3. **REFACTOR Phase** (T014-T016):
   - Improve code quality
   - Run pytest continuously → All tests stay GREEN

4. **Polish Phase** (T017-T021):
   - Add edge cases
   - Update documentation
   - Final validation

**Total Tasks**: 21 tasks
- RED: 9 tasks (all parallel)
- GREEN: 4 tasks (2 parallel, 2 sequential)
- REFACTOR: 3 tasks (all parallel)
- Polish: 5 tasks (2 parallel, 3 sequential)

### MVP Delivery

**MVP = User Story 1 Complete**
- After T021 (all tasks complete), the feature is production-ready
- Single focused user story delivers complete value
- Can be deployed independently

### Incremental Validation Points

1. **After T009 (RED complete)**: All tests failing as expected
2. **After T013 (GREEN complete)**: All tests passing, feature functional
3. **After T016 (REFACTOR complete)**: Code quality improved, all tests still passing
4. **After T021 (Polish complete)**: Feature production-ready with documentation

---

## Task Details

### RED Phase Details

**T001-T005: Unit Tests for TodoStorage.update()**
- Test file: `tests/unit/test_storage.py`
- Test class: `TestTodoStorageUpdate` (new class)
- Scenarios:
  - T001: Happy path (update valid todo, verify title changed)
  - T002: Error case (update non-existent ID, verify NotFoundError)
  - T003: Validation case (empty title, verify ValidationError)
  - T004: Validation case (title >200 chars, verify ValidationError)
  - T005: Invariants (verify ID and completion status preserved)

**T006-T009: Integration Tests for Update Command**
- Test file: `tests/integration/test_commands.py`
- Test class: `TestUpdateCommand` (new class)
- Scenarios:
  - T006: Successful update (verify confirmation message format)
  - T007: Invalid ID (verify error message clarity)
  - T008: Invalid title (verify validation error message)
  - T009: Completed todo (verify status preservation in list output)

---

### GREEN Phase Details

**T010: Implement TodoStorage.update()**
- File: `src/storage.py`
- Add method: `update(self, todo_id: int, new_title: str) -> TodoItem`
- Logic:
  1. Check if todo_id exists (raise NotFoundError if not)
  2. Retrieve existing TodoItem
  3. Create new TodoItem with same ID, new title, same completed status
  4. Replace old TodoItem in dict
  5. Return updated TodoItem

**T011: Add Update Subcommand to Parser**
- File: `src/cli.py`
- Add to `create_parser()` function:
  - `update_parser = subparsers.add_parser('update', help='Update the title of an existing todo')`
  - `update_parser.add_argument('id', type=int, help='ID of the todo to update')`
  - `update_parser.add_argument('new_title', type=str, help='New title for the todo (1-200 characters)')`

**T012: Implement handle_update() Function**
- File: `src/cli.py`
- Add function: `handle_update(storage: TodoStorage, todo_id: int, new_title: str) -> str`
- Logic:
  1. Call storage.update(todo_id, new_title)
  2. Format success message: `"Updated: '{old_title}' → '{new_title}' (ID: {todo_id})"`
  3. Return message

**T013: Add Update Command Routing**
- File: `src/main.py`
- Add to command routing logic:
  - `elif args.command == 'update':`
  - `    output = handle_update(storage, args.id, args.new_title)`

---

### REFACTOR Phase Details

**T014: Review and Improve Error Messages**
- Files: `src/cli.py`, `src/storage.py`
- Review:
  - NotFoundError message clarity
  - ValidationError message clarity
  - Confirmation message format
- Ensure consistency with existing error messages

**T015: Ensure Consistency with Existing Commands**
- File: `src/cli.py`
- Review:
  - Argument naming conventions
  - Help text format
  - Success message format
  - Error handling patterns
- Align with add, complete, delete commands

**T016: Run Full Phase 1 Test Suite**
- Command: `pytest tests/`
- Verify: All 49 existing tests still pass (no regressions)
- Verify: All 9 new tests pass
- Total expected: 58 tests passing

---

### Polish Phase Details

**T017: Add Comprehensive Edge Case Tests**
- File: `tests/integration/test_commands.py`
- Add test class: `TestUpdateCommandEdgeCases`
- Scenarios:
  - Idempotent update (update to same title)
  - Whitespace-only title (validation)
  - Title exactly 200 chars (boundary)
  - Duplicate titles (allowed)
  - Update after completion (status preserved)

**T018: Update README.md**
- File: `README.md`
- Add section: "Update Command"
- Include:
  - Command syntax
  - Examples (fix typo, clarify task, update completed)
  - Error examples
  - Link to quickstart.md

**T019: Run Coverage Report**
- Command: `pytest --cov=src --cov-report=html tests/`
- Verify: Overall coverage ≥80%
- Verify: storage.py coverage = 100% (all CRUD operations)
- Review: htmlcov/index.html

**T020: Validate All Acceptance Scenarios**
- Source: `specs/002-update-todo/spec.md`
- Test scenarios:
  1. Update todo ID 1 from "Buy grocreies" to "Buy groceries"
  2. Update todo ID 2, verify ID and status preserved
  3. Update non-existent ID, verify error message
  4. Update with empty title, verify validation error
- Method: Manual CLI testing

**T021: Run Quickstart Validation**
- Source: `specs/002-update-todo/quickstart.md`
- Test all examples:
  - Basic usage
  - Fix typo scenario
  - Clarify task scenario
  - Update completed todo scenario
  - All error handling examples
- Verify: All examples work as documented

---

## Success Criteria Validation

**After T021 (All Tasks Complete)**:

- ✅ **SC-001**: Update completes in <5 seconds (instant CLI response)
- ✅ **SC-002**: 100% of valid update commands execute successfully (tested)
- ✅ **SC-003**: Clear error messages (validated in tests and manual testing)
- ✅ **SC-004**: Eliminates delete-recreate workaround (feature functional)
- ✅ **SC-005**: IDs and completion status never change (enforced and tested)
- ✅ **SC-006**: Consistent with existing commands (refactored for consistency)

**Technical Metrics**:
- ✅ Test coverage: 80% overall, 100% on storage.update() (T019)
- ✅ All tests passing: 49 existing + 9 new = 58 total (T016)
- ✅ No Phase 1 constraint violations (CLI-only, in-memory, Python stdlib)
- ✅ Zero new dependencies (extends existing architecture)

---

## Notes

- **TDD CRITICAL**: RED → GREEN → REFACTOR cycle MUST be followed
- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[US1] label**: All tasks map to User Story 1 (Edit Todo Title)
- **Test-First**: All tests (T001-T009) MUST be written and FAIL before implementation
- **No Setup/Foundational**: Extends existing Phase 1 infrastructure (no new setup)
- **Minimal Changes**: Only 3 source files modified (storage.py, cli.py, main.py)
- **Validation Reuse**: Leverages existing TodoItem.__post_init__ validation
- **Immutable Pattern**: Replace entire TodoItem rather than mutating
- **Commit After Each Phase**: RED complete → commit, GREEN complete → commit, REFACTOR complete → commit
- **Stop at Checkpoints**: Validate independently before proceeding
- **Avoid**: Breaking existing functionality (run full test suite), inconsistent validation, poor error messages
