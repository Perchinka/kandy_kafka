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
    """
    Abstract base class for Kafka cluster adapters.

    Defines the interface for interacting with a Kafka cluster, including fetching topics
    and retrieving messages from a given topic.
    """

    @abstractmethod
    def get_topics(self) -> List[Topic]:
        """
        Retrieve a list of topics in the Kafka cluster.

        Returns:
            List[Topic]: A list of Topic objects representing the available topics in the cluster.
        """
        raise NotImplementedError

    @abstractmethod
    def get_messages(self, topic_name: str) -> List[KafkaMessage]:
        """
        Retrieve messages from a specified Kafka topic.

        Args:
            topic_name (str): The name of the Kafka topic to fetch messages from.

        Returns:
            List[KafkaMessage]: A list of KafkaMessage objects representing the retrieved messages.
        """
        raise NotImplementedError


class KafkaAdapter(AbstractKafkaClusterAdapter):
    """
    Kafka adapter that implements the methods to interact with a Kafka cluster using confluent-kafka library.
    """

    def __init__(self, host: str, port: int):
        """
        Initializes the Kafka adapter with the given host and port.

        Args:
            host (str): The hostname or IP address of the Kafka broker.
            port (int): The port number of the Kafka broker.
        """
        self.admin_client = AdminClient({"bootstrap.servers": f"{host}:{port}"})
        self.consumer: Consumer = Consumer(
            {
                "bootstrap.servers": f"{host}:{port}",
                "group.id": "kandy",  # Group ID used to identify the consumer group
                "auto.offset.reset": "earliest",  # Start reading from the earliest offset (Default setting)
            }
        )

    def get_topics(self) -> List[Topic]:
        """
        Retrieve a list of topics in the Kafka cluster.

        Returns:
            List[Topic]: A list of Topic objects, each containing details about the topic and its partitions.
        """

        # Retrieve metadata for all topics in the Kafka cluster
        metadata = self.admin_client.list_topics(timeout=10)

        # Describe each topic in the collection of topics
        topics = self.admin_client.describe_topics(
            TopicCollection(list(metadata.topics))
        )

        # Iterate over the topics and gather details for each
        result = []
        for _, feature in topics.items():
            topic: TopicDescription = feature.result()
            total_messages = 0

            # Retrieve partition details for the current topic
            partitions: List[Partition] = []
            for partition_metadata in topic.partitions:
                partition = Partition(topic_name=topic.name, id=partition_metadata.id)
                partitions.append(partition)

                # Get partition by id
                topic_partition = confluent_kafka.TopicPartition(
                    topic.name, partition_metadata.id
                )

                # Amount_of_messages in the topic is the difference between the latest offset and the earliest one
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
        """
        Fetches messages from the specified Kafka topic (from all partitions so far)

        Args:
            topic_name (str): The name of the Kafka topic to fetch messages from.

        Returns:
            List[KafkaMessage]: A list of KafkaMessage objects representing the consumed messages.
        """
        running = True
        messages: List[Message] = []

        # Callback for handling partition assignment, setting the offset to the beginning
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

        # Dictionary to track offsets for each partition (Needed to spot the end of the topic)
        partition_offsets = {
            partition: {"low": None, "high": None, "current": 0}
            for partition in topic_partitions
        }

        # Fetch watermark offsets for each partition to find start and end offsets
        for partition_id in partition_offsets.keys():
            tp = confluent_kafka.TopicPartition(topic_name, partition_id)
            low, high = self.consumer.get_watermark_offsets(tp)
            partition_offsets[partition_id]["low"] = low
            partition_offsets[partition_id]["high"] = high
            logging.info("Partition %d: Low: %d, High: %d", partition_id, low, high)

        # Polling cycle
        while running:
            msg = self.consumer.poll(timeout=0.1)

            if msg is None:
                # Check if all partitions have been fully consumed
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
                "Message consumed from partition %s: offset: %d",
                partition_id,
                msg.offset(),
            )

            # Stop after consuming a certain predefined number of messages
            # TODO replace with variable or config const
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
