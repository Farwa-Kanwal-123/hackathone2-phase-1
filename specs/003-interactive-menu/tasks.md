---
description: "Task breakdown for interactive menu feature implementation"
---

# Tasks: Interactive Menu-Based Todo Console

**Input**: Design documents from `/specs/003-interactive-menu/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/menu-interface.md, quickstart.md

**Tests**: TDD workflow enforced - tests written FIRST (RED phase) before implementation (GREEN phase)

**Organization**: Tasks follow TDD cycle (RED → GREEN → REFACTOR) and are organized by user story priority (P1 → P2 → P3)

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, etc.)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `main.py` at repository root, `src/`, `tests/` subdirectories
- All paths are absolute from repository root

---

## Phase 1: Setup (3 tasks)

**Purpose**: Initialize uv project configuration and create stub files for interactive menu

**Status**: Prerequisites - must complete before any user story implementation

- [X] T001 Create pyproject.toml for uv configuration at repository root
- [X] T002 [P] Create main.py stub at repository root with basic imports
- [X] T003 [P] Create src/interactive_menu.py stub with module docstring

**Checkpoint Setup**: Repository structure ready for TDD workflow

---

## Phase 2: Foundational (0 tasks)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**Status**: ✅ COMPLETE - All foundational components exist from Phase 1
- Storage layer: TodoStorage (in-memory dict) ✅
- Entity layer: TodoItem with validation ✅
- CLI handlers: handle_add, handle_list, handle_complete, handle_update, handle_delete ✅
- Exception handling: ValidationError, NotFoundError ✅
- Testing framework: pytest configured ✅

**⚠️ CRITICAL**: Foundation complete - User Story implementation can begin immediately after Setup phase

**Checkpoint**: Foundation ready - proceed to User Story 1

---

## Phase 3: User Story 1 - Interactive Menu Navigation (Priority: P1) 🎯 MVP

**Goal**: Display menu with numbered options, accept user choice, dispatch to appropriate handler, loop after completion

**Independent Test**: Start application with `uv run main.py`, verify menu displays, select option, confirm action executes, verify return to menu

**Acceptance Scenarios**:
1. App launch → welcome message + menu with 6 numbered options
2. Valid menu choice → corresponding action executes
3. Action completion → automatic return to menu
4. Exit choice → graceful termination with goodbye message

### RED Phase: Write Failing Tests (MUST complete BEFORE GREEN phase)

**Purpose**: Write tests that define expected behavior - all tests MUST FAIL initially

- [X] T004 [P] [US1] Write unit test for display_menu() output format in tests/unit/test_menu.py
- [X] T005 [P] [US1] Write unit test for get_menu_choice() with valid input (1-6) in tests/unit/test_menu.py
- [X] T006 [P] [US1] Write unit test for get_menu_choice() with invalid input (0, 7, "abc") in tests/unit/test_menu.py
- [X] T007 [P] [US1] Write integration test for menu loop workflow in tests/integration/test_interactive.py
- [X] T008 [P] [US1] Write integration test for exit workflow (option 6) in tests/integration/test_interactive.py
- [X] T009 [P] [US1] Write integration test for Ctrl+C exit handling in tests/integration/test_interactive.py

**Checkpoint RED**: Run pytest - all new tests MUST FAIL (menu functions not yet implemented)

---

### GREEN Phase: Implement Minimum Code (Make tests PASS)

**Purpose**: Write minimum code to make failing tests pass - no more, no less

- [X] T010 [US1] Implement display_menu() function in src/interactive_menu.py
- [X] T011 [US1] Implement get_menu_choice() function with input validation in src/interactive_menu.py
- [X] T012 [US1] Implement main menu loop in main.py with welcome/goodbye messages
- [X] T013 [US1] Implement menu dispatch logic (route choice to handlers) in main.py
- [X] T014 [US1] Implement Ctrl+C exception handling in main.py

**Checkpoint GREEN**: Run pytest - all tests (new + existing 63 tests from Phase 1) MUST PASS

---

### REFACTOR Phase: Improve Code Quality

**Purpose**: Improve code quality while keeping all tests passing

- [X] T015 [P] [US1] Review and improve error messages for invalid menu choices in src/interactive_menu.py
- [X] T016 [P] [US1] Add input sanitization (strip whitespace) to get_menu_choice() in src/interactive_menu.py
- [X] T017 [US1] Run full Phase 1 test suite (63 tests) to verify no regressions

**Checkpoint REFACTOR**: All tests still passing, code quality improved

---

**Checkpoint US1**: At this point, User Story 1 should be fully functional - menu displays, accepts input, loops correctly

---

## Phase 4: User Story 2 - Add Todo via Interactive Prompt (Priority: P1) 🎯 MVP

**Goal**: Prompt user for todo title interactively, validate input, call existing handle_add(), display confirmation

**Independent Test**: Select "Add todo" from menu, enter title when prompted, verify todo created and confirmation displayed

**Acceptance Scenarios**:
1. Select "Add" → prompt for title → create todo on Enter
2. Valid title → confirmation with ID and title
3. Empty title → error message + re-prompt
4. Success → return to menu

### RED Phase: Write Failing Tests

- [ ] T018 [P] [US2] Write unit test for prompt_for_input() basic functionality in tests/unit/test_menu.py
- [ ] T019 [P] [US2] Write unit test for prompt_for_input() empty input handling in tests/unit/test_menu.py
- [ ] T020 [P] [US2] Write unit test for interactive_add() function in tests/unit/test_menu.py
- [ ] T021 [P] [US2] Write integration test for add workflow (menu → prompt → add → menu) in tests/integration/test_interactive.py
- [ ] T022 [P] [US2] Write integration test for add with empty title error in tests/integration/test_interactive.py

**Checkpoint RED**: All User Story 2 tests fail (prompt and interactive_add not implemented)

---

### GREEN Phase: Implement Minimum Code

- [ ] T023 [US2] Implement prompt_for_input() function in src/interactive_menu.py
- [ ] T024 [US2] Implement interactive_add() function wrapping handle_add() in src/interactive_menu.py
- [ ] T025 [US2] Integrate interactive_add() into main menu dispatch in main.py

**Checkpoint GREEN**: User Story 2 tests pass, todos can be added interactively

---

### REFACTOR Phase: Improve Code Quality

- [ ] T026 [P] [US2] Improve error messages for empty title validation in src/interactive_menu.py
- [ ] T027 [P] [US2] Add whitespace stripping to prompt_for_input() in src/interactive_menu.py

**Checkpoint REFACTOR**: Add functionality polished, tests passing

---

**Checkpoint US2**: Add todo workflow complete and tested independently

---

## Phase 5: User Story 3 - View Todo List from Menu (Priority: P1) 🎯 MVP

**Goal**: Call existing handle_list(), display formatted todo list, handle empty list case

**Independent Test**: Add todos, select "List" from menu, verify all todos displayed with IDs/status/titles

**Acceptance Scenarios**:
1. Todos exist → display all with ID, status `[x]` or `[ ]`, title
2. No todos → friendly message "No todos found. Start by adding one!"
3. Mixed completed/incomplete → correct status markers
4. Display complete → return to menu

### RED Phase: Write Failing Tests

- [ ] T028 [P] [US3] Write unit test for interactive_list() function in tests/unit/test_menu.py
- [ ] T029 [P] [US3] Write integration test for list workflow with todos in tests/integration/test_interactive.py
- [ ] T030 [P] [US3] Write integration test for list workflow with empty list in tests/integration/test_interactive.py

**Checkpoint RED**: User Story 3 tests fail (interactive_list not implemented)

---

### GREEN Phase: Implement Minimum Code

- [ ] T031 [US3] Implement interactive_list() function wrapping handle_list() in src/interactive_menu.py
- [ ] T032 [US3] Integrate interactive_list() into main menu dispatch in main.py

**Checkpoint GREEN**: User Story 3 tests pass, todos can be listed interactively

---

**Checkpoint US3**: List todo workflow complete - MVP FUNCTIONAL (menu + add + list)

---

## Phase 6: User Story 4 - Complete Todo via Interactive Selection (Priority: P2)

**Goal**: Prompt for todo ID, validate numeric input, call handle_complete(), display confirmation

**Independent Test**: Add todo, select "Complete" from menu, enter ID, verify todo marked complete

**Acceptance Scenarios**:
1. Select "Complete" → prompt for ID → mark complete on valid ID
2. Valid ID → confirmation + todo marked `[x]`
3. Invalid ID → error message + re-prompt or return to menu
4. Success → return to menu

### RED Phase: Write Failing Tests

- [ ] T033 [P] [US4] Write unit test for prompt_for_id() numeric validation in tests/unit/test_menu.py
- [ ] T034 [P] [US4] Write unit test for interactive_complete() function in tests/unit/test_menu.py
- [ ] T035 [P] [US4] Write integration test for complete workflow in tests/integration/test_interactive.py
- [ ] T036 [P] [US4] Write integration test for complete with invalid ID in tests/integration/test_interactive.py

**Checkpoint RED**: User Story 4 tests fail (prompt_for_id and interactive_complete not implemented)

---

### GREEN Phase: Implement Minimum Code

- [ ] T037 [US4] Implement prompt_for_id() function with numeric validation in src/interactive_menu.py
- [ ] T038 [US4] Implement interactive_complete() function wrapping handle_complete() in src/interactive_menu.py
- [ ] T039 [US4] Integrate interactive_complete() into main menu dispatch in main.py

**Checkpoint GREEN**: User Story 4 tests pass, todos can be completed interactively

---

**Checkpoint US4**: Complete todo workflow functional and tested

---

## Phase 7: User Story 5 - Update Todo Title Interactively (Priority: P2)

**Goal**: Prompt for ID, prompt for new title, call handle_update(), display confirmation showing old → new

**Independent Test**: Add todo with typo, select "Update", enter ID and corrected title, verify change persists

**Acceptance Scenarios**:
1. Select "Update" → prompt for ID → prompt for new title → update
2. Valid ID + title → confirmation showing old → new title
3. Invalid ID or empty title → error message
4. Success → return to menu

### RED Phase: Write Failing Tests

- [ ] T040 [P] [US5] Write unit test for interactive_update() function in tests/unit/test_menu.py
- [ ] T041 [P] [US5] Write integration test for update workflow in tests/integration/test_interactive.py
- [ ] T042 [P] [US5] Write integration test for update with invalid ID in tests/integration/test_interactive.py
- [ ] T043 [P] [US5] Write integration test for update with empty title in tests/integration/test_interactive.py

**Checkpoint RED**: User Story 5 tests fail (interactive_update not implemented)

---

### GREEN Phase: Implement Minimum Code

- [ ] T044 [US5] Implement interactive_update() function wrapping handle_update() in src/interactive_menu.py
- [ ] T045 [US5] Integrate interactive_update() into main menu dispatch in main.py

**Checkpoint GREEN**: User Story 5 tests pass, todos can be updated interactively

---

**Checkpoint US5**: Update todo workflow functional and tested

---

## Phase 8: User Story 6 - Delete Todo Interactively (Priority: P3)

**Goal**: Prompt for ID, call handle_delete(), display confirmation

**Independent Test**: Add todo, select "Delete", enter ID, verify todo removed from list

**Acceptance Scenarios**:
1. Select "Delete" → prompt for ID → delete todo
2. Valid ID → confirmation message + todo removed
3. Invalid ID → error message + return to menu
4. Success → return to menu

### RED Phase: Write Failing Tests

- [ ] T046 [P] [US6] Write unit test for interactive_delete() function in tests/unit/test_menu.py
- [ ] T047 [P] [US6] Write integration test for delete workflow in tests/integration/test_interactive.py
- [ ] T048 [P] [US6] Write integration test for delete with invalid ID in tests/integration/test_interactive.py

**Checkpoint RED**: User Story 6 tests fail (interactive_delete not implemented)

---

### GREEN Phase: Implement Minimum Code

- [ ] T049 [US6] Implement interactive_delete() function wrapping handle_delete() in src/interactive_menu.py
- [ ] T050 [US6] Integrate interactive_delete() into main menu dispatch in main.py

**Checkpoint GREEN**: User Story 6 tests pass, todos can be deleted interactively

---

**Checkpoint US6**: Delete todo workflow functional and tested - ALL USER STORIES COMPLETE

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and validation across the feature

- [ ] T051 [P] Add comprehensive edge case tests (long titles, special chars, repeated invalid input) in tests/integration/test_interactive.py
- [ ] T052 [P] Update README.md with interactive menu launch instructions and examples
- [ ] T053 Run coverage report and verify 80% overall, 100% on src/interactive_menu.py
- [ ] T054 Validate all acceptance scenarios from spec.md manually with `uv run main.py`
- [ ] T055 Run quickstart.md validation (test all workflows work as documented)
- [ ] T056 Verify backward compatibility (existing CLI `python -m src.main` still works)

**Checkpoint FINAL**: Feature complete, all tests passing, documentation updated, backward compatible

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies (start here)
- **Foundational (Phase 2)**: ✅ COMPLETE (no tasks) - Phase 1 provides foundation
- **User Story 1-3 (P1 - Phases 3-5)**: Can start after Setup (Phase 1)
  - US1 (Menu Navigation): No dependencies beyond Setup
  - US2 (Add Todo): Depends on US1 (needs menu dispatch)
  - US3 (List Todos): Depends on US1 (needs menu dispatch)
- **User Story 4-5 (P2 - Phases 6-7)**: Can start after P1 stories
  - US4 (Complete): Depends on US1, US2 (needs todos to complete)
  - US5 (Update): Depends on US1, US2 (needs todos to update)
- **User Story 6 (P3 - Phase 8)**: Can start after P1 stories
  - US6 (Delete): Depends on US1, US2 (needs todos to delete)
- **Polish (Phase 9)**: Depends on all user stories completion

### User Story Dependencies

**P1 Stories (MVP - Must ship together)**:
- **User Story 1 (Menu Navigation)**: No dependencies - foundational
- **User Story 2 (Add Todo)**: Depends on US1 menu infrastructure
- **User Story 3 (List Todos)**: Depends on US1 menu infrastructure

**P2 Stories (Enhancement)**:
- **User Story 4 (Complete)**: Depends on US1 (menu), US2 (needs todos)
- **User Story 5 (Update)**: Depends on US1 (menu), US2 (needs todos)

**P3 Stories (Nice-to-have)**:
- **User Story 6 (Delete)**: Depends on US1 (menu), US2 (needs todos)

### Within User Stories: TDD Cycle

**CRITICAL ORDER for each story**:
1. **RED Phase**: Write ALL tests first (all [P] tests can run in parallel)
   - ALL tests MUST FAIL before proceeding to GREEN
2. **GREEN Phase**: Implement code to make tests pass
   - Limited parallelism (some tasks depend on prior completion)
3. **REFACTOR Phase** (if present): Improve quality without breaking tests
   - All refactor tasks can run in parallel

### Parallel Opportunities

**Setup Phase** - Limited parallelism:
- T001 must complete first (pyproject.toml needed for context)
- T002 and T003 can run in parallel after T001

**User Story RED Phases** - High parallelism:
- All test files can be written in parallel within each story
- Example US1 RED: T004, T005, T006, T007, T008, T009 (6 parallel tasks)

**User Story GREEN Phases** - Sequential execution:
- Must implement functions before integrating into main.py
- Example US2 GREEN: T023 → T024 → T025 (sequential)

**User Story REFACTOR Phases** - High parallelism:
- All improvements can run in parallel
- Example US1 REFACTOR: T015, T016 (2 parallel), then T017 (validation)

**Polish Phase** - High parallelism:
- T051, T052 can run in parallel
- T053, T054, T055, T056 sequential (validation after changes)

---

## Parallel Example: User Story 1 RED Phase

```bash
# Launch all US1 tests together:
Task T004: "Write unit test for display_menu()"
Task T005: "Write unit test for get_menu_choice() valid input"
Task T006: "Write unit test for get_menu_choice() invalid input"
Task T007: "Write integration test for menu loop workflow"
Task T008: "Write integration test for exit workflow"
Task T009: "Write integration test for Ctrl+C handling"
```

**Result**: 6 tests written in parallel, all FAIL (menu functions not yet implemented)

---

## Implementation Strategy

### TDD Workflow (Recommended)

1. **Setup Phase (T001-T003)**:
   - Create pyproject.toml and stub files
   - Verify `uv run main.py` can execute (even with empty implementation)

2. **MVP: P1 Stories First (US1, US2, US3)**:
   - US1 RED → US1 GREEN → US1 REFACTOR
   - US2 RED → US2 GREEN → US2 REFACTOR
   - US3 RED → US3 GREEN
   - **Result**: Functional interactive menu with add and list operations

3. **Enhancement: P2 Stories (US4, US5)**:
   - US4 RED → US4 GREEN
   - US5 RED → US5 GREEN
   - **Result**: Complete workflow (add, list, complete, update)

4. **Nice-to-have: P3 Story (US6)**:
   - US6 RED → US6 GREEN
   - **Result**: Full feature set (including delete)

5. **Polish Phase (T051-T056)**:
   - Add edge cases
   - Update documentation
   - Final validation

**Total Tasks**: 56 tasks
- Setup: 3 tasks
- RED: 27 tests (9 + 5 + 3 + 4 + 4 + 3 across 6 user stories)
- GREEN: 17 implementation tasks
- REFACTOR: 3 tasks
- Polish: 6 tasks

### MVP Delivery

**MVP = User Stories 1-3 Complete (P1 Stories)**
- After T017 (US1 complete), T027 (US2 complete), T032 (US3 complete)
- Menu navigation + add + list = complete interactive experience
- Can be deployed independently for user feedback

### Incremental Validation Points

1. **After T003 (Setup complete)**: `uv run main.py` executes without errors
2. **After T017 (US1 complete)**: Menu displays and navigation works
3. **After T027 (US2 complete)**: Can add todos interactively
4. **After T032 (US3 complete)**: MVP functional - add + list workflows work
5. **After T039 (US4 complete)**: Complete operation added
6. **After T045 (US5 complete)**: Update operation added
7. **After T050 (US6 complete)**: Full feature set implemented
8. **After T056 (Polish complete)**: Feature production-ready with docs

---

## Success Criteria Validation

**After T056 (All Tasks Complete)**:

- ✅ **SC-001**: Launch in <5 seconds via `uv run main.py` (validated in T054)
- ✅ **SC-002**: Add-list-complete workflow <30 seconds (validated in T054)
- ✅ **SC-003**: 95% first-attempt success rate (validated via clear prompts and error messages)
- ✅ **SC-004**: Zero crashes during normal operation (validated in all integration tests)
- ✅ **SC-005**: Clear error messages (validated in T026, T015)
- ✅ **SC-006**: No command memorization needed (menu-driven interface)

**Technical Metrics**:
- ✅ Test coverage: 80% overall, 100% on src/interactive_menu.py (T053)
- ✅ All tests passing: 63 existing + new tests (validated throughout)
- ✅ No Phase 1 constraint violations (CLI-only, in-memory, Python stdlib)
- ✅ Zero new runtime dependencies (uv is dev/build tool only)
- ✅ Backward compatibility preserved (T056)

---

## Notes

- **TDD CRITICAL**: RED → GREEN → REFACTOR cycle MUST be followed for each user story
- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] labels**: US1-US6 map to User Stories 1-6 from spec.md
- **Test-First**: All tests MUST be written and FAIL before implementation
- **No Entity Changes**: Reuses existing TodoItem, TodoStorage, CLI handlers (no modifications)
- **Minimal Code**: Interactive menu is thin wrapper around existing validated logic
- **uv Tooling**: pyproject.toml is configuration only, no runtime dependency
- **Commit After Each User Story**: US1 complete → commit, US2 complete → commit, etc.
- **Stop at Checkpoints**: Validate independently before proceeding to next user story
- **Avoid**: Breaking existing CLI functionality, duplicating validation logic, overengineering prompts
