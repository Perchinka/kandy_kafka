from abc import ABC, abstractmethod
import logging
import confluent_kafka
from confluent_kafka.admin import AdminClient, TopicDescription
from confluent_kafka import (
    Consumer,
    KafkaException,
    KafkaError,
    Message,
    TopicCollection,
)
from typing import List
from kandy_kafka.domain.models import KafkaMessage, Topic, Partition


class AbstractKafkaClusterAdapter(ABC):
    @abstractmethod
    def get_topics(self) -> List[Topic]:
        raise NotImplementedError

    @abstractmethod
    def get_messages(self, topic_name: str) -> List[KafkaMessage]:
        raise NotImplementedError


class KafkaAdapter(AbstractKafkaClusterAdapter):
    def __init__(self, host: str, port: int):
        self.admin_client = AdminClient({"bootstrap.servers": f"{host}:{port}"})
        self.consumer: Consumer = Consumer(
            {
                "bootstrap.servers": f"{host}:{port}",
                "group.id": "kandy",
                "auto.offset.reset": "earliest",
            }
        )

    @staticmethod
    def on_assign(consumer: Consumer, partitions):
        for partition in partitions:
            partition.offset = confluent_kafka.OFFSET_BEGINNING
        consumer.assign(partitions)

    def get_topics(self) -> List[Topic]:
        metadata = self.admin_client.list_topics(timeout=10)
        topics = self.admin_client.describe_topics(
            TopicCollection(list(metadata.topics))
        )

        result = []
        for _, feature in topics.items():
            topic: TopicDescription = feature.result()
            total_messages = 0

            partitions: List[Partition] = []
            for partition_metadata in topic.partitions:
                partition = Partition(topic_name=topic.name, id=partition_metadata.id)
                partitions.append(partition)

                # Get partition by id
                topic_partition = confluent_kafka.TopicPartition(
                    topic.name, partition_metadata.id
                )

                # Amount_of_messages in the topic = the latest offset - the earliest one
                low, high = self.consumer.get_watermark_offsets(topic_partition)
                partition_message_count = high - low
                total_messages += partition_message_count

            result.append(
                Topic(
                    id=topic.topic_id,
                    name=topic.name,
                    is_internal=topic.is_internal,
                    partitions=partitions,
                    amount_of_messages=total_messages,
                )
            )

        return result

    def get_messages(self, topic_name: str) -> List[KafkaMessage]:
        # TODO Add "from offset" parameter and pool not 50 first messages, but 50 from specified offset
        metadata = self.consumer.list_topics(topic_name, timeout=10)
        if metadata.topics[topic_name].error is not None:
            raise KafkaException(metadata.topics[topic_name].error)

        running = True

        messages: List[Message] = []

        self.consumer.subscribe([topic_name], on_assign=self.on_assign)
        while running:
            # Timeout isn't reliable though. # TODO Find a better way to handle connection
            msg = self.consumer.poll(timeout=10)
            if msg is None or len(messages) >= 50:
                running = False
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logging.error(f"Error: {msg.error()}")
                    break

            messages.append(
                KafkaMessage(
                    topic=topic_name,
                    offset=msg.offset(),
                    partition_id=msg.partition(),
                    headers=msg.headers(),
                    value=msg.value(),
                    key=msg.key(),
                )
            )
            self.consumer.commit()

        self.consumer.close()
        return messages

    # def create_topics(self, topics: List[str]):
    #     """Create topics"""
    #
    #     new_topics = [
    #         NewTopic(topic, num_partitions=3, replication_factor=1) for topic in topics
    #     ]
    #     # Call create_topics to asynchronously create topics, a dict
    #     # of <topic,future> is returned.
    #     futures = self.admin_client.create_topics(new_topics)
    #
    #     # Wait for operation to finish.
    #     # Timeouts are preferably controlled by passing request_timeout=15.0
    #     # to the create_topics() call.
    #     # All futures will finish at the same time.
    #     for topic, future in futures.items():
    #         try:
    #             future.result()  # The result itself is None
    #             print("Topic {} created".format(topic))
    #         except Exception as e:
    #             print("Failed to create topic {}: {}".format(topic, e))
    #
    # def delete_topics(self, topics):
    #     """delete topics"""
    #
    #     # Call delete_topics to asynchronously delete topics, a future is returned.
    #     # By default this operation on the broker returns immediately while
    #     # topics are deleted in the background. But here we give it some time (30s)
    #     # to propagate in the cluster before returning.
    #     #
    #     # Returns a dict of <topic,future>.
    #     fs = self.admin_client.delete_topics(topics, operation_timeout=30)
    #
    #     # Wait for operation to finish.
    #     for topic, f in fs.items():
    #         try:
    #             f.result()  # The result itself is None
    #             print("Topic {} deleted".format(topic))
    #         except Exception as e:
    #             print("Failed to delete topic {}: {}".format(topic, e))
    #
    # def example_list_consumer_groups(a, args):
    #     """
    #     List Consumer Groups
    #     """
    #     states = {ConsumerGroupState[state] for state in args}
    #     future = a.list_consumer_groups(request_timeout=10, states=states)
    #     try:
    #         list_consumer_groups_result = future.result()
    #         print("{} consumer groups".format(len(list_consumer_groups_result.valid)))
    #         for valid in list_consumer_groups_result.valid:
    #             print("    id: {} is_simple: {} state: {}".format(
    #                 valid.group_id, valid.is_simple_consumer_group, valid.state))
    #         print("{} errors".format(len(list_consumer_groups_result.errors)))
    #         for error in list_consumer_groups_result.errors:
    #             print("    error: {}".format(error))
    #     except Exception:
    #         raise
