import uuid
from pydantic import BaseModel
from typing import List, Optional


class Node(BaseModel):
    id: int
    host: str
    port: int
    rack: Optional[str]


class Partition(BaseModel):
    id: int
    leader: Node
    replicas: List[Node]
    isr: List[Node]


class Topic(BaseModel):
    name: str
    topic_id: str # TODO: Find way to convert confluent kafka Uuid to uuid.UUID
    is_internal: bool
    partitions: List[Partition]


class Consumer(BaseModel):
    group_id: str
    consumer_id: str
    host: str
    client_id: str
    assignments: List[Partition]
