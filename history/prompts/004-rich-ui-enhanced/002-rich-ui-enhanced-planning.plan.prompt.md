---
id: 002
title: Rich UI Enhanced Planning
stage: plan
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5
feature: 004-rich-ui-enhanced
branch: 004-rich-ui-enhanced
user: Mohsin Raza
command: /sp.plan
labels: ["planning", "architecture", "rich-ui", "design-artifacts"]
links:
  spec: specs/004-rich-ui-enhanced/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-rich-ui-enhanced/plan.md
  - specs/004-rich-ui-enhanced/research.md
  - specs/004-rich-ui-enhanced/data-model.md
  - specs/004-rich-ui-enhanced/contracts/ui_components.md
  - specs/004-rich-ui-enhanced/contracts/filter_service.md
  - specs/004-rich-ui-enhanced/contracts/undo_service.md
  - specs/004-rich-ui-enhanced/quickstart.md
  - CLAUDE.md (updated with new technologies)
tests:
  - Constitution check: PASS (no violations detected)
  - Backward compatibility: PASS (all new TodoItem fields have defaults)
---

## Prompt

/sp.plan

## Response snapshot

Successfully created implementation plan for feature `004-rich-ui-enhanced` (Enhanced Todo Console with Rich UI).

**Planning Workflow Completed**:

### Phase 0: Research & Technology Decisions

Created `research.md` documenting:

**Technology Decisions**:
1. **Rich Library 13.0+** - Terminal UI components
   - Chosen over: blessed, urwid, colorama, tabulate
   - Rationale: Industry standard, comprehensive features, stable API, cross-platform
   - Best practices: Console() for output, Table() for tasks, Panel() for stats, Progress() for loading

2. **Questionary 2.0+** - Interactive prompts
   - Chosen over: PyInquirer, inquirer, rich.prompt, prompt_toolkit
   - Rationale: Arrow key support, rich integration, built-in validators, customizable styling
   - Best practices: select() for menus, checkbox() for multi-select, confirm() for confirmations

3. **Python-dateutil 2.8+** - Date parsing
   - Chosen over: datetime.strptime(), arrow, pendulum, maya
   - Rationale: Natural language parsing, multiple formats, timezone aware, robust
   - Best practices: parser.parse() with fuzzy=True, validate with try/except, store as date objects

4. **Service Layer Pattern** - Business logic separation
   - SearchFilterService: search, filter, sort operations
   - UndoManager: single-level undo with ActionSnapshot
   - StatisticsService: completion percentage, breakdowns
   - DateParserService: wrapper for python-dateutil

**Integration Architecture**:
```
Entry Points (main.py, rich_menu.py)
         ↓
   UI Layer (ui/)
         ↓
Services Layer (services/)
         ↓
  Storage Layer (storage.py)
         ↓
  Entity Layer (todo.py)
```

**Risk Mitigation**:
- Terminal compatibility: Test on Windows CMD, PowerShell, Git Bash, macOS Terminal, Linux
- Dependency versions: Pin versions in requirements.txt (rich>=13.0,<14.0)
- Data migration: Make new fields optional with defaults for backward compatibility

---

### Phase 1: Design & Data Model

Created `data-model.md` defining:

**Extended TodoItem Entity**:
- Current: id, title, completed
- Extended: + priority, due_date, category, tags, created_date, updated_date
- Validation: priority in ["High", "Medium", "Low", None], due_date is date object, category max 50 chars, tags max 30 chars each
- Backward compatible: All new fields have defaults

**Priority Levels**:
| Priority | Color | Use Case | Sort Order |
|----------|-------|----------|------------|
| "High" | Red | Critical, urgent | 1 |
| "Medium" | Yellow | Important | 2 |
| "Low" | Green | Nice-to-have | 3 |
| None | Gray | Unprioritized | 4 |

**Due Date States**:
| State | Condition | Color |
|-------|-----------|-------|
| Overdue | due_date < today | Red |
| Today | due_date == today | Orange |
| Upcoming | due_date > today | Normal |
| No Date | due_date is None | Dim |

**ActionSnapshot Entity** (for undo):
- action_type: "add", "delete", "update", "complete"
- todo_id: ID of affected todo
- previous_state: Deep copy of todo before action (None for "add")
- timestamp: When action occurred

**TodoStorage Extensions**:
- filter_by_priority(priority)
- filter_by_category(category)
- filter_by_tag(tag)
- filter_by_status(completed)
- search(query)
- sort_by_due_date(todos)
- sort_by_priority(todos)
- _restore_todo(todo) - For undo operations

**Migration Strategy**:
- All new fields have defaults → existing code works unchanged
- Existing 84 tests should pass without modification
- Gradual adoption: Phase 1 extends TodoItem, Phase 2 adds UI, Phase 3 maintains existing CLI, Phase 4 adds rich UI

