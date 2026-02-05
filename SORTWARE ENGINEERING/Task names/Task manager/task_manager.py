"""
Task Manager Application
-----------------------
This program allows users to register, add, view, and manage tasks.
Only the 'admin' user can register new users and access admin features.
All data is stored in plain text files: user.txt and tasks.txt.
"""

import os
from datetime import datetime
from typing import List, Dict, Optional

USER_FILE = "user.txt"
TASK_FILE = "tasks.txt"
TASK_OVERVIEW_FILE = "task_overview.txt"
USER_OVERVIEW_FILE = "user_overview.txt"

ADMIN_MENU = [
    ("r", "register user"),
    ("a", "add task"),
    ("va", "view all tasks"),
    ("vm", "view my tasks"),
    ("vc", "view completed tasks"),
    ("del", "delete a task"),
    ("ds", "display statistics"),
    ("gr", "generate reports"),
    ("e", "exit")
]

USER_MENU = [
    ("a", "add task"),
    ("va", "view all tasks"),
    ("vm", "view my tasks"),
    ("e", "exit")
]


def is_valid_date(date_str: str) -> bool:
    """Validate that a string is a date in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def load_users() -> Dict[str, str]:
    """Load users and passwords from user.txt into a dictionary."""
    users = {}
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                for line in f:
                    if line.strip():
                        try:
                            parts = line.strip().split(", ")
                            if len(parts) == 2:
                                username = parts[0].strip()
                                password = parts[1].strip()
                                users[username] = password
                            else:
                                print("Warning: Skipping malformed user entry.")
                        except ValueError:
                            print("Warning: Skipping malformed user entry.")
        except Exception as e:
            print(f"Error reading {USER_FILE}: {e}")
    return users


def save_user(username: str, password: str) -> None:
    """Append a new user and password to user.txt."""
    try:
        with open(USER_FILE, "a") as f:
            f.write(f"{username}, {password}\n")
    except Exception as e:
        print(f"Error writing to {USER_FILE}: {e}")


def load_tasks() -> List[Dict[str, str]]:
    """Load all tasks from tasks.txt into a list of dictionaries."""
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
    """Overwrite tasks.txt with the provided list of tasks."""
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
    """Append a new task to tasks.txt."""
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
    """Prompt the user to log in, validating credentials."""
    while True:
        try:
            username_input = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
        except Exception as e:
            print(f"Input error: {e}")
            continue
        if username_input in users and users[username_input] == password:
            print("Login successful!\n")
            return username_input
        else:
            print("Invalid username or password. Please try again.\n")


def reg_user(users: Dict[str, str]) -> None:
    """Register a new user (admin only)."""
    while True:
        try:
            new_username = input("Enter new username: ").strip()
            if not new_username:
                print("Username cannot be empty.\n")
                continue
            if new_username in users:
                print(f"Error: Username '{new_username}' already exists. Please choose a different username.\n")
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
            users[new_username] = new_password
            print("User registered successfully!\n")
            break
        else:
            print("Passwords do not match. Try again.\n")


def add_task() -> None:
    """Prompt for and add a new task."""
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
            "completed": "n"
        }
        save_task(task)
        print("Task added successfully!\n")
        break


def view_all(tasks: List[Dict[str, str]]) -> None:
    """Display all tasks in a user-friendly format."""
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


def view_completed_tasks(tasks: List[Dict[str, str]]) -> None:
    """Display only completed tasks."""
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
    """Allow the admin to delete a task by its number in the list."""
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


def get_valid_task_number(user_tasks: List[Dict[str, str]], prompt: str = "Enter task number (-1 to return to main menu): ") -> int:
    """Recursively prompt user for a valid task number until valid input is provided."""
    try:
        task_num = int(input(prompt))
        if task_num == -1:
            return -1
        if 1 <= task_num <= len(user_tasks):
            return task_num
        else:
            print(f"Invalid task number. Please enter a number between 1 and {len(user_tasks)}, or -1 to return.\n")
            return get_valid_task_number(user_tasks, prompt)
    except ValueError:
        print("Invalid input. Please enter a valid integer.\n")
        return get_valid_task_number(user_tasks, prompt)
    except Exception as e:
        print(f"Error: {e}\n")
        return get_valid_task_number(user_tasks, prompt)


def edit_task(task: Dict[str, str], all_tasks: List[Dict[str, str]]) -> None:
    """Allow user to edit a task's username or due date."""
    if task['completed'].lower() == 'y':
        print("Cannot edit a completed task.\n")
        return

    print("\nEditing task:")
    print(f"Current assigned user: {task['username']}")
    print(f"Current due date: {task['due_date']}\n")

    while True:
        try:
            print("What would you like to edit?")
            print("1 - Change assigned user")
            print("2 - Change due date")
            print("3 - Change both")
            print("0 - Cancel")
            edit_choice = input("Enter your choice: ").strip()

            if edit_choice == "0":
                print("Edit cancelled.\n")
                return
            elif edit_choice == "1":
                new_user = input("Enter new username: ").strip()
                if not new_user:
                    print("Username cannot be empty.\n")
                    continue
                task['username'] = new_user
                save_all_tasks(all_tasks)
                print("Task updated successfully!\n")
                return
            elif edit_choice == "2":
                new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
                if not is_valid_date(new_due_date):
                    print("Invalid date format. Please use YYYY-MM-DD.\n")
                    continue
                task['due_date'] = new_due_date
                save_all_tasks(all_tasks)
                print("Task updated successfully!\n")
                return
            elif edit_choice == "3":
                new_user = input("Enter new username: ").strip()
                if not new_user:
                    print("Username cannot be empty.\n")
                    continue
                new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
                if not is_valid_date(new_due_date):
                    print("Invalid date format. Please use YYYY-MM-DD.\n")
                    continue
                task['username'] = new_user
                task['due_date'] = new_due_date
                save_all_tasks(all_tasks)
                print("Task updated successfully!\n")
                return
            else:
                print("Invalid choice. Please try again.\n")
        except Exception as e:
            print(f"Error: {e}\n")


