"""
Task Manager Application
------------------------
Main entry point for the Task Manager application.

This application allows users to:
- Register and manage user accounts
- Create and assign tasks
- View and edit tasks
- Generate reports and statistics
- Track task completion and overdue status

All data is stored in text files for persistence.
"""

from user_interface.user_interface import start_application


if __name__ == "__main__":
    start_application()
