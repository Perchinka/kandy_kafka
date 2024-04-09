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
        self.topics_names = []
        self.topics_list = urwid.SimpleFocusListWalker([])
        self.listbox = self.FocusChangeListBox(self.topics_list, self.on_topic_selected)
        self.rounded_layout = urwid.LineBox(self.listbox, tlcorner='╭', trcorner='╮', blcorner='╰', brcorner='╯')
        self.last_focus = None

    class FocusChangeListBox(urwid.ListBox):
        def __init__(self, body, on_focus_changed):
            super().__init__(body)
            self.on_focus_changed = on_focus_changed

        def keypress(self, size, key):
            focus_widget, _ = self.get_focus()
            key = super().keypress(size, key)
            if self.get_focus() != (focus_widget, _):
                self.on_focus_changed(None, None)
            return key

    def show(self):
        self.topics_list.clear()
        for topic_name in self.topics_names:
            selectable_item = urwid.SelectableIcon(topic_name, 100)
            self.topics_list.append(urwid.AttrMap(selectable_item, None, focus_map='focused'))
        if self.last_focus is not None and self.last_focus < len(self.topics_list):
            self.topics_list.set_focus(self.last_focus)
        return self.rounded_layout 
            
    def update(self, topics_names: List[str]):
        self.topics_names = topics_names

    def on_topic_selected(self, button, user_data):
        _, self.last_focus = self.topics_list.get_focus()

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