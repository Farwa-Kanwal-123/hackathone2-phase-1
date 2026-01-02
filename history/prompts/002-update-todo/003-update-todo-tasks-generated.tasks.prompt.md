---
id: 003
title: Update Todo Tasks Generated
stage: tasks
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5
feature: 002-update-todo
branch: 002-update-todo
user: Mohsin Raza
command: /sp.tasks update-todo
labels: ["tasks", "update-todo", "tdd", "task-breakdown"]
links:
  spec: specs/002-update-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-update-todo/tasks.md
tests:
  - N/A (task generation phase - tests will be implemented during RED phase)
---

## Prompt

/sp.tasks update-todo

## Response snapshot

Generated comprehensive task breakdown for **Update Todo Titles** feature with TDD workflow (RED → GREEN → REFACTOR).

### Task Generation Summary

**Feature**: `002-update-todo`
**Branch**: `002-update-todo`
**Total Tasks**: 21 tasks

---

### Task Organization

**Phase Structure**:
1. **Phase 1: Setup** - 0 tasks (✅ prerequisites exist from Phase 1)
2. **Phase 2: Foundational** - 0 tasks (✅ foundation exists from Phase 1)
3. **Phase 3: User Story 1 - Edit Todo Title** - 16 tasks (RED → GREEN → REFACTOR)
4. **Phase 4: Polish & Cross-Cutting Concerns** - 5 tasks

**TDD Cycle Breakdown**:
- **RED Phase** (T001-T009): 9 tasks - Write failing tests
- **GREEN Phase** (T010-T013): 4 tasks - Implement minimum code
- **REFACTOR Phase** (T014-T016): 3 tasks - Improve code quality
- **Polish Phase** (T017-T021): 5 tasks - Edge cases and validation

---

### Task Details by Phase

**Phase 1: Setup (0 tasks)**

**Status**: ✅ COMPLETE
- No tasks needed - all prerequisites exist from Phase 1 (60/60 tasks complete)
- TodoStorage, TodoItem, CLI infrastructure, test framework all ready

---

**Phase 2: Foundational (0 tasks)**

**Status**: ✅ COMPLETE
- No tasks needed - foundation exists from Phase 1
- Storage layer, validation, error handling, CLI framework, pytest all configured

**Checkpoint**: Foundation ready - TDD workflow can start immediately

---

**Phase 3: User Story 1 - Edit Todo Title (16 tasks)**

**Goal**: Allow users to update/edit existing todo titles via CLI command

**Independent Test**: Add a todo, edit its title by ID, list todos to verify the title changed while ID and completion status remained the same

**RED Phase: Write Failing Tests (9 tasks)**

All tests marked [P] - can run in parallel:

1. **T001 [P] [US1]**: Write unit test for TodoStorage.update() with valid todo in tests/unit/test_storage.py
2. **T002 [P] [US1]**: Write unit test for TodoStorage.update() with non-existent ID (NotFoundError) in tests/unit/test_storage.py
3. **T003 [P] [US1]**: Write unit test for TodoStorage.update() with empty title (ValidationError) in tests/unit/test_storage.py
4. **T004 [P] [US1]**: Write unit test for TodoStorage.update() with title >200 chars (ValidationError) in tests/unit/test_storage.py
5. **T005 [P] [US1]**: Write unit test for TodoStorage.update() preserves ID and completion status in tests/unit/test_storage.py
6. **T006 [P] [US1]**: Write integration test for successful update command in tests/integration/test_commands.py
7. **T007 [P] [US1]**: Write integration test for update command with non-existent ID in tests/integration/test_commands.py
8. **T008 [P] [US1]**: Write integration test for update command with invalid title in tests/integration/test_commands.py
9. **T009 [P] [US1]**: Write integration test for update command with completed todo (status preservation) in tests/integration/test_commands.py

**Checkpoint RED**: Run pytest - all new tests MUST FAIL (expected behavior not yet implemented)

