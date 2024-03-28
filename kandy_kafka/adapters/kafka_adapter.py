from abc import ABC, abstractmethod
from confluent_kafka import Consumer

class AbstractKafkaAdapter(ABC):
    @abstractmethod
    def get_brokers(self):
        raise NotImplementedError

    @abstractmethod
    def get_topics(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_consumer_groups(self):
        raise NotImplementedError


class KafkaAdapter(AbstractKafkaAdapter):
    def __init__(self, host):
        self.host = host

    def get_brokers(self):
        # TODO: logic to get broker information
        pass

    def get_topics(self):
        # TODO: logic to get topic information
        pass

    def get_consumer_groups(self):
        # TODO: logic to get consumer group information
        pass