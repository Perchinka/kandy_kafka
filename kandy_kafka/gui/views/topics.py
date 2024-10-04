from textual.containers import Horizontal, Vertical, Container
from textual.app import ComposeResult
from textual.widgets import (
    Label,
    ListItem,
    ListView,
    Input,
    DataTable,
    Header,
    Footer,
)

from kandy_kafka.domain.models import Topic


class TopicsView(Container):
    """View to display topics in a table."""

    BINDINGS = [
        ("s", "sort_by_size", "Sort By Size"),
        ("p", "sort_by_partitions", "Sort By Partitions"),
    ]

    def __init__(self):
        super().__init__()
        self.table = DataTable(id="topics-table")

    def build_table(self, topics: list[Topic]):
        """Build the DataTable widget to display the topics."""
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

        for topic in topics:
            topics_table.add_row(
                topic.name, len(topic.partitions), 1, topic.amount_of_messages, 0
            )

    def compose(self) -> ComposeResult:
        """Compose the view with the table."""
        yield Header()

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
        """Called when app is mounted, populate the topics table with placeholders"""

    def action_sort_by_size(self) -> None:
        table = self.query_one(DataTable)
        table.sort(
            "Size",
            key=lambda x: int(x.split(" ")[0]),
            reverse=self.sort_reverse("Size"),
        )

    def action_sort_by_partitions(self) -> None:
        table = self.query_one(DataTable)
        table.sort(
            "Partitions", key=lambda x: int(x), reverse=self.sort_reverse("Partitions")
        )
