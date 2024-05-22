import pytest

def test_that_error_is_raised_if_port_is_greater_than_65535():
    from kandy_kafka.utils.hosts import HostConfig
    with pytest.raises(ValueError):
        HostConfig(host="localhost", port=65536)


def test_that_error_is_raised_if_port_is_less_than_0():
    from kandy_kafka.utils.hosts import HostConfig
    with pytest.raises(ValueError):
        HostConfig(host="localhost", port=-1)

def test_that_error_is_raised_if_host_is_empty_string():
    from kandy_kafka.utils.hosts import HostConfig
    with pytest.raises(ValueError):
        HostConfig(host="", port=9092)

def test_that_error_is_raised_if_host_is_not_a_string():
    from kandy_kafka.utils.hosts import HostConfig
    with pytest.raises(ValueError):
        HostConfig(host=1234, port=9092)

# TODO, think about format of hostname for pydantic and write suitable tests, probably use pydantic.KafkaDsn module
# def test_that_error_is_raised_if_host_is_wrong_ip_format():
#     from kandy_kafka.utils.hosts import HostConfig
#     with pytest.raises(ValueError):
#         HostConfig(host="192.168.1", port=9092)
#     with pytest.raises(ValueError):
#         HostConfig(host="256.256.256.256", port=9092)
