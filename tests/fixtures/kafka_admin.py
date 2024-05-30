from confluent_kafka.admin import AdminClient
import pytest

class Server:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port

@pytest.fixture()
def server():
    return Server(
        host = 'localhost',
        port = 29092
    )

@pytest.fixture()
def kafka_admin(server):
    """Fixture to provide a Kafka Admin client for the duration of the test module."""
    client = AdminClient({'bootstrap.servers': f"{server.HOST}:{server.PORT}"})
    yield client

