import json
from datetime import datetime


# ==============================
# GET TASK STATUS
# ==============================

def get_task_status(task):
    if task["completed"]:
        return "Completed"

    try:
        due_date = datetime.strptime(
            task["due_date"],
            "%d-%m-%Y"
        ).date()

        today = datetime.today().date()

        if due_date < today:
            return "OVERDUE"
        elif due_date == today:
            return "DUE TODAY"
        else:
            return "Pending"

    except ValueError:
        return "Invalid Date"


# ==============================
# SAVE TASKS
# ==============================

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)


# ==============================
# ADD TASK
# ==============================

def add_task():
    task_name = input("Enter your task: ").strip()

    if not task_name:
        print("Task name cannot be empty.")
        return

    due_date = input("Enter due date (DD-MM-YYYY): ").strip()

    print("\nChoose Priority:")
    print("1. High")
    print("2. Medium")
    print("3. Low")

    priority_choice = input("Enter priority: ")

    if priority_choice == "1":
        priority = "High"
    elif priority_choice == "2":
        priority = "Medium"
    elif priority_choice == "3":
        priority = "Low"
    else:
        priority = "Medium"
        print("Invalid choice. Priority set to Medium.")

    task = {
        "name": task_name,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }

    tasks.append(task)
    save_tasks()

    print("✅ Task added successfully!")


# ==============================
# VIEW TASKS
# ==============================

def view_tasks():
    if not tasks:
        print("No tasks added yet.")
        return

    print("\n===== YOUR TASKS =====")

    for i, task in enumerate(tasks, start=1):
        status = get_task_status(task)

        print(
            f"{i}. {task['name']} | "
            f"Due: {task['due_date']} | "
            f"Priority: {task['priority']} | "
            f"{status}"
        )


# ==============================
# COMPLETE TASK
# ==============================

def complete_task():
    if not tasks:
        print("No tasks available.")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['name']}")

    try:
        task_number = int(
            input("Enter task number to complete: ")
        )

        if 1 <= task_number <= len(tasks):
            tasks[task_number - 1]["completed"] = True
            save_tasks()

            print("✅ Task marked as completed!")
        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


# ==============================
# DELETE TASK
# ==============================

def delete_task():
    if not tasks:
        print("No tasks available.")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['name']}")

    try:
        task_number = int(
            input("Enter task number to delete: ")
        )

        if 1 <= task_number <= len(tasks):
            deleted_task = tasks.pop(task_number - 1)
            save_tasks()

            print("🗑️ Deleted:", deleted_task["name"])
        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


# ==============================
# SEARCH TASKS
# ==============================

def search_tasks():
    if not tasks:
        print("No tasks available.")
        return

    search = input(
        "Enter task name to search: "
    ).strip().lower()

    found = False

    print("\n===== SEARCH RESULTS =====")

    for i, task in enumerate(tasks, start=1):
        if search in task["name"].lower():

            status = get_task_status(task)

            print(
                f"{i}. {task['name']} | "
                f"Due: {task['due_date']} | "
                f"Priority: {task['priority']} | "
                f"{status}"
            )

            found = True

    if not found:
        print("No matching tasks found.")


# ==============================
# DASHBOARD
# ==============================

def show_dashboard():
    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task["completed"]
    )

    pending_tasks = total_tasks - completed_tasks

    high_priority = sum(
        1 for task in tasks
        if task["priority"] == "High"
    )

    medium_priority = sum(
        1 for task in tasks
        if task["priority"] == "Medium"
    )

    low_priority = sum(
        1 for task in tasks
        if task["priority"] == "Low"
    )

    overdue_tasks = sum(
        1 for task in tasks
        if get_task_status(task) == "OVERDUE"
    )

    due_today = sum(
        1 for task in tasks
        if get_task_status(task) == "DUE TODAY"
    )

    print("\n===== STUDY PLANNER DASHBOARD =====")

    print("Total Tasks:", total_tasks)
    print("Completed Tasks:", completed_tasks)
    print("Pending Tasks:", pending_tasks)
    print("Overdue Tasks:", overdue_tasks)
    print("Due Today:", due_today)

    print("\n===== PRIORITY =====")

    print("High Priority:", high_priority)
    print("Medium Priority:", medium_priority)
    print("Low Priority:", low_priority)


# ==============================
# LOAD TASKS
# ==============================

try:
    with open("tasks.json", "r") as file:
        tasks = json.load(file)

except (FileNotFoundError, json.JSONDecodeError):
    tasks = []


# Make older tasks compatible
for task in tasks:
    task.setdefault("priority", "Medium")
    task.setdefault("completed", False)
    task.setdefault("due_date", "")


# ==============================
# MAIN PROGRAM
# ==============================

print("\n╔══════════════════════════════════════╗")
print("║       📚 STUDENT STUDY PLANNER      ║")
print("╚══════════════════════════════════════╝")


while True:

    print("\n┌──────────────────────────────────────┐")
    print("│              MAIN MENU               │")
    print("├──────────────────────────────────────┤")
    print("│ 1. ➕ Add Task                       │")
    print("│ 2. 📋 View Tasks                     │")
    print("│ 3. ✅ Mark Task as Completed         │")
    print("│ 4. 🗑️ Delete Task                    │")
    print("│ 5. 🔍 Search Tasks                   │")
    print("│ 6. 📊 Dashboard                      │")
    print("│ 7. 🚪 Exit                           │")
    print("└──────────────────────────────────────┘")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        complete_task()

    elif choice == "4":
        delete_task()

    elif choice == "5":
        search_tasks()

    elif choice == "6":
        show_dashboard()

    elif choice == "7":
        print("\nThank you for using Student Study Planner! 👋")
        break

    else:
        print("❌ Invalid choice. Please try again.")
