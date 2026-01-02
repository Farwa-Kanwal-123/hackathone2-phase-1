---
id: 002
title: Update Todo Planning Complete
stage: plan
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5
feature: 002-update-todo
branch: 002-update-todo
user: Mohsin Raza
command: /sp.plan
labels: ["planning", "update-todo", "architecture", "phase-1-extension"]
links:
  spec: specs/002-update-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-update-todo/plan.md
  - specs/002-update-todo/data-model.md
  - specs/002-update-todo/contracts/cli-interface.md
  - specs/002-update-todo/quickstart.md
tests:
  - N/A (planning phase - tests will be defined in tasks)
---

## Prompt

/sp.plan

## Response snapshot

Created comprehensive implementation plan and Phase 1 design artifacts for **Update Todo Titles** feature.

### Planning Summary

**Branch**: `002-update-todo`
**Stage**: Planning complete, ready for `/sp.tasks`

---

### Implementation Plan Created

**File**: `specs/002-update-todo/plan.md` (370 lines)

**Key Sections**:

1. **Summary**:
   - Add ability to update/edit existing todo titles via CLI command
   - Extends Phase 1 with `update` command
   - Follows established TDD patterns

2. **Technical Context**:
   - Language: Python 3.11+
   - Dependencies: Python stdlib, pytest 7.4.0+
   - Storage: In-memory dict (Phase 1 constraint)
   - Testing: TDD workflow (RED → GREEN → REFACTOR)

3. **Constitution Check**: ✅ PASS (both pre-design and post-design)
   - All 7 constitutional principles validated
   - No Phase 1 constraint violations
   - Quality gates defined (80% coverage, 100% on CRUD)

4. **Architecture**:
   - Layered design preserved (CLI → Storage → Entity)
   - Component responsibilities defined
   - Data flow documented with visual diagram

5. **Implementation Approach**:
   - Phase 0: No research needed (extends existing patterns)
   - Phase 1: Design artifacts (completed)
   - TDD workflow: RED → GREEN → REFACTOR

6. **Estimated Scope**: 10-15 tasks
   - Tests (RED): 4-6 tasks
   - Implementation (GREEN): 4-5 tasks
   - Refactor: 1-2 tasks
   - Polish: 1-2 tasks

---

### Phase 1 Design Artifacts Created

**1. data-model.md** (267 lines)

**Purpose**: Specifies data model changes for update operation

**Key Content**:
- **TodoItem**: No changes (reuses existing validation)
- **TodoStorage.update() Method** (NEW):
  ```python
  def update(self, todo_id: int, new_title: str) -> TodoItem:
      """Update the title of an existing todo."""
  ```
- **Implementation Strategy**:
  1. Check if todo_id exists (raise NotFoundError if not)
  2. Retrieve existing TodoItem
  3. Create new TodoItem with same ID, new title, same status
  4. Replace old TodoItem in storage
  5. Return updated TodoItem
- **Data Flow Diagram**: Visual representation of update operation
- **State Transitions**: Documented for all scenarios (incomplete, completed, errors)
- **Invariants**: ID immutability, status preservation, validation consistency, atomicity, determinism
- **Testing Considerations**: Unit tests (happy path, errors, edge cases), integration tests (CLI command, error messages)

**2. contracts/cli-interface.md** (337 lines)

**Purpose**: Specifies CLI command contract for update operation

**Key Content**:
- **Command Syntax**: `python -m src.main update <id> <new-title>`
- **Argument Specifications**:
  - `<id>`: Integer, required, must exist
  - `<new-title>`: String, 1-200 chars, not empty
- **Success Output Format**:
  ```
  Updated: '<old-title>' → '<new-title>' (ID: <id>)
  ```
- **Error Outputs**: 4 error types documented with examples
  1. Todo not found
  2. Empty/whitespace title
  3. Title exceeds 200 chars
  4. Invalid ID format (argparse error)
- **Exit Codes**: 0 (success), 1 (application error), 2 (usage error)
- **Argparse Configuration**: Subcommand definition
- **Help Output**: Command-specific and main help
- **Edge Cases**: Idempotency, duplicate titles, status preservation
- **Integration Workflows**: 2 complete workflow examples

**3. quickstart.md** (460 lines)

**Purpose**: Practical usage guide with examples

