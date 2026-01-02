# Tasks: Todo CLI Core

**Input**: Design documents from `/specs/001-todo-cli-core/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/

**Tests**: Tests are included per constitution requirement VII (Test-First Development - NON-NEGOTIABLE). TDD cycle mandatory: Tests written → Tests fail (RED) → Implement (GREEN) → Refactor.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project per plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure (src/, tests/unit/, tests/integration/)
- [x] T002 Create requirements.txt with pytest and pytest-cov dependencies
- [x] T003 [P] Create .gitignore for Python project (__pycache__/, *.pyc, .venv/, venv/, dist/, *.egg-info/, .pytest_cache/, .coverage, htmlcov/)
- [x] T004 [P] Create README.md with project overview and installation instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Create src/__init__.py (empty module marker)
- [x] T006 [P] Create tests/__init__.py (empty module marker)
- [x] T007 [P] Create tests/unit/__init__.py (empty module marker)
- [x] T008 [P] Create tests/integration/__init__.py (empty module marker)
- [x] T009 Create custom exception classes in src/exceptions.py (TodoError, ValidationError, NotFoundError, InvalidInputError)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items and view all todos in a list

**Independent Test**: Run CLI to add a todo, then list all todos. Verify todo appears with correct ID and title.

### Tests for User Story 1 (TDD - Write First, RED Phase)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T010 [P] [US1] Write test for TodoItem creation with valid title in tests/unit/test_todo.py
- [x] T011 [P] [US1] Write test for TodoItem title validation (empty, too long, whitespace-only) in tests/unit/test_todo.py
- [x] T012 [P] [US1] Write test for TodoStorage add operation in tests/unit/test_storage.py
- [x] T013 [P] [US1] Write test for TodoStorage list_all operation in tests/unit/test_storage.py
- [x] T014 [P] [US1] Write test for sequential ID generation in tests/unit/test_storage.py
- [x] T015 [P] [US1] Write integration test for "add" command in tests/integration/test_commands.py
- [x] T016 [P] [US1] Write integration test for "list" command (with todos) in tests/integration/test_commands.py
- [x] T017 [P] [US1] Write integration test for "list" command (empty list) in tests/integration/test_commands.py

### Implementation for User Story 1 (GREEN Phase)

- [x] T018 [P] [US1] Implement TodoItem class (dataclass) in src/todo.py with id, title, completed attributes
- [x] T019 [US1] Implement TodoItem validation in src/todo.py (__post_init__ method)
- [x] T020 [US1] Implement TodoStorage class in src/storage.py with __init__, todos dict, next_id counter
- [x] T021 [US1] Implement TodoStorage.add(title) method in src/storage.py (create TodoItem, assign ID, store, increment)
- [x] T022 [US1] Implement TodoStorage.list_all() method in src/storage.py (return sorted list of todos)
- [x] T023 [US1] Create CLI argument parser in src/cli.py with argparse setup and add/list subcommands
- [x] T024 [US1] Implement handle_add(storage, title) function in src/cli.py (call storage.add, format output)
- [x] T025 [US1] Implement handle_list(storage) function in src/cli.py (call storage.list_all, format as "ID. [status] title")
- [x] T026 [US1] Create main.py entry point in src/main.py (initialize storage, parse args, route commands, handle exceptions, exit codes)
- [x] T027 [US1] Run tests for User Story 1, verify all pass (GREEN phase complete)
- [x] T028 [US1] Refactor User Story 1 code for clarity while keeping tests green

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (MVP complete!)

---

## Phase 4: User Story 2 - Mark Todos as Complete (Priority: P2)

**Goal**: Enable users to mark todo items as complete to track progress

**Independent Test**: Add a todo, mark it complete by ID, list todos to verify status changed to [x]

### Tests for User Story 2 (TDD - Write First, RED Phase)

- [x] T029 [P] [US2] Write test for TodoStorage.complete(id) method in tests/unit/test_storage.py
- [x] T030 [P] [US2] Write test for completing non-existent todo (NotFoundError) in tests/unit/test_storage.py
- [x] T031 [P] [US2] Write test for idempotent complete (completing already-completed todo) in tests/unit/test_storage.py
- [x] T032 [P] [US2] Write integration test for "complete" command (valid ID) in tests/integration/test_commands.py
- [x] T033 [P] [US2] Write integration test for "complete" command (invalid ID) in tests/integration/test_commands.py
- [x] T034 [P] [US2] Write integration test for "complete" command (non-numeric ID) in tests/integration/test_commands.py

### Implementation for User Story 2 (GREEN Phase)

- [x] T035 [US2] Implement TodoStorage.complete(id) method in src/storage.py (validate ID exists, set completed=True)
- [x] T036 [US2] Add "complete" subcommand to CLI parser in src/cli.py
- [x] T037 [US2] Implement handle_complete(storage, todo_id) function in src/cli.py (validate ID, call storage.complete, format output)
- [x] T038 [US2] Update main.py to route "complete" command in src/main.py
- [x] T039 [US2] Run tests for User Story 2, verify all pass (GREEN phase complete)
- [x] T040 [US2] Refactor User Story 2 code while keeping tests green

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Delete Todos (Priority: P3)

**Goal**: Enable users to delete todo items to keep list clean and relevant

**Independent Test**: Add a todo, delete it by ID, list todos to verify it's removed

### Tests for User Story 3 (TDD - Write First, RED Phase)

- [x] T041 [P] [US3] Write test for TodoStorage.delete(id) method in tests/unit/test_storage.py
- [x] T042 [P] [US3] Write test for deleting non-existent todo (NotFoundError) in tests/unit/test_storage.py
- [x] T043 [P] [US3] Write test for ID gaps after deletion (IDs not reused) in tests/unit/test_storage.py
- [x] T044 [P] [US3] Write integration test for "delete" command (valid ID) in tests/integration/test_commands.py
- [x] T045 [P] [US3] Write integration test for "delete" command (invalid ID) in tests/integration/test_commands.py
- [x] T046 [P] [US3] Write integration test for "delete" command (non-numeric ID) in tests/integration/test_commands.py

### Implementation for User Story 3 (GREEN Phase)

- [x] T047 [US3] Implement TodoStorage.delete(id) method in src/storage.py (validate ID exists, delete from dict, do NOT decrement next_id)
- [x] T048 [US3] Add "delete" subcommand to CLI parser in src/cli.py
- [x] T049 [US3] Implement handle_delete(storage, todo_id) function in src/cli.py (validate ID, call storage.delete, format output)
- [x] T050 [US3] Update main.py to route "delete" command in src/main.py
- [x] T051 [US3] Run tests for User Story 3, verify all pass (GREEN phase complete)
- [x] T052 [US3] Refactor User Story 3 code while keeping tests green

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality checks

- [x] T053 [P] Add --help/-h flag handling in src/cli.py (display usage information for all commands)
- [x] T054 [P] Add comprehensive docstrings to all modules (src/todo.py, src/storage.py, src/cli.py, src/main.py)
- [x] T055 [P] Create comprehensive error message tests for all edge cases in tests/integration/test_commands.py
- [x] T056 Run full test suite with coverage (pytest --cov=src --cov-report=term-missing --cov-report=html)
- [x] T057 Verify coverage ≥80% overall, 100% on CRUD operations (src/storage.py)
- [x] T058 [P] Run code quality checks (optional: pylint src/, flake8 src/, black --check src/)
- [x] T059 Update README.md with complete usage examples matching quickstart.md
- [x] T060 Final validation: Run through all acceptance scenarios from spec.md manually

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories CAN proceed in parallel (if staffed)
  - OR sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD Red phase)
- TodoItem and exceptions before storage
- Storage before CLI handlers
- CLI handlers before main.py routing
- Implementation before refactoring
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup tasks**: T003, T004 can run in parallel (different files)
- **Foundational tasks**: T005-T008 can run in parallel (different files)
- **User Story 1 tests**: T010-T017 can ALL run in parallel (different test files/functions)
- **User Story 1 models**: T018 can be parallel with T020 (different files)
- **User Story 2 tests**: T029-T034 can ALL run in parallel
- **User Story 3 tests**: T041-T046 can ALL run in parallel
- **Polish tasks**: T053-T055, T058 can run in parallel (different concerns)
- **Once Foundational complete**: All user stories (P1, P2, P3) can start in parallel if team capacity allows

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all test writing tasks for User Story 1 together (TDD RED phase):
Task T010: "Write test for TodoItem creation with valid title"
Task T011: "Write test for TodoItem title validation"
Task T012: "Write test for TodoStorage add operation"
Task T013: "Write test for TodoStorage list_all operation"
Task T014: "Write test for sequential ID generation"
Task T015: "Write integration test for add command"
Task T016: "Write integration test for list command (with todos)"
Task T017: "Write integration test for list command (empty)"

# All 8 test tasks can be written simultaneously in different test files
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009) - CRITICAL blocker
3. Complete Phase 3: User Story 1 (T010-T028)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready - you have a working todo CLI!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T010-T028) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (T029-T040) → Test independently → Deploy/Demo
4. Add User Story 3 (T041-T052) → Test independently → Deploy/Demo
5. Polish (T053-T060) → Final quality checks → Production-ready
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T009)
2. Once Foundational is done:
   - Developer A: User Story 1 (T010-T028)
   - Developer B: User Story 2 (T029-T040)
   - Developer C: User Story 3 (T041-T052)
3. Stories complete and integrate independently
4. Team completes Polish together (T053-T060)

---

## TDD Workflow (Constitution Requirement)

For each user story phase:

1. **RED Phase**: Write all tests first (tasks marked "Write test...")
   - Run tests: `pytest tests/` → Should FAIL (no implementation yet)
   - Verify failures are due to missing implementation, not test errors

2. **GREEN Phase**: Implement minimum code to pass (tasks marked "Implement...")
   - Write code in src/ files
   - Run tests: `pytest tests/` → Should PASS (all green)
   - Do NOT over-engineer or add extra features

3. **REFACTOR Phase**: Improve code quality (tasks marked "Refactor...")
   - Clean up code while keeping tests green
   - Run tests after each refactor: `pytest tests/` → Must stay PASS
   - Improve names, extract functions, remove duplication

4. **VALIDATE Phase**: Confirm story complete (tasks marked "Run tests...")
   - Full test suite passes
   - Coverage meets targets (80% overall, 100% critical)
   - Manual acceptance scenarios from spec.md pass

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests FAIL before implementing (TDD RED phase)
- Verify tests PASS after implementing (TDD GREEN phase)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitution requirement: NO code without tests first (TDD mandatory)

---

## Task Count Summary

- **Total Tasks**: 60
- **Setup (Phase 1)**: 4 tasks
- **Foundational (Phase 2)**: 5 tasks
- **User Story 1 (Phase 3)**: 19 tasks (8 tests, 11 implementation)
- **User Story 2 (Phase 4)**: 12 tasks (6 tests, 6 implementation)
- **User Story 3 (Phase 5)**: 12 tasks (6 tests, 6 implementation)
- **Polish (Phase 6)**: 8 tasks
- **Parallel Opportunities**: 28 tasks marked [P] (47% can run in parallel)
- **MVP Scope**: Phases 1-3 (28 tasks for working todo CLI)
