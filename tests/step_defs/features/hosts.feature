Feature: Read and validate host configuration

  Scenario: Error when no configuration file is found
    Given No configuration file is present
    When the user tries to start Kandy
    Then the application should raise a FileNotFoundError
    And the application should prompt the user to create or specify a configuration file
