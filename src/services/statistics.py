"""
Statistics service

Calculates completion percentages, breakdowns, and overdue counts.
"""

from src.storage import TodoStorage
from datetime import date


class StatisticsService:
    """
    Service for calculating todo statistics.

    Provides completion percentage, priority breakdown, category breakdown,
    and overdue count calculations.
    """

    def __init__(self, storage: TodoStorage):
        """
        Initialize statistics service.

        Args:
            storage: TodoStorage instance (read-only access)
        """
        self.storage = storage

    def get_completion_stats(self) -> dict:
        """
        Calculate completion percentage and counts.

        Returns:
            Dictionary with total, completed, incomplete, and percentage

        Example:
            >>> stats.get_completion_stats()
            {"total": 10, "completed": 4, "incomplete": 6, "percentage": 40.0}
        """
        todos = self.storage.list_all()
        total = len(todos)
        completed = sum(1 for t in todos if t.completed)
        incomplete = total - completed

        return {
            "total": total,
            "completed": completed,
            "incomplete": incomplete,
            "percentage": (completed / total * 100) if total > 0 else 0.0
        }

    def get_priority_breakdown(self) -> dict:
        """
        Count tasks by priority level.

        Returns:
            Dictionary mapping priority levels to counts (None mapped to "None" string)

        Example:
            >>> stats.get_priority_breakdown()
            {"High": 2, "Medium": 5, "Low": 3, "None": 0}
        """
        todos = self.storage.list_all()
        breakdown = {"High": 0, "Medium": 0, "Low": 0, "None": 0}

        for todo in todos:
            priority = todo.priority if todo.priority else "None"
            if priority in breakdown:
                breakdown[priority] += 1

        return breakdown

    def get_category_breakdown(self) -> dict:
        """
        Count tasks by category.

        Returns:
            Dictionary mapping category names to counts (None mapped to "Uncategorized")
            Sorted by count descending

        Example:
            >>> stats.get_category_breakdown()
            {"Work": 5, "Personal": 3, "Uncategorized": 2}
        """
        todos = self.storage.list_all()
        breakdown = {}

        for todo in todos:
            category = todo.category if todo.category else "Uncategorized"
            breakdown[category] = breakdown.get(category, 0) + 1

        # Sort by count descending
        return dict(sorted(breakdown.items(), key=lambda x: x[1], reverse=True))

    def get_overdue_count(self) -> int:
        """
        Count overdue incomplete tasks.

        Returns:
            Number of incomplete tasks with due_date < today

        Example:
            >>> stats.get_overdue_count()
            2
        """
        todos = self.storage.list_all()
        today = date.today()

        return sum(1 for t in todos if t.due_date and t.due_date < today and not t.completed)
