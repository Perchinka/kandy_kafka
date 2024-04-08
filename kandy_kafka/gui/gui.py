from kandy_kafka.gui.menus import TopicsMenu
import urwid

class GUI:
    def __init__(self):
        self.menu = TopicsMenu()
        self.palette = [
            ('focused', 'black', 'white'),
            ('colored', 'dark blue', '') 
        ]

    def update_topics(self, topics):
        self.menu.update(topics)

    def run(self):
        urwid.MainLoop(self.menu.show(), palette=self.palette).run()
