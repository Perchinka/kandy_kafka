from typing import List, Optional
from confluent_kafka import Uuid
from pydantic import BaseModel


class Topic(BaseModel):
    id: Uuid  # confluent_kafka Uuid
    name: str
    is_internal: bool
    partitions: int  # TODO use list[partitions] model instead. For now I will just store amount of partitions, it's good enough
    amount_of_messages: int

    class Config:
        arbitrary_types_allowed = True


class Partition(BaseModel):
    id: int
    replicas: Optional[
        List[int]
    ]  # For now it will be optional as I don't need it yet, but in future it might be handy. Also it should be broker-id, but I'm not sure if it's int
    isrs: Optional[List[int]]  # Same as for the one above


class Message(BaseModel):
    pass
