from typing import List
import urwid
from abc import ABC, abstractmethod

from kandy_kafka.models import Topic

class Panel(ABC):
    @abstractmethod
    def show(self):
        raise NotImplementedError
    
    @abstractmethod
    def update(self):
        raise NotImplementedError


class TopicsPanel(Panel):
    def __init__(self) -> None:
        self.topics = []
        self.topics_list = urwid.SimpleFocusListWalker([])
        self.listbox = urwid.ListBox(self.topics_list)
        self.rounded_layout = urwid.LineBox(self.listbox, tlcorner='╭', trcorner='╮', blcorner='╰', brcorner='╯')

    def show(self):
        self.topics_list.clear()
        for topic in self.topics:
            selectable_item = urwid.SelectableIcon(topic.name, 100)
            self.topics_list.append(urwid.AttrMap(selectable_item, None, focus_map='focused'))
        return self.rounded_layout 
            
    def update(self, topics: List[Topic]):
        self.topics = topics

    def on_topic_selected(self, button, user_data):
        self.topic_data.set_text(str(self.topics[self.topics_list.focus_position]))

class TopicDataPanel(Panel):
    def __init__(self) -> None:
        self.topic_data = urwid.Text('')
        self.rounded_layout = urwid.LineBox(self.topic_data, tlcorner='╭', trcorner='╮', blcorner='╰', brcorner='╯')

    def show(self):
        return urwid.AttrMap(self.rounded_layout, "colored")

    def update(self, topic: Topic):
        data = {"name": topic.name,
                "is_internal": topic.is_internal,
                "Number of partitions": len(topic.partitions),
                "Partitions": [partition.id for partition in topic.partitions]}
        final_data = '\n'.join([f'{key}: {value}' for key, value in data.items()])
        self.topic_data.set_text(final_data)