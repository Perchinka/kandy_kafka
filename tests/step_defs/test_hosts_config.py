import pytest
from pytest_bdd import parsers, scenarios, given, when, then
import yaml

from kandy_kafka.config import Config
from kandy_kafka.exceptions import HostsFileHasWrongSyntax, HostsFileNotFound
from pathlib import Path

scenarios("../features/hosts.feature")


# Non-existing configuration file scenario
@pytest.fixture
@given("Configuration file is not present")
def non_existing_config_file(tmp_path):
    return tmp_path / "hosts.yaml"


@pytest.fixture
@when("system loads config")
def config():
    return Config()


@then("application should prompt user to create or specify a configuration file")
def check_prompt_to_create_config(config, non_existing_config_file):
    with pytest.raises(HostsFileNotFound):
        config.hosts_file = non_existing_config_file
        config.load_hosts("default")


# Wrong syntax scenario
@pytest.fixture
@given("Configuration file is present")
def config_file(tmp_path):
    file = tmp_path / "hosts.yaml"
    file.touch()
    return file


@pytest.fixture
@given(
    parsers.parse("Configuration file has {error_type} syntax error"),
    target_fixture="config_file_with_wrong_syntax",
)
def config_file_with_wrong_syntax(config_file, error_type):
    assert config_file.exists()
    config_fixture = (
        Path("tests") / "fixtures" / "hosts" / f"wrong_syntax_{error_type}.yaml"
    )
    config_file.write_text(config_fixture.read_text())


@then(parsers.parse("application should show {error}"))
def check_promt_to_fix_syntax(config, error, config_file):
    print(error)  # TODO check that actual error message is in the stderr (Or stdout)
    with pytest.raises(HostsFileHasWrongSyntax):
        config.load_hosts("default", config_file)


# Correct syntax scenario
@pytest.fixture
@given("Configuration file has valid syntax")
def config_file_with_correct_syntax(config_file):
    config_file.write_text(
        """
        default:
            host: localhost
            port: 9092
        """
    )


@then("config should have valid connection details")
def check_config_details(config, config_file):
    config.load_hosts("default", config_file)
    assert config.KAFKA_HOST == "localhost"
    assert config.KAFKA_PORT == 9092


# Invalid yaml syntax scenario
@pytest.fixture
@given("Configuration file has invalid yaml syntax")
def config_file_with_invalid_yaml_syntax(config_file):
    config_file.write_text("][")
    # Well, I could write some invalid yaml fixtures, but naaaah :D


@then("application should raise yaml error")
def check_yaml_error(config, config_file):
    with pytest.raises(yaml.YAMLError):
        config.load_hosts("default", config_file)
