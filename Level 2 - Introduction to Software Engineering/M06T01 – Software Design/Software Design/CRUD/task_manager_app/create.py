"""
CREATE Operation - Task Manager
Adds a new task to the task list
"""


def create_task(tasks, title, description="", category=""):
    """
    Create a new task and add it to the task list.

    Args:
        tasks (list): Current list of tasks
        title (str): Task title (required)
        description (str): Task description (optional)
        category (str): Task category (optional)

    Returns:
        list: Updated task list with new task
    """
    # Generate new ID (max existing ID + 1)
    if tasks:
        new_id = max(task["id"] for task in tasks) + 1
    else:
        new_id = 1

    # Create new task dictionary
    new_task = {
        "id": new_id,
        "title": title,
        "description": description,
        "completed": False,
        "category": category
    }

    # Add to task list
    tasks.append(new_task)

    print(f"? Task created: {title} (ID: {new_id})")

    return tasks


# Example usage
if __name__ == "__main__":
    # Initialize empty task list
    my_tasks = []

    # Create some tasks
    my_tasks = create_task(
        my_tasks,
        "Complete CRUD Matrix",
        "Document all operations",
        "assignment"
    )
    my_tasks = create_task(
        my_tasks,
        "Test application",
        "Run all CRUD operations",
        "testing"
    )
    my_tasks = create_task(
        my_tasks,
        "Submit assignment",
        "",
        "school"
    )

    # Display created tasks
    print(f"\nTotal tasks created: {len(my_tasks)}")
    for task in my_tasks:
        print(f"  - {task['title']} (ID: {task['id']})")
