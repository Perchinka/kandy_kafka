from kandy_kafka.adapters.kafka_adapter import KafkaAdapter

class KafkaMonitorModel:
    def __init__(self, host):
        self.kafka_adapter = KafkaAdapter(host)

    def get_brokers(self):
        return self.kafka_adapter.get_brokers()

    def get_topics(self):
        return self.kafka_adapter.get_topics()