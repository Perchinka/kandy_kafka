# The code block below is needed to avoid a cyclic import error, while using Bootstrap class for type-hinting
from __future__ import annotations
from typing import TYPE_CHECKING

from textual.widgets import Footer

if TYPE_CHECKING:
    from kandy_kafka.bootstrap import Bootstraped

from textual.app import App, ComposeResult
from textual.message import Message
from kandy_kafka.gui.views import TopicsView
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kandy_kafka.bootstrap import Bootstraped


class ReloadTopics(Message):
    """Message class for reloading topics."""


class Controller(App):
    """Main application controller"""

    BINDINGS = [("f", "fetch", "fetch")]
    CSS_PATH = "app.tcss"  # Textual CSS file for styling

    def __init__(self, bootstraped: Bootstraped):
        super().__init__()
        self.bootstrapped = bootstraped
        self.kafka_adapter = self.bootstrapped.kafka_adapter
        self.view = TopicsView()  # Instantiate the TopicsView from views.py

    async def reload_topics(self):
        """
        Reload the topics by pulling them from the KafkaModel and updating the TopicsView.
        """
        topics = self.kafka_adapter.get_topics()  # Fetch topics from Kafka
        self.view.udpdate_topics(topics)  # Update the table in the view

    async def action_fetch(self) -> None:
        """Handle the message to reload topics."""
        await self.reload_topics()

    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        yield self.view
        yield Footer()
