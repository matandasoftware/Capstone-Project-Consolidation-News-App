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


def view_completed(tasks: List[Dict[str, str]]) -> None:
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


def get_valid_task_number(max_tasks: int, attempt: int = 1) -> int:
    """
    Recursively get a valid task number from user input with enhanced validation.
    
    Args:
        max_tasks (int): Maximum valid task number (number of available tasks).
        attempt (int): Current attempt number for tracking recursive calls.
    
    Returns:
        int: Valid task number (1 to max_tasks) or -1 to return to main menu.
    
    Raises:
        RecursionError: If maximum recursion depth is reached (handled gracefully).
    """
    try:
        # Provide helpful context based on attempt number
        if attempt == 1:
            prompt = "Select a task number to edit or enter -1 to return to main menu: "
        elif attempt <= 3:
            prompt = f"Please enter a valid number (1-{max_tasks}) or -1 to return: "
        else:
            prompt = f"Attempt {attempt}: Enter a number between 1 and {max_tasks}, or -1 to return: "
        
        # Add helpful hints for multiple failed attempts
        if attempt == 4:
            print("💡 Hint: Make sure you're entering just the number (e.g., '1', '2', '3')")
        elif attempt == 6:
            print("💡 Available options: Numbers 1 through {} or -1 to go back".format(max_tasks))
        elif attempt >= 8:
            print("⚠️  Having trouble? Try entering -1 to return to the main menu.")
        
        user_input = input(prompt).strip()
        
        # Handle empty input
        if not user_input:
            print("❌ Input cannot be empty.")
            return get_valid_task_number(max_tasks, attempt + 1)
        
        # Try to convert to integer
        try:
            choice = int(user_input)
        except ValueError:
            print(f"❌ '{user_input}' is not a valid number.")
            return get_valid_task_number(max_tasks, attempt + 1)
        
        # Validate the choice
        if choice == -1:
            return -1
        elif 1 <= choice <= max_tasks:
            return choice
        else:
            print(f"❌ {choice} is out of range. Please choose between 1 and {max_tasks}.")
            return get_valid_task_number(max_tasks, attempt + 1)
            
    except RecursionError:
        print("⚠️  Too many invalid attempts. Returning to main menu for your safety.")
        return -1
    except KeyboardInterrupt:
        print("\n🚫 Operation cancelled by user.")
        return -1
    except Exception as e:
        print(f"⚠️  Unexpected error: {e}")
        return -1


def view_mine(tasks: List[Dict[str, str]], username: str) -> None:
    """
    Display tasks assigned to the current user with editing capabilities.
    Uses recursive input validation for enhanced user experience.

    Args:
        tasks (list): List of all task dictionaries.
        username (str): The current user's username.
    """
    user_tasks = [task for task in tasks if task['username'] == username]
    if not user_tasks:
        print("No tasks assigned to you.\n")
        return
    
    while True:
        print("Your Tasks:")
        for i, task in enumerate(user_tasks, 1):
            status_indicator = "✅" if task['completed'].lower() == 'y' else "📋"
            print(f"{i}. {status_indicator} Task:")
            print(f"   Title: {task['title']}")
            print(f"   Description: {task['description']}")
            print(f"   Assigned date: {task['assigned_date']}")
            print(f"   Due date: {task['due_date']}")
            print(f"   Completed: {task['completed']}\n")
        
        # Use recursive validation for task selection
        task_num = get_valid_task_number(len(user_tasks))
        
        if task_num == -1:
            break
        
        selected_task = user_tasks[task_num - 1]
        
        # Find the task index in the full tasks list
        task_index = -1
        for i, task in enumerate(tasks):
            if (task['username'] == selected_task['username'] and 
                task['title'] == selected_task['title'] and
                task['assigned_date'] == selected_task['assigned_date']):
                task_index = i
                break
        
        if task_index == -1:
            print("❌ Error: Task not found in main list.\n")
            continue
        
        print(f"\n📝 Selected Task: {selected_task['title']}")
        print("1. Mark as complete")
        print("2. Edit task")
        print("3. Return to task list")
        
        while True:
            try:
                action = input("Choose an action (1-3): ").strip()
                
                if action == "1":
                    if selected_task['completed'].lower() == 'y':
                        print("✅ Task is already completed.\n")
                    else:
                        tasks[task_index]['completed'] = 'y'
                        user_tasks[task_num - 1]['completed'] = 'y'
                        save_all_tasks(tasks)
                        print("✅ Task marked as complete!\n")
                    break
                
                elif action == "2":
                    if selected_task['completed'].lower() == 'y':
                        print("⚠️  Cannot edit a completed task.\n")
                        break
                    
                    print("What would you like to edit?")
                    print("1. Username")
                    print("2. Due date")
                    print("3. Both")
                    
                    edit_choice = input("Choose option (1-3): ").strip()
                    
                    if edit_choice in ["1", "3"]:
                        new_username = input("Enter new username: ").strip()
                        if new_username:
                            tasks[task_index]['username'] = new_username
                            user_tasks[task_num - 1]['username'] = new_username
                            print(f"👤 Username updated to: {new_username}")
                    
                    if edit_choice in ["2", "3"]:
                        while True:
                            new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
                            if is_valid_date(new_due_date):
                                tasks[task_index]['due_date'] = new_due_date
                                user_tasks[task_num - 1]['due_date'] = new_due_date
                                print(f"📅 Due date updated to: {new_due_date}")
                                break
                            else:
                                print("❌ Invalid date format. Please use YYYY-MM-DD.")
                    
                    save_all_tasks(tasks)
                    print("✅ Task updated successfully!\n")
                    break
                
                elif action == "3":
                    break
                else:
                    print("❌ Invalid choice. Please enter 1, 2, or 3.\n")
            
            except KeyboardInterrupt:
                print("\n🚫 Operation cancelled.")
                break
            except Exception as e:
                print(f"⚠️  Error: {e}\n")