---

**GREEN Phase: Implement Minimum Code (4 tasks)**

Sequential with some parallelism:

10. **T010 [US1]**: Implement TodoStorage.update() method in src/storage.py
11. **T011 [US1]**: Add update subcommand to CLI argument parser in src/cli.py (can parallel with T010)
12. **T012 [US1]**: Implement handle_update() function in src/cli.py (depends on T010)
13. **T013 [US1]**: Add update command routing in src/main.py (depends on T012)

**Checkpoint GREEN**: Run pytest - all tests (new + existing 49 tests from Phase 1) MUST PASS

---

**REFACTOR Phase: Improve Code Quality (3 tasks)**

All tasks can run in parallel:

14. **T014 [US1]**: Review and improve error messages for clarity in src/cli.py and src/storage.py
15. **T015 [US1]**: Ensure consistency with existing commands (add, complete, delete) in src/cli.py
16. **T016 [US1]**: Run full Phase 1 test suite (49 tests) to verify no regressions

**Checkpoint REFACTOR**: All tests still passing, code quality improved

**Checkpoint US1**: User Story 1 fully functional and testable independently

---

**Phase 4: Polish & Cross-Cutting Concerns (5 tasks)**

17. **T017 [P]**: Add comprehensive edge case tests (idempotency, whitespace-only, boundary) in tests/integration/test_commands.py
18. **T018 [P]**: Update README.md with update command documentation and examples (can parallel with T017)
19. **T019**: Run coverage report and verify 80% overall, 100% on storage.update()
20. **T020**: Validate all acceptance scenarios from spec.md manually
21. **T021**: Run quickstart.md validation (test all examples work as documented)

**Checkpoint FINAL**: Feature complete, all tests passing, documentation updated

---

### Implementation Details

**Files to Modify** (3 source files):
1. `src/storage.py` - Add TodoStorage.update() method
2. `src/cli.py` - Add handle_update() function and update subcommand
3. `src/main.py` - Add update command routing

**Files to Modify** (2 test files):
1. `tests/unit/test_storage.py` - Add TestTodoStorageUpdate class with 5 tests
2. `tests/integration/test_commands.py` - Add TestUpdateCommand class with 4 tests + edge cases

**Files to Update** (1 documentation file):
1. `README.md` - Add update command documentation

**No Changes** (3 files):
1. `src/todo.py` - TodoItem (validation reused)
2. `src/exceptions.py` - Exceptions (reused)
3. `src/__init__.py` - Package marker

---

### Parallel Opportunities Identified

**RED Phase (9 parallel tasks)**:
- All unit tests (T001-T005) can be written in parallel
- All integration tests (T006-T009) can be written in parallel
- Total: 9 tests written simultaneously

**GREEN Phase (2 parallel tasks)**:
- T010 (storage.update()) and T011 (CLI parser) can run in parallel
- T012 depends on T010
- T013 depends on T012

**REFACTOR Phase (3 parallel tasks)**:
- T014, T015, T016 can all run in parallel

**Polish Phase (2 parallel tasks)**:
- T017 (edge case tests) and T018 (README) can run in parallel
- T019, T020, T021 are sequential validation

**Total Parallel Opportunities**: 16 out of 21 tasks can run in parallel within their phases

---

### Dependencies & Execution Order

**Phase Dependencies**:
1. Setup (Phase 1) → ✅ COMPLETE (no tasks)
2. Foundational (Phase 2) → ✅ COMPLETE (no tasks)
3. User Story 1 (Phase 3) → Can start immediately
   - RED (T001-T009) MUST complete before GREEN
   - GREEN (T010-T013) MUST complete before REFACTOR
   - REFACTOR (T014-T016) MUST complete before Polish
4. Polish (Phase 4) → Depends on User Story 1 completion

