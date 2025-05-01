Feature: Marking a task as complete

  Scenario: User completes an unfinished task
    Given a task titled "Submit project proposal" that is not marked complete
    When the user clicks the complete button
    Then the task should be marked as completed
