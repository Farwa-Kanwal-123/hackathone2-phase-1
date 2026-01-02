"""
TodoItem entity and validation logic

Defines the core TodoItem dataclass with validation rules.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from src.exceptions import ValidationError


@dataclass
class TodoItem:
    """
    Represents a single todo item.

    Attributes:
        id: Unique identifier (assigned by storage)
        title: Todo description (1-200 characters, non-empty)
        completed: Whether the todo is done (defaults to False)
        priority: Priority level (High, Medium, Low, or None)
        due_date: Optional due date (datetime.date object)
        category: Optional category name (e.g., "Work", "Personal")
        tags: Optional list of tags (e.g., ["urgent", "bug-fix"])
        created_date: Timestamp when todo was created
        updated_date: Timestamp when todo was last updated
    """
    id: int
    title: str
    completed: bool = False
    priority: Optional[str] = None
    due_date: Optional[date] = None
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """
        Validate fields after initialization.

        Raises:
            ValidationError: If any field fails validation
        """
        # Existing validation: title
        stripped_title = self.title.strip()
        if not stripped_title:
            raise ValidationError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")

        # New validation: priority
        if self.priority is not None:
            if self.priority not in ["High", "Medium", "Low"]:
                raise ValidationError(
                    f"Priority must be 'High', 'Medium', 'Low', or None. Got: {self.priority}"
                )

        # New validation: due_date
        if self.due_date is not None:
            if not isinstance(self.due_date, date):
                raise ValidationError(
                    f"due_date must be a datetime.date object. Got: {type(self.due_date)}"
                )

        # New validation: category
        if self.category is not None:
            if not isinstance(self.category, str):
                raise ValidationError("category must be a string")
            if len(self.category) > 50:
                raise ValidationError("category cannot exceed 50 characters")

        # New validation: tags
        if not isinstance(self.tags, list):
            raise ValidationError("tags must be a list")
        for tag in self.tags:
            if not isinstance(tag, str):
                raise ValidationError(f"All tags must be strings. Got: {type(tag)}")
            if len(tag) > 30:
                raise ValidationError(f"Tag '{tag}' exceeds 30 characters")