def display_statistics(tasks: List[Dict[str, str]]) -> None:
    """
    Display comprehensive statistics about tasks and users.
    Reads from generated report files if available for enhanced information.

    Args:
        tasks (list): List of all task dictionaries.
    """
    if not tasks:
        print("No tasks available for statistics.\n")
        return
    
    # Check if enhanced reports exist
    task_overview_exists = os.path.exists("task_overview.txt")
    user_overview_exists = os.path.exists("user_overview.txt")
    
    if task_overview_exists and user_overview_exists:
        print("=" * 60)
        print("COMPREHENSIVE TASK STATISTICS (from generated reports)")
        print("=" * 60)
        
        try:
            # Read and display task overview statistics
            with open("task_overview.txt", "r") as f:
                lines = f.readlines()
                
            # Extract key statistics from the report
            for line in lines:
                if line.startswith("Total tasks:") or \
                   line.startswith("Completed tasks:") or \
                   line.startswith("Incomplete tasks:") or \
                   line.startswith("Overdue tasks:") or \
                   line.startswith("Percentage of"):
                    print(line.strip())
            
            print("\n" + "-" * 40)
            print("USER BREAKDOWN:")
            print("-" * 40)
            
            # Read and display user overview statistics
            with open("user_overview.txt", "r") as f:
                lines = f.readlines()
            
            current_user = None
            for line in lines:
                line = line.strip()
                if line.startswith("Total number of users:"):
                    print(line)
                    print()
                elif line.startswith("USER:"):
                    current_user = line.replace("USER: ", "")
                    print(f"📊 {current_user}:")
                elif line.startswith("  Total tasks assigned:") or \
                     line.startswith("  Completed tasks:") or \
                     line.startswith("  Incomplete tasks:") or \
                     line.startswith("  Overdue tasks:"):
                    print(f"   {line.strip()}")
                elif line.startswith("  Percentage of") and current_user:
                    print(f"   {line.strip()}")
                elif line == "" and current_user:
                    print()
                    current_user = None
            
            print("=" * 60)
            print("📈 Enhanced statistics loaded from generated reports!")
            print("💡 Use 'gr' to regenerate reports with latest data.")
            print("=" * 60)
            print()
            
        except Exception as e:
            print(f"Error reading report files: {e}")
            print("Falling back to basic statistics...\n")
            # Fall back to basic statistics
            _display_basic_statistics(tasks)
            
    else:
        print("=" * 50)
        print("BASIC TASK STATISTICS")
        print("=" * 50)
        print("💡 Generate reports (option 'gr') for enhanced statistics!")
        print("-" * 50)
        _display_basic_statistics(tasks)


def _display_basic_statistics(tasks: List[Dict[str, str]]) -> None:
    """
    Helper function to display basic statistics when enhanced reports are not available.
    
    Args:
        tasks (list): List of all task dictionaries.
    """
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task['completed'].lower() == 'y'])
    incomplete_tasks = total_tasks - completed_tasks
    
    # Count tasks per user
    user_task_count = {}
    for task in tasks:
        username = task['username']
        user_task_count[username] = user_task_count.get(username, 0) + 1
    
    # Calculate overdue tasks
    today = datetime.now().strftime("%Y-%m-%d")
    overdue_tasks = 0
    for task in tasks:
        if task['completed'].lower() == 'n' and task['due_date'] < today:
            overdue_tasks += 1
    
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Incomplete tasks: {incomplete_tasks}")
    print(f"Overdue tasks: {overdue_tasks}")
    
    if total_tasks > 0:
        completion_rate = (completed_tasks / total_tasks) * 100
        incomplete_rate = (incomplete_tasks / total_tasks) * 100
        overdue_rate = (overdue_tasks / total_tasks) * 100
        
        print(f"Completion rate: {completion_rate:.1f}%")
        print(f"Incomplete rate: {incomplete_rate:.1f}%")
        print(f"Overdue rate: {overdue_rate:.1f}%")
    
    print(f"\nTotal users with tasks: {len(user_task_count)}")
    print("Tasks per user:")
    for username, count in sorted(user_task_count.items()):
        percentage = (count / total_tasks) * 100 if total_tasks > 0 else 0
        print(f"  {username}: {count} tasks ({percentage:.1f}% of total)")
    
    print("=" * 50)
    print()


