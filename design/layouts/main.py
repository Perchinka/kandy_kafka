import urwid

import random
import uuid
from typing import List

from panwid.datatable import DataTable, DataTableColumn
from panwid.scroll import ScrollBar


class Scroller(ScrollBar):
    _thumb_char = ("light blue", "\u2588")
    _trough_char = ("dark blue", "\u2591")
    _thumb_indicator_top = ("white inverse", "\u234d")
    _thumb_indicator_bottom = ("white inverse", "\u2354")


class RoundedBox(urwid.LineBox):
    def __init__(self, body):
        super().__init__(body, tlcorner="╭", trcorner="╮", blcorner="╰", brcorner="╯")


class HorizontalMenu(urwid.Padding):
    def __init__(self):
        menu = urwid.Columns(
            [
                urwid.SelectableIcon("Home"),
                urwid.SelectableIcon("Topics"),
                urwid.SelectableIcon("About"),
                urwid.SelectableIcon("Exit"),
            ],
        )
        super().__init__(menu, left=2, right=100, min_width=100)


class SearchBar(RoundedBox):
    def __init__(self):
        super().__init__(urwid.Edit("Search: "))


class TopicsDataTable(RoundedBox):
    def __init__(self, topics: List):
        columns = [
            DataTableColumn("topic", "Topic"),
            DataTableColumn("partition", "Partition"),
            DataTableColumn("brokers", "Brokers"),
            DataTableColumn("size", "Size"),
        ]
        data = [dict(topic=urwid.LineBox(urwid.Text(topic)), partition=partition, brokers=brokers, size=size) for topic, partition, brokers, size in topics]
        table = DataTable(
            columns=columns,
            data=data,
            with_scrollbar=Scroller
        )
        super().__init__(urwid.Frame(table))


class TopicsList(urwid.Pile):
    def __init__(self, topics: List):
        super().__init__([('pack', SearchBar()), TopicsDataTable(topics)])


class TopicDetail(RoundedBox):
    def __init__(self, topic: str):
        body = urwid.Filler(urwid.Text(topic), valign="top")
        super().__init__(body)


class Body(urwid.Columns):
    def __init__(self, topics: List):
        super().__init__([TopicsList(topics), TopicDetail("Topic detatils")])


class Main:
    def __init__(self, topics: List):
        palette = [("reverse", "light gray", "black")]
        layout = urwid.Frame(body=Body(topics), header=HorizontalMenu())
        self.loop = urwid.MainLoop(layout, palette=palette)

    def run(self):
        self.loop.run()


if __name__ == "__main__":
    # random data
    topics = [(uuid.uuid4().hex, random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)) for _ in range(10)]
    Main(topics).run()
