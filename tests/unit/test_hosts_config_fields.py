# import pytest
# from kandy_kafka.exceptions import HostsFileHasWrongSyntax
#
# def test_that_error_is_raised_if_port_is_greater_than_65535():
#     with pytest.raises(HostsFileHasWrongSyntax):
#         KafkaConnection(host="localhost", port=65536)
#
# def test_that_error_is_raised_if_port_is_less_than_0():
#     with pytest.raises(HostsFileHasWrongSyntax):
#         KafkaConnection(host="localhost", port=-1)
#
# def test_that_error_is_raised_if_host_is_empty_string():
#     with pytest.raises(HostsFileHasWrongSyntax):
#         KafkaConnection(host="", port=9092)
#
# def test_that_error_is_raised_if_host_is_not_a_string():
#     with pytest.raises(HostsFileHasWrongSyntax):
#         KafkaConnection(host=1234, port=9092)
#
# def test_that_error_is_raised_if_host_is_wrong_ip_format():
#     with pytest.raises(HostsFileHasWrongSyntax):
#         KafkaConnection(host="192.168.1", port=9092)
#         KafkaConnection(host="256.256.256.256", port=9092)
#
# def test_that_HostsWrongSyntax_is_raised_if_empty_host():
#     with pytest.raises(HostsFileHasWrongSyntax):
#         KafkaConnection(host="", port=9092)
#
# @pytest.mark.parametrize("host", ["localhost", "127.0.0.1", "192.168.1.1", "example.com", "example.co.uk"])
# def tests_that_cluster_does_not_raise_errors_with_valid_hostnames(host):
#     cluster = KafkaConnection(host=host, port=9092)
#     assert cluster.host == host
#     assert cluster.port == 9092
#
# def tests_that_cluster_does_not_raise_errors_with_correct_ip():
#     cluster = KafkaConnection(host="192.168.1.1", port=9092)
#     assert cluster.host == "192.168.1.1"
#     assert cluster.port == 9092
#
