"""
Custom exception classes for Todo CLI Core.

These exceptions provide user-friendly error messages while maintaining
clean error handling throughout the application.
"""


class TodoError(Exception):
    """Base exception for all todo-related errors."""
    pass


class ValidationError(TodoError):
    """Raised when input validation fails (empty title, title too long, etc.)."""
    pass


class NotFoundError(TodoError):
    """Raised when a todo item is not found by its ID."""
    pass


class InvalidInputError(TodoError):
    """Raised when user provides invalid input (non-numeric ID, etc.)."""
    pass


class DateParseError(TodoError):
    """Raised when date parsing fails."""
    pass


class FilterValidationError(TodoError):
    """Raised when filter parameters are invalid."""
    pass
