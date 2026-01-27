"""
Demonstration of CRUD Operations - Task Manager
Complete demonstration showing Create, Read, Update, and Delete operations
"""

from create import create_task
from read import display_tasks, read_task, search_tasks
from update import update_task, mark_complete
from delete import delete_task, delete_completed_tasks


# Initialize empty task list
tasks = []

# ========== CREATE OPERATIONS ==========
print("\n" + "="*60)
print(" 1. CREATE OPERATIONS ".center(60))
print("="*60)

tasks = create_task(
    tasks,
    "Complete CRUD Matrix",
    "Document all CRUD operations",
    "assignment"
)
tasks = create_task(
    tasks,
    "Test application",
    "Run all test cases",
    "testing"
)
tasks = create_task(
    tasks,
    "Submit assignment",
    "Upload to learning portal",
    "school"
)
tasks = create_task(
    tasks,
    "Review feedback",
    "Check instructor comments",
    "school"
)

# ========== READ OPERATIONS ==========
print("\n" + "="*60)
print(" 2. READ OPERATIONS ".center(60))
print("="*60)
display_tasks(tasks)

print("\nReading specific task (ID: 2):")
read_task(tasks, 2)

# ========== SEARCH OPERATIONS ==========
print("\n" + "="*60)
print(" 3. SEARCH OPERATIONS ".center(60))
print("="*60)
search_tasks(tasks, "assignment")

# ========== UPDATE OPERATIONS ==========
print("\n" + "="*60)
print(" 4. UPDATE OPERATIONS ".center(60))
print("="*60)

tasks = update_task(
    tasks,
    1,
    description="All CRUD operations fully documented and tested"
)
tasks = mark_complete(tasks, 1)
tasks = update_task(tasks, 3, category="urgent", completed=True)

print("\nAfter updates:")
display_tasks(tasks)

# ========== DELETE OPERATIONS ==========
print("\n" + "="*60)
print(" 5. DELETE OPERATIONS ".center(60))
print("="*60)

tasks = delete_task(tasks, 2)

print("\nAfter deletion:")
display_tasks(tasks)

tasks = delete_completed_tasks(tasks)

print("\nFinal task list:")
display_tasks(tasks)

# ========== SUMMARY ==========
print("\n" + "="*60)
print(" CRUD OPERATIONS COMPLETED ".center(60))
print("="*60)
completed = sum(1 for task in tasks if task["completed"])
print(f"\nTotal: {len(tasks)} | Completed: {completed} | "
      f"Pending: {len(tasks) - completed}")
print("="*60 + "\n")
