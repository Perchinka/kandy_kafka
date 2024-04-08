from dataclasses import dataclass
from kandy_kafka.adapters.kafka_adapter import KafkaAdapter

@dataclass
class Bootstraped:
    kafka_adapter: KafkaAdapter

class Bootstrap:
    bootstraped: Bootstraped
    
    def __call__(self):
        self._start_kafka()

    def _start_kafka(self):
        self.bootstraped.kafka_adapter.connect()