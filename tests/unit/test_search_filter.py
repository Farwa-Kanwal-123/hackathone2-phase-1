"""
Unit tests for SearchFilterService

Tests cover search, filter_by_priority, filter_by_status, sort_by_priority,
and sort_by_due_date operations.
"""

import pytest
from datetime import date, timedelta
from src.storage import TodoStorage
from src.services.search_filter import SearchFilterService
from src.todo import TodoItem


class TestFilterByPriority:
    """Test priority filtering functionality"""

    def setup_method(self):
        """Set up test storage with todos of different priorities"""
        self.storage = TodoStorage()
        self.storage.add("High priority task")
        self.storage.todos[1].priority = "High"

        self.storage.add("Medium priority task")
        self.storage.todos[2].priority = "Medium"

        self.storage.add("Low priority task")
        self.storage.todos[3].priority = "Low"

        self.storage.add("No priority task")
        # Leave priority as None

        self.service = SearchFilterService(self.storage)

    def test_filter_by_priority_high(self):
        """Filter should return only High priority todos"""
        result = self.service.filter_by_priority("High")
        assert len(result) == 1
        assert result[0].priority == "High"
        assert result[0].title == "High priority task"

    def test_filter_by_priority_medium(self):
        """Filter should return only Medium priority todos"""
        result = self.service.filter_by_priority("Medium")
        assert len(result) == 1
        assert result[0].priority == "Medium"
        assert result[0].title == "Medium priority task"

    def test_filter_by_priority_low(self):
        """Filter should return only Low priority todos"""
        result = self.service.filter_by_priority("Low")
        assert len(result) == 1
        assert result[0].priority == "Low"
        assert result[0].title == "Low priority task"

    def test_filter_by_priority_none(self):
        """Filter should return todos with None priority"""
        result = self.service.filter_by_priority("None")
        assert len(result) == 1
        assert result[0].priority is None
        assert result[0].title == "No priority task"

    def test_filter_by_priority_invalid_raises_error(self):
        """Invalid priority should raise ValueError"""
        with pytest.raises(ValueError) as exc_info:
            self.service.filter_by_priority("Critical")

        assert "Priority must be one of" in str(exc_info.value)

    def test_filter_by_priority_empty_result(self):
        """Filter with no matches should return empty list"""
        # Remove all todos and add one without priority
        self.storage.todos.clear()
        self.storage.add("Task")

        result = self.service.filter_by_priority("High")
        assert result == []

    def test_filter_by_priority_multiple_matches(self):
        """Filter should return all matching todos"""
        self.storage.add("Another high priority")
        self.storage.todos[5].priority = "High"

        result = self.service.filter_by_priority("High")
        assert len(result) == 2
        assert all(t.priority == "High" for t in result)


class TestSortByPriority:
    """Test priority sorting functionality"""

    def setup_method(self):
        """Set up test storage with todos in random priority order"""
        self.storage = TodoStorage()
        self.storage.add("Task 1")
        self.storage.todos[1].priority = None

        self.storage.add("Task 2")
        self.storage.todos[2].priority = "Low"

        self.storage.add("Task 3")
        self.storage.todos[3].priority = "High"

        self.storage.add("Task 4")
        self.storage.todos[4].priority = "Medium"

        self.service = SearchFilterService(self.storage)

    def test_sort_by_priority_order(self):
        """Todos should be sorted High → Medium → Low → None"""
        todos = self.storage.list_all()
        sorted_todos = self.service.sort_by_priority(todos)

        assert len(sorted_todos) == 4
        assert sorted_todos[0].priority == "High"
        assert sorted_todos[1].priority == "Medium"
        assert sorted_todos[2].priority == "Low"
        assert sorted_todos[3].priority is None

    def test_sort_by_priority_stable(self):
        """Sort should be stable (preserve order for same priority)"""
        self.storage.add("Task 5")
        self.storage.todos[5].priority = "High"

        todos = self.storage.list_all()
        sorted_todos = self.service.sort_by_priority(todos)

        # Both High priority tasks should be first, in original order
        high_tasks = [t for t in sorted_todos if t.priority == "High"]
        assert len(high_tasks) == 2
        assert high_tasks[0].id < high_tasks[1].id  # Original order preserved

    def test_sort_by_priority_empty_list(self):
        """Sorting empty list should return empty list"""
        result = self.service.sort_by_priority([])
        assert result == []

    def test_sort_by_priority_single_item(self):
        """Sorting single item should return same item"""
        todos = [self.storage.todos[1]]
        result = self.service.sort_by_priority(todos)
        assert len(result) == 1
        assert result[0] == todos[0]

    def test_sort_by_priority_all_same(self):
        """Sorting todos with same priority should preserve order"""
        # Create fresh storage with new service
        storage = TodoStorage()
        storage.add("Task A")
        storage.todos[1].priority = "Medium"
        storage.add("Task B")
        storage.todos[2].priority = "Medium"
        storage.add("Task C")
        storage.todos[3].priority = "Medium"

        service = SearchFilterService(storage)
        todos = storage.list_all()
        sorted_todos = service.sort_by_priority(todos)

        assert [t.id for t in sorted_todos] == [1, 2, 3]

    def test_sort_by_priority_immutable(self):
        """Sort should not modify original list"""
        todos = self.storage.list_all()
        original_order = [t.id for t in todos]

        self.service.sort_by_priority(todos)

        # Original list should be unchanged
        assert [t.id for t in todos] == original_order


