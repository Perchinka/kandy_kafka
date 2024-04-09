from typing import List
from kandy_kafka.models import Topic

import urwid
import re

import logging

class TopicsView:
    def __init__(self, controler):
        self.controler = controler
        self.elements = {
            "topics_names": TopicsList(self),
            "topic_data": TopicDataPanel()
            }
        self.columns = urwid.Columns([
            ('weight', 1, self.elements["topics_names"].show()),
            ('weight', 1.5, self.elements["topic_data"].show())
        ], dividechars=1)

    def update_topics_names(self, topics_names: List[str]):
        self.elements["topics_names"].update_topics(topics_names)
        self.show()

    def get_topic(self, topic_name: str):
        return self.controler.get_topic(topic_name)
    
    def show(self):
        self.columns.contents[0] = (self.elements["topics_names"].show(), self.columns.options())
        self.controler.loop.draw_screen()


class TopicsList:
    def __init__(self, parent_view) -> None:
        self.parent_view = parent_view
        
        # Topics
        self.topics_names = []
        self.topics_list = urwid.SimpleFocusListWalker([])
        
        # Search Field
        self.search_field = urwid.Edit('Search: ')
        urwid.connect_signal(self.search_field, 'change', self.update_on_search)
        self.search_text = ''
        
        # UI
        self.listbox = self.FocusChangeListBox(self.topics_list, self.select_topic)
        self.layout = urwid.LineBox(urwid.Pile([self.listbox]), tlcorner='╭', trcorner='╮', blcorner='╰', brcorner='╯')
        self.last_focus = None
        self.layout = urwid.Pile([('pack', urwid.LineBox(self.search_field, tlcorner='╭', trcorner='╮', blcorner='╰', brcorner='╯')), self.layout])

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
        
    def filter_topics(self):
        search_text = self.search_text
        logging.info(f"Filtering topics with search text: {search_text}")
        if search_text:
            pattern = re.compile(search_text, re.IGNORECASE)
        else:
            pattern = re.compile('.*')
        
        self.topics_list.clear()
        for topic_name in self.topics_names:
            if pattern.search(topic_name):
                selectable_item = urwid.SelectableIcon(topic_name, 100)
                self.topics_list.append(urwid.AttrMap(selectable_item, None, focus_map='focused'))

    def show(self):
        self.filter_topics()
        if self.last_focus is not None and self.last_focus < len(self.topics_list):
            self.topics_list.set_focus(self.last_focus)
        return self.layout
    
    def update_on_search(self, edit, new_edit_text):
        logging.info(f"Search text changed to: {new_edit_text}")
        self.search_text = new_edit_text
        self.parent_view.show()
            
    def update_topics(self, topics_names: List[str] = None):
        if topics_names is not None:
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