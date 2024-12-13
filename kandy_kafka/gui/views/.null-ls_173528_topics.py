from __future__ import annotations

from kandy_kafka.domain.models import KafkaMessage, Topic
import logging

from typing import TYPE_CHECKING, Tuple, List

if TYPE_CHECKING:
    from kandy_kafka.bootstrap import Bootstraped

from textual import on, work
from textual.containers import Horizontal, Vertical, Container
from textual.app import ComposeResult
from textual.widgets import (
    Label,
    ListItem,
    ListView,
    Input,
    DataTable,
)

import re


class BaseTable(DataTable):
    """
    Base class for creating custom datatables in the Textual UI with Vim keybindings support
    and sorting functionality

    Attributes:
        sort_directions (dict): A dictionary to store the sorting direction of each column
    """

    BINDINGS = [
        ("j", "cursor_down"),
        ("k", "cursor_up"),
        ("G", "scroll_bottom"),
        ("g", "scroll_top"),
    ]  # Vim bindings

    def __init__(self, css_id: str):
        super().__init__(id=css_id)
        # Dictionary to store sorting directions for each column
        self.sort_directions = {}

    def build_table(self, columns: List[Tuple[str, str]]):
        """
        Build the table (set necessary columns)

        Args:
            columns (List[Tuple[str, str]]): A list of tuples containing column names and keys
        """
        self.cursor_type = "row"
        self.zebra_stripes = True

        for column_name, key in columns:
            self.add_column(column_name, key=key)

    def update_rows(self, rows: List[List]):
        """
        Update the table

        Args:
            rows (List[List]): List of rows to add to the table
        """
        self.clear()  # Clear existing rows

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
    """
    Table for displaying Kafka messages
    """

    def __init__(self) -> None:
        super().__init__("messages-table")

    def on_mount(self):
        """
        Build the table and set its border title on table creation
        """
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

    def update_messages(self, messages: List[KafkaMessage]):
        """
        Update the table with a list of Kafka messages

        Args:
            messages (List[KafkaMessage]): List of messages to display
        """
        rows = []
        for message in messages:
            rows.append(
                [
                    message.offset,
                    message.partition_id,
                    None,  # Placeholder for timestamp
                    message.key,
                    message.value,
                ]
            )

        self.update_rows(rows)


class TopicsTable(BaseTable):
    """
    Table for displaying Kafka topics in the Textual UI
    """

    def __init__(self) -> None:
        super().__init__("topics-table")

    def on_mount(self):
        """
        Build the table and set its border title on table creation
        """
        self.build_table(
            [
                ("Topic name", "name"),
                ("Partitions", " partitions"),
                ("Replication factor", "replication"),
                ("Amount of Messages", "messages"),
            ]
        )
        self.border_title = "Topics"

    def update_topics(self, topics: List[Topic]):
        """
        Update the table with a list of Kafka topics

        Args:
            topics (List[Topic]): List of topics to display
        """
        rows = []
        for topic in topics:
            rows.append(
                [topic.name, len(topic.partitions), 1, topic.amount_of_messages]
            )

        self.update_rows(rows)


class SearchHandler:
    """
    Class responsible for handling topic filtering based on search queries
    """

    @staticmethod
    def filter_topics(topics: list[Topic], query: str) -> list[Topic]:
        """
        Filter the list of topics based on a search query

        Args:
            topics (list[Topic]): List of topics to filter
            query (str): Search query used for filtering topics

        Returns:
            list[Topic]: A filtered list of topics that match the search query
        """
        if not query:
            return topics
        query = query.strip()
        return [
            topic for topic in topics if re.search(query, topic.name, re.IGNORECASE)
        ]


class TopicsView(Container):
    """
    Main view for displaying Kafka topics and messages in a two-pane layout

    This view includes a sidebar, a search input field, and tables for topics and messages
    """

    BINDINGS = [
        ("ctrl+r", "reload", "Reload topics"),
    ]

    def __init__(self, bootstraped: Bootstraped):
        """

        Args:
            bootstraped (Bootstraped): An instance of Bootstraped that contains the Kafka adapter
        """
        super().__init__()
        self.kafka_adapter = bootstraped.kafka_adapter

        self.topics_table = TopicsTable()
        self.messages_table = MessagesTable()

        self.topics = []

    def compose(self) -> ComposeResult:
        """

        Returns:
            ComposeResult: A generator that yields UI components for display
        """
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
        """
        This method preloads the topics from the Kafka adapter on the first mount
        """
        self.load_topics()

    def load_topics(self):
        """
        Load topics from the Kafka adapter and update the topics table
        """
        topics = self.kafka_adapter.get_topics()
        # TODO separate filtering logic
        self.topics = topics  # Store the topics for later filtering
        self.topics_table.update_topics(self.topics)
        self.topics_table.loading = False

    @work(thread=True)
    async def load_messages(self, topic_name):
        """
        Asynchronously load messages for the selected topic

        Args:
            topic_name (str): The name of the topic to load messages from
        """
        logging.info("Loading messages")
        messages = self.kafka_adapter.get_messages(topic_name)
        logging.info("Got messages")
        self.messages_table.update_messages(messages)
        self.messages_table.loading = False

    async def on_input_changed(self, event):
        """
        Handle changes to the search input field and filter topics accordingly

        Args:
            event: Event object containing information about the input change
        """
        search_query = event.value.strip()
        filtered_topics = SearchHandler.filter_topics(self.topics, search_query)
        self.topics_table.update_topics(filtered_topics)

    @on(DataTable.RowSelected, "#topics-table")
    def handle_row_selected(self, message: DataTable.RowSelected):
        """
        Handle the event when a row in the topics table is selected (Enter was pressed)

        Args:
            message (DataTable.RowSelected): Event object containing information about the selected row
        """
        self.messages_table.loading = True
        topic_name = message.data_table.get_cell(message.row_key, "name")
        self.load_messages(topic_name)

    # --------- Actions ----------
    def action_reload(self):
        """
        Action to reload the topics list (ctrl-R)
        """
        self.load_topics()
