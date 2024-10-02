import urwid
import logging
import signal

from kandy_kafka.gui.views import TopicsView

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kandy_kafka.bootstrap import Bootstraped


class Controller:
    def __init__(self, bootstraped: "Bootstraped"):
        self.bootstrapped = bootstraped
        self.kafka_adapter = self.bootstrapped.kafka_adapter
        self.view = TopicsView()
        # Load initial data
        self.reload_topics()

    def reload_topics(self):
        """
        Reload the topics by pulling them from the KafkaModel and updating the TopicsView.
        """
        topics = self.kafka_adapter.get_topics()
        self.view.build_table(topics)

    def handle_input(self, key):
        """
        Handle keyboard inputs ('r' to reload, 'Ctrl-C' to exit).
        """
        if key == "r" or key == "R":
            # Reload topics on 'R' press
            self.reload_topics()
        elif key == "ctrl c":
            # Exit on 'Ctrl-C'
            raise urwid.ExitMainLoop()

    def run(self):
        """
        Start the urwid main loop and handle signal for graceful exit.
        """
        loop = urwid.MainLoop(
            self.view.get_top_view(), unhandled_input=self.handle_input
        )
        signal.signal(signal.SIGINT, lambda signum, frame: loop.stop())
        loop.run()
