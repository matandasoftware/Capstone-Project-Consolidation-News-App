"""
READ Operation - Task Manager
Display tasks from the task list
"""


def display_tasks(tasks):
    """
    Display all tasks in a formatted way.

    Args:
        tasks (list): List of tasks to display

    Returns:
        None
    """
    if not tasks:
        print("No tasks found.")
        return

    print(f"\n{'='*60}")
    print(f"{'TASK LIST':^60}")
    print(f"{'='*60}")

    for task in tasks:
        status = "?" if task["completed"] else " "
        print(f"\nID: {task['id']}")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Category: {task['category']}")
        status_text = 'Completed' if task['completed'] else 'Pending'
        print(f"Status: [{status}] {status_text}")
        print("-" * 60)

    print(f"\nTotal tasks: {len(tasks)}")
    completed = sum(1 for task in tasks if task["completed"])
    pending = len(tasks) - completed
    print(f"Completed: {completed} | Pending: {pending}")


def read_task(tasks, task_id):
    """
    Display a specific task by ID.

    Args:
        tasks (list): List of tasks
        task_id (int): ID of task to display

    Returns:
        dict or None: Task dictionary if found, None otherwise
    """
    for task in tasks:
        if task["id"] == task_id:
            print(f"\n{'='*60}")
            print(f"TASK DETAILS - ID: {task_id}")
            print(f"{'='*60}")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Category: {task['category']}")
            status_text = 'Completed' if task['completed'] else 'Pending'
            print(f"Status: {status_text}")
            print(f"{'='*60}")
            return task

    print(f"? Task with ID {task_id} not found.")
    return None


def search_tasks(tasks, query):
    """
    Search tasks by keyword in title or description.

    Args:
        tasks (list): List of tasks
        query (str): Search keyword

    Returns:
        list: Matching tasks
    """
    if not query:
        print("? Search query cannot be empty.")
        return []

    query_lower = query.lower()
    results = []

    for task in tasks:
        title_match = query_lower in task["title"].lower()
        desc_match = query_lower in task["description"].lower()

        if title_match or desc_match:
            results.append(task)

    if results:
        print(f"\n? Found {len(results)} task(s) matching '{query}':")
        display_tasks(results)
    else:
        print(f"\n? No tasks found matching '{query}'.")

    return results


# Example usage
if __name__ == "__main__":
    # Sample task list
    sample_tasks = [
        {
            "id": 1,
            "title": "Complete CRUD Matrix",
            "description": "Document all operations",
            "completed": False,
            "category": "assignment"
        },
        {
            "id": 2,
            "title": "Test application",
            "description": "Run all CRUD operations",
            "completed": True,
            "category": "testing"
        },
        {
            "id": 3,
            "title": "Submit assignment",
            "description": "",
            "completed": False,
            "category": "school"
        }
    ]

    # Display all tasks
    display_tasks(sample_tasks)

    # Display specific task
    print("\n" + "="*60)
    read_task(sample_tasks, 2)

    # Search tasks
    print("\n" + "="*60)
    search_tasks(sample_tasks, "CRUD")
