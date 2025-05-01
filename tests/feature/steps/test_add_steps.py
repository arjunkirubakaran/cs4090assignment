from pytest_bdd import scenarios, given, when, then
from datetime import datetime, timedelta

scenarios('../add_task.feature')
scenarios('../complete_task.feature')
scenarios('../postpone_task.feature')
scenarios('../filter_created_this_week.feature')
scenarios('../task_age.feature')

task_list = []

@given("the task list is currently empty")
def empty_task_list():
    global task_list
    task_list = []

@when('the user creates a task called "Refactor login endpoint" with priority "Medium" and category "Work"')
def user_adds_task():
    global task_list
    task_list.append({
        "id": 1,
        "title": "Refactor login endpoint",
        "priority": "Medium",
        "category": "Work",
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@then('the task list should include one task with the title "Refactor login endpoint"')
def task_was_added():
    assert any(task["title"] == "Refactor login endpoint" for task in task_list)
    assert len(task_list) == 1

task = {}

@given('a task titled "Submit project proposal" that is not marked complete')
def setup_task():
    global task
    task = {"title": "Submit project proposal", "completed": False}

@when("the user clicks the complete button")
def mark_complete():
    global task
    task["completed"] = True

@then("the task should be marked as completed")
def check_completed():
    assert task["completed"] is True

@given("a task with a due date of today")
def task_due_today():
    global task
    task = {"due_date": datetime.now().strftime("%Y-%m-%d")}

@when("the user chooses to postpone the task")
def postpone():
    global task
    current = datetime.strptime(task["due_date"], "%Y-%m-%d")
    task["due_date"] = (current + timedelta(days=1)).strftime("%Y-%m-%d")

@then("the task's due date should be moved to tomorrow")
def check_new_due_date():
    expected = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    assert task["due_date"] == expected

all_tasks = []
filtered_tasks = []

@given("one task was created today and another 10 days ago")
def setup_recent_and_old():
    global all_tasks
    all_tasks = [
        {"id": 1, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        {"id": 2, "created_at": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")}
    ]

@when("the user filters for tasks created this week")
def apply_filter():
    global all_tasks, filtered_tasks
    week_ago = datetime.now() - timedelta(days=7)
    filtered_tasks = [
        t for t in all_tasks if datetime.strptime(t["created_at"], "%Y-%m-%d %H:%M:%S") >= week_ago
    ]

@then("only the task created today should be visible")
def verify_filtered():
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["id"] == 1

age_in_days = None

@given("a task was created 5 days ago")
def setup_old_task():
    global task
    created_at = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    task = {"created_at": created_at}

@when("the user views the task")
def calculate_age():
    global task, age_in_days
    created = datetime.strptime(task["created_at"], "%Y-%m-%d %H:%M:%S")
    age_in_days = (datetime.now() - created).days

@then("the system should show its age as 5 days")
def verify_age():
    assert age_in_days == 5