def view_mine(tasks: List[Dict[str, str]], username: str) -> None:
    """Display tasks assigned to the current user and allow editing."""
    user_tasks = [task for task in tasks if task['username'] == username]
    if not user_tasks:
        print("No tasks assigned to you.\n")
        return

    while True:
        print("\n" + "="*50)
        print("MY TASKS")
        print("="*50)
        for i, task in enumerate(user_tasks, 1):
            print(f"\nTask {i}:")
            print(f"  Title: {task['title']}")
            print(f"  Description: {task['description']}")
            print(f"  Assigned date: {task['assigned_date']}")
            print(f"  Due date: {task['due_date']}")
            print(f"  Completed: {'Yes' if task['completed'].lower() == 'y' else 'No'}")
        print("="*50)

        task_num = get_valid_task_number(user_tasks)
        
        if task_num == -1:
            return

        selected_task = user_tasks[task_num - 1]
        
        while True:
            try:
                print(f"\nSelected: {selected_task['title']}")
                print("1 - Mark as complete")
                print("2 - Edit task")
                print("0 - Back to task list")
                action = input("Enter your choice: ").strip()

                if action == "0":
                    break
                elif action == "1":
                    if selected_task['completed'].lower() == 'y':
                        print("This task is already marked as complete.\n")
                    else:
                        selected_task['completed'] = 'y'
                        save_all_tasks(tasks)
                        print("Task marked as complete!\n")
                    break
                elif action == "2":
                    edit_task(selected_task, tasks)
                    user_tasks = [task for task in tasks if task['username'] == username]
                    break
                else:
                    print("Invalid choice. Please try again.\n")
            except Exception as e:
                print(f"Error: {e}\n")


def generate_reports(tasks: List[Dict[str, str]], users: Dict[str, str]) -> None:
    """Generate task_overview.txt and user_overview.txt reports with statistics."""
    try:
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task['completed'].lower() == 'y')
        uncompleted_tasks = total_tasks - completed_tasks
        
        today = datetime.now()
        overdue_tasks = sum(
            1 for task in tasks 
            if task['completed'].lower() == 'n' and 
            datetime.strptime(task['due_date'], "%Y-%m-%d") < today
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

        with open(USER_OVERVIEW_FILE, "w") as f:
            f.write("USER OVERVIEW REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total number of users: {len(users)}\n")
            f.write(f"Total number of tasks: {total_tasks}\n\n")

            for user in users.keys():
                user_tasks = [task for task in tasks if task['username'] == user]
                user_total = len(user_tasks)
                user_completed = sum(1 for task in user_tasks if task['completed'].lower() == 'y')
                user_uncompleted = user_total - user_completed
                user_overdue = sum(
                    1 for task in user_tasks 
                    if task['completed'].lower() == 'n' and 
                    datetime.strptime(task['due_date'], "%Y-%m-%d") < today
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

        print("Reports generated successfully!\n")
        print(f"- {TASK_OVERVIEW_FILE}")
        print(f"- {USER_OVERVIEW_FILE}\n")

    except Exception as e:
        print(f"Error generating reports: {e}\n")


def display_statistics(tasks: List[Dict[str, str]], users: Dict[str, str]) -> None:
    """Display statistics from task_overview.txt and user_overview.txt."""
    if not os.path.exists(TASK_OVERVIEW_FILE) or not os.path.exists(USER_OVERVIEW_FILE):
        print("Reports not found. Generating reports...\n")
        generate_reports(tasks, users)

    try:
        print("\n" + "="*60)
        print("STATISTICS")
        print("="*60 + "\n")

        with open(TASK_OVERVIEW_FILE, "r") as f:
            print(f.read())
        
        print("\n" + "="*60 + "\n")
        
        with open(USER_OVERVIEW_FILE, "r") as f:
            print(f.read())
        
        print("="*60 + "\n")

    except Exception as e:
        print(f"Error displaying statistics: {e}\n")


def main() -> None:
    """Main program loop."""
    users = load_users()
    username = login(users)
    is_admin = username == "admin"
    
    while True:
        print("\nPlease select one of the following options:")
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
            elif choice == "gr":
                tasks = load_tasks()
                generate_reports(tasks, users)
            elif choice == "ds":
                tasks = load_tasks()
                display_statistics(tasks, users)
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