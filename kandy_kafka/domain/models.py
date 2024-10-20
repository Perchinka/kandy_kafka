from datetime import datetime
from typing import List, Optional, Tuple
from confluent_kafka import Uuid
from pydantic import BaseModel


class Partition(BaseModel):
    topic_name: str
    id: int


class Topic(BaseModel):
    id: Uuid  # confluent_kafka Uuid
    name: str
    is_internal: bool
    partitions: List[Partition]
    amount_of_messages: int

    model_config = {"arbitrary_types_allowed": True}


class KafkaMessage(BaseModel):
    topic: str
    offset: int
    partition_id: int
    # timestamp: datetime
    headers: Optional[List[Tuple[str, bytes]]] = None
    value: Optional[bytes] = None
    key: Optional[bytes] = None