**Key Content**:
- **Basic Usage**: Command syntax and example
- **Common Scenarios**: 4 detailed scenarios
  1. Fix a typo
  2. Clarify a task
  3. Update a completed todo
  4. Update multiple todos
- **Error Handling**: 4 error types with examples and solutions
- **Advanced Usage**:
  - Special characters in titles
  - Long titles (within limit)
  - Idempotent updates
  - Duplicate titles
- **Integration Workflows**: 2 complete workflows
  1. Add → Update → Complete → Update
  2. Batch update and reorganize
- **Tips and Best Practices**: 4 practical tips
- **Command Reference**: Full command, arguments, exit codes, help
- **Troubleshooting**: 4 common problems with solutions

---

### Architecture Decisions

**Decision 1: Immutable Update Pattern**

**Choice**: Replace entire TodoItem rather than modifying in place

**Rationale**:
- Reuses existing TodoItem validation (`__post_init__`)
- Maintains immutability principle
- Simplifies error handling (atomic operation)

**Alternatives Considered**:
- Mutate existing TodoItem → rejected (breaks immutability)
- Add update method to TodoItem → rejected (violates single responsibility)

---

**Decision 2: No Research Phase**

**Choice**: Skip Phase 0 research, proceed directly to design

**Rationale**:
- All components exist (storage, CLI, validation)
- Update follows same patterns as complete/delete
- No new dependencies or technologies
- No ambiguities in requirements

**Alternatives Considered**:
- Research validation patterns → not needed (reusing existing)
- Research CLI frameworks → not needed (using argparse)

---

**Decision 3: Validation Reuse**

**Choice**: Leverage TodoItem.__post_init__ validation for updates

**Rationale**:
- Ensures consistency between add and update
- No code duplication
- Single source of truth for validation rules

**Alternatives Considered**:
- Duplicate validation logic → rejected (violates DRY)
- Create separate validator class → rejected (over-engineering)

---

### Files Modified

**Created (4 files)**:
1. `specs/002-update-todo/plan.md` - Implementation plan (370 lines)
2. `specs/002-update-todo/data-model.md` - Data model specification (267 lines)
3. `specs/002-update-todo/contracts/cli-interface.md` - CLI contract (337 lines)
4. `specs/002-update-todo/quickstart.md` - Usage guide (460 lines)

**Updated (1 file)**:
1. `CLAUDE.md` - Agent context updated with technical details

**Total**: 5 files, 1,434 lines of documentation

---

### Constitution Compliance

**Pre-Design Check**: ✅ PASS
- I. Specification is the Source of Truth: ✅
- II. Agents, Not Prompts: ✅
- III. Quality Gates Over Speed: ✅
- IV. Deterministic Behavior: ✅
- V. Phase 1 Scope Boundaries: ✅
- VI. Agent Architecture: ✅
- VII. Test-First Development: ✅

**Post-Design Check**: ✅ PASS
- All design decisions traceable to spec
- TDD workflow defined
- Coverage targets set (80% overall, 100% CRUD)
- No Phase 1 violations

---

### Project Structure After Planning

```text
specs/002-update-todo/
├── spec.md                  # Feature specification (existing)
├── plan.md                  # Implementation plan (NEW)
├── data-model.md            # Entity changes (NEW)
├── quickstart.md            # Usage examples (NEW)
├── contracts/               # CLI contracts (NEW)
│   └── cli-interface.md     # Update command spec (NEW)
└── checklists/              # Quality validation (existing)
    └── requirements.md      # Spec quality checklist (existing)
```

---

### Source Code Impact (Planned)

**Files to Modify** (5 files):
1. `src/storage.py` - Add `update()` method
2. `src/cli.py` - Add `handle_update()` function, update subcommand
3. `src/main.py` - Add routing for update command
4. `tests/unit/test_storage.py` - Add update() method tests
5. `tests/integration/test_commands.py` - Add update command tests

**Files Unchanged** (3 files):
1. `src/todo.py` - TodoItem (no changes)
2. `src/exceptions.py` - Reuse existing exceptions
3. `src/__init__.py` - Package marker

---

### Success Metrics Defined

**From Specification (SC-001 to SC-006)**:
- ✅ Update completes in <5 seconds
- ✅ 100% valid commands succeed
- ✅ Clear error messages
- ✅ Eliminates delete-recreate workaround
- ✅ IDs and status never change
- ✅ Consistent with existing commands

