---
id: 003
title: Todo CLI Core Task Breakdown
stage: tasks
date: 2025-12-24
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-cli-core
branch: 001-todo-cli-core
user: Mohsin Raza
command: /sp.tasks
labels: ["tasks", "tdd", "implementation", "phase-1", "cli"]
links:
  spec: specs/001-todo-cli-core/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-cli-core/tasks.md
tests:
  - TDD approach: 20 test tasks before implementation
---

## Prompt

$ARGUMENTS

## Response snapshot

Generated comprehensive task breakdown for **Todo CLI Core** implementation.

**Tasks File**: `specs/001-todo-cli-core/tasks.md`

### Task Organization

**Total**: 60 tasks across 6 phases
**Parallel Opportunities**: 28 tasks (47%) marked [P]
**MVP Scope**: 28 tasks (Phases 1-3)

### Phase Breakdown

**Phase 1 - Setup** (4 tasks):
- T001-T004: Project structure, dependencies, .gitignore, README

**Phase 2 - Foundational** (5 tasks):
- T005-T009: Module markers, exception classes
- **CRITICAL BLOCKER**: Must complete before user stories

**Phase 3 - User Story 1 (P1): Add and View Todos** (19 tasks):
- **Tests (8 tasks)**: T010-T017 (TodoItem, TodoStorage, CLI integration)
- **Implementation (11 tasks)**: T018-T028 (TodoItem class, TodoStorage, CLI, main.py)
- **MVP Complete**: After T028, app can add and list todos

**Phase 4 - User Story 2 (P2): Mark Complete** (12 tasks):
- **Tests (6 tasks)**: T029-T034 (complete operation, error handling)
- **Implementation (6 tasks)**: T035-T040 (TodoStorage.complete, CLI handler)

**Phase 5 - User Story 3 (P3): Delete Todos** (12 tasks):
- **Tests (6 tasks)**: T041-T046 (delete operation, ID management)
- **Implementation (6 tasks)**: T047-T052 (TodoStorage.delete, CLI handler)

**Phase 6 - Polish** (8 tasks):
- T053-T060: Help text, docstrings, coverage validation, README updates

### TDD Workflow Enforcement

**Constitution Requirement VII**: Test-First Development (NON-NEGOTIABLE)

Each user story follows **Red-Green-Refactor** cycle:

1. **RED Phase**: Write tests first (T010-T017 for US1)
   - Run `pytest` → Tests FAIL (expected)
   - Verify failures are due to missing code, not test errors

2. **GREEN Phase**: Implement minimum code (T018-T026 for US1)
   - Write code to pass tests
   - Run `pytest` → Tests PASS (all green)

3. **REFACTOR Phase**: Clean code (T027-T028 for US1)
   - Improve clarity while tests stay green
   - Run `pytest` after each change → Must stay PASS

### Task Format Validation

✅ **All 60 tasks follow checklist format**:
- Checkbox: `- [ ]`
- Task ID: T001-T060 (sequential)
- [P] marker: 28 tasks (parallel execution)
- [Story] label: US1, US2, US3 (user story mapping)
- File paths: Exact locations specified

**Example**: `- [ ] T018 [P] [US1] Implement TodoItem class (dataclass) in src/todo.py with id, title, completed attributes`

### Dependencies & Execution Strategy

**Sequential Phases**:
1. Setup → Foundational → User Stories → Polish

**Parallel Opportunities**:
- All test tasks within a story can run in parallel
- Setup tasks T003-T004 can run together
- Foundational T005-T008 can run together
- User stories can proceed in parallel with multiple developers

**MVP Path** (Fastest to demo):
1. Setup (4 tasks)
2. Foundational (5 tasks)
3. User Story 1 only (19 tasks)
4. **STOP**: Working todo CLI with add/list (28 tasks total)

**Full Implementation Path**:
1. Phases 1-2 (9 tasks) → Foundation
2. User Story 1 (19 tasks) → MVP
3. User Story 2 (12 tasks) → Complete tracking
4. User Story 3 (12 tasks) → Full CRUD
5. Polish (8 tasks) → Production-ready
6. **Total**: 60 tasks for complete feature

### Test Coverage Targets

**From Constitution**:
- Overall: ≥80%
- Critical paths (CRUD): 100%
- Error handlers: ≥90%

**Test Tasks by Story**:
- US1: 8 test tasks (unit + integration)
- US2: 6 test tasks (complete operation)
- US3: 6 test tasks (delete operation)
- **Total**: 20 test tasks before 40 implementation tasks

### File Structure

**Source Files**:
- `src/exceptions.py` - Custom error classes
- `src/todo.py` - TodoItem entity
- `src/storage.py` - TodoStorage CRUD
- `src/cli.py` - CLI parsing and handlers
- `src/main.py` - Entry point

**Test Files**:
- `tests/unit/test_todo.py` - TodoItem tests
- `tests/unit/test_storage.py` - Storage tests
- `tests/unit/test_cli.py` - CLI tests
- `tests/integration/test_commands.py` - End-to-end tests

### Ready for Implementation

**Next Command**: `/sp.implement`

The implementation will:
1. Check all checklists complete (or ask to proceed)
2. Execute tasks in dependency order
3. Follow TDD cycle (RED → GREEN → REFACTOR)
4. Mark tasks complete in tasks.md
5. Validate quality gates

## Outcome

- ✅ Impact: Complete task breakdown with TDD workflow, 60 tasks organized by user story
- 🧪 Tests: 20 test tasks (RED phase) before 40 implementation tasks (GREEN/REFACTOR)
- 📁 Files: Created tasks.md (60 tasks, 400+ lines)
- 🔁 Next prompts: /sp.implement to execute tasks following TDD cycle
- 🧠 Reflection: Task breakdown enforces constitution TDD requirement - all tests written before implementation. Three independent user stories (P1-P3) enable incremental delivery. MVP achievable with just 28 tasks (Phases 1-3). 47% of tasks parallelizable. Clear Red-Green-Refactor cycle defined for each story.

## Evaluation notes (flywheel)

- Failure modes observed: None - tasks generated with proper TDD workflow and checklist format
- Graders run and results (PASS/FAIL): PASS - All 60 tasks follow checkbox format, TDD enforced, dependencies clear
- Prompt variant (if applicable): Empty input - tasks generated from spec.md user stories + plan.md architecture
- Next experiment (smallest change to try): Execute /sp.implement and validate TDD workflow is followed (tests fail RED, then pass GREEN)
