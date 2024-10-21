from abc import ABC, abstractmethod
import logging
import confluent_kafka
from confluent_kafka.admin import AdminClient, TopicDescription
from confluent_kafka import (
    Consumer,
    KafkaError,
    Message,
    TopicCollection,
    TopicPartition,
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
        running = True

        messages: List[Message] = []

        def on_assign(consumer: Consumer, partitions: List[TopicPartition]):
            for partition in partitions:
                partition.offset = confluent_kafka.OFFSET_BEGINNING
            consumer.assign(partitions)

        logging.info("Start polling messages")
        self.consumer.subscribe([topic_name], on_assign=on_assign)

        # Get the number of partitions for this topic
        topic_partitions = (
            self.admin_client.list_topics(timeout=10).topics[topic_name].partitions
        )
        partition_offsets = {
            partition: {"low": None, "high": None, "current": 0}
            for partition in topic_partitions
        }

        # Fetch watermark offsets for each partition to know where to stop
        for partition_id in partition_offsets.keys():
            tp = confluent_kafka.TopicPartition(topic_name, partition_id)
            low, high = self.consumer.get_watermark_offsets(tp)
            partition_offsets[partition_id]["low"] = low
            partition_offsets[partition_id]["high"] = high
            logging.info("Partition %d: Low: %d, High: %d", partition_id, low, high)

        while running:
            msg = self.consumer.poll(timeout=1)

            if msg is None:
                # If no message is returned, check if all partitions have been fully consumed
                all_done = all(
                    (
                        partition_offsets[partition]["current"]
                        >= partition_offsets[partition]["high"] - 1
                    )
                    for partition in partition_offsets
                )
                if all_done:
                    logging.info("All partitions have been fully consumed. Stopping.")
                    running = False
                continue

            if msg.error() and msg.error().code() != KafkaError._NO_ERROR:
                # Log errors but continue to consume from other partitions
                logging.error("Kafka error: %s", msg.error())
                continue

            # Record the current offset for the partition
            partition_id = msg.partition()
            partition_offsets[partition_id]["current"] = msg.offset()

            # Collect the message
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

            logging.info(
                "Message consumed from partition %s: offset: ",
                partition_id,
                msg.offset(),
            )

            # Optionally, stop after consuming a certain number of messages
            if len(messages) >= 50:
                logging.info("Reached limit of 50 messages. Stopping.")
                running = False
                continue

        logging.info("End polling messages for topic: %s", topic_name)
        return messages

    # async def create_topics(self, topics: List[str]):
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
