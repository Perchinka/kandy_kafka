import pytest
from kandy_kafka.adapters.kafka_adapter import KafkaAdapter
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Consumer, Producer


@pytest.fixture
def kafka_adapter(server):
    """Instantiate a KafkaAdapter object and return it as a fixture"""
    adapter = KafkaAdapter(server.HOST, server.PORT)
    yield adapter


def test_should_return_topic_list(kafka_adapter):
    topics = kafka_adapter.get_topics()
    assert isinstance(topics, list)
    assert set(topics) == set(["test","test2","test3"])


def test_should_return_messages_from_topic(kafka_adapter):
    messages = kafka_adapter.get_messages("test_topic_1")
    assert isinstance(messages, list)
    assert len(messages) == 10
    assert all(isinstance(message, str) for message in messages)
