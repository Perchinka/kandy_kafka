from typing import List, Optional
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

    class Config:
        arbitrary_types_allowed = True


class Message(BaseModel):
    pass
