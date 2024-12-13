from dataclasses import dataclass
import logging
from typing import Any
from kandy_kafka.adapters.kafka_adapter import KafkaAdapter
from kandy_kafka.config import Config
from kandy_kafka.gui.controller import Controller


@dataclass
class Bootstraped:
    """
    Data class to hold essential components for the bootstrapped system

    Attributes:
        config (Config): The configuration object
        kafka_adapter (KafkaAdapter): The adapter used to interface with the Kafka cluster
    """

    config: Config
    kafka_adapter: KafkaAdapter


class Bootstrap:
    """
    Class responsible for bootstrapping the application by loading configuration and setting up Kafka components

    This class creates an instance of `Bootstraped` which holds the configuration and Kafka adapter
    and starts the application by initializing the Controller

    Attributes:
        bootstraped (Bootstraped): A static attribute that stores the bootstrapped components once initialized
    """

    bootstraped: Bootstraped

    def __call__(self, *args: Any, **kwds: Any) -> Bootstraped:
        """
        Invokes the bootstrap process. This method loads configuration, initializes the Kafka adapter
        and starts the application by launching the Controller

        Args:
            *args (Any): Additional arguments (not used in the current implementation)
            **kwds (Any): Keyword arguments containing 'host', 'port', and optionally 'clustername' for Kafka setup

        Returns:
            Bootstraped: Returns an instance of `Bootstraped` containing the config and Kafka adapter
        """
        logging.info("ATTEMPTING TO BOOTSTRAP - initializing config")
        config = Config(kwds["host"], kwds["port"])

        # TODO rewrite this
        if kwds["clustername"]:
            config.load_hosts(kwds["clustername"])

        logging.info("ATTEMPTING TO BOOTSTRAP - creating KafkaAdapter")
        kafka_adapter = KafkaAdapter(config.KAFKA_HOST, config.KAFKA_PORT)

        Bootstrap.bootstraped = Bootstraped(
            config=config,
            kafka_adapter=kafka_adapter,
        )

        controller = Controller(Bootstrap.bootstraped)
        controller.run()
        # TODO: Implement graceful connection error handling for better fault tolerance

        logging.info("BOOTSTRAPING Completed")

        return Bootstrap.bootstraped
