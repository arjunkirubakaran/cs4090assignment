import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tasks import postpone_task_by_one_day, filter_tasks_created_this_week, get_task_age_in_days

def test_postpone_task_by_one_day():
    task = {"due_date": "2025-05-01"}
    updated = postpone_task_by_one_day(task)
    expected = (datetime.strptime("2025-05-01", "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    assert updated["due_date"] == expected

def test_filter_tasks_created_this_week():
    now = datetime.now()
    recent = now.strftime("%Y-%m-%d %H:%M:%S")
    old = (now - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")

    tasks = [
        {"id": 1, "created_at": recent},
        {"id": 2, "created_at": old}
    ]

    filtered = filter_tasks_created_this_week(tasks)
    assert len(filtered) == 1
    assert filtered[0]["id"] == 1

from tasks import get_task_age_in_days

def test_get_task_age_in_days():
    five_days_ago = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    task = {"created_at": five_days_ago}
    age = get_task_age_in_days(task)
    assert age == 5
