import pytest
from kandy_kafka.utils.hosts import read_hosts
import pathlib

@pytest.fixture
def default_config():
    return {
        "default": {
            "host": "localhost",
            "port": 9092,
        }
    }

def test_if_config_file_doesnt_exist_default_config_created(default_config):
    file = pathlib.Path.home() / '.config' / 'kandy' / 'hosts.yaml'
    if file.exists():
        file.rename(file.with_suffix('.bak'))

    config = read_hosts()

    assert file.exists()
    assert config == [default_config]

