import urwid

import random
import uuid
from typing import List

from panwid.datatable import DataTable, DataTableColumn, DataTableDivider


class RoundedBox(urwid.LineBox):
    def __init__(self, body):
        super().__init__(body, tlcorner="╭", trcorner="╮", blcorner="╰", brcorner="╯")


class HorizontalMenu(urwid.Padding):
    def __init__(self):
        menu = urwid.Columns(
            [
                urwid.SelectableIcon("Consumers"),
                urwid.SelectableIcon("Topics"),
                urwid.SelectableIcon("Brokers"),
            ],
        )
        super().__init__(menu, left=2, right=100, min_width=100)


class SearchBar(RoundedBox):
    def __init__(self):
        super().__init__(urwid.Edit("Search: "))


class TopicsDataTable(RoundedBox):
    def __init__(self, topics: List):
        columns = [
            DataTableColumn(
                "topic",
                "Topic",
                width=("weight", 2),
                align="center",
                format_fn=lambda x: x.upper(),
            ),
            DataTableDivider(u"\N{BOX DRAWINGS DOUBLE VERTICAL}"),
            DataTableColumn(
                "partitions",
                "Partitions",
                align="center",
                width=(13),
            ),
            DataTableDivider(u"\N{BOX DRAWINGS DOUBLE VERTICAL}"),
            DataTableColumn(
                "brokers",
                "Brokers",
                align="center",
            ),
            DataTableDivider(u"\N{BOX DRAWINGS DOUBLE VERTICAL}"),
            DataTableColumn(
                "size",
                "Size",
                align="center",
            ),
        ]
        data = [dict(topic=topic, partitions=partitions, brokers=brokers, size=size) for topic, partitions, brokers, size in topics]
        table = DataTable(
            columns=columns,
            data=data,
            with_scrollbar=True,
            sort_refocus=True,
            cell_selection=True
        )
        super().__init__(urwid.Frame(table))


class TopicsList(urwid.Pile):
    def __init__(self, topics: List):
        super().__init__([('pack', SearchBar()), TopicsDataTable(topics)])


class TopicDetail(RoundedBox):
    def __init__(self, topic: str):
        body = urwid.Filler(urwid.Text(topic), valign="top")
        super().__init__(body)


class TopicsView(urwid.Columns):
    def __init__(self, topics: List):
        super().__init__([TopicsList(topics), TopicDetail("Topic detatils")])


class Main:
    def __init__(self, topics: List):
        palette = [
            ('table_row_body', "", ""),
            ('table_row_body focused', "white", 'black'),
            ('table_row_body column_focused', "", 'black'),
            ('table_row_body highlight', "", ""),
            ('table_row_body highlight focused', "", 'black'),
            ('table_row_body highlight column_focused', "", 'black'),
            ('table_row_header', "", ''),
            ('table_row_header focused', "", ''),
            ('table_row_header column_focused', "", 'black'),
            ('table_row_header highlight', "", 'yellow'),
            ('table_row_header highlight focused', "", 'yellow'),
            ('table_row_header highlight column_focused', "", 'yellow'),
            ('table_row_footer', "", 'white'),
            ('table_row_footer focused', "", 'dark gray'),
            ('table_row_footer column_focused', "", 'black'),
            ('table_row_footer highlight', "", 'yellow'),
            ('table_row_footer highlight focused', "", 'yellow'),
            ('table_row_footer highlight column_focused', "", 'yellow') 
        ]
        layout = urwid.Frame(body=TopicsView(topics), header=HorizontalMenu())
        self.loop = urwid.MainLoop(layout, palette=palette)

    def run(self):
        self.loop.run()


if __name__ == "__main__":
    n = 100
    topics = [(uuid.uuid4().hex, random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)) for _ in range(n)]
    Main(topics).run()
