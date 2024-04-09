from kandy_kafka.gui.topic_view import TopicsView
from kandy_kafka.adapters.kafka_adapter import KafkaAdapter

from urwid import MainLoop

class Controller:
    def __init__(self, bootstraped):
        self.bootstraped = bootstraped

    def update_topics_names(self, loop, data=None):
        topic_names = self.bootstraped.kafka_adapter.get_topics_names()
        self.view.update_topics_names(topic_names)
        self.loop.set_alarm_in(1, self.update_topics_names)

    def get_topic(self, topic_name: str):
        return self.bootstraped.kafka_adapter.get_topic(topic_name)
    
    def run(self):
        self.view = TopicsView(self)
        self.loop = MainLoop(self.view.columns, palette=self.bootstraped.config.PALETTE)
        self.loop.set_alarm_in(1, self.update_topics_names)
        self.loop.run()

