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
def check_if_file_not_found_error_is_raised(start_kandy, rename_config_file_if_exsits):
    with pytest.raises(FileNotFoundError):
        read_hosts()

@then('the application should prompt the user to create or specify a configuration file')
def check_prompt_to_create_config():
    # Have no idea how to tests this yet. Probably will do custom Exception and use it
    pass


@scenario("features/hosts.feature","Wrong yaml syntax error")
def test_that_error_is_raised_if_wrong_syntax():
    pass

@pytest.fixture
@given("A configuration file is present and has a wrong syntax")
def create_config_file():
    file = Path.home() / '.config' / 'kandy' / 'hosts.yaml'  
    backup_file = file.with_suffix('.back')
    
    if file.exists():
        file.rename(backup_file)

    file.write_text('askdl') 
    # Wrong yaml syntax is written to the file,
    # Probably should use parametrized tests, so I can check that error raises with diffrent syntax errors
    # (Or research for libs, wich will do that for me)

    yield

    if backup_file.exists():
        backup_file.rename(file)

@then('the application should raise a YAMLError')
def check_if_syntax_error_is_raised():
    with pytest.raises(SyntaxError): # TODO: research for proper way to do that
        read_hosts()
