Feature: Read and validate host configuration

  Scenario: Error when no configuration file is found
    Given Configuration file is not present
    When system loads config  
    Then application should prompt user to create or specify a configuration file
  
  Scenario Outline: Configuration file has syntax error
    Given Configuration file is present
    And Configuration file has <error_type> syntax error
    When system loads config
    Then application should show <error>

    Examples:
      | error_type | error |
      | missing_host | "Host is missing" |
      | missing_port | "Port is missing" |
      | empty_file | "Configuration file is empty" |

  Scenario: Configuration file is valid
    Given Configuration file is present
    And Configuration file has valid syntax
    When system loads config
    Then config should have valid connection details

  Scenario: Configuration file has invalid yaml syntax
    Given Configuration file is present
    And Configuration file has invalid yaml syntax
    When system loads config
    Then application should raise yaml error