class TestSearchFunctionality:
    """Test search functionality (already implemented)"""

    def setup_method(self):
        """Set up test storage with searchable todos"""
        self.storage = TodoStorage()
        self.storage.add("Fix authentication bug")
        self.storage.add("Add new feature to dashboard")
        self.storage.add("Write unit tests")
        self.storage.add("Debug API endpoint")

        self.service = SearchFilterService(self.storage)

    def test_search_case_insensitive(self):
        """Search should be case-insensitive"""
        result = self.service.search("bug")
        assert len(result) == 2  # "bug" in "authentication bug" and "Debug"

    def test_search_partial_match(self):
        """Search should support partial matches"""
        result = self.service.search("test")
        assert len(result) == 1
        assert "tests" in result[0].title

    def test_search_no_matches(self):
        """Search with no matches should return empty list"""
        result = self.service.search("nonexistent")
        assert result == []

    def test_search_empty_raises_error(self):
        """Empty search query should raise ValueError"""
        with pytest.raises(ValueError) as exc_info:
            self.service.search("")

        assert "Search query cannot be empty" in str(exc_info.value)


class TestFilterByStatus:
    """Test status filtering functionality (already implemented)"""

    def setup_method(self):
        """Set up test storage with completed and incomplete todos"""
        self.storage = TodoStorage()
        self.storage.add("Incomplete task 1")
        self.storage.add("Completed task 1")
        self.storage.complete(2)
        self.storage.add("Incomplete task 2")
        self.storage.add("Completed task 2")
        self.storage.complete(4)

        self.service = SearchFilterService(self.storage)

    def test_filter_by_status_completed(self):
        """Filter should return only completed todos"""
        result = self.service.filter_by_status("completed")
        assert len(result) == 2
        assert all(t.completed for t in result)

    def test_filter_by_status_incomplete(self):
        """Filter should return only incomplete todos"""
        result = self.service.filter_by_status("incomplete")
        assert len(result) == 2
        assert all(not t.completed for t in result)

    def test_filter_by_status_all(self):
        """Filter 'all' should return all todos"""
        result = self.service.filter_by_status("all")
        assert len(result) == 4


class TestSortByDueDate:
    """Test due date sorting functionality (already implemented)"""

    def setup_method(self):
        """Set up test storage with todos of different due dates"""
        self.storage = TodoStorage()
        today = date.today()

        self.storage.add("Overdue task")
        self.storage.todos[1].due_date = today - timedelta(days=1)

        self.storage.add("Due today")
        self.storage.todos[2].due_date = today

        self.storage.add("Due tomorrow")
        self.storage.todos[3].due_date = today + timedelta(days=1)

        self.storage.add("No due date")
        # Leave due_date as None

        self.service = SearchFilterService(self.storage)

    def test_sort_by_due_date_order(self):
        """Todos should be sorted overdue → today → upcoming → no date"""
        todos = self.storage.list_all()
        sorted_todos = self.service.sort_by_due_date(todos)

        assert len(sorted_todos) == 4
        assert "Overdue" in sorted_todos[0].title
        assert "today" in sorted_todos[1].title
        assert "tomorrow" in sorted_todos[2].title
        assert sorted_todos[3].due_date is None


