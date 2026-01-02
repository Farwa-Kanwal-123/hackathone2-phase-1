---
id: 002
title: Todo CLI Core Implementation Plan
stage: plan
date: 2025-12-24
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-cli-core
branch: 001-todo-cli-core
user: Mohsin Raza
command: /sp.plan todo-cli-core
labels: ["planning", "architecture", "phase-1", "cli", "python"]
links:
  spec: specs/001-todo-cli-core/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-cli-core/plan.md
  - specs/001-todo-cli-core/data-model.md
  - specs/001-todo-cli-core/contracts/cli-interface.md
  - specs/001-todo-cli-core/quickstart.md
tests:
  - N/A (planning phase - test strategy defined)
---

## Prompt

todo-cli-core

## Response snapshot

Created comprehensive implementation plan for **Todo CLI Core** feature.

**Plan File**: `specs/001-todo-cli-core/plan.md`

### Planning Summary

**Technical Stack**:
- Language: Python 3.11+
- CLI Framework: argparse (stdlib)
- Storage: In-memory dict
- Testing: pytest with coverage
- Platform: Cross-platform (Windows, macOS, Linux)

**Architecture**:
- `src/todo.py` - TodoItem entity and validation
- `src/storage.py` - In-memory storage (CRUD operations)
- `src/cli.py` - CLI parsing and command routing
- `src/main.py` - Entry point and orchestration

**Constitution Compliance**: ✅ **FULL COMPLIANCE**
- All 7 core principles satisfied
- Zero Phase 1 violations (no databases, no file I/O, no web frameworks)
- Deterministic behavior (sequential IDs, no randomness)
- TDD approach planned (Red-Green-Refactor)
- Quality gates defined (80% coverage, 100% critical paths)

**Phase 0 (Research)**: ✅ SKIPPED
- All technology decisions predetermined by Phase 1 constraints
- Python stdlib provides all necessary functionality
- No external research required

**Phase 1 (Design)**: ✅ COMPLETE

Generated 3 design artifacts:

1. **data-model.md** (16 KB):
   - TodoItem entity: id (int), title (str), completed (bool)
   - TodoStorage: dict[int, TodoItem], next_id counter
   - Validation rules: title 1-200 chars, unique sequential IDs
   - State transitions: pending → completed, any → deleted
   - CRUD operations specified with error handling

2. **contracts/cli-interface.md** (14 KB):
   - 5 commands: add, list, complete, delete, help
   - Exact input/output specifications
   - Error messages for all failure modes
   - Exit codes (0 success, 1 error)
   - Full workflow examples

3. **quickstart.md** (10 KB):
   - 5-minute tutorial for new users
   - Command reference with examples
   - Common workflows (daily tasks, weekly planning)
   - Troubleshooting guide
   - Tips and best practices

**Testing Strategy**:
- Unit tests: TodoItem validation, storage CRUD, CLI parsing
- Integration tests: End-to-end command workflows
- Coverage targets: 80% overall, 100% critical paths, 90% error handlers
- TDD: Write tests first (RED), implement (GREEN), refactor

**Error Handling**:
- Custom exception hierarchy: TodoError → ValidationError, NotFoundError, InvalidInputError
- User-friendly messages (no stack traces)
- Consistent "Error: " prefix format

**Data Model**:
- Sequential ID generation (1, 2, 3...)
- IDs never reused (even after deletion)
- In-memory dict storage (no persistence)
- Title validation (1-200 chars, non-empty, trimmed)

**CLI Interface**:
- `todo add <title>` - Output: "Todo added: {title} (ID: {id})"
- `todo list` - Output: Formatted list with `[ ]` or `[x]` status
- `todo complete <id>` - Output: "Todo #{id} marked as complete"
- `todo delete <id>` - Output: "Todo #{id} deleted"
- `todo --help` - Output: Usage information

### Constitution Re-Check (Post-Design)

✅ **Phase 1 Scope**: Only argparse and dict used (allowed)
✅ **Deterministic**: Sequential IDs, consistent output format
✅ **Quality Gates**: TDD strategy defined, coverage targets set
✅ **No Violations**: Zero prohibited technologies introduced

### Next Steps

**Ready for**: `/sp.tasks` to generate implementation tasks

The `/sp.tasks` command will:
1. Read plan.md and spec.md
2. Break down into specific testable tasks
3. Assign task IDs and priorities
4. Define acceptance criteria per task
5. Organize by user story (P1, P2, P3)

## Outcome

- ✅ Impact: Complete implementation plan with full constitution compliance, zero violations
- 🧪 Tests: Test strategy defined (TDD, 80% coverage, unit + integration tests)
- 📁 Files: Created plan.md, data-model.md, contracts/cli-interface.md, quickstart.md (4 files, ~40 KB)
- 🔁 Next prompts: /sp.tasks to generate implementation task breakdown
- 🧠 Reflection: Planning phase demonstrates Phase 1 discipline - all technology choices predetermined by constitution (argparse, dict, pytest). No research needed. Design artifacts provide complete blueprint for implementation. Constitution check passes with zero violations. TDD strategy ensures quality gates enforced. Ready for task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan generated with full constitution compliance
- Graders run and results (PASS/FAIL): PASS - Constitution check shows zero violations, all design artifacts complete
- Prompt variant (if applicable): Minimal input ("todo-cli-core") expanded into full plan with architecture, data model, CLI contracts, and quickstart guide
- Next experiment (smallest change to try): Proceed to /sp.tasks and validate that plan provides sufficient detail for task generation
