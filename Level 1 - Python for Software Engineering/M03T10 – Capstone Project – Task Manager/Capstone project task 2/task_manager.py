"""
Task Manager Application
-----------------------
This program allows users to register, add, view, and manage tasks.
Only the 'admin' user can register new users and access admin features.
All data is stored in plain text files: user.txt and tasks.txt.
"""

import os
from datetime import datetime
from typing import List, Dict

# Constants for file names
USER_FILE = "user.txt"
TASK_FILE = "tasks.txt"

# Menu option constants
ADMIN_MENU = [
    ("r", "register user"),
    ("a", "add task"),
    ("va", "view all tasks"),
    ("vm", "view my tasks"),
    ("vc", "view completed tasks"),
    ("del", "delete tasks"),
    ("e", "exit")
]
USER_MENU = [
    ("a", "add task"),
    ("va", "view all tasks"),
    ("vm", "view my tasks"),
    ("e", "exit")
]


def view_completed_tasks(tasks: List[Dict[str, str]]) -> None:
    """
    Display only completed tasks (where completed == 'y').

    Args:
        tasks (list): List of all task dictionaries.
    """
    completed_tasks = [
        task for task in tasks if task['completed'].lower() == 'y'
    ]
    if not completed_tasks:
        print("No completed tasks found.\n")
        return
    for i, task in enumerate(completed_tasks, 1):
        print(f"Completed Task {i}:")
        print(f"  Assigned to: {task['username']}")
        print(f"  Title: {task['title']}")
        print(f"  Description: {task['description']}")
        print(f"  Assigned date: {task['assigned_date']}")
        print(f"  Due date: {task['due_date']}")
        print(f"  Completed: {task['completed']}\n")


def delete_task(tasks: List[Dict[str, str]]) -> None:
    """
    Allow the admin to delete a task by its number in the list.

    Args:
        tasks (list): List of all task dictionaries.
    Side effects:
        Updates tasks.txt after deletion.
    """
    if not tasks:
        print("No tasks to delete.\n")
        return
    for i, task in enumerate(tasks, 1):
        print(
            f"{i}. {task['title']} (Assigned to: {task['username']}, "
            f"Due: {task['due_date']}, Completed: {task['completed']})"
        )
    try:
        choice = int(
            input("Enter the number of the task to delete (0 to cancel): ")
        )
        if choice == 0:
            print("Cancelled.\n")
            return
        if 1 <= choice <= len(tasks):
            removed = tasks.pop(choice - 1)
            save_all_tasks(tasks)
            print(f"Task '{removed['title']}' deleted successfully!\n")
        else:
            print("Invalid task number.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")
    except Exception as e:
        print(f"Error: {e}")


