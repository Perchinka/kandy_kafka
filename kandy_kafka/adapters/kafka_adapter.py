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
from typing import Dict, List, Tuple

class AbstractKafkaClusterAdapter(ABC):
    @abstractmethod
    def get_topics_list(self) -> List[Topic]:
        raise NotImplementedError

    @abstractmethod
    def get_brokers_list(self) -> List[Node]:
        raise NotImplementedError
    
    @abstractmethod
    def get_topic(self, topic_name: str) -> Topic:
        raise NotImplementedError
    
    @abstractmethod
    def get_broker(self, broker_id: int) -> Node:
        raise NotImplementedError
    
    @abstractmethod
    def get_consumer_groups(self) -> List[List[Consumer]]:
        raise NotImplementedError
    
    @abstractmethod
    def poll_data(self) -> Tuple[List[Topic], List[Node], List[str]]:
        raise NotImplementedError
      

class KafkaAdapter(AbstractKafkaClusterAdapter):
    def __init__(self, host: str, port: int):
        self.admin_client = AdminClient({
            "bootstrap.servers": f"{host}:{port}"
        })
    
    def get_topics_list(self) -> List[Topic]:
        topics = self.admin_client.list_topics().topics
        topics_list = []
        for topic_name in topics:
            topics_list.append(self.get_topic(topic_name))
        return topics_list
    
    def get_brokers_list(self) -> List[Node]:
        brokers = self.admin_client.list_topics().brokers
        brokers_list = []
        for broker_id in brokers:
            brokers_list.append(self.get_broker(broker_id))
        return brokers_list

    
    def get_topic(self, topic_name: str) -> Topic:
        topic = self.admin_client.describe_topics(TopicCollection([topic_name]))[topic_name].result()
        partitions = []
        for partition in topic.partitions:
            replicas = []
            isr = []
            for replica in partition.replicas:
                replicas.append(Node(id=replica.id, host=replica.host, port=replica.port, rack=replica.rack))
            for isr_node in partition.isr:
                isr.append(Node(id=isr_node.id, host=isr_node.host, port=isr_node.port, rack=isr_node.rack))
            partitions.append(Partition(id=partition.id,
                                        leader=Node(id=partition.leader.id,
                                                    host=partition.leader.host,
                                                    port=partition.leader.port,
                                                    rack=partition.leader.rack),
                                        replicas=replicas, 
                                        isr=isr))
        return Topic(name=topic_name, topic_id=str(topic.topic_id), is_internal=topic.is_internal, partitions=partitions)
    

    def get_broker(self, broker_id: int):
        broker = self.admin_client.describe_cluster().brokers[broker_id]
        return Node(id=broker.id, host=broker.host, port=broker.port, rack=broker.rack)
    

    def get_consumer_groups(self):
        consumer_groups = self.admin_client.list_groups()
        return consumer_groups
        
    
    def poll_data(self) -> Dict:
        topics = self.get_topics_list()
        brokers = self.get_brokers_list()
        consumer_groups = self.get_consumer_groups()

        return {"topic": topics,
                "broker": brokers,
                "consumer_group": consumer_groups}