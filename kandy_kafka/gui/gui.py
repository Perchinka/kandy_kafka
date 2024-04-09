from __future__ import annotations
from typing import TYPE_CHECKING

import logging
from kandy_kafka.gui.views import TopicsView
import urwid

from kandy_kafka.bootstrap import Bootstrap


class GUI:
    def __init__(self):
        self.palette = [
            ('focused', 'black', 'white'),
            ('colored', 'dark blue', '') 
        ] # TODO, make it configurable

        self.view = TopicsView()
        self.loop = urwid.MainLoop(self.view.columns, palette=self.palette)
        self.loop.set_alarm_in(1, self.update_topics_names)

    def update_topics_names(self, loop, data=None):
        topic_names = Bootstrap.bootstraped.kafka_adapter.get_topics_names()
        self.view.update_topics_names(topic_names)
        self.loop.set_alarm_in(1, self.update_topics_names)
        return True
    
    def run(self):
        self.loop.run()
        logging.info("GUI started")
        return True

    def stop(self):
        self.loop.stop()
        logging.info("GUI stopped")
        return True