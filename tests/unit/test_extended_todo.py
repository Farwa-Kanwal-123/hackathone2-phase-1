"""
Unit tests for extended TodoItem entity

Tests cover priority validation, due date validation, category validation,
tags validation, and timestamp fields.
"""

import pytest
from datetime import date, datetime
from src.todo import TodoItem
from src.exceptions import ValidationError


class TestTodoItemPriorityValidation:
    """Test priority field validation"""

    def test_priority_high_valid(self):
        """High priority should be accepted"""
        todo = TodoItem(id=1, title="Urgent task", completed=False, priority="High")
        assert todo.priority == "High"

    def test_priority_medium_valid(self):
        """Medium priority should be accepted"""
        todo = TodoItem(id=1, title="Important task", completed=False, priority="Medium")
        assert todo.priority == "Medium"

    def test_priority_low_valid(self):
        """Low priority should be accepted"""
        todo = TodoItem(id=1, title="Low task", completed=False, priority="Low")
        assert todo.priority == "Low"

    def test_priority_none_valid(self):
        """None priority (no priority) should be accepted"""
        todo = TodoItem(id=1, title="No priority task", completed=False, priority=None)
        assert todo.priority is None

    def test_priority_default_is_none(self):
        """Priority should default to None if not specified"""
        todo = TodoItem(id=1, title="Task", completed=False)
        assert todo.priority is None

    def test_priority_invalid_raises_error(self):
        """Invalid priority should raise ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            TodoItem(id=1, title="Task", completed=False, priority="Critical")

        assert "Priority must be 'High', 'Medium', 'Low', or None" in str(exc_info.value)

    def test_priority_case_sensitive(self):
        """Priority values are case-sensitive"""
        with pytest.raises(ValidationError):
            TodoItem(id=1, title="Task", completed=False, priority="high")

        with pytest.raises(ValidationError):
            TodoItem(id=1, title="Task", completed=False, priority="MEDIUM")


class TestTodoItemDueDateValidation:
    """Test due_date field validation"""

    def test_due_date_valid(self):
        """Valid date object should be accepted"""
        today = date.today()
        todo = TodoItem(id=1, title="Task", completed=False, due_date=today)
        assert todo.due_date == today

    def test_due_date_none_valid(self):
        """None due_date should be accepted"""
        todo = TodoItem(id=1, title="Task", completed=False, due_date=None)
        assert todo.due_date is None

    def test_due_date_default_is_none(self):
        """due_date should default to None if not specified"""
        todo = TodoItem(id=1, title="Task", completed=False)
        assert todo.due_date is None

    def test_due_date_invalid_type_raises_error(self):
        """Non-date object should raise ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            TodoItem(id=1, title="Task", completed=False, due_date="2025-12-31")

        assert "due_date must be a datetime.date object" in str(exc_info.value)


class TestTodoItemCategoryValidation:
    """Test category field validation"""

    def test_category_valid(self):
        """Valid category string should be accepted"""
        todo = TodoItem(id=1, title="Task", completed=False, category="Work")
        assert todo.category == "Work"

    def test_category_none_valid(self):
        """None category should be accepted"""
        todo = TodoItem(id=1, title="Task", completed=False, category=None)
        assert todo.category is None

    def test_category_default_is_none(self):
        """category should default to None if not specified"""
        todo = TodoItem(id=1, title="Task", completed=False)
        assert todo.category is None

    def test_category_max_length_50(self):
        """Category can be up to 50 characters"""
        long_category = "A" * 50
        todo = TodoItem(id=1, title="Task", completed=False, category=long_category)
        assert todo.category == long_category

    def test_category_exceeds_50_raises_error(self):
        """Category exceeding 50 characters should raise ValidationError"""
        too_long = "A" * 51
        with pytest.raises(ValidationError) as exc_info:
            TodoItem(id=1, title="Task", completed=False, category=too_long)

        assert "category cannot exceed 50 characters" in str(exc_info.value)

    def test_category_invalid_type_raises_error(self):
        """Non-string category should raise ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            TodoItem(id=1, title="Task", completed=False, category=123)

        assert "category must be a string" in str(exc_info.value)


class TestTodoItemTagsValidation:
    """Test tags field validation"""

    def test_tags_valid_list(self):
        """Valid list of tags should be accepted"""
        tags = ["urgent", "bug", "frontend"]
        todo = TodoItem(id=1, title="Task", completed=False, tags=tags)
        assert todo.tags == tags

    def test_tags_empty_list_valid(self):
        """Empty list should be accepted"""
        todo = TodoItem(id=1, title="Task", completed=False, tags=[])
        assert todo.tags == []

    def test_tags_default_is_empty_list(self):
        """tags should default to empty list if not specified"""
        todo = TodoItem(id=1, title="Task", completed=False)
        assert todo.tags == []

    def test_tags_single_tag(self):
        """Single tag in list should be accepted"""
        todo = TodoItem(id=1, title="Task", completed=False, tags=["urgent"])
        assert todo.tags == ["urgent"]

    def test_tags_max_length_30(self):
        """Each tag can be up to 30 characters"""
        long_tag = "A" * 30
        todo = TodoItem(id=1, title="Task", completed=False, tags=[long_tag])
        assert todo.tags == [long_tag]

    def test_tags_exceeds_30_raises_error(self):
        """Tag exceeding 30 characters should raise ValidationError"""
        too_long = "A" * 31
        with pytest.raises(ValidationError) as exc_info:
            TodoItem(id=1, title="Task", completed=False, tags=[too_long])

        assert "exceeds 30 characters" in str(exc_info.value)

    def test_tags_non_list_raises_error(self):
        """Non-list tags should raise ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            TodoItem(id=1, title="Task", completed=False, tags="urgent")

        assert "tags must be a list" in str(exc_info.value)

    def test_tags_non_string_element_raises_error(self):
        """Non-string tag elements should raise ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            TodoItem(id=1, title="Task", completed=False, tags=["urgent", 123])

        assert "All tags must be strings" in str(exc_info.value)


class TestTodoItemTimestamps:
    """Test created_date and updated_date timestamp fields"""

    def test_created_date_auto_set(self):
        """created_date should be automatically set to current time"""
        before = datetime.now()
        todo = TodoItem(id=1, title="Task", completed=False)
        after = datetime.now()

        assert before <= todo.created_date <= after

    def test_updated_date_auto_set(self):
        """updated_date should be automatically set to current time"""
        before = datetime.now()
        todo = TodoItem(id=1, title="Task", completed=False)
        after = datetime.now()

        assert before <= todo.updated_date <= after

    def test_created_and_updated_same_on_creation(self):
        """created_date and updated_date should be approximately equal on creation"""
        todo = TodoItem(id=1, title="Task", completed=False)
        # Allow 1 second difference
        time_diff = abs((todo.updated_date - todo.created_date).total_seconds())
        assert time_diff < 1.0
