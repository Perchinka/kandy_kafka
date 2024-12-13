# The code block below is needed to avoid a cyclic import error, while using Bootstrap class for type-hinting
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kandy_kafka.bootstrap import Bootstraped

from textual.widgets import Footer
from textual.app import App, ComposeResult
from kandy_kafka.gui.views import TopicsView


class Controller(App):
    """
    Main application controller (GUI)

    This class controls the overall flow of the Textual-based application, managing
    views and keybindings for user interaction.

    Attributes:
        view (TopicsView): The main view displaying Kafka topics.
    """

    # Key bindings for navigation and control within the application
    BINDINGS = [
        (
            "h",
            "focus_previous",
        ),  # TODO solve problem with search field. Probably instead of fixed search field it's better to use ctrl-F pop-up
        ("l", "focus_next"),
    ]
    CSS_PATH = "app.css"  # Textual CSS file for styling

    def __init__(self, bootstraped: Bootstraped):
        super().__init__()
        self.view = TopicsView(bootstraped)  # Instantiate the TopicsView from views.py

    def compose(self) -> ComposeResult:
        yield self.view
        yield Footer()
