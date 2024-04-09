from typing import List
from kandy_kafka.models import Topic

import urwid


class TopicsView:
    def __init__(self, controler):
        self.controler = controler
        self.elements = {
            "topics_names": TopicsList(),
            "topic_data": TopicDataPanel()
            }
        self.columns = urwid.Columns([
            ('weight', 1, self.elements["topics_names"].show()),
            ('weight', 1.5, self.elements["topic_data"].show())
        ], dividechars=1)
        

    def update_topics_names(self, topics_names: List[str]):
        self.elements["topics_names"].update(topics_names)
        self.update()

    def get_topic(self, topic_name: str):
        return self.controler.get_topic(topic_name)
    
    def update(self):
        self.columns.contents[0] = (self.elements["topics_names"].show(), self.columns.options())


class TopicsList:
    def __init__(self) -> None:
        self.topics_names = []
        self.topics_list = urwid.SimpleFocusListWalker([])
        self.listbox = self.FocusChangeListBox(self.topics_list, self.select_topic)
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

    def get_selected_topic(self):
        if self.last_focus is not None and self.last_focus < len(self.topics_list):
            return self.topics_list[self.last_focus].get_text()[0]

    def select_topic(self, button, user_data):
        _, self.last_focus = self.topics_list.get_focus()


class TopicDataPanel:
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