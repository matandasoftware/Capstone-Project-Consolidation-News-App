"""
UPDATE Operation - Task Manager
Modify existing tasks in the task list
"""


def update_task(tasks, task_id, **kwargs):
    """
    Update an existing task's attributes.

    Args:
        tasks (list): List of tasks
        task_id (int): ID of task to update
        **kwargs: Attributes to update (title, description, completed,
                  category)

    Returns:
        list: Updated task list
    """
    for task in tasks:
        if task["id"] == task_id:
            # Update allowed fields
            if "title" in kwargs:
                task["title"] = kwargs["title"]
            if "description" in kwargs:
                task["description"] = kwargs["description"]
            if "completed" in kwargs:
                task["completed"] = kwargs["completed"]
            if "category" in kwargs:
                task["category"] = kwargs["category"]

            print(f"? Task {task_id} updated successfully")
            print(f"  Updated: {', '.join(kwargs.keys())}")
            return tasks

    print(f"? Task with ID {task_id} not found.")
    return tasks


def mark_complete(tasks, task_id):
    """
    Mark a task as completed.

    Args:
        tasks (list): List of tasks
        task_id (int): ID of task to mark complete

    Returns:
        list: Updated task list
    """
    return update_task(tasks, task_id, completed=True)


def mark_incomplete(tasks, task_id):
    """
    Mark a task as incomplete.

    Args:
        tasks (list): List of tasks
        task_id (int): ID of task to mark incomplete

    Returns:
        list: Updated task list
    """
    return update_task(tasks, task_id, completed=False)


# Example usage
if __name__ == "__main__":
    # Sample task list
    my_tasks = [
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
            "completed": False,
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

    print("Original tasks:")
    for task in my_tasks:
        status = 'Completed' if task['completed'] else 'Pending'
        print(f"  {task['id']}: {task['title']} - {status}")

    print("\n" + "="*60)

    # Update task title and description
    my_tasks = update_task(
        my_tasks,
        1,
        title="Complete CRUD Matrix (Updated)",
        description="All CRUD operations documented"
    )

    # Mark task as complete
    print()
    my_tasks = mark_complete(my_tasks, 2)

    # Update category
    print()
    my_tasks = update_task(my_tasks, 3, category="urgent")

    print("\n" + "="*60)
    print("\nUpdated tasks:")
    for task in my_tasks:
        status = 'Completed' if task['completed'] else 'Pending'
        print(f"  {task['id']}: {task['title']} - {status}")
