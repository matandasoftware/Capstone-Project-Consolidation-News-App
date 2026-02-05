"""
DELETE Operation - Task Manager
Remove tasks from the task list
"""


def delete_task(tasks, task_id):
    """
    Delete a task from the task list.

    Args:
        tasks (list): List of tasks
        task_id (int): ID of task to delete

    Returns:
        list: Updated task list without deleted task
    """
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(i)
            print(
                f"? Task deleted: {deleted_task['title']} (ID: {task_id})"
            )
            return tasks

    print(f"? Task with ID {task_id} not found.")
    return tasks


def delete_completed_tasks(tasks):
    """
    Delete all completed tasks.

    Args:
        tasks (list): List of tasks

    Returns:
        list: Updated task list without completed tasks
    """
    initial_count = len(tasks)
    tasks = [task for task in tasks if not task["completed"]]
    deleted_count = initial_count - len(tasks)

    print(f"? Deleted {deleted_count} completed task(s)")
    return tasks


def delete_all_tasks(tasks):
    """
    Delete all tasks (clear the list).

    Args:
        tasks (list): List of tasks

    Returns:
        list: Empty task list
    """
    task_count = len(tasks)
    tasks.clear()
    print(f"? Deleted all {task_count} task(s)")
    return tasks


# Example usage
if __name__ == "__main__":
    # Sample task list
    my_tasks = [
        {
            "id": 1,
            "title": "Complete CRUD Matrix",
            "description": "Document all operations",
            "completed": True,
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
            "completed": True,
            "category": "school"
        },
        {
            "id": 4,
            "title": "Review code",
            "description": "",
            "completed": False,
            "category": "development"
        }
    ]

    print("Original tasks:")
    for task in my_tasks:
        status = "?" if task["completed"] else " "
        print(f"  {task['id']}: [{status}] {task['title']}")

    print("\n" + "="*60)

    # Delete a specific task
    my_tasks = delete_task(my_tasks, 2)

    print("\nAfter deleting task 2:")
    for task in my_tasks:
        status = "?" if task["completed"] else " "
        print(f"  {task['id']}: [{status}] {task['title']}")

    print("\n" + "="*60)

    # Delete all completed tasks
    my_tasks = delete_completed_tasks(my_tasks)

    print("\nAfter deleting completed tasks:")
    for task in my_tasks:
        status = "?" if task["completed"] else " "
        print(f"  {task['id']}: [{status}] {task['title']}")

    print("\n" + "="*60)
    print(f"\nRemaining tasks: {len(my_tasks)}")
