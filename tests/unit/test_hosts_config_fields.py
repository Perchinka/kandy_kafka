import pytest
from kandy_kafka.utils.hosts import Cluster

def test_that_error_is_raised_if_port_is_greater_than_65535():
    with pytest.raises(ValueError):
        Cluster(host="localhost", port=65536)


def test_that_error_is_raised_if_port_is_less_than_0():
    with pytest.raises(ValueError):
        Cluster(host="localhost", port=-1)

def test_that_error_is_raised_if_host_is_empty_string():
    with pytest.raises(ValueError):
        Cluster(host="", port=9092)

def test_that_error_is_raised_if_host_is_not_a_string():
    with pytest.raises(ValueError):
        Cluster(host=1234, port=9092)

def test_that_error_is_raised_if_host_is_wrong_ip_format():
    with pytest.raises(ValueError):
        Cluster(host="192.168.1", port=9092)
    with pytest.raises(ValueError):
        Cluster(host="256.256.256.256", port=9092)

def test_that_ValueError_is_raised_if_empty_host():
    with pytest.raises(ValueError):
        Cluster(host="", port=9092)

def tests_that_cluster_does_not_raise_errors_with_correct_host():
    cluster = Cluster(host="localhost", port=9092)
    assert cluster.host == "localhost"
    assert cluster.port == 9092

def tests_that_cluster_does_not_raise_errors_with_correct_ip():
    cluster = Cluster(host="192.168.1.1", port=9092)
    assert cluster.host == "192.168.1.1"
    assert cluster.port == 9092

