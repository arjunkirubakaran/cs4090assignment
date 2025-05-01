Feature: Filtering recent tasks

  Scenario: Show tasks created within the last 7 days
    Given one task was created today and another 10 days ago
    When the user filters for tasks created this week
    Then only the task created today should be visible
