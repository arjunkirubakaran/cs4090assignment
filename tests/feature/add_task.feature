Feature: Adding a task to the system

  Scenario: User submits a complete task entry
    Given the task list is currently empty
    When the user creates a task called "Refactor login endpoint" with priority "Medium" and category "Work"
    Then the task list should include one task with the title "Refactor login endpoint"