def generate_reports(tasks: List[Dict[str, str]]) -> None:
    """
    Generate detailed reports and save to files with comprehensive statistics.

    Args:
        tasks (list): List of all task dictionaries.
    """
    if not tasks:
        print("No tasks available for report generation.\n")
        return
    
    try:
        # Get current date for overdue calculations
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Calculate overall statistics
        total_tasks = len(tasks)
        completed_tasks = len([task for task in tasks if task['completed'].lower() == 'y'])
        incomplete_tasks = total_tasks - completed_tasks
        overdue_tasks = len([task for task in tasks 
                           if task['completed'].lower() == 'n' and task['due_date'] < today])
        
        # Generate task overview report
        with open("task_overview.txt", "w") as f:
            f.write("TASK OVERVIEW REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"Total tasks: {total_tasks}\n")
            f.write(f"Completed tasks: {completed_tasks}\n")
            f.write(f"Incomplete tasks: {incomplete_tasks}\n")
            f.write(f"Overdue tasks: {overdue_tasks}\n")
            
            if total_tasks > 0:
                completion_percentage = (completed_tasks / total_tasks) * 100
                incomplete_percentage = (incomplete_tasks / total_tasks) * 100
                overdue_percentage = (overdue_tasks / total_tasks) * 100
                
                f.write(f"Percentage of completed tasks: {completion_percentage:.1f}%\n")
                f.write(f"Percentage of incomplete tasks: {incomplete_percentage:.1f}%\n")
                f.write(f"Percentage of overdue tasks: {overdue_percentage:.1f}%\n")
            
            f.write("\nALL TASKS:\n")
            f.write("-" * 30 + "\n")
            for i, task in enumerate(tasks, 1):
                f.write(f"Task {i}:\n")
                f.write(f"  Title: {task['title']}\n")
                f.write(f"  Assigned to: {task['username']}\n")
                f.write(f"  Due date: {task['due_date']}\n")
                f.write(f"  Completed: {task['completed']}\n")
                
                # Add overdue status
                if task['completed'].lower() == 'n' and task['due_date'] < today:
                    f.write(f"  Status: OVERDUE\n")
                elif task['completed'].lower() == 'y':
                    f.write(f"  Status: COMPLETED\n")
                else:
                    f.write(f"  Status: PENDING\n")
                f.write("\n")
        
        # Generate user overview report with enhanced statistics
        with open("user_overview.txt", "w") as f:
            f.write("USER OVERVIEW REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Get all users from tasks and count total users
            users = set(task['username'] for task in tasks)
            total_users = len(users)
            f.write(f"Total number of users: {total_users}\n\n")
            
            for username in sorted(users):
                user_tasks = [task for task in tasks if task['username'] == username]
                completed = len([task for task in user_tasks if task['completed'].lower() == 'y'])
                total_user_tasks = len(user_tasks)
                incomplete = total_user_tasks - completed
                
                # Calculate overdue tasks for this user
                user_overdue = len([task for task in user_tasks 
                                  if task['completed'].lower() == 'n' and task['due_date'] < today])
                
                f.write(f"USER: {username}\n")
                f.write(f"  Total tasks assigned: {total_user_tasks}\n")
                f.write(f"  Completed tasks: {completed}\n")
                f.write(f"  Incomplete tasks: {incomplete}\n")
                f.write(f"  Overdue tasks: {user_overdue}\n")
                
                if total_user_tasks > 0:
                    completion_percentage = (completed / total_user_tasks) * 100
                    incomplete_percentage = (incomplete / total_user_tasks) * 100
                    overdue_percentage = (user_overdue / total_user_tasks) * 100
                    
                    f.write(f"  Percentage of completed tasks: {completion_percentage:.1f}%\n")
                    f.write(f"  Percentage of incomplete tasks: {incomplete_percentage:.1f}%\n")
                    f.write(f"  Percentage of overdue tasks: {overdue_percentage:.1f}%\n")
                
                # Show percentage of total tasks assigned to this user
                if total_tasks > 0:
                    user_task_percentage = (total_user_tasks / total_tasks) * 100
                    f.write(f"  Percentage of all tasks assigned to user: {user_task_percentage:.1f}%\n")
                
                f.write("\n")
        
        print("Enhanced reports generated successfully!")
        print("- task_overview.txt: Comprehensive task statistics with percentages and overdue status")
        print("- user_overview.txt: Detailed per-user statistics with all percentage calculations\n")
        
    except Exception as e:
        print(f"Error generating reports: {e}\n")


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
                view_completed(tasks)
            elif choice == "del":
                tasks = load_tasks()
                delete_task(tasks)
            elif choice == "ds":
                tasks = load_tasks()
                display_statistics(tasks)
            elif choice == "gr":
                tasks = load_tasks()
                generate_reports(tasks)
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