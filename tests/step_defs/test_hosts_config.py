import pytest
from pytest_bdd import scenario, given, when, then
import yaml
from kandy_kafka.utils.hosts import read_hosts
from pathlib import Path

@scenario('features/hosts.feature', 'Error when no configuration file is found')
def test_that_error_is_raised_if_no_config():
    pass

@pytest.fixture
@given('No configuration file is present')
def rename_config_file_to_bak_if_exsits():
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
def check_if_file_not_found_error_is_raised(start_kandy, rename_config_file_to_bak_if_exsits):
    with pytest.raises(FileNotFoundError):
        read_hosts()

@then('the application should prompt the user to create or specify a configuration file')
def check_prompt_to_create_config():
    pass
    # TODO: copy from below


@scenario("features/hosts.feature","Wrong yaml syntax error")
def test_that_error_is_raised_if_wrong_syntax():
    pass

@pytest.fixture
@given("A configuration file is present and has a wrong syntax")
def create_config_file(rename_config_file_to_bak_if_exsits):
    file = Path.home() / '.config' / 'kandy' / 'hosts.yaml'
    with open(file, 'w') as f:
        f.write("wrong syntax: ][") # TODO: make it parametrized
    
    # Probably will work, didn't test it yet. Should rename original file to bak after that rewrite it with wrong syntax config (Will be fixtures)
    # After tests should rename bak to original file back

@then('the application should raise a YAMLError')
def check_if_syntax_error_is_raised():
    with pytest.raises(yaml.YAMLError): # Should it? TODO: Think of way of handling it
        read_hosts()

@then("the application should prompt the user to fix the configuration file")
def check_promt_to_fix_syntax(capsys):
    with pytest.raises(yaml.YAMLError):
        read_hosts()
    _, err = capsys.readouterr()
    assert "Syntax error in the configuration file" in err
