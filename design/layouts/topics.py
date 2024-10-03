from textual.app import App
from textual.widgets import (
    Label,
    ListItem,
    ListView,
    Input,
    DataTable,
    Header,
    Footer,
)
from textual.containers import Horizontal, Vertical
from random import randint


class TopicsView(App):
    """Main Kafka interface TUI"""

    BINDINGS = [
        ("s", "sort_by_size", "Sort By Size"),
        ("p", "sort_by_partitions", "Sort By Partitions"),
    ]

    def compose(self):
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
                DataTable(
                    id="topics-table",
                ),
                id="center-pane",
            ),
        )
        yield Footer()

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

        for i in range(10):
            topics_table.add_row(
                f"topic_{i}",
                str(randint(1, 10)),
                str(randint(1, 3)),
                str(randint(0, 800)),
                f"{i * 1024} KB",
            )

    def action_sort_by_size(self) -> None:
        table = self.query_one(DataTable)
        table.sort("Size", key=lambda x: x, reverse=self.sort_reverse("Size"))

    def action_sort_by_partitions(self) -> None:
        table = self.query_one(DataTable)
        table.sort(
            "Partitions", key=lambda x: x, reverse=self.sort_reverse("Partitions")
        )


if __name__ == "__main__":
    TopicsView().run()