class TestFilterByDueDateRange:
    """Test filter_by_due_date_range() method (NEW for Phase 8)"""

    def setup_method(self):
        """Set up test storage with various due dates"""
        self.storage = TodoStorage()
        today = date.today()

        # Overdue (2 days ago)
        self.storage.add("Overdue task")
        self.storage.todos[1].due_date = today - timedelta(days=2)

        # Due today
        self.storage.add("Task due today")
        self.storage.todos[2].due_date = today

        # Due tomorrow
        self.storage.add("Task due tomorrow")
        self.storage.todos[3].due_date = today + timedelta(days=1)

        # Due in 5 days (this week)
        self.storage.add("Task due this week")
        self.storage.todos[4].due_date = today + timedelta(days=5)

        # Due in 15 days (this month)
        self.storage.add("Task due this month")
        self.storage.todos[5].due_date = today + timedelta(days=15)

        # No due date
        self.storage.add("Task with no due date")

        self.service = SearchFilterService(self.storage)

    def test_filter_by_due_date_range_overdue(self):
        """Should return only overdue todos"""
        results = self.service.filter_by_due_date_range("overdue")
        assert len(results) == 1
        assert results[0].id == 1

    def test_filter_by_due_date_range_today(self):
        """Should return only todos due today"""
        results = self.service.filter_by_due_date_range("today")
        assert len(results) == 1
        assert results[0].id == 2

    def test_filter_by_due_date_range_week(self):
        """Should return todos due within 7 days (including overdue and today)"""
        results = self.service.filter_by_due_date_range("week")
        # Should include: overdue (1), today (2), tomorrow (3), this week (4)
        assert len(results) == 4
        assert {t.id for t in results} == {1, 2, 3, 4}

    def test_filter_by_due_date_range_month(self):
        """Should return todos due within 30 days (including overdue and today)"""
        results = self.service.filter_by_due_date_range("month")
        # Should include: overdue (1), today (2), tomorrow (3), this week (4), this month (5)
        assert len(results) == 5
        assert {t.id for t in results} == {1, 2, 3, 4, 5}

    def test_filter_by_due_date_range_none(self):
        """Should return todos with no due date"""
        results = self.service.filter_by_due_date_range("none")
        assert len(results) == 1
        assert results[0].id == 6
        assert results[0].due_date is None

    def test_filter_by_due_date_range_invalid_raises_error(self):
        """Should raise ValueError for invalid range"""
        with pytest.raises(ValueError, match="Range must be one of"):
            self.service.filter_by_due_date_range("invalid")


