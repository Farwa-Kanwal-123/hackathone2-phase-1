"""
Unit tests for TodoStorage class

Tests cover:
- Adding todos (T012)
- Listing all todos (T013)
- Sequential ID generation (T014)
- Completing todos (T029-T031)
- Deleting todos (T041-T043)
"""

import pytest
from src.storage import TodoStorage
from src.exceptions import ValidationError, NotFoundError


class TestTodoStorageAdd:
    """Tests for TodoStorage.add() method (T012)"""

    def test_add_todo_returns_created_item(self):
        """Test that add() creates and returns a TodoItem"""
        storage = TodoStorage()

        todo = storage.add("Buy groceries")

        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.completed is False

    def test_add_todo_stores_item(self):
        """Test that add() stores the TodoItem in storage"""
        storage = TodoStorage()

        storage.add("Buy groceries")
        all_todos = storage.list_all()

        assert len(all_todos) == 1
        assert all_todos[0].title == "Buy groceries"

    def test_add_empty_title_raises_validation_error(self):
        """Test that adding empty title raises ValidationError"""
        storage = TodoStorage()

        with pytest.raises(ValidationError):
            storage.add("")

    def test_add_whitespace_title_raises_validation_error(self):
        """Test that adding whitespace-only title raises ValidationError"""
        storage = TodoStorage()

        with pytest.raises(ValidationError):
            storage.add("   ")


class TestTodoStorageListAll:
    """Tests for TodoStorage.list_all() method (T013)"""

    def test_list_all_returns_empty_list_when_no_todos(self):
        """Test that list_all() returns empty list initially"""
        storage = TodoStorage()

        todos = storage.list_all()

        assert todos == []

    def test_list_all_returns_all_todos(self):
        """Test that list_all() returns all added todos"""
        storage = TodoStorage()
        storage.add("Buy groceries")
        storage.add("Write tests")
        storage.add("Deploy app")

        todos = storage.list_all()

        assert len(todos) == 3
        assert todos[0].title == "Buy groceries"
        assert todos[1].title == "Write tests"
        assert todos[2].title == "Deploy app"

    def test_list_all_returns_sorted_by_id(self):
        """Test that list_all() returns todos sorted by ID"""
        storage = TodoStorage()
        storage.add("First")
        storage.add("Second")
        storage.add("Third")

        todos = storage.list_all()

        assert todos[0].id == 1
        assert todos[1].id == 2
        assert todos[2].id == 3


class TestTodoStorageSequentialIDs:
    """Tests for sequential ID generation (T014)"""

    def test_first_todo_gets_id_1(self):
        """Test that first todo gets ID 1"""
        storage = TodoStorage()

        todo = storage.add("First todo")

        assert todo.id == 1

    def test_sequential_ids_increment(self):
        """Test that IDs increment sequentially"""
        storage = TodoStorage()

        todo1 = storage.add("First")
        todo2 = storage.add("Second")
        todo3 = storage.add("Third")

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3

    def test_ids_are_deterministic(self):
        """Test that IDs are deterministic (always start from 1)"""
        storage1 = TodoStorage()
        storage2 = TodoStorage()

        todo1 = storage1.add("Test")
        todo2 = storage2.add("Test")

        assert todo1.id == 1
        assert todo2.id == 1


class TestTodoStorageComplete:
    """Tests for TodoStorage.complete() method (T029-T031)"""

    def test_complete_marks_todo_as_done(self):
        """Test that complete() marks a todo as completed (T029)"""
        storage = TodoStorage()
        todo = storage.add("Buy groceries")

        # Initially incomplete
        assert todo.completed is False

        # Complete the todo
        completed_todo = storage.complete(todo.id)

        # Verify it's now completed
        assert completed_todo.completed is True
        assert completed_todo.id == todo.id
        assert completed_todo.title == todo.title

    def test_complete_nonexistent_todo_raises_error(self):
        """Test that completing non-existent todo raises NotFoundError (T030)"""
        storage = TodoStorage()

        with pytest.raises(NotFoundError, match="Todo with ID 999 not found"):
            storage.complete(999)

    def test_complete_is_idempotent(self):
        """Test that completing already-completed todo is idempotent (T031)"""
        storage = TodoStorage()
        todo = storage.add("Buy groceries")

        # Complete once
        storage.complete(todo.id)
        assert todo.completed is True

        # Complete again (should not raise error)
        completed_todo = storage.complete(todo.id)
        assert completed_todo.completed is True

    def test_complete_persists_in_storage(self):
        """Test that completed status persists in storage"""
        storage = TodoStorage()
        todo = storage.add("Buy groceries")

        storage.complete(todo.id)

        # Retrieve from storage
        all_todos = storage.list_all()
        assert len(all_todos) == 1
        assert all_todos[0].completed is True


