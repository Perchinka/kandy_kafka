from abc import ABC, abstractmethod
from confluent_kafka import KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
import logging

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
        self.admin_client = AdminClient({'bootstrap.servers': self.host})

    def get_brokers(self) -> dict:
        cluster_metadata = self.admin_client.list_topics(timeout=10)
        return cluster_metadata.brokers

    def get_topics(self) -> dict:
        cluster_metadata = self.admin_client.list_topics(timeout=10)
        return cluster_metadata.topics

    def get_consumer_groups(self) -> dict:
        try:
            return self.admin_client.list_groups(timeout=10)
        except KafkaException as e:
            if e.args[0].code() == KafkaError._TiIMED_OUT:
                logging.error('Timed out while trying to list consumer groups')
            else:
                raise e