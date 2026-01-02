# Feature Specification: Update Todo Titles

**Feature Branch**: `002-update-todo`
**Created**: 2025-12-25
**Status**: Draft
**Input**: User description: "update-todo - Add ability to update/edit existing todo titles"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Edit Todo Title (Priority: P1)

As a user, I want to edit the title of an existing todo so that I can correct typos, clarify tasks, or update descriptions without deleting and re-creating the todo.

**Why this priority**: This is the core functionality requested. Users frequently need to modify todo titles after creation (typos, changed requirements, better descriptions). Currently, the only workaround is delete-and-recreate, which is cumbersome and loses the original ID.

**Independent Test**: Add a todo, edit its title by ID, list todos to verify the title changed while ID and completion status remained the same.

**Acceptance Scenarios**:

1. **Given** I have a todo with ID 1 titled "Buy grocreies", **When** I update it to "Buy groceries", **Then** the system confirms the update and the todo shows the corrected title when listed
2. **Given** I have a todo with ID 2, **When** I update its title to a new description, **Then** the todo retains its original ID and completion status
3. **Given** I try to update a non-existent todo, **When** I provide an invalid ID, **Then** I receive a clear error message
4. **Given** I try to update a todo with an empty title, **When** I attempt the update, **Then** I receive a validation error

---

### Edge Cases

- What happens when a user tries to update a todo with an empty or whitespace-only title?
- What happens when a user tries to update a todo that doesn't exist?
- What happens when a user provides a title exceeding the 200-character limit?
- What happens when a user updates a completed todo - does it remain completed?
- Can a user update a todo to have the same title as another todo (duplicates allowed)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to update an existing todo's title by providing the todo ID and new title
- **FR-002**: System MUST validate that the new title follows the same rules as todo creation (1-200 characters, not empty, not whitespace-only)
- **FR-003**: System MUST preserve the todo's original ID when updating the title
- **FR-004**: System MUST preserve the todo's completion status when updating the title
- **FR-005**: System MUST return a clear error message when attempting to update a non-existent todo ID
- **FR-006**: System MUST return a validation error when attempting to update with an invalid title (empty, too long, whitespace-only)
- **FR-007**: System MUST provide a CLI command for updating todos (e.g., `todo update <id> "<new-title>"`)
- **FR-008**: System MUST confirm successful updates with a message showing the old and new titles
- **FR-009**: System MUST support updating both completed and incomplete todos
- **FR-010**: System MUST exit with code 0 on successful update and non-zero on error

### Key Entities

- **Todo Item** (existing entity, modified behavior):
  - ID: Unique numeric identifier (unchanged during update)
  - Title: Text description (can be modified via update command)
  - Status: Completion state (unchanged during update)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can update a todo title in under 5 seconds (command entry to confirmation)
- **SC-002**: 100% of valid update commands execute successfully without crashes or errors
- **SC-003**: All error messages for update operations are clear enough that users can correct their input without consulting documentation
- **SC-004**: Users prefer updating todos over delete-and-recreate workflow (eliminates the workaround)
- **SC-005**: Update operations maintain data integrity (IDs and completion status never change)
- **SC-006**: The update command follows the same usability patterns as existing commands (add, list, complete, delete)

## Assumptions

- Update functionality follows Phase 1 constraints (CLI-only, in-memory storage, no persistence)
- Users are familiar with existing todo commands (add, list, complete, delete)
- The same validation rules apply to updates as to creating new todos
- Updating a todo's title does not change its position in the list (ordered by ID)
- No audit trail or history of title changes is required for Phase 1
- Duplicate titles across different todos are allowed (no uniqueness constraint)
- The update command is synchronous and provides immediate feedback
- Standard terminal environment (Windows, macOS, Linux)
- Python 3.11+ is available on the user's system
- Update command does not affect the in-memory session lifecycle (data still lost on exit)

## Out of Scope

- Undo/redo functionality for updates
- History or audit trail of title changes
- Bulk update operations (updating multiple todos at once)
- Updating completion status (use existing `complete` command)
- Updating todo IDs (IDs are immutable)
- File persistence or database storage
- Filtering or searching during update operations
- Rich text formatting in titles
- Multi-line or formatted todo descriptions