class TestTodoStorageDelete:
    """Tests for TodoStorage.delete() method (T041-T043)"""

    def test_delete_removes_todo(self):
        """Test that delete() removes a todo from storage (T041)"""
        storage = TodoStorage()
        todo1 = storage.add("Buy groceries")
        todo2 = storage.add("Write tests")

        # Delete first todo
        storage.delete(todo1.id)

        # Verify it's removed
        all_todos = storage.list_all()
        assert len(all_todos) == 1
        assert all_todos[0].id == todo2.id
        assert all_todos[0].title == "Write tests"

    def test_delete_nonexistent_todo_raises_error(self):
        """Test that deleting non-existent todo raises NotFoundError (T042)"""
        storage = TodoStorage()

        with pytest.raises(NotFoundError, match="Todo with ID 999 not found"):
            storage.delete(999)

    def test_delete_preserves_id_gaps(self):
        """Test that IDs are not reused after deletion (T043)"""
        storage = TodoStorage()

        # Add three todos
        todo1 = storage.add("First")
        todo2 = storage.add("Second")
        todo3 = storage.add("Third")

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3

        # Delete second todo
        storage.delete(2)

        # Add a new todo - should get ID 4, not 2
        todo4 = storage.add("Fourth")
        assert todo4.id == 4

        # Verify list has correct todos
        all_todos = storage.list_all()
        assert len(all_todos) == 3
        assert all_todos[0].id == 1
        assert all_todos[1].id == 3  # Gap where ID 2 was deleted
        assert all_todos[2].id == 4

    def test_delete_all_todos(self):
        """Test deleting all todos results in empty list"""
        storage = TodoStorage()
        todo1 = storage.add("First")
        todo2 = storage.add("Second")

        storage.delete(todo1.id)
        storage.delete(todo2.id)

        all_todos = storage.list_all()
        assert len(all_todos) == 0

    def test_delete_returns_none(self):
        """Test that delete() returns None (no return value)"""
        storage = TodoStorage()
        todo = storage.add("Buy groceries")

        result = storage.delete(todo.id)

        assert result is None


class TestTodoStorageUpdate:
    """Tests for TodoStorage.update() method (T001-T005)"""

    def test_update_valid_todo(self):
        """Test that update() changes todo title with valid input (T001)"""
        storage = TodoStorage()
        todo = storage.add("Buy grocreies")

        # Update the todo
        updated_todo = storage.update(todo.id, "Buy groceries")

        # Verify title changed
        assert updated_todo.title == "Buy groceries"
        assert updated_todo.id == todo.id
        assert updated_todo.completed is False

        # Verify change persists in storage
        all_todos = storage.list_all()
        assert len(all_todos) == 1
        assert all_todos[0].title == "Buy groceries"

    def test_update_nonexistent_id_raises_error(self):
        """Test that updating non-existent ID raises NotFoundError (T002)"""
        storage = TodoStorage()

        with pytest.raises(NotFoundError, match="Todo with ID 999 not found"):
            storage.update(999, "New title")

    def test_update_empty_title_raises_error(self):
        """Test that updating with empty title raises ValidationError (T003)"""
        storage = TodoStorage()
        todo = storage.add("Original title")

        with pytest.raises(ValidationError):
            storage.update(todo.id, "")

    def test_update_long_title_raises_error(self):
        """Test that updating with title >200 chars raises ValidationError (T004)"""
        storage = TodoStorage()
        todo = storage.add("Original title")

        long_title = "A" * 201

        with pytest.raises(ValidationError):
            storage.update(todo.id, long_title)

    def test_update_preserves_id_and_status(self):
        """Test that update() preserves ID and completion status (T005)"""
        storage = TodoStorage()

        # Add and complete a todo
        todo = storage.add("Original title")
        storage.complete(todo.id)

        # Verify it's completed
        assert todo.completed is True
        original_id = todo.id

        # Update the completed todo
        updated_todo = storage.update(todo.id, "Updated title")

        # Verify ID preserved
        assert updated_todo.id == original_id

        # Verify completion status preserved
        assert updated_todo.completed is True

        # Verify title changed
        assert updated_todo.title == "Updated title"

        # Verify change persists in storage
        all_todos = storage.list_all()
        assert len(all_todos) == 1
        assert all_todos[0].id == original_id
        assert all_todos[0].completed is True
        assert all_todos[0].title == "Updated title"
