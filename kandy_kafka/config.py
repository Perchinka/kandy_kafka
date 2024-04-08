import os
import logging
from kandy_kafka import logger


class Config:
    LOGGING_LEVEL: str

    KAFKA_HOST: str
    KAFKA_PORT: int

    POLLER_INTERVAL: int = 1

    def __init__(self) -> None:
        self.LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
        logger.setup_logger(self.LOGGING_LEVEL)
        
        self.KAFKA_HOST = os.getenv("KAFKA_HOST", None)
        self.KAFKA_PORT = int(os.getenv("KAFKA_PORT", None))