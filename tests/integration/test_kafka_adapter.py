import pytest
from kandy_kafka.adapters.kafka_adapter import KafkaAdapter
from confluent_kafka.admin import NewTopic


@pytest.fixture
def kafka_adapter(server):
    adapter = KafkaAdapter(server.HOST, server.PORT)
    yield adapter

@pytest.fixture
def kafka_topics(kafka_admin):
    """Fixture to create test topics in a kafka cluster"""
    topics = [
        "test_topic_1",
        "test_topic_2",
        "test_topic_3"
    ]
    
    new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics]
    fs = kafka_admin.create_topics(new_topics)
    
    for topic, f in fs.items():
        try:
            f.result()
            print(f"Topic {topic} created")
        except Exception as e:
            print(f"Failed to create topic {topic}: {e}")

    yield topics
    
    fs = kafka_admin.delete_topics(topics)
    for topic, f in fs.items():
        try:
            f.result()
            print(f"Topic {topic} deleted")
        except Exception as e:
            print(f"Failed to delete topic {topic}: {e}")


def test_should_return_topic_list(kafka_adapter, kafka_topics):
    topics = kafka_adapter.get_topics()
    assert isinstance(topics, list)
    assert set(topics) == set(kafka_topics)

