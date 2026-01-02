"""
Unit tests for StatisticsService

Tests statistics calculation methods:
- get_completion_stats() - completion percentage and counts
- get_priority_breakdown() - count by priority level
- get_category_breakdown() - count by category
- get_overdue_count() - count of overdue todos
"""

import pytest
from datetime import date, timedelta
from src.storage import TodoStorage
from src.services.statistics import StatisticsService


class TestGetCompletionStats:
    """Test get_completion_stats() method"""

    def setup_method(self):
        """Set up test storage with varied completion states"""
        self.storage = TodoStorage()

        # 3 completed
        self.storage.add("Completed task 1")
        self.storage.complete(1)
        self.storage.add("Completed task 2")
        self.storage.complete(2)
        self.storage.add("Completed task 3")
        self.storage.complete(3)

        # 2 incomplete
        self.storage.add("Incomplete task 1")
        self.storage.add("Incomplete task 2")

        self.service = StatisticsService(self.storage)

    def test_completion_stats_calculates_percentage(self):
        """Should calculate completion percentage correctly"""
        stats = self.service.get_completion_stats()
        assert stats["percentage"] == 60.0  # 3/5 = 60%

    def test_completion_stats_counts_total(self):
        """Should count total todos correctly"""
        stats = self.service.get_completion_stats()
        assert stats["total"] == 5

    def test_completion_stats_counts_completed(self):
        """Should count completed todos correctly"""
        stats = self.service.get_completion_stats()
        assert stats["completed"] == 3

    def test_completion_stats_counts_incomplete(self):
        """Should count incomplete todos correctly"""
        stats = self.service.get_completion_stats()
        assert stats["incomplete"] == 2

    def test_completion_stats_empty_storage(self):
        """Should handle empty storage"""
        empty_storage = TodoStorage()
        service = StatisticsService(empty_storage)
        stats = service.get_completion_stats()

        assert stats["total"] == 0
        assert stats["completed"] == 0
        assert stats["incomplete"] == 0
        assert stats["percentage"] == 0.0

    def test_completion_stats_all_completed(self):
        """Should handle 100% completion"""
        all_complete_storage = TodoStorage()
        all_complete_storage.add("Task 1")
        all_complete_storage.complete(1)
        all_complete_storage.add("Task 2")
        all_complete_storage.complete(2)

        service = StatisticsService(all_complete_storage)
        stats = service.get_completion_stats()

        assert stats["percentage"] == 100.0

    def test_completion_stats_all_incomplete(self):
        """Should handle 0% completion"""
        all_incomplete_storage = TodoStorage()
        all_incomplete_storage.add("Task 1")
        all_incomplete_storage.add("Task 2")

        service = StatisticsService(all_incomplete_storage)
        stats = service.get_completion_stats()

        assert stats["percentage"] == 0.0


class TestGetPriorityBreakdown:
    """Test get_priority_breakdown() method"""

    def setup_method(self):
        """Set up test storage with varied priorities"""
        self.storage = TodoStorage()

        # High priority: 2
        self.storage.add("High priority task 1")
        self.storage.todos[1].priority = "High"
        self.storage.add("High priority task 2")
        self.storage.todos[2].priority = "High"

        # Medium priority: 3
        self.storage.add("Medium priority task 1")
        self.storage.todos[3].priority = "Medium"
        self.storage.add("Medium priority task 2")
        self.storage.todos[4].priority = "Medium"
        self.storage.add("Medium priority task 3")
        self.storage.todos[5].priority = "Medium"

        # Low priority: 1
        self.storage.add("Low priority task")
        self.storage.todos[6].priority = "Low"

        # None priority: 2
        self.storage.add("No priority task 1")
        self.storage.add("No priority task 2")

        self.service = StatisticsService(self.storage)

    def test_priority_breakdown_counts_high(self):
        """Should count High priority todos correctly"""
        breakdown = self.service.get_priority_breakdown()
        assert breakdown["High"] == 2

    def test_priority_breakdown_counts_medium(self):
        """Should count Medium priority todos correctly"""
        breakdown = self.service.get_priority_breakdown()
        assert breakdown["Medium"] == 3

    def test_priority_breakdown_counts_low(self):
        """Should count Low priority todos correctly"""
        breakdown = self.service.get_priority_breakdown()
        assert breakdown["Low"] == 1

    def test_priority_breakdown_counts_none(self):
        """Should count None priority todos correctly"""
        breakdown = self.service.get_priority_breakdown()
        assert breakdown["None"] == 2

    def test_priority_breakdown_all_keys_present(self):
        """Should include all priority levels in breakdown"""
        breakdown = self.service.get_priority_breakdown()
        assert set(breakdown.keys()) == {"High", "Medium", "Low", "None"}

    def test_priority_breakdown_empty_storage(self):
        """Should handle empty storage"""
        empty_storage = TodoStorage()
        service = StatisticsService(empty_storage)
        breakdown = service.get_priority_breakdown()

        assert breakdown["High"] == 0
        assert breakdown["Medium"] == 0
        assert breakdown["Low"] == 0
        assert breakdown["None"] == 0

    def test_priority_breakdown_single_priority(self):
        """Should handle storage with only one priority type"""
        single_priority_storage = TodoStorage()
        single_priority_storage.add("Task 1")
        single_priority_storage.todos[1].priority = "High"
        single_priority_storage.add("Task 2")
        single_priority_storage.todos[2].priority = "High"

        service = StatisticsService(single_priority_storage)
        breakdown = service.get_priority_breakdown()

        assert breakdown["High"] == 2
        assert breakdown["Medium"] == 0
        assert breakdown["Low"] == 0
        assert breakdown["None"] == 0


