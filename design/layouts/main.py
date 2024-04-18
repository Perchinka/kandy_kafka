import urwid
from typing import List

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

class TopicsNames(RoundedBox):
    def __init__(self, topics: List):
        body = urwid.ListBox(
            urwid.SimpleFocusListWalker(
                [urwid.AttrMap(urwid.SelectableIcon(topic, 100), None, focus_map="reverse") for topic in topics]
            )
        )
        super().__init__(body)

class TopicsList(urwid.Pile):
    def __init__(self, topics: List):
        super().__init__([('pack', SearchBar()), TopicsNames(topics)])

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
    topics = ["Test", "Topic", "Thing", "Hehehe"]*100
    Main(topics).run()
