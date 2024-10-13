from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from kandy_kafka.bootstrap import Bootstraped

from textual.containers import Horizontal, Vertical, Container
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import (
    Label,
    ListItem,
    ListView,
    Input,
    DataTable,
    LoadingIndicator,
)
from kandy_kafka.domain.models import Topic

import re
from typing import List


class BaseTable(DataTable):
    BINDINGS = [("j", "cursor_down"), ("k", "cursor_up")]  # Vim bindings

    def __init__(self, id: str):
        super().__init__(id=id)
        # Dictionary to store sorting directions for each column
        self.sort_directions = {}

    def build_table(self, columns: List[Tuple[str, str]]):
        """Build the DataTable for topics."""
        self.cursor_type = "row"
        self.zebra_stripes = True

        for column_name, key in columns:
            self.add_column(column_name, key=key)

    def update_rows(self, rows: List[List]):
        """Update the table with the provided list of topics."""
        self.clear()

        for row in rows:
            self.add_row(*row)

    # def toggle_sort_direction(self, column: str) -> bool:
    #     """Toggle the sort direction for the given column."""
    #     # Flip the sort direction and store it
    #     self.sort_directions[column] = not self.sort_directions[column]
    #     return self.sort_directions[column]
    #
    # def get_sort_key(self, column: str):
    #     """Return the appropriate key function for sorting based on the column."""
    #     return lambda topic: topic.name  # Default to sorting by topic name
    #
    # def sort_table(self, topics: list[Topic], column: str) -> list[Topic]:
    #     """Sort the topics list by the specified column."""
    #     reverse = self.toggle_sort_direction(column)
    #     key_func = self.get_sort_key(column)
    #     return sorted(topics, key=key_func, reverse=reverse)


class MessagesTable(BaseTable):
    def __init__(self) -> None:
        super().__init__("messages-table")

    def on_mount(self):
        self.build_table(
            [
                ("Offset", "offset"),
                ("Partition", "partition"),
                ("Timestamp", "timestamp"),
                ("Key", "key"),
                ("Value", "Value"),
            ]
        )
        self.border_title = "Messages"


class TopicsTable(BaseTable):
    def __init__(self) -> None:
        super().__init__("topics-table")

    def on_mount(self):
        self.build_table(
            [
                ("Topic name", "name"),
                ("Partitions", " partitions"),
                ("Replication factor", "replication"),
                ("Amount of Messages", "messages"),
            ]
        )
        self.border_title = "Topics"

    def update_topics_in_table(self, topics: List[Topic]):
        """Update the table with the provided list of topics."""
        rows = []
        for topic in topics:
            rows.append(
                [topic.name, len(topic.partitions), 1, topic.amount_of_messages]
            )

        self.update_rows(rows)


class SearchHandler:
    """Class responsible for filtering topics based on search queries."""

    @staticmethod
    def filter_topics(topics: list[Topic], query: str) -> list[Topic]:
        """Filter the list of topics based on the search query."""
        if not query:
            return topics
        query = query.strip()
        return [
            topic for topic in topics if re.search(query, topic.name, re.IGNORECASE)
        ]


class TopicsView(Container):
    BINDINGS = [
        ("ctrl+r", "reload", "reload"),
    ]

    def __init__(self, bootstraped: Bootstraped):
        super().__init__()
        self.kafka_adapter = bootstraped.kafka_adapter

        self.topics_table = TopicsTable()
        self.messages_table = MessagesTable()

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                ListView(
                    ListItem(Label("Brokers")),
                    ListItem(Label("Topics")),
                    ListItem(Label("Consumers")),
                ),
                id="sidebar",
            ),
            Vertical(
                Input(
                    placeholder="Search Topics...", id="search-field"
                ),  # Create class that will work with input
                Horizontal(
                    self.topics_table,
                    self.messages_table,
                ),
                id="center-pane",
            ),
        )

    def on_mount(self):
        self.load_topics()

    def load_topics(self):
        self.topics_table.loading = True
        topics = self.kafka_adapter.get_topics()
        self.topics = topics  # Store the topics for later filtering
        self.topics_table.update_topics_in_table(self.topics)
        self.topics_table.loading = False

    async def on_input_changed(self, event):
        """Called whenever the input in the search field changes."""
        search_query = event.value.strip()
        filtered_topics = SearchHandler.filter_topics(self.topics, search_query)
        self.topics_table.update_topics_in_table(filtered_topics)

    # Actions
    def action_reload(self):
        self.load_topics()
