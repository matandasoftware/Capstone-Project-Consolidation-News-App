"""Business logic layer for the Task Manager application."""

from datetime import datetime
from typing import Dict, List
from constants import (
    TASK_COMPLETE, TASK_INCOMPLETE, TASK_OVERVIEW_FILE,
    USER_OVERVIEW_FILE, DATE_FORMAT
)
from data_access import UserRepository, TaskRepository
from utilities import get_current_date, is_valid_date


class Task:
    """Represents a task in the system."""

    def __init__(self, username: str, title: str, description: str,
                 assigned_date: str, due_date: str, completed: str = TASK_INCOMPLETE):
        self.username = username
        self.title = title
        self.description = description
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.completed = completed

    def to_dict(self) -> Dict[str, str]:
        """Convert task to dictionary format."""
        return {
            "username": self.username,
            "title": self.title,
            "description": self.description,
            "assigned_date": self.assigned_date,
            "due_date": self.due_date,
            "completed": self.completed
        }

    def is_complete(self) -> bool:
        """Check if task is complete."""
        return self.completed.lower() == TASK_COMPLETE

    def mark_complete(self) -> None:
        """Mark task as complete."""
        self.completed = TASK_COMPLETE

    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        from utilities import is_overdue
        return is_overdue(self.due_date, self.completed)


class UserService:
    """Handles user-related business logic."""

    def __init__(self):
        self.user_repo = UserRepository()

    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate a user with username and password.

        Args:
            username (str): The username to authenticate.
            password (str): The password to verify.

        Returns:
            bool: True if authentication successful, False otherwise.
        """
        users = self.user_repo.load_users()
        return username in users and users[username] == password

    def register_user(self, username: str, password: str) -> tuple[bool, str]:
        """
        Register a new user.

        Args:
            username (str): The new username.
            password (str): The new password.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not username:
            return False, "Username cannot be empty."

        users = self.user_repo.load_users()
        if username in users:
            return False, f"Username '{username}' already exists. Please choose a different username."

        if not password:
            return False, "Password cannot be empty."

        self.user_repo.save_user(username, password)
        return True, "User registered successfully!"

    def get_all_users(self) -> Dict[str, str]:
        """Get all registered users."""
        return self.user_repo.load_users()


class TaskService:
    """Handles task-related business logic."""

    def __init__(self):
        self.task_repo = TaskRepository()

    def create_task(self, username: str, title: str, description: str,
                   due_date: str) -> tuple[bool, str]:
        """
        Create a new task.

        Args:
            username (str): User to assign task to.
            title (str): Task title.
            description (str): Task description.
            due_date (str): Task due date in YYYY-MM-DD format.

        Returns:
            tuple: (success: bool, message: str)
        """
        if not username:
            return False, "Username cannot be empty."
        if not title:
            return False, "Task title cannot be empty."
        if not description:
            return False, "Task description cannot be empty."
        if not is_valid_date(due_date):
            return False, "Invalid date format. Please use YYYY-MM-DD."

        task = Task(
            username=username,
            title=title,
            description=description,
            assigned_date=get_current_date(),
            due_date=due_date,
            completed=TASK_INCOMPLETE
        )

        self.task_repo.save_task(task.to_dict())
        return True, "Task added successfully!"

    def get_all_tasks(self) -> List[Dict[str, str]]:
        """Get all tasks."""
        return self.task_repo.load_tasks()

    def get_user_tasks(self, username: str) -> List[Dict[str, str]]:
        """Get all tasks for a specific user."""
        all_tasks = self.task_repo.load_tasks()
        return [task for task in all_tasks if task['username'] == username]

    def get_completed_tasks(self) -> List[Dict[str, str]]:
        """Get all completed tasks."""
        all_tasks = self.task_repo.load_tasks()
        return [task for task in all_tasks if task['completed'].lower() == TASK_COMPLETE]

    def mark_task_complete(self, task: Dict[str, str]) -> tuple[bool, str]:
        """
        Mark a task as complete.

        Args:
            task (dict): The task to mark as complete.

        Returns:
            tuple: (success: bool, message: str)
        """
        if task['completed'].lower() == TASK_COMPLETE:
            return False, "This task is already marked as complete."

        task['completed'] = TASK_COMPLETE
        all_tasks = self.task_repo.load_tasks()
        self.task_repo.save_all_tasks(all_tasks)
        return True, "Task marked as complete!"

    def edit_task(self, task: Dict[str, str], new_username: str = None,
                 new_due_date: str = None) -> tuple[bool, str]:
        """
        Edit a task's username or due date.

        Args:
            task (dict): The task to edit.
            new_username (str, optional): New username to assign.
            new_due_date (str, optional): New due date.

        Returns:
            tuple: (success: bool, message: str)
        """
        if task['completed'].lower() == TASK_COMPLETE:
            return False, "Cannot edit a completed task."

        if new_username is not None:
            if not new_username:
                return False, "Username cannot be empty."
            task['username'] = new_username

        if new_due_date is not None:
            if not is_valid_date(new_due_date):
                return False, "Invalid date format. Please use YYYY-MM-DD."
            task['due_date'] = new_due_date

        all_tasks = self.task_repo.load_tasks()
        self.task_repo.save_all_tasks(all_tasks)
        return True, "Task updated successfully!"

    def delete_task(self, task_index: int) -> tuple[bool, str]:
        """
        Delete a task by index.

        Args:
            task_index (int): Index of task to delete (0-based).

        Returns:
            tuple: (success: bool, message: str)
        """
        all_tasks = self.task_repo.load_tasks()

        if not all_tasks:
            return False, "No tasks to delete."

        if task_index < 0 or task_index >= len(all_tasks):
            return False, "Invalid task number."

        removed = all_tasks.pop(task_index)
        self.task_repo.save_all_tasks(all_tasks)
        return True, f"Task '{removed['title']}' deleted successfully!"

    def get_task_statistics(self) -> Dict[str, float]:
        """
        Get statistics about all tasks.

        Returns:
            dict: Dictionary containing task statistics including total,
                  completed, incomplete counts and percentages.
        """
        all_tasks = self.get_all_tasks()
        total = len(all_tasks)

        if total == 0:
            return {
                "total": 0,
                "completed": 0,
                "incomplete": 0,
                "completion_rate": 0.0,
                "incomplete_rate": 0.0
            }

        completed = sum(1 for task in all_tasks if task['completed'].lower() == TASK_COMPLETE)
        incomplete = total - completed
        completion_rate = (completed / total) * 100
        incomplete_rate = (incomplete / total) * 100

        return {
            "total": total,
            "completed": completed,
            "incomplete": incomplete,
            "completion_rate": completion_rate,
            "incomplete_rate": incomplete_rate
        }


