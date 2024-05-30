from kandy_kafka.gui.topic_view import TopicsView
from urwid import MainLoop

import logging

class Controller:
    def __init__(self, bootstraped):
        self.bootstrapped = bootstraped

    def update_topics_names(self, loop, data=None):
        topic_names = self.bootstrapped.kafka_adapter.get_topics_names()
        self.view.update_topics_names(topic_names)
        logging.info("Polling")
        loop.set_alarm_in(1, self.update_topics_names)

    def get_topic(self, topic_name: str):
        return self.bootstrapped.kafka_adapter.get_topic(topic_name)
    
    def run(self):
        self.view = TopicsView(self)
        self.loop = MainLoop(self.view.columns, palette=self.bootstrapped.config.PALETTE)
        self.loop.set_alarm_in(1, self.update_topics_names)
        self.loop.run()