**Technical Metrics**:
- Test coverage: 80% overall, 100% on storage.update()
- All tests passing (TDD workflow)
- No Phase 1 constraint violations
- Zero new dependencies

---

### Risks and Mitigations Identified

**Risk 1**: Inconsistent validation between add and update
- **Mitigation**: Reuse TodoItem.__post_init__ validation
- **Verification**: Integration tests verify same error messages

**Risk 2**: Breaking existing functionality
- **Mitigation**: No changes to existing methods (only additions)
- **Verification**: Run full Phase 1 test suite (49 tests)

**Risk 3**: Poor error messages for update-specific scenarios
- **Mitigation**: Explicitly test error message clarity
- **Verification**: QA agent verifies messages against spec

---

### Next Steps

**Immediate**: Ready for `/sp.tasks` to create task breakdown

**Task Breakdown Will Include**:
- RED Phase: Write failing tests (4-6 tasks)
- GREEN Phase: Implement update functionality (4-5 tasks)
- REFACTOR Phase: Improve code quality (1-2 tasks)
- Polish Phase: Documentation and validation (1-2 tasks)

**Expected Total**: 10-15 tasks

**Implementation Order**:
1. Tests (RED): Write failing tests for storage and CLI
2. Implementation (GREEN): Implement TodoStorage.update() and CLI routing
3. Refactor: Extract common patterns, improve error messages
4. Polish: Update documentation, run full validation

---

### Validation Results

**Planning Quality**:
- ✅ All design decisions traceable to spec requirements
- ✅ Architecture extends Phase 1 without breaking changes
- ✅ TDD workflow defined with clear phases
- ✅ Quality gates established
- ✅ Risks identified with mitigations

**Documentation Quality**:
- ✅ Data model specification complete (267 lines)
- ✅ CLI interface contract complete (337 lines)
- ✅ Quickstart guide complete (460 lines)
- ✅ Implementation plan complete (370 lines)

**Constitution Compliance**:
- ✅ All 7 principles validated (pre-design and post-design)
- ✅ No [NEEDS CLARIFICATION] markers
- ✅ All requirements testable and traceable

**Ready for**: `/sp.tasks` - No planning updates needed

---

### Key Highlights

**Minimal Code Changes**:
- Only 3 source files modified (storage, cli, main)
- No changes to TodoItem or exceptions
- Extends existing architecture without refactoring

**Validation Reuse**:
- Leverages TodoItem.__post_init__ for consistency
- No duplicate validation logic
- Single source of truth

**Clear Error Messages**:
- 4 error types defined with examples
- User-friendly messages documented
- Consistent with existing commands

**Comprehensive Documentation**:
- 1,434 lines of design artifacts
- 4 new documentation files
- Examples for all scenarios

**TDD Ready**:
- Test requirements defined in data-model.md
- Integration test scenarios in cli-interface.md
- Coverage targets established (80%/100%)

## Outcome

- ✅ Impact: Planning complete for update-todo feature with comprehensive design artifacts
- 🧪 Tests: N/A (planning phase - test requirements documented in artifacts)
- 📁 Files: Created 4 files (plan, data-model, cli-interface, quickstart), updated 1 file (agent context)
- 🔁 Next prompts: /sp.tasks to create task breakdown with TDD workflow
- 🧠 Reflection: Planning phase completed successfully with all Phase 1 design artifacts generated. Implementation plan defines architecture (layered design, component responsibilities, data flow), validates constitution compliance (7 principles passed), and documents design decisions (immutable update pattern, validation reuse, no research needed). Data model specifies TodoStorage.update() method with implementation strategy, state transitions, and invariants. CLI interface contract defines command syntax, arguments, output formats, error handling, and edge cases. Quickstart guide provides practical examples for all scenarios. All artifacts traceable to spec requirements. Estimated 10-15 tasks for implementation. No Phase 1 constraint violations. Ready for task breakdown.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully
- Graders run and results (PASS/FAIL): PASS - Constitution check (7/7 principles), Phase 1 design artifacts complete (4/4 files), all requirements traceable to spec
- Prompt variant (if applicable): User ran /sp.plan after completing /sp.specify for update-todo feature
- Next experiment (smallest change to try): Run /sp.tasks to create task breakdown with TDD workflow (RED → GREEN → REFACTOR phases)
