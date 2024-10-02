import pytest
from kandy_kafka.adapters.kafka_adapter import KafkaAdapter
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Consumer, Message, Producer


@pytest.fixture
def kafka_adapter(server):
    """Instantiate a KafkaAdapter object and return it as a fixture"""
    adapter = KafkaAdapter(server.HOST, server.PORT)
    yield adapter


def test_should_return_topic_list(kafka_adapter):
    topics = kafka_adapter.get_topics()
    assert isinstance(topics, list)
    assert all(topic in topics for topic in ["test1", "test2", "test3"])


def test_should_return_10_messages_from_topic(kafka_adapter):
    messages = kafka_adapter.get_messages("test1")
    assert isinstance(messages, list)
    assert len(messages) == 10
    assert all(isinstance(message, Message) for message in messages)


def test_should_return_50_messages_from_topic_with_100_messages(kafka_adapter):
    messages = kafka_adapter.get_messages("test2")
    assert isinstance(messages, list)
    assert len(messages) == 50
    assert all(isinstance(message, Message) for message in messages)
