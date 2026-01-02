"""
Search and filter service

Provides search, filter, and sort operations for TodoItems.
"""

from typing import List, Optional
from src.storage import TodoStorage
from src.todo import TodoItem
from datetime import date, timedelta

# Priority ordering for sorting (High → Medium → Low → None)
PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3, None: 4}


class SearchFilterService:
    """
    Service for searching, filtering, and sorting todos.

    All methods are stateless and return new lists (do not modify storage).
    """

    def __init__(self, storage: TodoStorage):
        """
        Initialize search/filter service.

        Args:
            storage: TodoStorage instance (read-only access)
        """
        self.storage = storage

    def search(self, query: str) -> List[TodoItem]:
        """
        Search todos by title keyword (case-insensitive).

        Args:
            query: Search keyword (partial match allowed)

        Returns:
            List of matching TodoItem objects (empty if no matches)

        Raises:
            ValueError: If query is empty or whitespace-only

        Example:
            >>> service.search("bug")
            [TodoItem(id=1, title="Fix bug in auth"), TodoItem(id=5, title="Debug API")]
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        query_lower = query.lower()
        todos = self.storage.list_all()

        return [t for t in todos if query_lower in t.title.lower()]

    def filter_by_priority(self, priority: str) -> List[TodoItem]:
        """
        Filter todos by priority level.

        Args:
            priority: "High", "Medium", "Low", or "None"

        Returns:
            List of TodoItem objects with matching priority

        Raises:
            ValueError: If priority is not valid
        """
        valid_priorities = ["High", "Medium", "Low", "None"]
        if priority not in valid_priorities:
            raise ValueError(
                f"Priority must be one of {valid_priorities}. Got: {priority}"
            )

        todos = self.storage.list_all()

        if priority == "None":
            return [t for t in todos if t.priority is None]
        else:
            return [t for t in todos if t.priority == priority]

    def filter_by_status(self, status: str) -> List[TodoItem]:
        """
        Filter todos by completion status.

        Args:
            status: "completed", "incomplete", or "all"

        Returns:
            List of TodoItem objects matching status

        Raises:
            ValueError: If status is not valid
        """
        valid_statuses = ["completed", "incomplete", "all"]
        if status not in valid_statuses:
            raise ValueError(
                f"Status must be one of {valid_statuses}. Got: {status}"
            )

        todos = self.storage.list_all()

        if status == "all":
            return todos
        elif status == "completed":
            return [t for t in todos if t.completed]
        else:  # incomplete
            return [t for t in todos if not t.completed]

    def sort_by_priority(self, todos: List[TodoItem]) -> List[TodoItem]:
        """
        Sort todos by priority (High → Medium → Low → None).

        Args:
            todos: List of TodoItem objects to sort

        Returns:
            New list sorted by priority (original list unchanged)
        """
        return sorted(todos, key=lambda t: PRIORITY_ORDER.get(t.priority, 4))

    def sort_by_due_date(self, todos: List[TodoItem]) -> List[TodoItem]:
        """
        Sort todos by due date (overdue → today → upcoming → no date).

        Args:
            todos: List of TodoItem objects to sort

        Returns:
            New list sorted by due date (original list unchanged)
        """
        def due_date_key(todo: TodoItem):
            if todo.due_date is None:
                return (3, date.max)  # No date last

            today = date.today()
            if todo.due_date < today:
                return (0, todo.due_date)  # Overdue first
            elif todo.due_date == today:
                return (1, todo.due_date)  # Today second
            else:
                return (2, todo.due_date)  # Upcoming third

        return sorted(todos, key=due_date_key)

    def filter_by_category(self, category: Optional[str]) -> List[TodoItem]:
        """
        Filter todos by category.

        Args:
            category: Category name to filter by, or None for uncategorized

        Returns:
            List of todos matching the category

        Raises:
            ValueError: If category is empty string or whitespace-only

        Example:
            >>> service = SearchFilterService(storage)
            >>> work_todos = service.filter_by_category("Work")
        """
        # Allow None (for uncategorized todos)
        if category == "":
            raise ValueError("Category cannot be empty")

        if category is not None and category.strip() == "":
            raise ValueError("Category cannot be empty")

        todos = self.storage.list_all()
        return [t for t in todos if t.category == category]

    def filter_by_tag(self, tag: str) -> List[TodoItem]:
        """
        Filter todos by tag.

        Args:
            tag: Tag to search for (exact match)

        Returns:
            List of todos containing the tag

        Raises:
            ValueError: If tag is empty string or whitespace-only

        Example:
            >>> service = SearchFilterService(storage)
            >>> urgent_todos = service.filter_by_tag("urgent")
        """
        if not tag or tag.strip() == "":
            raise ValueError("Tag cannot be empty")

        todos = self.storage.list_all()
        return [t for t in todos if tag in t.tags]

    def _filter_by_date_range_logic(self, todos: List[TodoItem], range_type: str) -> List[TodoItem]:
        """
        Helper method to apply date range filtering logic.

        Args:
            todos: List of todos to filter
            range_type: One of "overdue", "today", "week", "month", "none"

        Returns:
            Filtered list of todos

        Note: This is a private helper method used by filter_by_due_date_range()
              and apply_combined_filters() to avoid code duplication.
        """
        today = date.today()

        if range_type == "none":
            return [t for t in todos if t.due_date is None]
        elif range_type == "overdue":
            return [t for t in todos if t.due_date is not None and t.due_date < today]
        elif range_type == "today":
            return [t for t in todos if t.due_date == today]
        elif range_type == "week":
            # Due within 7 days (including past, today, and up to 7 days in future)
            week_end = today + timedelta(days=7)
            return [t for t in todos if t.due_date is not None and t.due_date <= week_end]
        elif range_type == "month":
            # Due within 30 days (including past, today, and up to 30 days in future)
            month_end = today + timedelta(days=30)
            return [t for t in todos if t.due_date is not None and t.due_date <= month_end]

        return todos  # Fallback (should not reach here with validation)

    def filter_by_due_date_range(self, range_type: str) -> List[TodoItem]:
        """
        Filter todos by due date range.

        Args:
            range_type: One of "overdue", "today", "week", "month", "none"
                - overdue: Due date in the past
                - today: Due date is today
                - week: Due within 7 days (including overdue and today)
                - month: Due within 30 days (including overdue and today)
                - none: No due date set

        Returns:
            List of todos matching the date range

        Raises:
            ValueError: If range_type is not valid

        Example:
            >>> service = SearchFilterService(storage)
            >>> overdue_todos = service.filter_by_due_date_range("overdue")
        """
        valid_ranges = ["overdue", "today", "week", "month", "none"]
        if range_type not in valid_ranges:
            raise ValueError(
                f"Range must be one of {valid_ranges}. Got: {range_type}"
            )

        todos = self.storage.list_all()
        return self._filter_by_date_range_logic(todos, range_type)

    def apply_combined_filters(self, criteria: dict) -> List[TodoItem]:
        """
        Apply multiple filters with AND logic.

        Args:
            criteria: Dictionary with filter criteria:
                - "status": "completed", "incomplete", or "all"
                - "priority": "High", "Medium", "Low", or "None"
                - "category": category name or None
                - "tag": tag name
                - "due_date_range": "overdue", "today", "week", "month", or "none"

        Returns:
            List of todos matching ALL criteria

        Example:
            >>> criteria = {"status": "incomplete", "priority": "High", "category": "Work"}
            >>> urgent_work = service.apply_combined_filters(criteria)
        """
        todos = self.storage.list_all()

        # Apply each filter if present in criteria
        if "status" in criteria:
            if criteria["status"] == "completed":
                todos = [t for t in todos if t.completed]
            elif criteria["status"] == "incomplete":
                todos = [t for t in todos if not t.completed]
            # "all" means no filtering

        if "priority" in criteria:
            priority = criteria["priority"]
            if priority == "None":
                todos = [t for t in todos if t.priority is None]
            else:
                todos = [t for t in todos if t.priority == priority]

        if "category" in criteria:
            todos = [t for t in todos if t.category == criteria["category"]]

        if "tag" in criteria:
            tag = criteria["tag"]
            todos = [t for t in todos if tag in t.tags]

        if "due_date_range" in criteria:
            range_type = criteria["due_date_range"]
            todos = self._filter_by_date_range_logic(todos, range_type)

        return todos

    def sort_by_created_date(self, todos: List[TodoItem], reverse: bool = False) -> List[TodoItem]:
        """
        Sort todos by created_date timestamp.

        Args:
            todos: List of TodoItem objects to sort
            reverse: If True, sort newest first; if False, oldest first (default)

        Returns:
            New list sorted by created_date (original list unchanged)

        Example:
            >>> oldest_first = service.sort_by_created_date(todos)
            >>> newest_first = service.sort_by_created_date(todos, reverse=True)
        """
        return sorted(todos, key=lambda t: t.created_date, reverse=reverse)

    def sort_by_title(self, todos: List[TodoItem]) -> List[TodoItem]:
        """
        Sort todos alphabetically by title (case-insensitive).

        Args:
            todos: List of TodoItem objects to sort

        Returns:
            New list sorted by title (original list unchanged)

        Example:
            >>> alphabetical = service.sort_by_title(todos)
        """
        return sorted(todos, key=lambda t: t.title.lower())