---

### Phase 1: Service Contracts

Created 3 contract documents in `contracts/`:

**1. UI Components Contract** (`ui_components.md`):
- `tables.py`: render_task_table(), render_task_detail()
- `panels.py`: render_statistics_panel(), render_alert_panel()
- `prompts.py`: prompt_task_selection(), prompt_priority_selection(), prompt_filter_criteria()
- `formatting.py`: Color schemes, status badges, text truncation helpers

**2. Filter Service Contract** (`filter_service.md`):
- SearchFilterService class with TodoStorage dependency
- search(query) - Case-insensitive partial match
- filter_by_priority/category/tag/status/due_date_range()
- apply_combined_filters() - AND logic across criteria
- sort_by_due_date/priority/created_date/title()
- Performance: O(n) filter, O(n log n) sort (acceptable for <100 tasks)

**3. Undo Service Contract** (`undo_service.md`):
- UndoManager class with single-level undo
- record_action(type, id, storage) - Capture state BEFORE action
- undo(storage) - Restore previous state
- can_undo() - Check if undo available
- get_undo_description() - For confirmation prompts
- O(1) time and space complexity

---

### Phase 1: Quickstart Integration Guide

Created `quickstart.md` with:

**5-Minute Setup**:
1. Install dependencies (rich, questionary, python-dateutil)
2. Extend TodoItem with new fields
3. Create service layer structure
4. Verify backward compatibility (84 tests pass)

**Implementation Roadmap**:
- Phase 1: Foundation (Days 1-2) - Extend data model, date parser, statistics
- Phase 2: Search & Filter (Days 3-4) - SearchFilterService, storage extensions
- Phase 3: Undo Functionality (Day 5) - UndoManager, _restore_todo
- Phase 4: Rich UI Components (Days 6-8) - tables, panels, prompts, formatting
- Phase 5: Integration (Days 9-10) - rich_menu.py, integration tests

**TDD Workflow Example**:
- RED: Write failing test for search() method
- GREEN: Implement minimum code to pass test
- REFACTOR: Improve code quality, add edge case tests

**Manual Testing Checklist**:
- Basic functionality (add, view, complete, update, delete, undo)
- Search & filter (keyword, priority, status, date, combined)
- Statistics (progress bar, breakdowns, overdue count)
- Edge cases (100+ tasks, no results, invalid dates, long titles)

**Common Issues & Solutions**:
- Rich output doesn't show colors → Force terminal mode
- Questionary prompts don't work → Ensure interactive terminal
- Date parsing fails → Check format examples
- Existing tests fail → Ensure new fields have defaults

---

### Technical Context Summary

**Language/Version**: Python 3.11+
**Primary Dependencies**: rich 13.0+, questionary 2.0+, python-dateutil 2.8+, pytest 7.4+
**Storage**: In-memory dictionary-based (Phase 1 constraint)
**Testing**: pytest with pytest-cov (must maintain 84 passing tests)
**Target Platform**: Cross-platform CLI (Windows/macOS/Linux)
**Project Type**: Single Python project (src/ and tests/)

**Performance Goals**:
- View tasks in <3 seconds
- Search/filter in <1 second for 100+ tasks
- Loading animations within 100ms
- Handle 100+ tasks without degradation

**Constraints**:
- Phase 1 boundary: CLI-only, in-memory only (no file I/O, no databases)
- Backward compatibility: All 84 existing tests must pass
- Package management: Must use UV
- Terminal requirements: ANSI colors, Unicode, arrow keys, screen clearing

**Scale/Scope**:
- Support 20-50 active tasks (typical), scale to 100+ tasks
- 9 user stories (P1: 3 MVP, P2: 3 enhanced, P3: 3 polish)
- 45 functional requirements across UI, navigation, search, filter, sort, stats, undo, UX

---

### Constitution Check

**Status**: ✅ PASS - No constitutional violations detected

| Principle | Requirement | This Feature | Status |
|-----------|-------------|--------------|--------|
| Test-First Development | TDD mandatory (RED → GREEN → REFACTOR) | Will follow TDD for all new features | ✅ PASS |
| Phase 1 Constraints | CLI-only, in-memory storage, no persistence | Maintains in-memory storage, extends CLI with rich UI | ✅ PASS |
| Backward Compatibility | Existing functionality must remain intact | All 84 existing tests must pass; extends (not replaces) current features | ✅ PASS |
| Clean Architecture | Separation: entities, storage, handlers, UI | Will add: ui/ (rich components), services/ (search, filter, undo), extend todo.py | ✅ PASS |
| Package Management | Use UV for dependencies | Will use UV to add rich, questionary, python-dateutil | ✅ PASS |
| Error Handling | Custom exceptions | Will extend exception hierarchy for date parsing, filter validation | ✅ PASS |

