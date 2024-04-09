from abc import ABC, abstractmethod
from typing import List
from kandy_kafka.gui.panels import TopicsPanel, TopicDataPanel
from kandy_kafka.models import Topic

import urwid


class TopicsView:
    def __init__(self):
        self.elements = {
            "topics_names": TopicsPanel(),
            "topic_data": TopicDataPanel()
            }
        self.columns = urwid.Columns([
            ('weight', 1, self.elements["topics_names"].show()),
            ('weight', 1.5, self.elements["topic_data"].show())
        ], dividechars=1)
        

    def update_topics_names(self, topics_names: List[str]):
        self.elements["topics_names"].update(topics_names)
        self.update()
    
    def update(self):
        self.columns.contents[0] = (self.elements["topics_names"].show(), self.columns.options())
