# Implementation Plan: Enhanced Todo Console with Rich UI

**Branch**: `004-rich-ui-enhanced` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-rich-ui-enhanced/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the existing in-memory todo console app into a visually rich, interactive application using the Rich library for beautiful UI components (tables, progress bars, panels, status badges) and questionary for arrow-key navigation. Extend the TodoItem model to support priority levels, due dates, categories/tags, and implement enhanced features including search, filtering, sorting, statistics dashboard, and undo functionality. Maintain Phase 1 constraints (CLI-only, in-memory storage) while delivering a professional-grade user experience with visual feedback, confirmations, and comprehensive error handling.

## Technical Context

**Language/Version**: Python 3.11+ (existing project requirement)
**Primary Dependencies**:
- **rich 13.0+** - Terminal UI library for tables, progress bars, panels, syntax highlighting, colors
- **questionary 2.0+** - Interactive prompts and arrow-key navigation menus
- **python-dateutil 2.8+** - Flexible date parsing (natural language, multiple formats)
- **pytest 7.4+** - Testing framework (existing)

**Storage**: In-memory dictionary-based (Phase 1 constraint - no persistence, no databases, no file I/O)
**Testing**: pytest with pytest-cov (existing setup, must maintain 84 passing tests)
**Target Platform**: Cross-platform CLI (Windows/macOS/Linux terminals with ANSI color + Unicode support)
**Project Type**: Single Python project with src/ and tests/ structure
**Performance Goals**:
- View tasks in <3 seconds with rich display
- Search/filter response in <1 second for 100+ tasks
- Loading animations display within 100ms
- Handle 100+ tasks without performance degradation

**Constraints**:
- **Phase 1 Boundary**: CLI-only (no GUI, no web), in-memory only (no file I/O, no databases)
- **Backward Compatibility**: Existing 84 tests must continue passing (63 Phase 1 + 21 interactive menu)
- **Package Management**: Must use UV package manager
- **Terminal Requirements**: ANSI colors, Unicode characters, arrow key input, screen clearing capability

**Scale/Scope**:
- Support 20-50 active tasks (typical usage)
- Scale to 100+ tasks without degradation
- 9 user stories (P1: 3 MVP features, P2: 3 enhanced features, P3: 3 polish features)
- 45 functional requirements across UI, navigation, search, filtering, sorting, statistics, undo, UX

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Status**: No formal constitution defined (`.specify/memory/constitution.md` contains template only)

**Implicit Principles** (derived from existing codebase patterns):

| Principle | Requirement | This Feature | Status |
|-----------|-------------|--------------|--------|
| **Test-First Development** | TDD workflow mandatory (RED → GREEN → REFACTOR) | Will follow TDD for all new features | ✅ PASS |
| **Phase 1 Constraints** | CLI-only, in-memory storage, no persistence | Maintains in-memory storage, extends CLI with rich UI | ✅ PASS |
| **Backward Compatibility** | Existing functionality must remain intact | All 84 existing tests must pass; extends (not replaces) current features | ✅ PASS |
| **Clean Architecture** | Separation: entities (todo.py), storage (storage.py), handlers (cli.py), UI (interactive_menu.py) | Will add: ui/ (rich components), services/ (search, filter, undo), extend todo.py | ✅ PASS |
| **Package Management** | Use UV for dependencies | Will use UV to add rich, questionary, python-dateutil | ✅ PASS |
| **Error Handling** | Custom exceptions (ValidationError, NotFoundError, TodoError) | Will extend exception hierarchy for date parsing, filter validation | ✅ PASS |

**Pre-Phase 0 Gate**: ✅ PASS - No constitutional violations detected

**Post-Phase 1 Re-check**: Will validate after design artifacts are created

## Project Structure

### Documentation (this feature)

