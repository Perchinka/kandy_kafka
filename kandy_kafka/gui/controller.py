# The code block below is needed to avoid a cyclic import error, while using Bootstrap class for type-hinting
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kandy_kafka.bootstrap import Bootstraped

from textual.widgets import Footer
from textual.app import App, ComposeResult
from kandy_kafka.gui.views import TopicsView


class Controller(App):
    """Main application controller"""

    BINDINGS = [
        ("ctrl+l", "focus_next"),
    ]
    CSS_PATH = "app.css"  # Textual CSS file for styling

    def __init__(self, bootstraped: Bootstraped):
        super().__init__()
        self.view = TopicsView(bootstraped)  # Instantiate the TopicsView from views.py
        self.bind("ctrl+j", "focus_previous")

    async def reload_topics(self):
        self.view.load_topics()  # Update the table in the view

    def compose(self) -> ComposeResult:
        yield self.view
        yield Footer()
