from kandy_kafka.model.model import KafkaMonitorModel
from kandy_kafka.view.cli import KafkaMonitorCLIView

class KafkaMonitorController:
    def __init__(self):
        self.model = None
        self.view = KafkaMonitorCLIView()

    def connect(self, host: str):
        # TODO: config with connections info and aliases (kinda ssh config file)
        host = 'localhost:9092' # For now will be hardcoded TODO: replace with actual logic
        self.model = KafkaMonitorModel(host)

    def run(self):
        self.connect('localhost:9092')
        brokers = str(self.model.get_brokers())
        self.view.display_output(brokers)