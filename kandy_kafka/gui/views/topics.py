from kandy_kafka.domain.models import Topic

import re

from textual.containers import Horizontal, Vertical, Container
from textual.reactive import reactive
from textual import events
from textual.app import ComposeResult
from textual.widgets import (
    Label,
    ListItem,
    ListView,
    Input,
    DataTable,
)


class TopicsView(Container):
    """View to display topics in a table."""

    BINDINGS = [
        ("s", "sort_by_size", "Sort By Size"),
        ("p", "sort_by_partitions", "Sort By Partitions"),
    ]

    def __init__(self):
        super().__init__()
        self.table = DataTable(id="topics-table")
        self.topics = []  # Store all topics
        self.filtered_topics = reactive([])

    def build_table(self):
        """Build the DataTable for topics"""
        self.table.clear()

        topics_table = self.query_one("#topics-table", DataTable)
        topics_table.cursor_type = "row"
        topics_table.zebra_stripes = True

        for col in (
            "Topic name",
            "Partitions",
            "Replication Factor",
            "Number of messages",
            "Size",
        ):
            topics_table.add_column(col, key=col)

    def update_table(self, topics: list[Topic]):
        """Update the table with the provided list of topics."""
        self.table.clear()
        topics_table = self.query_one("#topics-table", DataTable)

        for topic in topics:
            topics_table.add_row(
                topic.name, len(topic.partitions), 1, topic.amount_of_messages, 0
            )

    def show_topics(self, topics: list[Topic]):
        """Show the given list of topics in the table."""
        self.topics = topics  # Store the topics for filtering
        self.filtered_topics = (
            topics  # Initially, filtered topics is the same as topics
        )
        self.update_table(self.filtered_topics)

    def compose(self) -> ComposeResult:
        """Compose the view with the table."""
        yield Horizontal(
            Vertical(
                ListView(
                    ListItem(Label("Brokers")),
                    ListItem(Label("Topics")),
                    ListItem(Label("Consumers")),
                ),
                id="navigation-pane",
            ),
            Vertical(
                Input(placeholder="Search Topics...", id="search-field"),
                self.table,
                id="center-pane",
            ),
        )

    current_sorts: set = set()

    def sort_reverse(self, sort_type: str):
        """Determine if `sort_type` is ascending or descending."""
        reverse = sort_type in self.current_sorts
        if reverse:
            self.current_sorts.remove(sort_type)
        else:
            self.current_sorts.add(sort_type)
        return reverse

    async def on_mount(self):
        self.build_table()

    def action_sort_by_size(self) -> None:
        table = self.query_one(DataTable)
        table.sort(
            "Size",
            key=lambda x: x,
            reverse=self.sort_reverse("Size"),
        )

    def action_sort_by_partitions(self) -> None:
        table = self.query_one(DataTable)
        table.sort(
            "Partitions", key=lambda x: int(x), reverse=self.sort_reverse("Partitions")
        )

    async def on_input_changed(self, event):
        """Called whenever the input in the search field changes."""
        search_query = event.value.strip()

        if search_query == "":
            # If the search query is empty, show all topics
            self.filtered_topics = self.topics
        else:
            # Use regex to filter topics based on search query
            self.filtered_topics = [
                topic
                for topic in self.topics
                if re.search(search_query, topic.name, re.IGNORECASE)
            ]

        self.update_table(self.filtered_topics)
