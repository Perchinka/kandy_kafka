import pytest
from pytest_bdd import scenario, given, when, then
from kandy_kafka.utils.hosts import read_hosts
from pathlib import Path

@scenario('features/hosts.feature', 'Error when no configuration file is found')
def test_that_error_is_raised_if_no_config():
    pass

@pytest.fixture
@given('No configuration file is present')
def rename_config_file_if_exsits():
    file = Path.home() / '.config' / 'kandy' / 'hosts.yaml'
    backup_file = file.with_suffix('.bak')
    if file.exists():
        file.rename(backup_file)

    yield

    # Teardown to restore the configuration file after the test
    if backup_file.exists():
        backup_file.rename(file)

@pytest.fixture
@when('the user tries to start Kandy')
def start_kandy():
    pass

@then('the application should raise a FileNotFoundError')
def check_if_error_is_raised(start_kandy, rename_config_file_if_exsits):
    with pytest.raises(FileNotFoundError):
        read_hosts()

@then('the application should prompt the user to create or specify a configuration file')
def check_prompt_to_create_config():
    pass
