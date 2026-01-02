"""
Contract tests for SearchFilterService

Verifies that SearchFilterService follows expected contracts:
- All filter methods return lists (not None)
- All filter methods do not modify storage
- All sort methods return new lists (immutability)
- All methods handle edge cases consistently
"""

import pytest
from datetime import date, timedelta
from src.storage import TodoStorage
from src.services.search_filter import SearchFilterService


class TestSearchFilterServiceContracts:
    """Contract tests for SearchFilterService"""

    def setup_method(self):
        """Set up test storage"""
        self.storage = TodoStorage()
        self.storage.add("Test task 1")
        self.storage.add("Test task 2")
        self.storage.todos[2].priority = "High"
        self.storage.todos[2].category = "Work"
        self.storage.todos[2].tags = ["urgent"]
        self.storage.todos[2].due_date = date.today()

        self.service = SearchFilterService(self.storage)

    def test_all_filter_methods_return_lists(self):
        """All filter methods should return lists, never None"""
        # search()
        assert isinstance(self.service.search("test"), list)
        assert isinstance(self.service.search("nonexistent"), list)

        # filter_by_priority()
        assert isinstance(self.service.filter_by_priority("High"), list)
        assert isinstance(self.service.filter_by_priority("None"), list)

        # filter_by_status()
        assert isinstance(self.service.filter_by_status("completed"), list)
        assert isinstance(self.service.filter_by_status("incomplete"), list)

        # filter_by_category()
        assert isinstance(self.service.filter_by_category("Work"), list)
        assert isinstance(self.service.filter_by_category(None), list)

        # filter_by_tag()
        assert isinstance(self.service.filter_by_tag("urgent"), list)
        assert isinstance(self.service.filter_by_tag("nonexistent"), list)

    def test_filter_methods_do_not_modify_storage(self):
        """Filter methods should not modify storage"""
        original_count = len(self.storage.list_all())
        original_todos = {k: v for k, v in self.storage.todos.items()}

        # Run various filter operations
        self.service.search("test")
        self.service.filter_by_priority("High")
        self.service.filter_by_status("incomplete")
        self.service.filter_by_category("Work")
        self.service.filter_by_tag("urgent")

        # Storage should be unchanged
        assert len(self.storage.list_all()) == original_count
        assert self.storage.todos == original_todos

    def test_sort_methods_return_new_lists(self):
        """Sort methods should return new lists (immutability)"""
        todos = self.storage.list_all()
        original_order = [t.id for t in todos]

        # sort_by_priority
        sorted_by_priority = self.service.sort_by_priority(todos)
        assert sorted_by_priority is not todos  # New list
        assert [t.id for t in todos] == original_order  # Original unchanged

        # sort_by_due_date
        sorted_by_due_date = self.service.sort_by_due_date(todos)
        assert sorted_by_due_date is not todos
        assert [t.id for t in todos] == original_order

    def test_empty_result_consistency(self):
        """All filter methods should return empty lists (not None) when no matches"""
        # Create storage with no matches
        storage = TodoStorage()
        service = SearchFilterService(storage)

        assert service.search("anything") == []
        assert service.filter_by_priority("High") == []
        assert service.filter_by_status("completed") == []
        assert service.filter_by_category("Work") == []
        assert service.filter_by_tag("urgent") == []

    def test_filter_methods_preserve_todo_properties(self):
        """Filter methods should return TodoItem objects with all properties intact"""
        results = self.service.filter_by_priority("High")
        assert len(results) == 1

        todo = results[0]
        # All properties should be intact
        assert hasattr(todo, "id")
        assert hasattr(todo, "title")
        assert hasattr(todo, "completed")
        assert hasattr(todo, "priority")
        assert hasattr(todo, "category")
        assert hasattr(todo, "tags")
        assert hasattr(todo, "due_date")
        assert hasattr(todo, "created_date")
        assert hasattr(todo, "updated_date")

    def test_validation_errors_are_consistent(self):
        """All filter methods should raise ValueError for invalid input consistently"""
        # Empty/whitespace search query
        with pytest.raises(ValueError):
            self.service.search("")
        with pytest.raises(ValueError):
            self.service.search("   ")

        # Invalid priority
        with pytest.raises(ValueError):
            self.service.filter_by_priority("Invalid")

        # Invalid status
        with pytest.raises(ValueError):
            self.service.filter_by_status("invalid")

        # Empty category
        with pytest.raises(ValueError):
            self.service.filter_by_category("")

        # Empty tag
        with pytest.raises(ValueError):
            self.service.filter_by_tag("")
