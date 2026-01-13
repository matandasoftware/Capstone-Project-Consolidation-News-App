"""Data access layer for the Task Manager application."""

import os
from typing import Dict, List
from configuration.constants import (
    USERS_FILE, TASKS_FILE, FIELD_SEPARATOR
)


class UserRepository:
    """Handles user data persistence."""

    @staticmethod
    def load_users() -> Dict[str, str]:
        """
        Load users and passwords from user.txt into a dictionary.

        Returns:
            dict: Mapping of usernames to passwords.
        """
        users = {}
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, "r") as f:
                    for line in f:
                        if line.strip():
                            try:
                                parts = line.strip().split(FIELD_SEPARATOR)
                                if len(parts) == 2:
                                    username = parts[0].strip()
                                    password = parts[1].strip()
                                    users[username] = password
                                else:
                                    print("Warning: Skipping malformed user entry.")
                            except ValueError:
                                print("Warning: Skipping malformed user entry.")
            except Exception as e:
                print(f"Error reading {USERS_FILE}: {e}")
        return users

    @staticmethod
    def save_user(username: str, password: str) -> None:
        """
        Append a new user and password to user.txt.

        Args:
            username (str): The new username.
            password (str): The new password.
        """
        try:
            with open(USERS_FILE, "a") as f:
                f.write(f"{username}{FIELD_SEPARATOR}{password}\n")
        except Exception as e:
            print(f"Error writing to {USERS_FILE}: {e}")


class TaskRepository:
    """Handles task data persistence."""

    @staticmethod
    def load_tasks() -> List[Dict[str, str]]:
        """
        Load all tasks from tasks.txt into a list of dictionaries.

        Returns:
            list: List of task dictionaries.
        """
        tasks = []
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, "r") as f:
                    for line in f:
                        if line.strip():
                            parts = line.strip().split(FIELD_SEPARATOR)
                            if len(parts) == 6:
                                task = {
                                    "username": parts[0],
                                    "title": parts[1],
                                    "description": parts[2],
                                    "assigned_date": parts[3],
                                    "due_date": parts[4],
                                    "completed": parts[5]
                                }
                                tasks.append(task)
                            else:
                                print("Warning: Skipping malformed task entry.")
            except Exception as e:
                print(f"Error reading {TASKS_FILE}: {e}")
        return tasks

    @staticmethod
    def save_all_tasks(tasks: List[Dict[str, str]]) -> None:
        """
        Overwrite tasks.txt with the provided list of tasks.

        Args:
            tasks (list): List of task dictionaries to save.
        """
        try:
            with open(TASKS_FILE, "w") as f:
                for task in tasks:
                    f.write(
                        f"{task['username']}{FIELD_SEPARATOR}{task['title']}{FIELD_SEPARATOR}"
                        f"{task['description']}{FIELD_SEPARATOR}{task['assigned_date']}{FIELD_SEPARATOR}"
                        f"{task['due_date']}{FIELD_SEPARATOR}{task['completed']}\n"
                    )
        except Exception as e:
            print(f"Error writing to {TASKS_FILE}: {e}")

    @staticmethod
    def save_task(task: Dict[str, str]) -> None:
        """
        Append a new task to tasks.txt.

        Args:
            task (dict): Task dictionary to save.
        """
        try:
            with open(TASKS_FILE, "a") as f:
                f.write(
                    f"{task['username']}{FIELD_SEPARATOR}{task['title']}{FIELD_SEPARATOR}"
                    f"{task['description']}{FIELD_SEPARATOR}{task['assigned_date']}{FIELD_SEPARATOR}"
                    f"{task['due_date']}{FIELD_SEPARATOR}{task['completed']}\n"
                )
        except Exception as e:
            print(f"Error writing to {TASKS_FILE}: {e}")
