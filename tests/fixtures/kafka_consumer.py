from confluent_kafka import Consumer
import pytest


@pytest.fixture
def create_test_topic():
    def _create_test_topic(bootstrap_servers, topic_name):
        consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_servers,
            }
        )
        consumer.subscribe([topic_name])
        consumer.poll(0)
        consumer.close()

    return _create_test_topic


@pytest.fixture
def consumer(server):
    consumer = Consumer(
        {
            "bootstrap.servers": f"{server.HOST}:{server.PORT}",
            "group.id": "test-group",
            "auto.offset.reset": "earliest",
        }
    )
    yield consumer
    consumer.close()
