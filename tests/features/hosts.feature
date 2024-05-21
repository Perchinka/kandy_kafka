Feature: Read and validate host configuration

  Scenario: Default configuration is used when file does not exist
    Given the configuration file does not exist
    When the configuration is read
    Then the default configuration is used

  Scenario: Valid configuration file is used
    Given the configuration file contains valid host data
    When the configuration is read and validated
    Then the configuration is used

  Scenario: Invalid configuration file raises error
    Given the configuration file contains invalid host data
    When the configuration is read and validated
    Then an error is raised
