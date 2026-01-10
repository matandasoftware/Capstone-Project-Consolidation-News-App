"""Utility functions for the Task Manager application."""

from datetime import datetime
from constants import DATE_FORMAT


def is_valid_date(date_string):
    """Check if a string is a valid date in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_string, DATE_FORMAT)
        return True
    except ValueError:
        return False


def get_current_date():
    """Get the current date in YYYY-MM-DD format."""
    return datetime.now().strftime(DATE_FORMAT)


def is_overdue(due_date, completed):
    """Check if a task is overdue."""
    from constants import TASK_INCOMPLETE
    if completed != TASK_INCOMPLETE:
        return False
    try:
        due = datetime.strptime(due_date, DATE_FORMAT)
        now = datetime.now()
        return due.date() < now.date()
    except ValueError:
        return False
