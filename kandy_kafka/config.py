import os
from kandy_kafka import logger
from pathlib import Path
from typing import List

from kandy_kafka.exceptions import HostsFileHasWrongSyntax, HostsFileNotFound

import yaml


class Config:
    LOGGING_LEVEL: str

    KAFKA_HOST: str
    KAFKA_PORT: int

    DATA_POLLING_INTERVAL: int  # Time in seconds - how often to poll data from Kafka

    PALETTE: List

    def __init__(self, host="localhost", port=29092) -> None:
        self.LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
        logger.setup_logger(self.LOGGING_LEVEL)

        self.hosts_file = Path.home() / ".config" / "kandy" / "hosts.yaml"

        self.KAFKA_HOST = host
        self.KAFKA_PORT = port

        self.PALETTE = [
            ("focused", "black", "white"),
            ("colored", "dark blue", ""),
        ]  # TODO will move it to the config file in feature realises

    def load_hosts(self, clustername="default", config_file=None) -> None:
        if not self.hosts_file.exists():
            raise HostsFileNotFound(f"Hosts file {self.hosts_file} not found")

        if config_file:
            self.hosts_file = config_file

        with open(self.hosts_file, "r") as file:
            hosts = yaml.safe_load(file)
            if hosts is None:
                raise HostsFileHasWrongSyntax(f"Hosts file {self.hosts_file} is empty")

            if clustername not in hosts:
                raise HostsFileHasWrongSyntax(
                    f"Clustername {clustername} not found in {self.hosts_file}"
                )

            cluster = hosts[clustername]
            self.KAFKA_HOST = cluster.get("host")
            self.KAFKA_PORT = cluster.get("port")

            if not self.KAFKA_HOST or not self.KAFKA_PORT:
                raise HostsFileHasWrongSyntax(
                    f"Host or port not found in {self.hosts_file}"
                )
