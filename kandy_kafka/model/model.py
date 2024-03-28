from kandy_kafka.adapters.kafka_adapter import KafkaAdapter

class KafkaMonitorModel:
    def __init__(self, host: str):
        self.kafka_adapter = KafkaAdapter(host)

    def get_brokers(self) -> dict:
        return self.kafka_adapter.get_brokers()

    def get_topics(self) -> dict:
        return self.kafka_adapter.get_topics()