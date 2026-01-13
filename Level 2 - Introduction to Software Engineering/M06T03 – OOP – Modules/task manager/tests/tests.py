"""Unit tests for the Task Manager application."""

import unittest
import sys
import os
from unittest.mock import MagicMock, patch
# from datetime import datetime  # Unused import

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from business_logic.business_logic import Task, UserService, TaskService
from utilities.utilities import is_valid_date, get_current_date
from configuration.constants import TASK_COMPLETE, TASK_INCOMPLETE


class TestTask(unittest.TestCase):
    """Test cases for Task class."""

    def test_task_creation(self):
        """Use Case 1: Creating a new task object."""
        task = Task(
            username="testuser",
            title="Test Task",
            description="Test Description",
            assigned_date="2025-01-01",
            due_date="2025-01-15"
        )

        self.assertEqual(task.username, "testuser")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.assigned_date, "2025-01-01")
        self.assertEqual(task.due_date, "2025-01-15")
        self.assertEqual(task.completed, TASK_INCOMPLETE)

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            username="testuser",
            title="Test Task",
            description="Test Description",
            assigned_date="2025-01-01",
            due_date="2025-01-15"
        )

        task_dict = task.to_dict()

        self.assertIsInstance(task_dict, dict)
        self.assertEqual(task_dict["username"], "testuser")
        self.assertEqual(task_dict["title"], "Test Task")
        self.assertEqual(task_dict["completed"], TASK_INCOMPLETE)

    def test_task_is_complete(self):
        """Test checking if task is complete."""
        incomplete_task = Task(
            username="testuser",
            title="Incomplete Task",
            description="Test",
            assigned_date="2025-01-01",
            due_date="2025-01-15",
            completed=TASK_INCOMPLETE
        )

        complete_task = Task(
            username="testuser",
            title="Complete Task",
            description="Test",
            assigned_date="2025-01-01",
            due_date="2025-01-15",
            completed=TASK_COMPLETE
        )

        self.assertFalse(incomplete_task.is_complete())
        self.assertTrue(complete_task.is_complete())

    def test_task_mark_complete(self):
        """Use Case 2: Marking a task as complete."""
        task = Task(
            username="testuser",
            title="Test Task",
            description="Test Description",
            assigned_date="2025-01-01",
            due_date="2025-01-15"
        )

        self.assertFalse(task.is_complete())
        task.mark_complete()
        self.assertTrue(task.is_complete())
        self.assertEqual(task.completed, TASK_COMPLETE)


class TestUserService(unittest.TestCase):
    """Test cases for UserService class."""

    @patch('business_logic.UserRepository')
    def test_authenticate_valid_user(self, mock_repo_class):
        """Use Case 3: Authenticating a valid user."""
        mock_repo = MagicMock()
        mock_repo.load_users.return_value = {
            "testuser": "password123"
        }
        mock_repo_class.return_value = mock_repo

        service = UserService()
        result = service.authenticate("testuser", "password123")

        self.assertTrue(result)

    @patch('business_logic.UserRepository')
    def test_authenticate_invalid_password(self, mock_repo_class):
        """Test authenticating with invalid password."""
        mock_repo = MagicMock()
        mock_repo.load_users.return_value = {
            "testuser": "password123"
        }
        mock_repo_class.return_value = mock_repo

        service = UserService()
        result = service.authenticate("testuser", "wrongpassword")

        self.assertFalse(result)

    @patch('business_logic.UserRepository')
    def test_register_new_user(self, mock_repo_class):
        """Test registering a new user."""
        mock_repo = MagicMock()
        mock_repo.load_users.return_value = {}
        mock_repo.save_user.return_value = None
        mock_repo_class.return_value = mock_repo

        service = UserService()
        success, message = service.register_user("newuser", "password123")

        self.assertTrue(success)
        self.assertIn("successfully", message.lower())
        mock_repo.save_user.assert_called_once_with("newuser", "password123")

    @patch('business_logic.UserRepository')
    def test_register_existing_user(self, mock_repo_class):
        """Test attempting to register an existing user."""
        mock_repo = MagicMock()
        mock_repo.load_users.return_value = {
            "testuser": "password123"
        }
        mock_repo_class.return_value = mock_repo

        service = UserService()
        success, message = service.register_user("testuser", "newpassword")

        self.assertFalse(success)
        self.assertIn("already exists", message)