**Within Each Phase**:
- RED: All tasks independent (9 parallel)
- GREEN: T010 || T011 → T012 → T013
- REFACTOR: All tasks independent (3 parallel)
- Polish: T017 || T018 → T019 → T020 → T021

---

### TDD Workflow Enforcement

**CRITICAL ORDER** (cannot be changed):

1. **RED Phase First**: Write ALL tests (T001-T009)
   - All tests MUST FAIL
   - Do NOT proceed to GREEN until all tests fail correctly
   - Validates test quality (tests catch absence of feature)

2. **GREEN Phase Next**: Implement code (T010-T013)
   - Write minimum code to make tests pass
   - All tests MUST PASS (including 49 existing tests)
   - Validates implementation correctness

3. **REFACTOR Phase Last**: Improve quality (T014-T016)
   - Improve code without breaking tests
   - All tests MUST stay GREEN
   - Validates quality improvements are safe

4. **Polish Phase Final**: Validation (T017-T021)
   - Add edge cases
   - Update documentation
   - Final validation

**Validation Points**:
- After T009: All new tests failing ✅
- After T013: All tests passing (58 total) ✅
- After T016: All tests still passing, code improved ✅
- After T021: Feature production-ready ✅

---

### Implementation Strategy

**MVP First (User Story 1 Only)**:

1. Complete RED Phase (T001-T009) → Tests fail ✅
2. Complete GREEN Phase (T010-T013) → Tests pass ✅
3. Complete REFACTOR Phase (T014-T016) → Quality improved ✅
4. Complete Polish Phase (T017-T021) → Production ready ✅

**Total Tasks**: 21 tasks for complete feature

**No Incremental Delivery** (single user story):
- Feature has only one user story (P1: Edit Todo Title)
- All tasks contribute to single MVP
- MVP = User Story 1 complete = Feature complete

---

### Format Validation

**All Tasks Follow Checklist Format**: ✅ PASS

**Format**: `- [ ] [TaskID] [P?] [Story?] Description with file path`

**Sample Tasks**:
- ✅ `- [ ] T001 [P] [US1] Write unit test for TodoStorage.update() with valid todo in tests/unit/test_storage.py`
- ✅ `- [ ] T010 [US1] Implement TodoStorage.update() method in src/storage.py`
- ✅ `- [ ] T017 [P] Add comprehensive edge case tests (idempotency, whitespace-only, boundary) in tests/integration/test_commands.py`

**Validation**:
- ✅ All tasks have checkbox `- [ ]`
- ✅ All tasks have sequential ID (T001-T021)
- ✅ All parallelizable tasks marked [P]
- ✅ All user story tasks marked [US1]
- ✅ All tasks include file paths
- ✅ All descriptions are specific and actionable

---

### Success Criteria Mapping

**After T021 (All Tasks Complete)**:

- ✅ **SC-001**: Update in <5 seconds (tested in T020)
- ✅ **SC-002**: 100% valid commands succeed (tested T001-T009, validated T020)
- ✅ **SC-003**: Clear error messages (tested T007-T008, improved T014)
- ✅ **SC-004**: Eliminates delete-recreate workaround (feature functional after T013)
- ✅ **SC-005**: IDs and status never change (tested T005, T009)
- ✅ **SC-006**: Consistent with existing commands (ensured T015)

**Technical Metrics** (validated T019):
- ✅ Coverage: 80% overall, 100% on storage.update()
- ✅ All tests passing: 49 existing + 9 new = 58 total
- ✅ No Phase 1 violations: CLI-only, in-memory, Python stdlib
- ✅ Zero new dependencies: Extends existing architecture

---

### Task Count Summary

**Total Tasks**: 21
- **Setup**: 0 tasks (prerequisites exist)
- **Foundational**: 0 tasks (foundation exists)
- **User Story 1**: 16 tasks
  - RED: 9 tasks (all parallel)
  - GREEN: 4 tasks (2 parallel, 2 sequential)
  - REFACTOR: 3 tasks (all parallel)
