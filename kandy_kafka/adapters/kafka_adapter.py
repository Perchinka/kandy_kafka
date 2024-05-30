from abc import ABC, abstractmethod
import uuid
from confluent_kafka import TopicCollection
from confluent_kafka.admin import AdminClient, TopicDescription
import logging

from kandy_kafka.models import (
    Topic,
    Partition,
    Node,
    Consumer
)
from typing import Dict, List

class AbstractKafkaClusterAdapter(ABC):
    @abstractmethod
    def get_topics(self) -> List[str]:
        raise NotImplementedError

class KafkaAdapter(AbstractKafkaClusterAdapter):
    def __init__(self, host: str, port: int):
        self.admin_client = AdminClient({
            "bootstrap.servers": f"{host}:{port}"
        })

    def get_topics(self) -> List[str]:
        topics = self.admin_client.list_topics().topics
        return list(topics)