class TestTaskService(unittest.TestCase):
    """Test cases for TaskService class."""

    @patch('business_logic.TaskRepository')
    def test_create_task(self, mock_repo_class):
        """Use Case 4: Creating and adding a new task."""
        mock_repo = MagicMock()
        mock_repo.save_task.return_value = None
        mock_repo_class.return_value = mock_repo

        service = TaskService()
        success, message = service.create_task(
            username="testuser",
            title="New Task",
            description="Task description",
            due_date="2025-12-31"
        )

        self.assertTrue(success)
        self.assertIn("successfully", message.lower())
        mock_repo.save_task.assert_called_once()

    @patch('business_logic.TaskRepository')
    def test_create_task_invalid_date(self, mock_repo_class):
        """Test creating task with invalid date."""
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo

        service = TaskService()
        success, message = service.create_task(
            username="testuser",
            title="New Task",
            description="Task description",
            due_date="invalid-date"
        )

        self.assertFalse(success)
        self.assertIn("invalid", message.lower())

    @patch('business_logic.TaskRepository')
    def test_get_all_tasks(self, mock_repo_class):
        """Test retrieving all tasks."""
        mock_repo = MagicMock()
        mock_repo.load_tasks.return_value = [
            {
                "username": "testuser",
                "title": "Task 1",
                "description": "Description 1",
                "assigned_date": "2025-01-01",
                "due_date": "2025-01-15",
                "completed": TASK_INCOMPLETE
            },
            {
                "username": "testuser",
                "title": "Task 2",
                "description": "Description 2",
                "assigned_date": "2025-01-02",
                "due_date": "2025-01-16",
                "completed": TASK_COMPLETE
            }
        ]
        mock_repo_class.return_value = mock_repo

        service = TaskService()
        tasks = service.get_all_tasks()

        self.assertEqual(len(tasks), 2)
        self.assertIsInstance(tasks[0], dict)
        self.assertEqual(tasks[0]["title"], "Task 1")

    @patch('business_logic.TaskRepository')
    def test_get_completed_tasks(self, mock_repo_class):
        """Test retrieving only completed tasks."""
        mock_repo = MagicMock()
        mock_repo.load_tasks.return_value = [
            {
                "username": "user1",
                "title": "Task 1",
                "description": "Description 1",
                "assigned_date": "2025-01-01",
                "due_date": "2025-01-15",
                "completed": TASK_INCOMPLETE
            },
            {
                "username": "user2",
                "title": "Task 2",
                "description": "Description 2",
                "assigned_date": "2025-01-02",
                "due_date": "2025-01-16",
                "completed": TASK_COMPLETE
            },
            {
                "username": "user3",
                "title": "Task 3",
                "description": "Description 3",
                "assigned_date": "2025-01-03",
                "due_date": "2025-01-17",
                "completed": TASK_COMPLETE
            }
        ]
        mock_repo_class.return_value = mock_repo

        service = TaskService()
        completed_tasks = service.get_completed_tasks()

        self.assertEqual(len(completed_tasks), 2)
        for task in completed_tasks:
            self.assertEqual(task["completed"], TASK_COMPLETE)

    @patch('business_logic.TaskRepository')
    def test_get_task_statistics(self, mock_repo_class):
        """Test calculating task statistics."""
        mock_repo = MagicMock()
        mock_repo.load_tasks.return_value = [
            {
                "username": "user1",
                "title": "Task 1",
                "description": "Description 1",
                "assigned_date": "2025-01-01",
                "due_date": "2025-01-15",
                "completed": TASK_INCOMPLETE
            },
            {
                "username": "user2",
                "title": "Task 2",
                "description": "Description 2",
                "assigned_date": "2025-01-02",
                "due_date": "2025-01-16",
                "completed": TASK_COMPLETE
            },
            {
                "username": "user1",
                "title": "Task 3",
                "description": "Description 3",
                "assigned_date": "2025-01-03",
                "due_date": "2099-12-31",
                "completed": TASK_INCOMPLETE
            },
            {
                "username": "user1",
                "title": "Task 4",
                "description": "Description 4",
                "assigned_date": "2025-01-04",
                "due_date": "2025-01-17",
                "completed": TASK_COMPLETE
            }
        ]
        mock_repo_class.return_value = mock_repo

        service = TaskService()
        stats = service.get_task_statistics()

        self.assertEqual(stats["total"], 4)
        self.assertEqual(stats["completed"], 2)
        self.assertEqual(stats["incomplete"], 2)
        self.assertEqual(stats["completion_rate"], 50.0)
        self.assertEqual(stats["incomplete_rate"], 50.0)


class TestUtilities(unittest.TestCase):
    """Test cases for utility functions."""

    def test_is_valid_date_valid(self):
        """Test valid date formats."""
        self.assertTrue(is_valid_date("2025-01-15"))
        self.assertTrue(is_valid_date("2025-12-31"))
        self.assertTrue(is_valid_date("2024-02-29"))  # Leap year

    def test_is_valid_date_invalid(self):
        """Test invalid date formats."""
        self.assertFalse(is_valid_date("2025-13-01"))  # Invalid month
        self.assertFalse(is_valid_date("2025-01-32"))  # Invalid day
        self.assertFalse(is_valid_date("15-01-2025"))  # Wrong format
        self.assertFalse(is_valid_date("2025/01/15"))  # Wrong separator
        self.assertFalse(is_valid_date("not a date"))
        self.assertFalse(is_valid_date(""))

    def test_get_current_date_format(self):
        """Test current date format."""
        current_date = get_current_date()
        self.assertTrue(is_valid_date(current_date))
        self.assertEqual(len(current_date), 10)  # YYYY-MM-DD is 10 chars


if __name__ == "__main__":
    unittest.main()
