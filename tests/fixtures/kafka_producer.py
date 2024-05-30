from confluent_kafka import Producer
from pytest import fixture

@fixture
def producer(server):
    producer = Producer({
        'bootstrap.servers': f'{server.HOST}:{server.PORT}'
    })
    yield producer
    producer.close()
