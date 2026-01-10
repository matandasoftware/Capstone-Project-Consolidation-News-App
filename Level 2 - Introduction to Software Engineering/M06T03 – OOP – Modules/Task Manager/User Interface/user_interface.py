"""User interface layer for the Task Manager application."""

import os
from typing import Dict, List
from config import ADMIN_USERNAME, ADMIN_MENU, USER_MENU
from business_logic import UserService, TaskService, ReportService
from constants import TASK_OVERVIEW_FILE, USER_OVERVIEW_FILE


class UserInterface:
    """Handles all user interactions."""

    def __init__(self):
        self.user_service = UserService()
        self.task_service = TaskService()
        self.report_service = ReportService()
        self.current_user = None
        self.is_admin = False

    def start(self) -> None:
        """Start the application."""
        self._login()
        self._main_menu()

    def _login(self) -> None:
        """Handle user login."""
        print("=" * 50)
        print("TASK MANAGER - LOGIN")
        print("=" * 50)

        while True:
            try:
                username = input("\nEnter username: ").strip()
                password = input("Enter password: ").strip()
            except Exception as e:
                print(f"Input error: {e}")
                continue

            if self.user_service.authenticate(username, password):
                self.current_user = username
                self.is_admin = (username == ADMIN_USERNAME)
                print("Login successful!\n")
                return
            else:
                print("Invalid username or password. Please try again.")

    def _main_menu(self) -> None:
        """Display and handle main menu."""
        while True:
            print("\n" + "=" * 50)
            print("MAIN MENU")
            print("=" * 50)
            print("\nPlease select one of the following options:")

            menu = ADMIN_MENU if self.is_admin else USER_MENU
            for code, desc in menu:
                print(f"{code:<4}- {desc}")

            try:
                choice = input("\nEnter your choice: ").strip().lower()
            except Exception as e:
                print(f"Input error: {e}")
                continue

            if choice == "e":
                print("\nGoodbye!")
                break

            self._handle_menu_choice(choice)

    def _handle_menu_choice(self, choice: str) -> None:
        """Handle menu choice."""
        if self.is_admin:
            if choice == "r":
                self._register_user()
            elif choice == "a":
                self._add_task()
            elif choice == "va":
                self._view_all_tasks()
            elif choice == "vm":
                self._view_my_tasks()
            elif choice == "vc":
                self._view_completed_tasks()
            elif choice == "del":
                self._delete_task()
            elif choice == "gr":
                self._generate_reports()
            elif choice == "ds":
                self._display_statistics()
            else:
                print("Invalid option. Please try again.")
        else:
            if choice == "a":
                self._add_task()
            elif choice == "va":
                self._view_all_tasks()
            elif choice == "vm":
                self._view_my_tasks()
            else:
                print("Invalid option. Please try again.")

    def _register_user(self) -> None:
        """Register a new user (admin only)."""
        print("\n" + "=" * 50)
        print("REGISTER NEW USER")
        print("=" * 50)

        while True:
            try:
                new_username = input("\nEnter new username: ").strip()
                new_password = input("Enter new password: ").strip()
                confirm_password = input("Confirm password: ").strip()
            except Exception as e:
                print(f"Input error: {e}")
                continue

            if new_password != confirm_password:
                print("Passwords do not match. Try again.\n")
                continue

            success, message = self.user_service.register_user(new_username, new_password)
            print(f"\n{message}")

            if success:
                break

    def _add_task(self) -> None:
        """Add a new task."""
        print("\n" + "=" * 50)
        print("ADD NEW TASK")
        print("=" * 50)

        while True:
            try:
                username = input("\nEnter username to assign task to: ").strip()
                title = input("Enter task title: ").strip()
                description = input("Enter task description: ").strip()
                due_date = input("Enter due date (YYYY-MM-DD): ").strip()
            except Exception as e:
                print(f"Input error: {e}")
                continue

            success, message = self.task_service.create_task(
                username, title, description, due_date
            )
            print(f"\n{message}")

            if success:
                break

    def _view_all_tasks(self) -> None:
        """View all tasks."""
        tasks = self.task_service.get_all_tasks()

        print("\n" + "=" * 50)
        print("ALL TASKS")
        print("=" * 50)

        if not tasks:
            print("\nNo tasks found.")
            return

        for i, task in enumerate(tasks, 1):
            self._display_task(i, task)

    def _view_my_tasks(self) -> None:
        """View and interact with tasks assigned to current user."""
        while True:
            tasks = self.task_service.get_all_tasks()
            user_tasks = [task for task in tasks if task['username'] == self.current_user]

            print("\n" + "=" * 50)
            print("MY TASKS")
            print("=" * 50)

            if not user_tasks:
                print("\nNo tasks assigned to you.")
                return

            for i, task in enumerate(user_tasks, 1):
                self._display_task(i, task)

            task_num = self._get_valid_task_number(len(user_tasks))

            if task_num == -1:
                return

            selected_task = user_tasks[task_num - 1]
            self._task_action_menu(selected_task, tasks)

    def _view_completed_tasks(self) -> None:
        """View all completed tasks (admin only)."""
        tasks = self.task_service.get_completed_tasks()

        print("\n" + "=" * 50)
        print("COMPLETED TASKS")
        print("=" * 50)

        if not tasks:
            print("\nNo completed tasks found.")
            return

        for i, task in enumerate(tasks, 1):
            self._display_task(i, task)

    def _delete_task(self) -> None:
        """Delete a task (admin only)."""
        tasks = self.task_service.get_all_tasks()

        print("\n" + "=" * 50)
        print("DELETE TASK")
        print("=" * 50)

        if not tasks:
            print("\nNo tasks to delete.")
            return

        for i, task in enumerate(tasks, 1):
            print(f"\n{i}. {task['title']} (Assigned to: {task['username']}, "
                  f"Due: {task['due_date']}, Completed: {task['completed']})")

        try:
            choice = int(input("\nEnter the number of the task to delete (0 to cancel): "))
            if choice == 0:
                print("Cancelled.")
                return

            success, message = self.task_service.delete_task(choice - 1)
            print(f"\n{message}")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"Error: {e}")

    def _generate_reports(self) -> None:
        """Generate reports (admin only)."""
        print("\n" + "=" * 50)
        print("GENERATE REPORTS")
        print("=" * 50)

        success, message = self.report_service.generate_reports()
        print(f"\n{message}")

    def _display_statistics(self) -> None:
        """Display statistics from reports (admin only)."""
        if not os.path.exists(TASK_OVERVIEW_FILE) or not os.path.exists(USER_OVERVIEW_FILE):
            print("\nReports not found. Generating reports...")
            self.report_service.generate_reports()

        try:
            print("\n" + "=" * 60)
            print("STATISTICS")
            print("=" * 60 + "\n")

            with open(TASK_OVERVIEW_FILE, "r") as f:
                print(f.read())

            print("\n" + "=" * 60 + "\n")

            with open(USER_OVERVIEW_FILE, "r") as f:
                print(f.read())

            print("=" * 60)

        except Exception as e:
            print(f"Error displaying statistics: {e}")

    def _task_action_menu(self, task: Dict[str, str], all_tasks: List[Dict[str, str]]) -> None:
        """Display task action menu."""
        while True:
            try:
                print(f"\n" + "=" * 50)
                print(f"Selected: {task['title']}")
                print("=" * 50)
                print("1 - Mark as complete")
                print("2 - Edit task")
                print("0 - Back to task list")
                action = input("Enter your choice: ").strip()

                if action == "0":
                    return
                elif action == "1":
                    success, message = self.task_service.mark_task_complete(task)
                    print(f"\n{message}")
                    if success:
                        return
                elif action == "2":
                    self._edit_task_menu(task, all_tasks)
                    return
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"Error: {e}")

    def _edit_task_menu(self, task: Dict[str, str], all_tasks: List[Dict[str, str]]) -> None:
        """Display edit task menu."""
        if task['completed'].lower() == 'y':
            print("\nCannot edit a completed task.")
            return

        print("\n" + "=" * 50)
        print("EDIT TASK")
        print("=" * 50)
        print(f"Current assigned user: {task['username']}")
        print(f"Current due date: {task['due_date']}")

        while True:
            try:
                print("\nWhat would you like to edit?")
                print("1 - Change assigned user")
                print("2 - Change due date")
                print("3 - Change both")
                print("0 - Cancel")
                edit_choice = input("Enter your choice: ").strip()

                if edit_choice == "0":
                    print("Edit cancelled.")
                    return
                elif edit_choice == "1":
                    new_user = input("Enter new username: ").strip()
                    success, message = self.task_service.edit_task(task, new_username=new_user)
                    print(f"\n{message}")
                    if success:
                        return
                elif edit_choice == "2":
                    new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
                    success, message = self.task_service.edit_task(task, new_due_date=new_due_date)
                    print(f"\n{message}")
                    if success:
                        return
                elif edit_choice == "3":
                    new_user = input("Enter new username: ").strip()
                    new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
                    success, message = self.task_service.edit_task(
                        task, new_username=new_user, new_due_date=new_due_date
                    )
                    print(f"\n{message}")
                    if success:
                        return
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"Error: {e}")

    def _display_task(self, number: int, task: Dict[str, str]) -> None:
        """Display a single task."""
        print(f"\nTask {number}:")
        print(f"  Assigned to: {task['username']}")
        print(f"  Title: {task['title']}")
        print(f"  Description: {task['description']}")
        print(f"  Assigned date: {task['assigned_date']}")
        print(f"  Due date: {task['due_date']}")
        print(f"  Completed: {'Yes' if task['completed'].lower() == 'y' else 'No'}")

    def _get_valid_task_number(self, max_tasks: int) -> int:
        """
        Get valid task number from user.

        Args:
            max_tasks (int): Maximum valid task number.

        Returns:
            int: Valid task number (1 to max_tasks) or -1 to return.
        """
        while True:
            try:
                task_num = int(input("\nEnter task number (-1 to return to main menu): "))
                if task_num == -1:
                    return -1
                if 1 <= task_num <= max_tasks:
                    return task_num
                else:
                    print(f"Invalid task number. Please enter a number between 1 and {max_tasks}, or -1 to return.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
            except Exception as e:
                print(f"Error: {e}")


def start_application() -> None:
    """Start the Task Manager application."""
    ui = UserInterface()
    ui.start()
