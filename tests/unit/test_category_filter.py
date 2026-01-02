"""
Unit tests for category and tag filtering

Tests filter_by_category() and filter_by_tag() functions in SearchFilterService.
"""

import pytest
from datetime import date
from src.todo import TodoItem
from src.storage import TodoStorage
from src.services.search_filter import SearchFilterService


class TestFilterByCategory:
    """Test filter_by_category() function"""

    def setup_method(self):
        """Set up test storage with categorized todos"""
        self.storage = TodoStorage()
        self.storage.add("Work task 1")
        self.storage.todos[1].category = "Work"
        self.storage.add("Work task 2")
        self.storage.todos[2].category = "Work"
        self.storage.add("Personal task 1")
        self.storage.todos[3].category = "Personal"
        self.storage.add("Uncategorized task")
        # Task 4 has no category (None)

        self.service = SearchFilterService(self.storage)

    def test_filter_by_category_single_match(self):
        """Should return todos with matching category"""
        results = self.service.filter_by_category("Personal")
        assert len(results) == 1
        assert results[0].id == 3
        assert results[0].category == "Personal"

    def test_filter_by_category_multiple_matches(self):
        """Should return all todos with matching category"""
        results = self.service.filter_by_category("Work")
        assert len(results) == 2
        assert all(t.category == "Work" for t in results)
        assert {t.id for t in results} == {1, 2}

    def test_filter_by_category_no_matches(self):
        """Should return empty list when no matches"""
        results = self.service.filter_by_category("Shopping")
        assert results == []

    def test_filter_by_category_none(self):
        """Should return todos with no category when filtering by None"""
        results = self.service.filter_by_category(None)
        assert len(results) == 1
        assert results[0].id == 4
        assert results[0].category is None

    def test_filter_by_category_case_sensitive(self):
        """Should be case-sensitive"""
        results = self.service.filter_by_category("work")  # lowercase
        assert results == []

    def test_filter_by_category_empty_string(self):
        """Should raise ValueError for empty string"""
        with pytest.raises(ValueError, match="Category cannot be empty"):
            self.service.filter_by_category("")

    def test_filter_by_category_whitespace_only(self):
        """Should raise ValueError for whitespace-only string"""
        with pytest.raises(ValueError, match="Category cannot be empty"):
            self.service.filter_by_category("   ")


class TestFilterByTag:
    """Test filter_by_tag() function"""

    def setup_method(self):
        """Set up test storage with tagged todos"""
        self.storage = TodoStorage()
        self.storage.add("Task with urgent tag")
        self.storage.todos[1].tags = ["urgent"]
        self.storage.add("Task with urgent and important tags")
        self.storage.todos[2].tags = ["urgent", "important"]
        self.storage.add("Task with important tag")
        self.storage.todos[3].tags = ["important"]
        self.storage.add("Task with no tags")
        # Task 4 has empty tags list

        self.service = SearchFilterService(self.storage)

    def test_filter_by_tag_single_match(self):
        """Should return todos containing the tag"""
        results = self.service.filter_by_tag("important")
        assert len(results) == 2
        assert {t.id for t in results} == {2, 3}
        assert all("important" in t.tags for t in results)

    def test_filter_by_tag_multiple_todos(self):
        """Should return all todos with the tag"""
        results = self.service.filter_by_tag("urgent")
        assert len(results) == 2
        assert {t.id for t in results} == {1, 2}

    def test_filter_by_tag_no_matches(self):
        """Should return empty list when no matches"""
        results = self.service.filter_by_tag("personal")
        assert results == []

    def test_filter_by_tag_case_sensitive(self):
        """Should be case-sensitive"""
        results = self.service.filter_by_tag("Urgent")  # capitalized
        assert results == []

    def test_filter_by_tag_empty_string(self):
        """Should raise ValueError for empty string"""
        with pytest.raises(ValueError, match="Tag cannot be empty"):
            self.service.filter_by_tag("")

    def test_filter_by_tag_whitespace_only(self):
        """Should raise ValueError for whitespace-only string"""
        with pytest.raises(ValueError, match="Tag cannot be empty"):
            self.service.filter_by_tag("   ")

    def test_filter_by_tag_exact_match_only(self):
        """Should match exact tag, not partial"""
        self.storage.add("Task with important-work tag")
        self.storage.todos[5].tags = ["important-work"]

        results = self.service.filter_by_tag("important")
        # Should not match "important-work"
        assert 5 not in {t.id for t in results}


class TestCategoryAndTagCombination:
    """Test combining category and tag filters"""

    def setup_method(self):
        """Set up test storage with category and tags"""
        self.storage = TodoStorage()
        self.storage.add("Work urgent task")
        self.storage.todos[1].category = "Work"
        self.storage.todos[1].tags = ["urgent"]

        self.storage.add("Work important task")
        self.storage.todos[2].category = "Work"
        self.storage.todos[2].tags = ["important"]

        self.storage.add("Personal urgent task")
        self.storage.todos[3].category = "Personal"
        self.storage.todos[3].tags = ["urgent"]

        self.service = SearchFilterService(self.storage)

    def test_filter_by_category_then_tag(self):
        """Should be able to chain filters"""
        # First filter by category
        work_todos = self.service.filter_by_category("Work")

        # Then filter results by tag
        # Note: We need a new service with filtered todos
        temp_storage = TodoStorage()
        for todo in work_todos:
            temp_storage.todos[todo.id] = todo
        temp_service = SearchFilterService(temp_storage)

        urgent_work_todos = temp_service.filter_by_tag("urgent")
        assert len(urgent_work_todos) == 1
        assert urgent_work_todos[0].id == 1
