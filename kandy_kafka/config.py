import os
from kandy_kafka import logger


class Config:
    LOGGING_LEVEL: str

    KAFKA_HOST: str
    KAFKA_PORT: int

    DATA_POLLING_INTERVAL: int # Time in seconds - how often to poll data from Kafka

    def __init__(self) -> None:
        self.LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
        logger.setup_logger(self.LOGGING_LEVEL)
        
        self.KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
        self.KAFKA_PORT = int(os.getenv("KAFKA_PORT", 29092))