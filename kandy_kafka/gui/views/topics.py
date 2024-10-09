from textual.containers import Horizontal, Vertical, Container
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import (
    Label,
    ListItem,
    ListView,
    Input,
    DataTable,
)
from kandy_kafka.domain.models import Topic

import re


class TopicsDataTable(DataTable):
    BINDINGS = [("m", "sort('messages')", "Sort by messages")]

    def __init__(self, id: str):
        super().__init__(id=id)

        # Dictionary to store sorting directions for each column
        self.sort_directions = {
            "Number of messages": False,  # False = Ascending, True = Descending
            "Partitions": False,
        }

    def build_table(self):
        """Build the DataTable for topics."""
        self.clear()
        self.cursor_type = "row"
        self.zebra_stripes = True

        for col in (
            "Topic name",
            "Partitions",
            "Replication Factor",
            "Number of messages",
        ):
            self.add_column(col, key=col)

    def update_table(self, topics: list[Topic]):
        """Update the table with the provided list of topics."""
        self.clear()

        for topic in topics:
            self.add_row(
                topic.name,
                len(topic.partitions),
                1,  # Hardcoded Replication Factor, until I find a way to fetch this info from kafka
                topic.amount_of_messages,
            )

    def toggle_sort_direction(self, column: str) -> bool:
        """Toggle the sort direction for the given column."""
        # Flip the sort direction and store it
        self.sort_directions[column] = not self.sort_directions[column]
        return self.sort_directions[column]

    def get_sort_key(self, column: str):
        """Return the appropriate key function for sorting based on the column."""
        if column == "Number of messages":
            return lambda topic: topic.amount_of_messages
        elif column == "Partitions":
            return lambda topic: len(topic.partitions)
        return lambda topic: topic.name  # Default to sorting by topic name

    def sort_table(self, topics: list[Topic], column: str) -> list[Topic]:
        """Sort the topics list by the specified column."""
        reverse = self.toggle_sort_direction(column)
        key_func = self.get_sort_key(column)
        return sorted(topics, key=key_func, reverse=reverse)


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
    """Main view to display topics in a table with search and sorting."""

    def __init__(self):
        super().__init__()
        self.topics_table = TopicsDataTable(id="topics-table")
        self.messages_table = DataTable(id="messages-table")
        self.topics = []  # Store all topics
        self.filtered_topics = reactive([])  # Reactive field for filtered topics

    def compose(self) -> ComposeResult:
        """Compose the view with the table, search, and navigation."""
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
                Input(placeholder="Search Topics...", id="search-field"),
                Horizontal(
                    self.topics_table,
                    self.messages_table,
                ),
                id="center-pane",
            ),
        )

    async def on_mount(self):
        """Called when app is mounted, build the initial table."""
        self.topics_table.build_table()
        self.topics_table.border_title = "Topics"
        self.topics_table.focus()

    def show_topics(self, topics: list[Topic]):
        """Show the given list of topics in the table."""
        self.topics = topics  # Store the topics for later filtering
        self.filtered_topics = topics  # Initially, filtered topics = all topics
        self.topics_table.update_table(self.filtered_topics)

    def action_sort_by_messages(self) -> None:
        """Sort the table by the size column."""
        self.filtered_topics = self.topics_table.sort_table(
            self.filtered_topics, "Size"  # pyright: ignore[reportArgumentType]
        )
        self.topics_table.update_table(self.filtered_topics)

    def action_sort_by_partitions(self) -> None:
        """Sort the table by the number of partitions."""
        self.filtered_topics = self.topics_table.sort_table(
            self.filtered_topics, "Partitions"  # pyright: ignore[reportArgumentType]
        )
        self.topics_table.update_table(self.filtered_topics)

    async def on_input_changed(self, event):
        """Called whenever the input in the search field changes."""
        search_query = event.value.strip()
        self.filtered_topics = SearchHandler.filter_topics(self.topics, search_query)
        self.topics_table.update_table(self.filtered_topics)
