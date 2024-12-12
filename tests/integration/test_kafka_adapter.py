import pytest
from confluent_kafka import Producer
from confluent_kafka.admin import NewTopic
from kandy_kafka.adapters.kafka_adapter import KafkaAdapter
from kandy_kafka.domain.models import KafkaMessage, Topic

import string
import random


# --- Helper Functions ---


def generate_random_string(length=6):
    """Generate a random string of fixed length."""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def create_topic(kafka_admin_client, topic_name, num_partitions, replication_factor=1):
    """Create a Kafka topic with the specified name, partitions, and replication factor."""
    topic = NewTopic(
        topic_name, num_partitions=num_partitions, replication_factor=replication_factor
    )
    kafka_admin_client.create_topics([topic])
    return topic_name


def produce_messages(producer, topic_name, messages):
    """Produce a list of messages to a Kafka topic."""
    for message in messages:
        producer.produce(topic_name, value=message)
    producer.flush()


def produce_random_messages(server, topic_name, num_messages=10):
    """
    Produce a specific number of random messages to a Kafka topic.

    Parameters:
    - server (object): Server configuration object containing host and port.
    - topic_name (str): Kafka topic to produce messages to.
    - num_messages (int): Number of random messages to produce.
    """
    producer = Producer({"bootstrap.servers": f"{server.HOST}:{server.PORT}"})
    messages = [f"message-{i}" for i in range(num_messages)]
    produce_messages(producer, topic_name, messages)


# --- Fixtures ---


@pytest.fixture
def kafka_adapter(server):
    """Fixture to initialize and yield a KafkaAdapter object."""
    adapter = KafkaAdapter(server.HOST, server.PORT)
    yield adapter
    adapter.consumer.close()


@pytest.fixture
def create_test_topic(kafka_admin_client, server):
    """
    Fixture to create a unique test topic for each test and produce messages into it.

    This fixture generates a unique topic name, creates the topic in Kafka,
    produces a specific number of messages, and returns the topic name for consumption.
    """

    def _create_topic_with_messages(
        num_messages, num_partitions=1, topic_name=generate_random_string()
    ):
        create_topic(kafka_admin_client, topic_name, num_partitions)
        produce_random_messages(server, topic_name, num_messages)
        return topic_name

    return _create_topic_with_messages


# --- Test Cases ---


def test_should_return_topic_list(kafka_adapter, create_test_topic):
    """
    Test if KafkaAdapter returns a list of topics after auto-producing messages to a new topic.
    """
    topic_name = create_test_topic(num_messages=10)

    topics = kafka_adapter.get_topics()

    assert isinstance(topics, list)
    assert all(isinstance(topic, Topic) for topic in topics)
    assert topic_name in [topic.name for topic in topics]


def test_should_return_10_messages_from_topic_with_10_messages(
    kafka_adapter, create_test_topic
):
    """
    Test if KafkaAdapter correctly returns 10 messages from a topic with exactly 10 messages.
    """
    # Create a topic with exactly 10 messages
    topic_name = create_test_topic(num_messages=10)

    messages = kafka_adapter.get_messages(topic_name)

    assert isinstance(messages, list)
    assert len(messages) == 10
    assert all(isinstance(message, KafkaMessage) for message in messages)


def test_should_return_50_messages_from_topic_with_100_messages(
    kafka_adapter, create_test_topic
):
    """
    Test if KafkaAdapter returns a maximum of 50 messages from a topic with 100 messages. (50 is the default limit)
    """
    # Create a topic with 100 messages
    topic_name = create_test_topic(num_messages=100)

    # Fetch messages from the KafkaAdapter
    messages = kafka_adapter.get_messages(topic_name)

    assert isinstance(messages, list)
    assert len(messages) == 50  # Assuming that KafkaAdapter limits consumption to 50
    assert all(isinstance(message, KafkaMessage) for message in messages)


@pytest.mark.parametrize(
    "num_topics, num_messages, num_partitions",
    [
        (
            random.randint(1, 5),
            random.randint(51, 100),
            random.randint(1, 50),
        ),
    ],
)
def test_kafka_adapter_consume(
    kafka_adapter, kafka_admin_client, num_topics, num_messages, num_partitions, server
):
    """
    Test if KafkaAdapter correctly consumes messages from topics with random amount of partitions

    Parameters:
    - num_topics (int): Number of topics to create.
    - num_messages (int): Number of messages per topic.
    - num_partitions (int): Number of partitions per topic.
    """
    created_topics = []

    # Create topics and produce messages
    for _ in range(num_topics):
        topic_name = f"test-topic-{generate_random_string()}"
        create_topic(kafka_admin_client, topic_name, num_partitions)
        created_topics.append(topic_name)

        produce_random_messages(server, topic_name, num_messages)

    # Test KafkaAdapter consumption
    consumed_topics = kafka_adapter.get_topics()
    for topic in consumed_topics:
        if topic.name in created_topics:
            messages = kafka_adapter.get_messages(topic.name)
            assert len(messages) == min(num_messages, 50)
            assert all(isinstance(message, KafkaMessage) for message in messages)
            assert all(message.topic == topic.name for message in messages)
