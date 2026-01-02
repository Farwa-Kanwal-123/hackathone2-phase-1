"""
Unit tests for TodoItem class

Tests cover:
- TodoItem creation with valid data
- Title validation (empty, too long, whitespace-only)
"""

import pytest
from src.todo import TodoItem
from src.exceptions import ValidationError


class TestTodoItemCreation:
    """Tests for TodoItem creation with valid data (T010)"""

    def test_create_todo_item_with_valid_title(self):
        """Test creating a TodoItem with a valid title"""
        todo = TodoItem(id=1, title="Buy groceries", completed=False)

        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.completed is False

    def test_create_todo_item_defaults_to_incomplete(self):
        """Test that completed defaults to False"""
        todo = TodoItem(id=2, title="Write tests")

        assert todo.completed is False


class TestTodoItemValidation:
    """Tests for TodoItem title validation (T011)"""

    def test_empty_title_raises_validation_error(self):
        """Test that empty title raises ValidationError"""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            TodoItem(id=1, title="", completed=False)

    def test_whitespace_only_title_raises_validation_error(self):
        """Test that whitespace-only title raises ValidationError"""
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            TodoItem(id=1, title="   ", completed=False)

    def test_title_too_long_raises_validation_error(self):
        """Test that title exceeding 200 characters raises ValidationError"""
        long_title = "a" * 201
        with pytest.raises(ValidationError, match="Title cannot exceed 200 characters"):
            TodoItem(id=1, title=long_title, completed=False)

    def test_title_exactly_200_characters_is_valid(self):
        """Test that title with exactly 200 characters is valid"""
        valid_title = "a" * 200
        todo = TodoItem(id=1, title=valid_title, completed=False)

        assert todo.title == valid_title
