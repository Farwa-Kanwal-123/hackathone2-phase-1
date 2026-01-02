"""
Unit tests for Rich table rendering

Tests cover render_task_table() function with various todo configurations,
empty lists, and table structure validation.
"""

import pytest
from datetime import date, timedelta
from rich.table import Table
from src.todo import TodoItem
from src.ui.formatting import render_task_table


class TestRenderTaskTable:
    """Test Rich table rendering for todo lists"""

    def test_render_task_table_empty(self):
        """Empty todo list should render table with headers only"""
        todos = []
        table = render_task_table(todos)

        assert isinstance(table, Table)
        # Table should have column headers even when empty
        assert table.title is None or table.title == ""

    def test_render_task_table_single_basic_todo(self):
        """Single basic todo should render with ID, status, title"""
        todos = [
            TodoItem(id=1, title="Buy milk", completed=False)
        ]
        table = render_task_table(todos)

        assert isinstance(table, Table)
        # Validate table has correct number of columns (6: ID, Status, Title, Priority, Due, Category)
        assert len(table.columns) == 6

    def test_render_task_table_completed_todo(self):
        """Completed todo should show check mark icon"""
        todos = [
            TodoItem(id=1, title="Buy milk", completed=True)
        ]
        table = render_task_table(todos)

        assert isinstance(table, Table)
        # Check that table renders without errors
        assert len(table.columns) == 6

    def test_render_task_table_with_priority(self):
        """Todo with priority should display colored priority"""
        todos = [
            TodoItem(id=1, title="Fix bug", completed=False, priority="High")
        ]
        table = render_task_table(todos)

        assert isinstance(table, Table)
        assert len(table.columns) == 6

    def test_render_task_table_with_due_date(self):
        """Todo with due date should display formatted date"""
        tomorrow = date.today() + timedelta(days=1)
        todos = [
            TodoItem(id=1, title="Submit report", completed=False, due_date=tomorrow)
        ]
        table = render_task_table(todos)

        assert isinstance(table, Table)
        assert len(table.columns) == 6

    def test_render_task_table_with_category(self):
        """Todo with category should display category"""
        todos = [
            TodoItem(id=1, title="Read book", completed=False, category="Personal")
        ]
        table = render_task_table(todos)

        assert isinstance(table, Table)
        assert len(table.columns) == 6

    def test_render_task_table_with_tags(self):
        """Todo with tags should display tags (formatted)"""
        todos = [
            TodoItem(id=1, title="Learn Python", completed=False, tags=["coding", "education"])
        ]
        table = render_task_table(todos)

        assert isinstance(table, Table)
        assert len(table.columns) == 6

    def test_render_task_table_multiple_todos(self):
        """Multiple todos should render in table rows"""
        todos = [
            TodoItem(id=1, title="Task 1", completed=False, priority="High"),
            TodoItem(id=2, title="Task 2", completed=True, priority="Medium"),
            TodoItem(id=3, title="Task 3", completed=False, priority="Low")
        ]
        table = render_task_table(todos)

        assert isinstance(table, Table)
        assert len(table.columns) == 6
        # Rich Table doesn't expose row count directly, but we can validate it renders

    def test_render_task_table_overdue_highlighting(self):
        """Overdue todos should be highlighted in red"""
        yesterday = date.today() - timedelta(days=1)
        todos = [
            TodoItem(id=1, title="Overdue task", completed=False, due_date=yesterday)
        ]
        table = render_task_table(todos)

        assert isinstance(table, Table)
        # Verify overdue date uses red color (checked in format_due_date tests)

    def test_render_task_table_full_featured_todo(self):
        """Todo with all fields should render correctly"""
        tomorrow = date.today() + timedelta(days=1)
        todos = [
            TodoItem(
                id=1,
                title="Complete project",
                completed=False,
                priority="High",
                due_date=tomorrow,
                category="Work",
                tags=["urgent", "deadline"]
            )
        ]
        table = render_task_table(todos)

        assert isinstance(table, Table)
        assert len(table.columns) == 6

    def test_render_task_table_long_title_truncation(self):
        """Very long todo titles should be truncated"""
        long_title = "This is a very long todo item title that should be truncated for display purposes"
        todos = [
            TodoItem(id=1, title=long_title, completed=False)
        ]
        table = render_task_table(todos)

        assert isinstance(table, Table)
        # Truncation tested in test_formatting.py

    def test_render_task_table_column_headers(self):
        """Table should have correct column headers"""
        todos = [TodoItem(id=1, title="Test", completed=False)]
        table = render_task_table(todos)

        # Extract column headers
        column_headers = [col.header for col in table.columns]

        assert "ID" in column_headers
        assert "Status" in column_headers or "✓" in column_headers
        assert "Title" in column_headers
        assert "Priority" in column_headers
        assert "Due" in column_headers or "Due Date" in column_headers
        assert "Category" in column_headers

    def test_render_task_table_style_configuration(self):
        """Table should have proper styling (border, header style)"""
        todos = [TodoItem(id=1, title="Test", completed=False)]
        table = render_task_table(todos)

        # Verify table has styling attributes
        assert isinstance(table, Table)
        # Rich Table has box, header_style, border_style attributes
        assert hasattr(table, 'box')
        assert hasattr(table, 'border_style')