- **Polish**: 5 tasks (2 parallel, 3 sequential)

**Parallel vs Sequential**:
- Parallel: 16 tasks (76%)
- Sequential: 5 tasks (24%)

**Task Distribution**:
- Testing: 14 tasks (67%) - T001-T009, T017, T019-T021
- Implementation: 4 tasks (19%) - T010-T013
- Quality: 3 tasks (14%) - T014-T016

---

### Key Highlights

**TDD Enforced**:
- RED → GREEN → REFACTOR cycle clearly defined
- Tests written first (9 tests before any implementation)
- Checkpoints at each phase transition

**Minimal Changes**:
- Only 3 source files modified (storage, cli, main)
- No changes to TodoItem or exceptions (reuse existing)
- Extends Phase 1 architecture without refactoring

**Validation Reuse**:
- Leverages TodoItem.__post_init__ for consistency
- No duplicate validation logic
- Single source of truth

**Comprehensive Testing**:
- 9 tests for update functionality
- Unit tests (5) + Integration tests (4)
- Edge cases covered in polish phase

**Clear Dependencies**:
- Phase dependencies explicit (RED before GREEN)
- Task dependencies within phases documented
- Parallel opportunities maximized (16/21 tasks)

**Production Ready**:
- All acceptance scenarios validated (T020)
- Quickstart examples verified (T021)
- Coverage targets enforced (T019)
- Documentation updated (T018)

---

### Files Created

**Generated**:
1. `specs/002-update-todo/tasks.md` - Task breakdown (21 tasks, TDD workflow)

**Total**: 1 file, 550+ lines of task documentation

---

### Next Steps

**Immediate**: Ready for `/sp.implement` to execute tasks

**Implementation Order**:
1. RED Phase (T001-T009): Write all tests, verify failures
2. GREEN Phase (T010-T013): Implement update functionality, verify passes
3. REFACTOR Phase (T014-T016): Improve quality, verify still passes
4. Polish Phase (T017-T021): Edge cases, documentation, validation

**Estimated Execution Time**:
- RED Phase: 30-45 minutes (9 parallel tests)
- GREEN Phase: 20-30 minutes (4 tasks, some sequential)
- REFACTOR Phase: 15-20 minutes (3 parallel tasks)
- Polish Phase: 20-30 minutes (validation and documentation)
- **Total**: ~90-120 minutes for complete feature

**MVP Scope**: All 21 tasks (single user story = complete feature)

## Outcome

- ✅ Impact: Task breakdown complete for update-todo feature with TDD workflow
- 🧪 Tests: 9 tests defined in RED phase (T001-T009), edge cases in polish (T017)
- 📁 Files: Created 1 file (tasks.md with 21 tasks)
- 🔁 Next prompts: /sp.implement to execute RED → GREEN → REFACTOR → Polish workflow
- 🧠 Reflection: Task generation completed successfully with strict TDD workflow enforced. All 21 tasks follow checklist format with proper IDs, labels, and file paths. Tasks organized into RED (9 tests), GREEN (4 implementation), REFACTOR (3 quality), and Polish (5 validation) phases. No setup or foundational tasks needed (extends Phase 1). Parallel opportunities maximized (16/21 tasks can run in parallel within phases). Dependencies clearly documented with checkpoints at each phase transition. All tasks traceable to spec requirements and plan architecture. Format validation passed (checkbox, ID, [P] marker, [US1] label, file paths). Ready for implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - task generation completed successfully
- Graders run and results (PASS/FAIL): PASS - Format validation (21/21 tasks follow checklist format), TDD workflow enforced (RED → GREEN → REFACTOR), all tasks traceable to spec
- Prompt variant (if applicable): User ran /sp.tasks update-todo after completing /sp.plan
- Next experiment (smallest change to try): Run /sp.implement to execute TDD workflow starting with RED phase (write failing tests)
