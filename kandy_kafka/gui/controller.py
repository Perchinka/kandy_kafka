# The code block below is needed to avoid a cyclic import error, while using Bootstrap class for type-hinting
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kandy_kafka.bootstrap import Bootstraped

from textual.widgets import Footer, Header
from textual.app import App, ComposeResult
from kandy_kafka.gui.views import TopicsView


class Controller(App):
    """Main application controller"""

    BINDINGS = [("ctrl+r", "reload", "reload")]
    CSS_PATH = "app.tcss"  # Textual CSS file for styling

    def __init__(self, bootstraped: Bootstraped):
        super().__init__()
        self.bootstrapped = bootstraped
        self.kafka_adapter = self.bootstrapped.kafka_adapter
        self.view = TopicsView()  # Instantiate the TopicsView from views.py

    async def on_mount(self):
        await self.reload_topics()

    async def reload_topics(self):
        topics = self.kafka_adapter.get_topics()  # Fetch topics from Kafka
        self.view.show_topics(topics)  # Update the table in the view

    async def action_reload(self) -> None:
        await self.reload_topics()

    def compose(self) -> ComposeResult:
        yield self.view
        yield Footer()