class TestApplyCombinedFilters:
    """Test apply_combined_filters() method for multi-criteria filtering (NEW for Phase 8)"""

    def setup_method(self):
        """Set up test storage with varied todos"""
        self.storage = TodoStorage()
        today = date.today()

        # Task 1: High priority, Work category, due today, incomplete
        self.storage.add("Fix critical bug")
        self.storage.todos[1].priority = "High"
        self.storage.todos[1].category = "Work"
        self.storage.todos[1].due_date = today
        self.storage.todos[1].tags = ["urgent", "bug"]

        # Task 2: High priority, Work category, overdue, incomplete
        self.storage.add("Deploy hotfix")
        self.storage.todos[2].priority = "High"
        self.storage.todos[2].category = "Work"
        self.storage.todos[2].due_date = today - timedelta(days=1)
        self.storage.todos[2].tags = ["urgent"]

        # Task 3: Medium priority, Personal category, due tomorrow, incomplete
        self.storage.add("Buy groceries")
        self.storage.todos[3].priority = "Medium"
        self.storage.todos[3].category = "Personal"
        self.storage.todos[3].due_date = today + timedelta(days=1)

        # Task 4: Low priority, Work category, no due date, completed
        self.storage.add("Update documentation")
        self.storage.todos[4].priority = "Low"
        self.storage.todos[4].category = "Work"
        self.storage.todos[4].completed = True

        self.service = SearchFilterService(self.storage)

    def test_apply_combined_filters_status_and_priority(self):
        """Should filter by status AND priority"""
        criteria = {
            "status": "incomplete",
            "priority": "High"
        }
        results = self.service.apply_combined_filters(criteria)
        assert len(results) == 2
        assert {t.id for t in results} == {1, 2}

    def test_apply_combined_filters_category_and_status(self):
        """Should filter by category AND status"""
        criteria = {
            "category": "Work",
            "status": "incomplete"
        }
        results = self.service.apply_combined_filters(criteria)
        assert len(results) == 2
        assert {t.id for t in results} == {1, 2}

    def test_apply_combined_filters_all_criteria(self):
        """Should filter by all criteria at once"""
        criteria = {
            "status": "incomplete",
            "priority": "High",
            "category": "Work",
            "due_date_range": "week"
        }
        results = self.service.apply_combined_filters(criteria)
        # Should match task 1 and 2 (both High, Work, incomplete, due within week)
        assert len(results) == 2
        assert {t.id for t in results} == {1, 2}

    def test_apply_combined_filters_no_matches(self):
        """Should return empty list when no todos match all criteria"""
        criteria = {
            "status": "completed",
            "priority": "High"
        }
        results = self.service.apply_combined_filters(criteria)
        assert results == []

    def test_apply_combined_filters_empty_criteria(self):
        """Should return all todos when criteria is empty"""
        criteria = {}
        results = self.service.apply_combined_filters(criteria)
        assert len(results) == 4

    def test_apply_combined_filters_with_tag(self):
        """Should filter by tag combined with other criteria"""
        criteria = {
            "tag": "urgent",
            "category": "Work"
        }
        results = self.service.apply_combined_filters(criteria)
        assert len(results) == 2
        assert {t.id for t in results} == {1, 2}


class TestSortByCreatedDate:
    """Test sort_by_created_date() method (NEW for Phase 8)"""

    def setup_method(self):
        """Set up test storage with todos created at different times"""
        from datetime import datetime, timedelta
        self.storage = TodoStorage()

        # Create todos with manually set created_date to ensure proper ordering
        self.storage.add("First task")
        self.storage.todos[1].created_date = datetime(2025, 1, 1, 10, 0, 0)

        self.storage.add("Second task")
        self.storage.todos[2].created_date = datetime(2025, 1, 2, 10, 0, 0)

        self.storage.add("Third task")
        self.storage.todos[3].created_date = datetime(2025, 1, 3, 10, 0, 0)

        self.service = SearchFilterService(self.storage)

    def test_sort_by_created_date_oldest_first(self):
        """Should sort by created_date timestamp (oldest first)"""
        todos = self.storage.list_all()
        sorted_todos = self.service.sort_by_created_date(todos)
        # Should be in creation order: 1, 2, 3
        assert [t.id for t in sorted_todos] == [1, 2, 3]

    def test_sort_by_created_date_newest_first(self):
        """Should sort by created_date timestamp (newest first when reverse=True)"""
        todos = self.storage.list_all()
        sorted_todos = self.service.sort_by_created_date(todos, reverse=True)
        # Should be in reverse creation order: 3, 2, 1
        assert [t.id for t in sorted_todos] == [3, 2, 1]


class TestSortByTitle:
    """Test sort_by_title() method (NEW for Phase 8)"""

    def setup_method(self):
        """Set up test storage with todos with different titles"""
        self.storage = TodoStorage()

        self.storage.add("Zebra task")
        self.storage.add("Alpha task")
        self.storage.add("Beta task")

        self.service = SearchFilterService(self.storage)

    def test_sort_by_title_alphabetical(self):
        """Should sort alphabetically by title"""
        todos = self.storage.list_all()
        sorted_todos = self.service.sort_by_title(todos)
        # Alphabetical order: Alpha (2), Beta (3), Zebra (1)
        assert [t.id for t in sorted_todos] == [2, 3, 1]

    def test_sort_by_title_case_insensitive(self):
        """Should sort case-insensitively"""
        self.storage.add("apple task")
        self.storage.add("BANANA task")
        todos = self.storage.list_all()
        sorted_todos = self.service.sort_by_title(todos)
        # Should be: Alpha, apple, BANANA, Beta, Zebra
        titles = [t.title for t in sorted_todos]
        assert titles == ["Alpha task", "apple task", "BANANA task", "Beta task", "Zebra task"]
