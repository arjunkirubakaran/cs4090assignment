Feature: Viewing how old a task is

  Scenario: User checks task age
    Given a task was created 5 days ago
    When the user views the task
    Then the system should show its age as 5 days
