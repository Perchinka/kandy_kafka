from abc import ABC, abstractmethod
from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer, Producer, TopicPartition
from datetime import datetime

from typing import List

class AbstractKafkaClusterAdapter(ABC):
    @abstractmethod
    def get_topics(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_messages(self, topic: str) -> List[str]:
        raise NotImplementedError

class KafkaAdapter(AbstractKafkaClusterAdapter):
    def __init__(self, host: str, port: int):
        self.admin_client = AdminClient({
            "bootstrap.servers": f"{host}:{port}"
        })
        self.consumer: Consumer = Consumer({
                                "bootstrap.servers": f"{host}:{port}",
                                "group.id": "kandy",
                                "auto.offset.reset": "earliest"
                            })

    def get_topics(self) -> List[str]:
        topics = self.admin_client.list_topics(timeout=10).topics
        return list(topics)

    def get_messages(self, topic: str) -> List[str]:
        now = int(datetime.now().timestamp() * 1000)
        one_hour_ago = now - (60 * 60 * 1000)

        topic_partition = TopicPartition(topic, 0, one_hour_ago)
        self.consumer.assign([topic_partition])

        self.consumer.seek(topic_partition)
    
        messages = self.consumer.consume(timeout=1)
        return messages