def is_valid_date(date_str: str) -> bool:
    """
    Validate that a string is a date in YYYY-MM-DD format.

    Args:
        date_str (str): The date string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def load_users() -> Dict[str, str]:
    """
    Load users and passwords from user.txt into a dictionary.

    Returns:
        dict: Mapping of usernames to passwords.
    """
    users = {}
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                for line in f:
                    if line.strip():
                        try:
                            username, password = line.strip().split(", ")
                            users[username] = password
                        except ValueError:
                            print("Warning: Skipping malformed user entry.")
        except Exception as e:
            print(f"Error reading {USER_FILE}: {e}")
    return users


def save_user(username: str, password: str) -> None:
    """
    Append a new user and password to user.txt.

    Args:
        username (str): The new username.
        password (str): The new password.
    """
    try:
        with open(USER_FILE, "a") as f:
            f.write(f"{username}, {password}\n")
    except Exception as e:
        print(f"Error writing to {USER_FILE}: {e}")


def load_tasks() -> List[Dict[str, str]]:
    """
    Load all tasks from tasks.txt into a list of dictionaries.

    Returns:
        list: List of task dictionaries.
    """
    tasks = []
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, "r") as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(", ")
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
            print(f"Error reading {TASK_FILE}: {e}")
    return tasks


def save_all_tasks(tasks: List[Dict[str, str]]) -> None:
    """
    Overwrite tasks.txt with the provided list of tasks.

    Args:
        tasks (list): List of task dictionaries to save.
    """
    try:
        with open(TASK_FILE, "w") as f:
            for task in tasks:
                f.write(
                    f"{task['username']}, {task['title']}, "
                    f"{task['description']}, {task['assigned_date']}, "
                    f"{task['due_date']}, {task['completed']}\n"
                )
    except Exception as e:
        print(f"Error writing to {TASK_FILE}: {e}")


def save_task(task: Dict[str, str]) -> None:
    """
    Append a new task to tasks.txt.

    Args:
        task (dict): Task dictionary to save.
    """
    try:
        with open(TASK_FILE, "a") as f:
            f.write(
                f"{task['username']}, {task['title']}, {task['description']}, "
                f"{task['assigned_date']}, {task['due_date']}, "
                f"{task['completed']}\n"
            )
    except Exception as e:
        print(f"Error writing to {TASK_FILE}: {e}")


def login(users: Dict[str, str]) -> str:
    """
    Prompt the user to log in, validating credentials.

    Args:
        users (dict): Mapping of usernames to passwords.

    Returns:
        str: The username of the successfully logged-in user.
    """
    while True:
        try:
            username_input = input("Enter username: ")
            password = input("Enter password: ")
        except Exception as e:
            print(f"Input error: {e}")
            continue
        if username_input in users and users[username_input] == password:
            print("Login successful!\n")
            return username_input
        else:
            print("Invalid username or password. Please try again.\n")


def reg_user(users: Dict[str, str]) -> None:
    """
    Register a new user (admin only). Prompts for username and password,
    checks for duplicates and empty fields, and saves the new user if valid.

    Args:
        users (dict): Current users for duplicate checking.
    Side effects:
        Writes to user.txt if registration is successful.
    """
    while True:
        try:
            new_username = input("Enter new username: ").strip()
            if not new_username:
                print("Username cannot be empty.\n")
                continue
            if new_username in users:
                print("Username already exists. Try another.\n")
                continue
            new_password = input("Enter new password: ").strip()
            if not new_password:
                print("Password cannot be empty.\n")
                continue
            confirm_password = input("Confirm password: ").strip()
        except Exception as e:
            print(f"Input error: {e}")
            continue
        if new_password == confirm_password:
            save_user(new_username, new_password)
            print("User registered successfully!\n")
            break
        else:
            print("Passwords do not match. Try again.\n")


def add_task() -> None:
    """
    Prompt for and add a new task with input validation and error handling.
    Prompts for username, title, description, and due date. Validates all
    fields and date format.
    Side effects:
        Writes new task to tasks.txt if successful.
    """
    while True:
        try:
            username = input("Enter username to assign task to: ").strip()
            if not username:
                print("Username cannot be empty.\n")
                continue
            title = input("Enter task title: ").strip()
            if not title:
                print("Task title cannot be empty.\n")
                continue
            description = input("Enter task description: ").strip()
            if not description:
                print("Task description cannot be empty.\n")
                continue
            due_date = input("Enter due date (YYYY-MM-DD): ").strip()
            if not is_valid_date(due_date):
                print("Invalid date format. Please use YYYY-MM-DD.\n")
                continue
        except Exception as e:
            print(f"Input error: {e}")
            continue
        assigned_date = datetime.now().strftime("%Y-%m-%d")
        task = {
            "username": username,
            "title": title,
            "description": description,
            "assigned_date": assigned_date,
            "due_date": due_date,
            "completed": "n"  # Use 'y' for yes, 'n' for no
        }
        save_task(task)
        print("Task added successfully!\n")
        break


def view_all(tasks: List[Dict[str, str]]) -> None:
    """
    Display all tasks in a user-friendly format.

    Args:
        tasks (list): List of all task dictionaries.
    """
    if not tasks:
        print("No tasks found.\n")
        return
    for i, task in enumerate(tasks, 1):
        print(f"Task {i}:")
        print(f"  Assigned to: {task['username']}")
        print(f"  Title: {task['title']}")
        print(f"  Description: {task['description']}")
        print(f"  Assigned date: {task['assigned_date']}")
        print(f"  Due date: {task['due_date']}")
        print(f"  Completed: {task['completed']}\n")


def view_mine(tasks: List[Dict[str, str]], username: str) -> None:
    """
    Display tasks assigned to the current user.

    Args:
        tasks (list): List of all task dictionaries.
        username (str): The current user's username.
    """
    user_tasks = [task for task in tasks if task['username'] == username]
    if not user_tasks:
        print("No tasks assigned to you.\n")
        return
    for i, task in enumerate(user_tasks, 1):
        print(f"Task {i}:")
        print(f"  Title: {task['title']}")
        print(f"  Description: {task['description']}")
        print(f"  Assigned date: {task['assigned_date']}")
        print(f"  Due date: {task['due_date']}")
        print(f"  Completed: {task['completed']}\n")


def main() -> None:
    """
    Main program loop: handles user login and menu navigation.
    Handles admin-only registration, task addition, viewing, and marking
    complete.
    """
    users = load_users()
    username = login(users)
    is_admin = username == "admin"
    while True:
        print("Please select one of the following options:")
        menu = ADMIN_MENU if is_admin else USER_MENU
        for code, desc in menu:
            print(f"{code:<4}- {desc}")
        try:
            choice = input("Enter your choice: ").strip().lower()
        except Exception as e:
            print(f"Input error: {e}")
            continue
        if is_admin:
            if choice == "r":
                reg_user(users)
                users = load_users()  # Refresh users after registration
            elif choice == "a":
                add_task()
            elif choice == "va":
                tasks = load_tasks()
                view_all(tasks)
            elif choice == "vm":
                tasks = load_tasks()
                view_mine(tasks, username)
            elif choice == "vc":
                tasks = load_tasks()
                view_completed_tasks(tasks)
            elif choice == "del":
                tasks = load_tasks()
                delete_task(tasks)
            elif choice == "e":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.\n")
        else:
            if choice == "a":
                add_task()
            elif choice == "va":
                tasks = load_tasks()
                view_all(tasks)
            elif choice == "vm":
                tasks = load_tasks()
                view_mine(tasks, username)
            elif choice == "e":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.\n")


if __name__ == "__main__":
    main()