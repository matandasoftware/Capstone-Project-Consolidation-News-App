import unittest
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'+ '')))

from business_logic import Task, UserService, TaskService
from utilities import is_valid_date, get_current_date
from constants import TASK_COMPLETE, TASK_INCOMPLETE
class TestTask(unittest.TestCase):
    """Test cases for Task class."""

    def test_task_creation(self):
        """Test creating a new task object."""
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
        """Test marking a task as complete."""
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

    def test_task_is_overdue(self):
        """Test checking if task is overdue."""
        # Create task with past due date
        overdue_task = Task(
            username="testuser",
            title="Overdue Task",
            description="Test",
            assigned_date="2025-01-01",
            due_date="2025-01-15",
            completed=TASK_INCOMPLETE
        )

        # Create task with future due date
        future_task = Task(
            username="testuser",
            title="Future Task",
            description="Test",
            assigned_date="2025-01-01",
            due_date="2099-12-31",
            completed=TASK_INCOMPLETE
        )

        # Create completed task with past due date (should not be overdue)
        completed_task = Task(
            username="testuser",
            title="Completed Task",
            description="Test",
            assigned_date="2025-01-01",
            due_date="2025-01-15",
            completed=TASK_COMPLETE
        )

        self.assertTrue(overdue_task.is_overdue())
        self.assertFalse(future_task.is_overdue())
        self.assertFalse(completed_task.is_overdue())


class TestUserService(unittest.TestCase):
    """Test cases for UserService class."""

    @patch('business_logic.UserRepository')
    def test_authenticate_valid_user(self, mock_repo_class):
        """Test authenticating with valid credentials."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_users.return_value = {
            "testuser": "password123"
        }
        mock_repo_class.return_value = mock_repo

        service = UserService()

        # Act
        result = service.authenticate("testuser", "password123")

        # Assert
        self.assertTrue(result)

    @patch('business_logic.UserRepository')
    def test_authenticate_invalid_password(self, mock_repo_class):
        """Test authenticating with invalid password."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_users.return_value = {
            "testuser": "password123"
        }
        mock_repo_class.return_value = mock_repo

        service = UserService()

        # Act
        result = service.authenticate("testuser", "wrongpassword")

        # Assert
        self.assertFalse(result)

    @patch('business_logic.UserRepository')
    def test_authenticate_nonexistent_user(self, mock_repo_class):
        """Test authenticating with nonexistent username."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_users.return_value = {
            "testuser": "password123"
        }
        mock_repo_class.return_value = mock_repo

        service = UserService()

        # Act
        result = service.authenticate("nonexistent", "password123")

        # Assert
        self.assertFalse(result)

    @patch('business_logic.UserRepository')
    def test_user_exists(self, mock_repo_class):
        """Test checking if user exists."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_users.return_value = {
            "testuser": "password123"
        }
        mock_repo_class.return_value = mock_repo

        service = UserService()

        # Act & Assert
        self.assertTrue(service.user_exists("testuser"))
        self.assertFalse(service.user_exists("nonexistent"))

    @patch('business_logic.UserRepository')
    def test_register_new_user(self, mock_repo_class):
        """Test registering a new user."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_users.return_value = {}
        mock_repo.save_user.return_value = True
        mock_repo_class.return_value = mock_repo

        service = UserService()

        # Act
        result = service.register_user("newuser", "newpassword")

        # Assert
        self.assertTrue(result)
        mock_repo.save_user.assert_called_once_with("newuser", "newpassword")

    @patch('business_logic.UserRepository')
    def test_register_existing_user(self, mock_repo_class):
        """Test attempting to register an existing user."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_users.return_value = {
            "testuser": "password123"
        }
        mock_repo_class.return_value = mock_repo

        service = UserService()

        # Act
        result = service.register_user("testuser", "newpassword")

        # Assert
        self.assertFalse(result)


class TestTaskService(unittest.TestCase):
    """Test cases for TaskService class."""

    @patch('business_logic.TaskRepository')
    def test_add_task(self, mock_repo_class):
        """Test adding a new task."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.save_task.return_value = True
        mock_repo_class.return_value = mock_repo

        service = TaskService()

        # Act
        result = service.add_task(
            username="testuser",
            title="New Task",
            description="Task description",
            due_date="2025-12-31"
        )

        # Assert
        self.assertTrue(result)
        self.assertTrue(mock_repo.save_task.called)

    @patch('business_logic.TaskRepository')
    def test_get_all_tasks(self, mock_repo_class):
        """Test retrieving all tasks."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_tasks.return_value = [
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

        # Act
        tasks = service.get_all_tasks()

        # Assert
        self.assertEqual(len(tasks), 2)
        self.assertIsInstance(tasks[0], Task)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")

    @patch('business_logic.TaskRepository')
    def test_get_tasks_for_user(self, mock_repo_class):
        """Test retrieving tasks for a specific user."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_tasks.return_value = [
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
                "due_date": "2025-01-17",
                "completed": TASK_INCOMPLETE
            }
        ]
        mock_repo_class.return_value = mock_repo

        service = TaskService()

        # Act
        user1_tasks = service.get_tasks_for_user("user1")

        # Assert
        self.assertEqual(len(user1_tasks), 2)
        self.assertEqual(user1_tasks[0].title, "Task 1")
        self.assertEqual(user1_tasks[1].title, "Task 3")

    @patch('business_logic.TaskRepository')
    def test_get_completed_tasks(self, mock_repo_class):
        """Test retrieving only completed tasks."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_tasks.return_value = [
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
                "due_date": "2025-01-17",
                "completed": TASK_COMPLETE
            }
        ]
        mock_repo_class.return_value = mock_repo

        service = TaskService()

        # Act
        completed_tasks = service.get_completed_tasks()

        # Assert
        self.assertEqual(len(completed_tasks), 2)
        self.assertTrue(all(task.is_complete() for task in completed_tasks))

    @patch('business_logic.TaskRepository')
    def test_delete_task(self, mock_repo_class):
        """Test deleting a task."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_tasks.return_value = [
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
            }
        ]
        mock_repo.save_all_tasks.return_value = True
        mock_repo_class.return_value = mock_repo

        service = TaskService()

        # Act
        result = service.delete_task(0)

        # Assert
        self.assertTrue(result)
        self.assertTrue(mock_repo.save_all_tasks.called)

    @patch('business_logic.TaskRepository')
    def test_get_task_statistics(self, mock_repo_class):
        """Test calculating task statistics."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_all_tasks.return_value = [
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

        # Act
        stats = service.get_task_statistics()

        # Assert
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

