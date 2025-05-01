import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import tasks  # force src module to be tracked by pytest-cov

import tempfile
from datetime import datetime, timedelta
import pytest
from tasks import (
    load_tasks, save_tasks, generate_unique_id,
    filter_tasks_by_priority, search_tasks,
    filter_tasks_by_category, filter_tasks_by_completion, get_overdue_tasks
)

def test_generate_unique_id():
    tasks = [{"id": 1}, {"id": 2}, {"id": 3}]
    new_id = generate_unique_id(tasks)
    assert new_id == 4

def test_save_and_load_tasks():
    test_data = [{"id": "1", "title": "Test", "priority": "High"}]
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.json') as tmp:
        save_tasks(test_data, tmp.name)
        tmp.seek(0)
        loaded = load_tasks(tmp.name)
    assert loaded == test_data
    os.remove(tmp.name)

def test_filter_tasks_by_priority():
    tasks = [
        {"id": "1", "title": "Do A", "priority": "High"},
        {"id": "2", "title": "Do B", "priority": "Low"}
    ]
    high_tasks = filter_tasks_by_priority(tasks, "High")
    assert len(high_tasks) == 1
    assert high_tasks[0]["priority"] == "High"

def test_search_tasks():
    tasks = [
        {"id": "1", "title": "Go shopping"},
        {"id": "2", "title": "Call mom"},
        {"id": "3", "title": "shop groceries"}
    ]
    result = search_tasks(tasks, "shop")
    assert len(result) == 2
    titles = [task["title"] for task in result]
    assert "Go shopping" in titles and "shop groceries" in titles
from datetime import datetime, timedelta

def test_filter_tasks_by_category():
    tasks = [
        {"id": 1, "title": "Math HW", "category": "School"},
        {"id": 2, "title": "Buy groceries", "category": "Personal"},
    ]
    result = filter_tasks_by_category(tasks, "School")
    assert len(result) == 1
    assert result[0]["title"] == "Math HW"

def test_filter_tasks_by_completion():
    tasks = [
        {"id": 1, "title": "Done Task", "completed": True},
        {"id": 2, "title": "To Do Task", "completed": False},
    ]
    result = filter_tasks_by_completion(tasks, True)
    assert len(result) == 1
    assert result[0]["title"] == "Done Task"

from datetime import datetime

def get_overdue_tasks(tasks):
    today = datetime.today().date()
    overdue = []

    for task in tasks:
        due_str = task.get("due")
        if due_str:
            try:
                due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
                if due_date < today:
                    overdue.append(task)
            except ValueError:
                continue  # skip bad dates

    return overdue
def test_generate_unique_id_empty():
    assert generate_unique_id([]) == 1

def test_filter_tasks_by_priority_no_match():
    tasks = [{"id": 1, "priority": "Low"}]
    result = filter_tasks_by_priority(tasks, "High")
    assert result == []

def test_get_overdue_tasks_bad_date():
    tasks = [{"id": 1, "title": "Invalid Due", "due": "not-a-date"}]
    result = get_overdue_tasks(tasks)
    assert result == []

def test_load_tasks_file_not_found():
    result = load_tasks("nonexistent_file.json")
    assert result == []

def test_load_tasks_invalid_json():
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write("This is not JSON!")
        tmp.seek(0)
        result = load_tasks(tmp.name)
    assert result == []

def test_search_tasks_empty_fields():
    tasks = [{"id": 1}]  # no title or description keys
    result = search_tasks(tasks, "anything")
    assert result == []