class TestGetCategoryBreakdown:
    """Test get_category_breakdown() method"""

    def setup_method(self):
        """Set up test storage with varied categories"""
        self.storage = TodoStorage()

        # Work: 3
        self.storage.add("Work task 1")
        self.storage.todos[1].category = "Work"
        self.storage.add("Work task 2")
        self.storage.todos[2].category = "Work"
        self.storage.add("Work task 3")
        self.storage.todos[3].category = "Work"

        # Personal: 2
        self.storage.add("Personal task 1")
        self.storage.todos[4].category = "Personal"
        self.storage.add("Personal task 2")
        self.storage.todos[5].category = "Personal"

        # Uncategorized (None): 1
        self.storage.add("Uncategorized task")

        self.service = StatisticsService(self.storage)

    def test_category_breakdown_counts_categories(self):
        """Should count each category correctly"""
        breakdown = self.service.get_category_breakdown()
        assert breakdown["Work"] == 3
        assert breakdown["Personal"] == 2
        assert breakdown["Uncategorized"] == 1

    def test_category_breakdown_includes_uncategorized(self):
        """Should include uncategorized (None) todos"""
        breakdown = self.service.get_category_breakdown()
        assert "Uncategorized" in breakdown
        assert breakdown["Uncategorized"] == 1

    def test_category_breakdown_empty_storage(self):
        """Should handle empty storage"""
        empty_storage = TodoStorage()
        service = StatisticsService(empty_storage)
        breakdown = service.get_category_breakdown()

        assert breakdown == {}

    def test_category_breakdown_all_uncategorized(self):
        """Should handle storage with only uncategorized todos"""
        uncategorized_storage = TodoStorage()
        uncategorized_storage.add("Task 1")
        uncategorized_storage.add("Task 2")

        service = StatisticsService(uncategorized_storage)
        breakdown = service.get_category_breakdown()

        assert breakdown == {"Uncategorized": 2}

    def test_category_breakdown_sorted_by_count(self):
        """Should return categories sorted by count (descending)"""
        breakdown = self.service.get_category_breakdown()
        counts = list(breakdown.values())

        # Verify counts are in descending order
        assert counts == sorted(counts, reverse=True)


class TestGetOverdueCount:
    """Test get_overdue_count() method"""

    def setup_method(self):
        """Set up test storage with varied due dates"""
        self.storage = TodoStorage()
        today = date.today()

        # Overdue (3 days ago): incomplete
        self.storage.add("Overdue task 1")
        self.storage.todos[1].due_date = today - timedelta(days=3)

        # Overdue (1 day ago): incomplete
        self.storage.add("Overdue task 2")
        self.storage.todos[2].due_date = today - timedelta(days=1)

        # Overdue (2 days ago): completed (should not count)
        self.storage.add("Overdue but completed")
        self.storage.todos[3].due_date = today - timedelta(days=2)
        self.storage.complete(3)

        # Due today: incomplete (not overdue)
        self.storage.add("Due today")
        self.storage.todos[4].due_date = today

        # Due tomorrow: incomplete (not overdue)
        self.storage.add("Due tomorrow")
        self.storage.todos[5].due_date = today + timedelta(days=1)

        # No due date: incomplete (not overdue)
        self.storage.add("No due date")

        self.service = StatisticsService(self.storage)

    def test_overdue_count_counts_overdue_incomplete(self):
        """Should count only incomplete overdue todos"""
        count = self.service.get_overdue_count()
        assert count == 2

    def test_overdue_count_excludes_completed(self):
        """Should not count completed overdue todos"""
        # Verify by checking the actual count
        count = self.service.get_overdue_count()
        assert count == 2  # Only 2 incomplete overdue

    def test_overdue_count_excludes_today(self):
        """Should not count todos due today"""
        count = self.service.get_overdue_count()
        assert count == 2  # Does not include today's todo

    def test_overdue_count_excludes_future(self):
        """Should not count todos due in the future"""
        count = self.service.get_overdue_count()
        assert count == 2  # Does not include future todos

    def test_overdue_count_empty_storage(self):
        """Should return 0 for empty storage"""
        empty_storage = TodoStorage()
        service = StatisticsService(empty_storage)
        count = service.get_overdue_count()

        assert count == 0

    def test_overdue_count_no_overdue(self):
        """Should return 0 when no todos are overdue"""
        no_overdue_storage = TodoStorage()
        today = date.today()

        no_overdue_storage.add("Due tomorrow")
        no_overdue_storage.todos[1].due_date = today + timedelta(days=1)

        service = StatisticsService(no_overdue_storage)
        count = service.get_overdue_count()

        assert count == 0
