import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from unittest.mock import patch
from tasks import filter_tasks_by_priority, save_tasks

@pytest.mark.parametrize("priority,expected_count", [
    ("High", 2),
    ("Medium", 1),
    ("Low", 0)
])
def test_filter_tasks_by_priority_param(priority, expected_count):
    tasks = [
        {"id": 1, "priority": "High"},
        {"id": 2, "priority": "High"},
        {"id": 3, "priority": "Medium"}
    ]
    result = filter_tasks_by_priority(tasks, priority)
    assert len(result) == expected_count

def test_save_tasks_mocked():
    with patch("builtins.open") as mock_open:
        tasks = [{"id": 1, "title": "Mock Test"}]
        save_tasks(tasks, "fakefile.json")
        mock_open.assert_called_once()