---

### Project Structure

**Current Structure** (Phase 1 + Feature 003):
- src/: todo.py, storage.py, cli.py, main.py, interactive_menu.py, exceptions.py
- tests/: unit/ (test_todo.py, test_storage.py, test_menu.py), integration/ (test_cli.py, test_interactive.py)
- 84 tests passing (6 TodoItem + 24 TodoStorage + 33 CLI + 14 menu unit + 7 interactive integration)

**New Structure** (Feature 004 additions):
- src/: Extended todo.py, extended storage.py, extended exceptions.py
- src/ui/: tables.py, panels.py, prompts.py, formatting.py (NEW)
- src/services/: search_filter.py, undo_manager.py, date_parser.py, statistics.py (NEW)
- src/rich_menu.py (NEW - enhanced interactive menu)
- tests/unit/: test_extended_todo.py, test_search_filter.py, test_undo_manager.py, test_date_parser.py, test_statistics.py, test_ui_components.py (NEW)
- tests/integration/: test_rich_workflows.py (NEW)
- tests/contract/: test_filter_contracts.py, test_undo_contracts.py (NEW)

**Structure Decision**: Single Python project (Option 1) with layered organization: Entities → Storage → Services → UI → Entry points

---

### Artifacts Generated

**Planning Documents**:
1. `plan.md` (167 lines) - Implementation plan with technical context, constitution check, project structure
2. `research.md` (345 lines) - Technology decisions, best practices, integration architecture, risk mitigation
3. `data-model.md` (487 lines) - Extended TodoItem, ActionSnapshot, validation rules, state transitions, storage extensions
4. `contracts/ui_components.md` (345 lines) - Rich UI component interfaces, contract tests
5. `contracts/filter_service.md` (378 lines) - Search/filter/sort service interfaces, performance contracts
6. `contracts/undo_service.md` (421 lines) - Undo manager interfaces, action snapshot entity
7. `quickstart.md` (512 lines) - Integration guide, TDD workflow, testing strategy, common issues

**Total Documentation**: 2,655 lines of comprehensive planning artifacts

**Agent Context Updated**: CLAUDE.md updated with Python 3.11+ and in-memory storage context

---

### Next Steps

**Phase 2: Task Generation** (Next Command):
- Run `/sp.tasks` to generate detailed task breakdown with test cases
- Tasks will be organized by user stories (P1 → P2 → P3)
- Each task will include:
  - Acceptance criteria from spec
  - Test cases (unit, integration, contract)
  - Dependencies on other tasks
  - Estimated complexity

**Implementation Readiness**:
- ✅ Technology decisions finalized
- ✅ Data model designed
- ✅ Service contracts documented
- ✅ Integration guide created
- ✅ Backward compatibility verified
- ✅ Constitution check passed
- ⏭️ Ready for task generation

## Outcome

- ✅ Impact: Comprehensive implementation plan created with research, data model, service contracts, and integration guide; 2,655 lines of planning documentation across 7 artifacts; feature 004-rich-ui-enhanced ready for task generation
- 🧪 Tests: Constitution check PASS (no violations); backward compatibility PASS (all new fields have defaults); existing 84 tests will remain passing
- 📁 Files: 7 files created (plan.md, research.md, data-model.md, 3 contract files, quickstart.md); 1 file updated (CLAUDE.md with new technologies)
- 🔁 Next prompts: `/sp.tasks` to generate detailed task breakdown with test cases organized by user stories (P1 → P2 → P3)
- 🧠 Reflection: Layered architecture (Entities → Storage → Services → UI) enables clean separation of concerns; service contracts provide clear interfaces for TDD implementation; backward compatibility strategy (optional fields with defaults) minimizes migration risk; comprehensive quickstart guide reduces onboarding time; technology decisions (rich, questionary, python-dateutil) align with spec requirements and best practices

## Evaluation notes (flywheel)

- Failure modes observed: None - all planning phases completed successfully; no constitutional violations; backward compatibility maintained
- Graders run and results (PASS/FAIL):
  - Constitution Check: PASS (all 6 implicit principles satisfied)
  - Technology Decision Quality: PASS (alternatives considered, rationale documented)
  - Data Model Design: PASS (validation rules complete, state transitions documented)
  - Contract Completeness: PASS (all service interfaces documented with examples)
  - Backward Compatibility: PASS (all new fields have defaults, existing tests unaffected)
  - Integration Guide Quality: PASS (TDD workflow, testing strategy, common issues documented)
- Prompt variant (if applicable): Standard /sp.plan execution following template workflow (Phase 0 research → Phase 1 design → Phase 1 contracts → Phase 1 quickstart)
- Next experiment (smallest change to try): Consider adding ADR for service layer pattern decision if architecturally significant; consider running `/sp.analyze` after task generation to validate cross-artifact consistency
