import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from hypothesis import given, strategies as st
from tasks import filter_tasks_by_priority, search_tasks, generate_unique_id, filter_tasks_by_completion, save_tasks
import json

@given(st.lists(st.dictionaries(keys=st.just("priority"), values=st.sampled_from(["High", "Medium", "Low"]))))
def test_filtered_priority_output_matches_input(task_list):
    for level in ["High", "Medium", "Low"]:
        filtered = filter_tasks_by_priority(task_list, level)
        for task in filtered:
            assert task.get("priority") == level

@given(
    st.lists(st.fixed_dictionaries({
        "title": st.text(min_size=0, max_size=30),
        "description": st.text(min_size=0, max_size=100)
    })),
    st.text(min_size=1, max_size=10)
)
def test_search_tasks_returns_tasks_with_query(tasks, query):
    result = search_tasks(tasks, query)
    for task in result:
        combined = f"{task.get('title', '')}{task.get('description', '')}".lower()
        assert query.lower() in combined

@given(st.lists(st.integers(min_value=1, max_value=999)), st.integers(min_value=1, max_value=999))
def test_generate_unique_id_never_duplicates(existing_ids, extra):
    task_list = [{"id": i} for i in existing_ids]
    new_id = generate_unique_id(task_list)
    all_ids = [task["id"] for task in task_list]
    assert new_id not in all_ids or new_id == max(all_ids) + 1 if all_ids else new_id == 1

@given(st.lists(st.dictionaries(keys=st.just("completed"), values=st.booleans())))
def test_completed_filter_returns_only_true(tasks):
    result = filter_tasks_by_completion(tasks, True)
    assert all(task.get("completed") for task in result)

@given(st.lists(st.dictionaries(keys=st.text(min_size=1), values=st.text())))
def test_save_tasks_creates_valid_json(tasks):
    test_file = "test_tasks_output.json"
    save_tasks(tasks, test_file)
    with open(test_file, "r") as f:
        loaded = json.load(f)
    assert loaded == tasks
    os.remove(test_file)
