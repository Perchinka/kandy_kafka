from abc import ABC, abstractmethod
from typing import List
from kandy_kafka.gui.panels import TopicsPanel, TopicDataPanel
from kandy_kafka.models import Topic

import urwid

class Menu(ABC):
    @abstractmethod
    def update(self, **data):
        raise NotImplementedError


class TopicsMenu(Menu):
    def __init__(self):
        self.panels = {
            "topics": TopicsPanel(),
            "topic_data": TopicDataPanel()
            }
        
    def show(self):
        return urwid.Columns([
            ('weight', 1, self.panels["topics"].show()),
            ('weight', 1.5, self.panels["topic_data"].show())
        ], dividechars=1)

    def update(self, topics: List[Topic]):
        self.panels["topics"].update(topics)
        self.panels["topic_data"].update(topics[0])
