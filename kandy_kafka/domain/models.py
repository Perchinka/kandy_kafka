from typing import List, Optional, Tuple
from confluent_kafka import Uuid
from pydantic import BaseModel


class Partition(BaseModel):
    """
    Represents a partition in a Kafka topic

    Attributes:
        topic_name (str): The name of the Kafka topic
        id (int): The partition ID
    """

    topic_name: str
    id: int


class Topic(BaseModel):
    """
    Represents a Kafka topic

    Attributes:
        id (Uuid): The unique identifier for the Kafka topic
        name (str): The name of the Kafka topic
        is_internal (bool): Indicates if the topic is an internal Kafka topic
        partitions (List[Partition]): A list of partitions associated with the topic
        amount_of_messages (int): The total number of messages in the topic
    """

    id: Uuid  # confluent_kafka Uuid
    name: str
    is_internal: bool
    partitions: List[Partition]
    amount_of_messages: int

    model_config = {"arbitrary_types_allowed": True}


class KafkaMessage(BaseModel):
    """
    Represents a Kafka message

    Attributes:
        topic (str): The topic from which the message was consumed
        offset (int): The offset of the message within its partition
        partition_id (int): The ID of the partition from which the message was consumed
        headers (Optional[List[Tuple[str, bytes]]]): Optional headers associated with the message
        value (Optional[bytes]): The value (body) of the Kafka message
        key (Optional[bytes]): The key associated with the Kafka message
    """

    topic: str
    offset: int
    partition_id: int
    # timestamp: datetime #
    headers: Optional[List[Tuple[str, bytes]]] = None
    value: Optional[bytes] = None
    key: Optional[bytes] = None
