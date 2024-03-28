import urwid
from kandy_kafka.view.view import AbstractView

class KafkaMonitorCLIView(AbstractView):
    def __init__(self):
        self.loop = None

    def display_output(self, output: str):
        if output is None:
            output = 'Test'
        txt = urwid.Text(output)
        attr = urwid.AttrMap(txt, 'streak')
        fill = urwid.Filler(attr)
        padding = urwid.Padding(fill, left=2, right=2)
        linebox = urwid.LineBox(padding)
        palette = [('streak', 'black', 'dark red')]
        self.loop = urwid.MainLoop(linebox, palette)
        self.loop.run()
        
    def stop(self):
        if self.loop:
            self.loop.stop()