```text
specs/004-rich-ui-enhanced/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output - in progress)
├── research.md          # Phase 0 output (/sp.plan command - to be generated)
├── data-model.md        # Phase 1 output (/sp.plan command - to be generated)
├── quickstart.md        # Phase 1 output (/sp.plan command - to be generated)
├── contracts/           # Phase 1 output (/sp.plan command - to be generated)
│   ├── ui_components.md     # Rich UI component interfaces
│   ├── filter_service.md    # Search/filter/sort interfaces
│   └── undo_service.md      # Undo/action history interfaces
├── checklists/          # Quality validation (completed)
│   └── requirements.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**Current Structure** (Phase 1 + Feature 003):
```text
src/
├── __init__.py
├── todo.py              # TodoItem entity (id, title, completed)
├── storage.py           # TodoStorage (in-memory dict-based)
├── cli.py               # CLI handlers (add, list, complete, delete, update)
├── main.py              # Traditional CLI entry point
├── interactive_menu.py  # Interactive menu (feature 003)
└── exceptions.py        # Custom exceptions

tests/
├── unit/
│   ├── test_todo.py         # TodoItem tests (6 tests)
│   ├── test_storage.py      # TodoStorage tests (24 tests)
│   └── test_menu.py         # Menu unit tests (14 tests)
└── integration/
    ├── test_cli.py          # CLI integration tests (33 tests)
    └── test_interactive.py  # Interactive workflow tests (7 tests)

main.py                  # Interactive mode entry point (feature 003)
pyproject.toml           # UV configuration (feature 003)
requirements.txt         # Dependencies (pytest, pytest-cov)
```

**New Structure** (Feature 004 additions):
```text
src/
├── todo.py              # EXTENDED: Add priority, due_date, category, tags, created_date, updated_date
├── storage.py           # EXTENDED: Add search, filter, sort methods
├── exceptions.py        # EXTENDED: Add DateParseError, FilterValidationError
├── ui/                  # NEW: Rich UI components
│   ├── __init__.py
│   ├── tables.py            # Rich table rendering for tasks
│   ├── panels.py            # Statistics panels, progress bars
│   ├── prompts.py           # Questionary prompts (arrow navigation)
│   └── formatting.py        # Color schemes, status badges, icons
├── services/            # NEW: Business logic services
│   ├── __init__.py
│   ├── search_filter.py     # Search, filter, sort logic
│   ├── undo_manager.py      # Undo/action history management
│   ├── date_parser.py       # Date parsing (python-dateutil wrapper)
│   └── statistics.py        # Statistics calculations
└── rich_menu.py         # NEW: Enhanced interactive menu with rich UI

tests/
├── unit/
│   ├── test_extended_todo.py    # Tests for priority, dates, categories
│   ├── test_search_filter.py    # Search/filter/sort tests
│   ├── test_undo_manager.py     # Undo functionality tests
│   ├── test_date_parser.py      # Date parsing tests
│   ├── test_statistics.py       # Statistics calculation tests
│   └── test_ui_components.py    # Rich UI component tests
├── integration/
│   └── test_rich_workflows.py   # End-to-end rich UI workflows
└── contract/            # NEW: Contract tests for service interfaces
    ├── test_filter_contracts.py
    └── test_undo_contracts.py

requirements.txt         # UPDATED: Add rich, questionary, python-dateutil
```

**Structure Decision**:
- **Single Python project structure** (Option 1) - matches existing architecture
- **Layered organization**: Entities (todo.py) → Storage (storage.py) → Services (services/) → UI (ui/) → Entry points (main.py, rich_menu.py)
- **Extension strategy**: Extend existing files (todo.py, storage.py, exceptions.py) + add new modules (ui/, services/)
- **Test organization**: Mirror source structure (unit/, integration/, contract/)
- **Backward compatibility**: All existing files remain; new functionality is additive

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**Status**: No constitutional violations detected - complexity tracking not required.

The implementation follows existing patterns:
- Extends existing entities rather than creating new ones
- Adds service layer for new functionality (search, filter, undo, statistics)
- Maintains in-memory storage (Phase 1 constraint)
- Uses established testing patterns (TDD workflow)
- New dependencies (rich, questionary, python-dateutil) are necessary for spec requirements
