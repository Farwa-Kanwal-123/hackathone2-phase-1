"""
Main entry point for Todo CLI

Orchestrates storage initialization, argument parsing, command routing,
and error handling.
"""

import sys
from src.cli import (
    create_parser,
    handle_add,
    handle_list,
    handle_complete,
    handle_delete,
    handle_update,
)
from src.storage import TodoStorage
from src.exceptions import TodoError, ValidationError, NotFoundError, InvalidInputError


def main() -> int:
    """
    Main entry point for the CLI application.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Initialize in-memory storage
    storage = TodoStorage()

    # Parse command-line arguments
    parser = create_parser()
    args = parser.parse_args()

    # Handle no command provided
    if not args.command:
        parser.print_help()
        return 0

    try:
        # Route to appropriate handler
        if args.command == "add":
            output = handle_add(storage, args.title)
        elif args.command == "list":
            output = handle_list(storage)
        elif args.command == "complete":
            output = handle_complete(storage, args.id)
        elif args.command == "delete":
            output = handle_delete(storage, args.id)
        elif args.command == "update":
            output = handle_update(storage, args.id, args.new_title)
        else:
            print(f"Error: Unknown command '{args.command}'")
            return 1

        # Print success output
        print(output)
        return 0

    except ValidationError as e:
        # Input validation errors (empty title, too long, etc.)
        print(f"Error: {e}")
        return 1

    except NotFoundError as e:
        # Todo not found by ID
        print(f"Error: {e}")
        return 1

    except InvalidInputError as e:
        # Invalid user input (non-numeric ID, etc.)
        print(f"Error: {e}")
        return 1

    except TodoError as e:
        # Generic todo errors
        print(f"Error: {e}")
        return 1

    except Exception as e:
        # Unexpected errors (should not happen in normal operation)
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
