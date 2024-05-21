from os import rename
from pytest import fixture
from pytest_bdd import scenario, given, when, then
from kandy_kafka.utils.hosts import read_hosts
import pathlib

@fixture
def default_config():
    return {
        "default": {
            "host": "localhost",
            "port": 9092,
        }
    }

@fixture
def clean_config_directory():
    file = pathlib.Path.home() / '.config' / 'kandy' / 'hosts.bak'
    if file.exists():
        file.rename(file.with_suffix('.yaml'))

@scenario('features/hosts.feature', 'Default configuration')
def test_if_config_file_doesnt_exist_default_config_created():
    pass

@fixture
@given('The configuration file does not exist')
def rename_config_file_if_exsits():
    file = pathlib.Path.home() / '.config' / 'kandy' / 'hosts.yaml'
    if file.exists():
        file.rename(file.with_suffix('.bak'))

    return file.exists()

@fixture
@when('I read the configuration file')
def read_config_file():
    return read_hosts()

@then('I should get the default configuration and the file should be created')
def check_default_config_and_file_creation(default_config, read_config_file, clean_config_directory):
    file = pathlib.Path.home() / '.config' / 'kandy' / 'hosts.yaml'
    config = read_config_file

    assert file.exists()
    assert config == [default_config]

