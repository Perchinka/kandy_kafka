from dataclasses import dataclass
import logging
from typing import Any
from kandy_kafka.adapters.kafka_adapter import KafkaAdapter
from kandy_kafka.config import Config
from kandy_kafka.gui.controller import Controller


@dataclass
class Bootstraped:
    config: Config
    kafka_adapter: KafkaAdapter


class Bootstrap:
    bootstraped: Bootstraped

    def __call__(self, *args: Any, **kwds: Any) -> Bootstraped:
        logging.info("ATTEMPTING TO BOOTSTRAP - loading config")
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
        # TODO make graceful connection error handling and uncomment line above

        logging.info("BOOTSTRAPING Completed")

        return Bootstrap.bootstraped