class ReportService:
    """Handles report generation."""

    def __init__(self):
        self.task_repo = TaskRepository()
        self.user_repo = UserRepository()

    def generate_reports(self) -> tuple[bool, str]:
        """
        Generate task_overview.txt and user_overview.txt reports.

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            tasks = self.task_repo.load_tasks()
            users = self.user_repo.load_users()

            self._generate_task_overview(tasks)
            self._generate_user_overview(tasks, users)

            return True, f"Reports generated successfully!\n- {TASK_OVERVIEW_FILE}\n- {USER_OVERVIEW_FILE}"
        except Exception as e:
            return False, f"Error generating reports: {e}"

    def _generate_task_overview(self, tasks: List[Dict[str, str]]) -> None:
        """Generate task overview report."""
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task['completed'].lower() == TASK_COMPLETE)
        uncompleted_tasks = total_tasks - completed_tasks

        today = datetime.now()
        overdue_tasks = sum(
            1 for task in tasks
            if task['completed'].lower() == TASK_INCOMPLETE and
            datetime.strptime(task['due_date'], DATE_FORMAT) < today
        )

        incomplete_percentage = (uncompleted_tasks / total_tasks * 100) if total_tasks > 0 else 0
        overdue_percentage = (overdue_tasks / total_tasks * 100) if total_tasks > 0 else 0

        with open(TASK_OVERVIEW_FILE, "w") as f:
            f.write("TASK OVERVIEW REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total number of tasks: {total_tasks}\n")
            f.write(f"Total number of completed tasks: {completed_tasks}\n")
            f.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
            f.write(f"Total number of overdue tasks: {overdue_tasks}\n")
            f.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n")
            f.write(f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n")

    def _generate_user_overview(self, tasks: List[Dict[str, str]],
                                users: Dict[str, str]) -> None:
        """Generate user overview report."""
        total_tasks = len(tasks)
        today = datetime.now()

        with open(USER_OVERVIEW_FILE, "w") as f:
            f.write("USER OVERVIEW REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total number of users: {len(users)}\n")
            f.write(f"Total number of tasks: {total_tasks}\n\n")

            for user in users.keys():
                user_tasks = [task for task in tasks if task['username'] == user]
                user_total = len(user_tasks)
                user_completed = sum(1 for task in user_tasks if task['completed'].lower() == TASK_COMPLETE)
                user_uncompleted = user_total - user_completed
                user_overdue = sum(
                    1 for task in user_tasks
                    if task['completed'].lower() == TASK_INCOMPLETE and
                    datetime.strptime(task['due_date'], DATE_FORMAT) < today
                )

                user_task_percentage = (user_total / total_tasks * 100) if total_tasks > 0 else 0
                user_completed_percentage = (user_completed / user_total * 100) if user_total > 0 else 0
                user_uncompleted_percentage = (user_uncompleted / user_total * 100) if user_total > 0 else 0
                user_overdue_percentage = (user_overdue / user_total * 100) if user_total > 0 else 0

                f.write(f"User: {user}\n")
                f.write(f"  Total tasks assigned: {user_total}\n")
                f.write(f"  Percentage of total tasks: {user_task_percentage:.2f}%\n")
                f.write(f"  Percentage of completed tasks: {user_completed_percentage:.2f}%\n")
                f.write(f"  Percentage of uncompleted tasks: {user_uncompleted_percentage:.2f}%\n")
                f.write(f"  Percentage of overdue tasks: {user_overdue_percentage:.2f}%\n\n")
