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
        config = Config()
        
        # Here I should load hosts config and ask user to choose cluster

        logging.info("ATTEMPTING TO BOOTSTRAP - creating KafkaAdapter")
        kafka_adapter = KafkaAdapter(config.KAFKA_HOST, config.KAFKA_PORT)

        Bootstrap.bootstraped = Bootstraped(
            config=config,
            kafka_adapter=kafka_adapter,
        )

        controller = Controller(Bootstrap.bootstraped)
        controller.run()

        logging.info("BOOTSTRAPING Completed")

        return Bootstrap.bootstraped
