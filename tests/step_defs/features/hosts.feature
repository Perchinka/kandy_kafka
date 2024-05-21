Feature: Read and validate host configuration

  Scenario: Default configuration
    Given The configuration file does not exist
    When I read the configuration file
    Then I should get the default configuration and the file should be created

  Scenario: Valid configuration file is used
    Given the configuration file contains valid host data
   When the configuration is read and validated
    Then the configuration is used

  Scenario: Invalid configuration file raises error
    Given the configuration file contains invalid host data
    When the configuration is read and validated
    Then an error is raised
