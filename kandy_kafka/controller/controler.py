from kandy_kafka.model.model import KafkaMonitorModel
from kandy_kafka.view.cli import KafkaMonitorCLIView

class KafkaMonitorController:
    def __init__(self, host):
        self.model = KafkaMonitorModel(host)
        self.view = KafkaMonitorCLIView()

    def run(self):
        brokers = self.model.get_brokers()

        self.view.display_output(brokers)