Feature: Postponing a task

  Scenario: User delays a task by one day
    Given a task with a due date of today
    When the user chooses to postpone the task
    Then the task's due date should be moved to tomorrow
