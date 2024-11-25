import os
from kandy_kafka import logger
from pathlib import Path

from kandy_kafka.exceptions import HostsFileHasWrongSyntax, HostsFileNotFound

import yaml


class Config:
    """
    Configuration class for setting up Kafka connection and general application settings

    Attributes:
        LOGGING_LEVEL (str): The logging level for the application
        KAFKA_HOST (str): The host address of the Kafka server
        KAFKA_PORT (int): The port of the Kafka server
        DATA_POLLING_INTERVAL (int): Interval in seconds for polling data from Kafka
        PALETTE (List): The color palette for the application UI
    """

    LOGGING_LEVEL: str

    KAFKA_HOST: str
    KAFKA_PORT: int

    DATA_POLLING_INTERVAL: int  # Time in seconds - how often to poll data from Kafka

    def __init__(self, host="localhost", port=29092) -> None:
        """
        Initializes the Config class with default host and port for Kafka

        Args:
            host (str): Kafka host, defaults to "localhost"
            port (int): Kafka port, defaults to 29092
        """
        self.LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
        logger.setup_logger(self.LOGGING_LEVEL)

        self.hosts_file = Path.home() / ".config" / "kandy" / "hosts.yaml"

        self.KAFKA_HOST = host
        self.KAFKA_PORT = port

    def load_hosts(self, clustername="default", config_file=None) -> None:
        """
        Loads the Kafka host and port settings from a hosts YAML file based on the cluster name

        Args:
            clustername (str): The name of the Kafka cluster, defaults to "default"
            config_file (Path, optional): Optional path to a specific configuration file

        Raises:
            HostsFileNotFound: If the hosts file is not found
            HostsFileHasWrongSyntax: If the hosts file has incorrect syntax or the cluster is not found
        """
        if not self.hosts_file.exists():
            raise HostsFileNotFound(f"Hosts file {self.hosts_file} not found")

        # Optionally use a non-default config file
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
