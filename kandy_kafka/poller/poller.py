import threading
import time

from kandy_kafka.adapters.kafka_adapter import KafkaAdapter
from kandy_kafka.poller.cache import _cache # Temporary

class Poller:
    def __init__(self, host: str, port: int, interval: int = 1, cache: dict = _cache):
        self.kafka_adapter = KafkaAdapter(host, port)
        self.interval = interval
        self.running = False
        self.thread = None
        self.cache = cache

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            data = self.kafka_adapter.poll_data()
            self.cache = data.copy()
            time.sleep(self.interval)

    def get_cache(self):
        return self.cache