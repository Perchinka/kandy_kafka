from abc import ABC, abstractmethod
import uuid
from confluent_kafka import TopicCollection
from confluent_kafka.admin import AdminClient, TopicDescription
import logging

from kandy_kafka.models import (
    Topic,
    Partition,
    Broker,
)
from typing import List

class AbstractKafkaClusterAdapter(ABC):
    @abstractmethod
    def get_topics_list(self) -> List[Topic]:
        raise NotImplementedError

    @abstractmethod
    def get_brokers_list(self):
        raise NotImplementedError
      

class ClusterAdapter(AbstractKafkaClusterAdapter):
    def __init__(self, host: str, port: int):
        self.admin_client = AdminClient({
            "bootstrap.servers": f"{host}:{port}"
        })
    
    def get_topics_list(self) -> List[Topic]:
        topics = self.admin_client.list_topics().topics
        return topics
    
    def get_brokers_list(self):
        brokers = self.admin_client.list_topics().brokers
        return brokers
    
    def get_topic(self, topic_name: str) -> Topic:
        topic = self.admin_client.describe_topics(TopicCollection([topic_name]))[topic_name].result()
        partitions = []
        for partition in topic.partitions:
            replicas = []
            isr = []
            for replica in partition.replicas:
                replicas.append(Broker(id=replica.id, host=replica.host, port=replica.port, rack=replica.rack))
            for isr_node in partition.isr:
                isr.append(Broker(id=isr_node.id, host=isr_node.host, port=isr_node.port, rack=isr_node.rack))
            partitions.append(Partition(id=partition.id,
                                        leader=Broker(id=partition.leader.id,
                                                    host=partition.leader.host,
                                                    port=partition.leader.port,
                                                    rack=partition.leader.rack),
                                        replicas=replicas, 
                                        isr=isr))
        return Topic(name=topic_name, topic_id=str(topic.topic_id), is_internal=topic.is_internal, partitions=partitions)
        
