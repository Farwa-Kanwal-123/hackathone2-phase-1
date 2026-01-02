---
id: 002
title: Interactive Menu Planning
stage: plan
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5
feature: 003-interactive-menu
branch: 003-interactive-menu
user: Mohsin Raza
command: /sp.plan
labels: ["planning", "interactive-menu", "architecture", "uv-integration"]
links:
  spec: specs/003-interactive-menu/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-interactive-menu/plan.md
  - specs/003-interactive-menu/data-model.md
  - specs/003-interactive-menu/contracts/menu-interface.md
  - specs/003-interactive-menu/quickstart.md
tests:
  - Constitution check: PASS (all principles compliant)
  - Phase boundaries: PASS (CLI-only, in-memory, no new dependencies)
---

## Prompt

/sp.plan

## Response snapshot

Successfully created implementation plan for `003-interactive-menu` feature - Interactive Menu-Based Todo Console with uv support.

**Plan Summary**:

**Technical Approach**: Create thin interactive presentation layer that wraps existing CLI handlers with menu loop and prompts. Add new `main.py` entry point at repository root for `uv run main.py`, create `interactive_menu.py` module for menu logic, configure `pyproject.toml` for uv support.

**Architecture**:
- **Entry Point**: New `main.py` at root (menu loop)
- **Interactive Layer**: `src/interactive_menu.py` (menu display, prompts, input validation)
- **Existing Layers**: Reuse CLI handlers, storage, entities (NO CHANGES)
- **uv Integration**: `pyproject.toml` configuration (Python 3.11+, no runtime dependencies)

**Key Design Decisions**:

1. **Minimal Changes**: No modifications to existing TodoItem, TodoStorage, or CLI handlers
   - Rationale: Preserve validated logic, maintain backward compatibility
   - Impact: Existing CLI (`python -m src.main`) continues working

2. **Entry Point Strategy**: New `main.py` at root (separate from `src/main.py`)
   - Rationale: Two execution modes - interactive (`uv run main.py`) vs CLI (`python -m src.main`)
   - Impact: Both modes coexist without conflict

3. **Handler Reuse**: Interactive functions wrap existing CLI handlers
   - Rationale: DRY principle, leverage existing validation and error handling
   - Impact: Minimal code duplication, shared business logic

4. **Menu Loop Pattern**: Standard while-True loop with exit condition
   - Rationale: Industry-standard interactive CLI pattern
   - Impact: Predictable control flow, clean exit handling

**Phase 0 - Research**: SKIPPED
- No research needed (standard patterns, no unknowns)
- uv is tooling only (not runtime dependency)

**Phase 1 - Design Artifacts Created**:
1. ✅ `data-model.md`: Confirmed no entity changes, interactive layer documented
2. ✅ `contracts/menu-interface.md`: Menu display format, prompt patterns, error messages specified
3. ✅ `quickstart.md`: Usage examples for all 6 menu workflows, error handling, troubleshooting

**Project Structure**:
- `main.py` (NEW - root entry point)
- `pyproject.toml` (NEW - uv configuration)
- `src/interactive_menu.py` (NEW - menu logic)
- `src/{storage,cli,todo,exceptions,main}.py` (NO CHANGES)
- `tests/unit/test_menu.py` (NEW)
- `tests/integration/test_interactive.py` (NEW)

**TDD Workflow Planned**:
- **RED**: 8-10 tests (menu display, input validation, workflow integration)
- **GREEN**: 5-7 implementation tasks (main.py, interactive_menu.py, uv config)
- **REFACTOR**: 2-3 quality tasks (error handling, input sanitization)
- **Polish**: 3-4 doc/validation tasks

**Estimated Scope**: 20-25 tasks total

**Constitution Compliance**:
✅ All 7 principles checked and passed:
- I. Specification as Source of Truth: Spec exists, all requirements documented
- II. Agents Not Prompts: QA agents ready for validation
- III. Quality Gates Over Speed: TDD enforced, 80% coverage target
- IV. Deterministic Behavior: No randomness, predictable menu flow
- V. Phase 1 Boundaries: CLI-only, in-memory, no databases
- VI. Agent Architecture: Follows existing patterns
- VII. Test-First: RED → GREEN → REFACTOR cycle planned

**Success Metrics**:
- Launch in <5s via `uv run main.py`
- Add-list-complete workflow <30s
- 95% first-attempt success rate
- Zero crashes
- Clear error messages
- No command memorization needed

**Risks Identified & Mitigated**:
1. uv not installed → Document installation, provide fallback
2. Input edge cases (Ctrl+C, EOF) → Comprehensive exception handling
3. Terminal compatibility → Text-only (no ANSI codes)
4. Breaking existing CLI → No changes to src/main.py or handlers

## Outcome

- ✅ Impact: Comprehensive implementation plan created; thin presentation layer minimizes risk; backward compatibility preserved
- 🧪 Tests: TDD workflow planned with 20-25 tasks; unit + integration tests for menu and workflows
- 📁 Files: 4 files created (plan.md, data-model.md, menu-interface.md, quickstart.md)
- 🔁 Next prompts: `/sp.tasks` to generate task breakdown from plan
- 🧠 Reflection: Design emphasizes reuse over rewrite; interactive layer as thin wrapper ensures minimal complexity

## Evaluation notes (flywheel)

- Failure modes observed: None - plan complete with constitutional compliance validated
- Graders run and results (PASS/FAIL):
  - Constitution Check: PASS (all 7 principles compliant)
  - Phase Boundaries: PASS (CLI-only, in-memory, no new runtime deps)
  - Design Quality: PASS (layered architecture, separation of concerns, minimal changes)
  - Backward Compatibility: PASS (existing CLI preserved, no breaking changes)
- Prompt variant (if applicable): Standard /sp.plan execution with existing infrastructure
- Next experiment (smallest change to try): Consider adding confirmation prompt for delete operation in tasks phase
