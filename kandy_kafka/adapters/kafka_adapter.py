from abc import ABC, abstractmethod
from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer, KafkaException, Producer, TopicPartition
from datetime import datetime, timedelta

from typing import List

import logging 

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

        current_time = datetime.now()
        start_time = current_time - timedelta(hours=1)
        end_time = current_time

        # Convert datetime to timestamps in milliseconds
        start_timestamp = int(start_time.timestamp() * 1000)
        end_timestamp = int(end_time.timestamp() * 1000)

        self.consumer.assign([TopicPartition(topic, p) for p in self.consumer.list_topics(topic).topics[topic].partitions.keys()])

        partitions_for_timestamp = [TopicPartition(topic, p, start_timestamp) for p in self.consumer.list_topics(topic).topics[topic].partitions.keys()]
        start_offsets = self.consumer.offsets_for_times(partitions_for_timestamp)

        partitions_for_timestamp = [TopicPartition(topic, p, end_timestamp) for p in self.consumer.list_topics(topic).topics[topic].partitions.keys()]
        end_offsets = self.consumer.offsets_for_times(partitions_for_timestamp)

        for partition in start_offsets:
            self.consumer.seek(partition)

        messages = []

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)  # Poll for messages

                if msg is None:
                    break  # No message received, continue polling

                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        # End of partition event
                        print(f"End of partition reached {msg.partition()}")
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    if msg.timestamp()[1] > end_timestamp:
                        print("End time reached. Stopping consumption.")
                        break

                    messages.append(msg.value().decode('utf-8'))
                    print(f"Received message: {msg.value().decode('utf-8')}")

        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()
            print("Total messages consumed:", len(messages))
            return messages
