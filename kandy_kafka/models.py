import uuid
from pydantic import BaseModel
from typing import List, Optional


class Broker(BaseModel): # Called Node in confluent kafka library
    id: int
    host: str
    port: int
    rack: Optional[str]


class Partition(BaseModel):
    id: int
    leader: Broker
    replicas: List[Broker]
    isr: List[Broker]


class Topic(BaseModel):
    name: str
    topic_id: str # TODO: Find way to convert confluent kafka Uuid to uuid.UUID
    is_internal: bool
    partitions: List[Partition]
