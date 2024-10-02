from textual.widgets import DataTable, Header, Footer
from textual.containers import Container
from textual.app import ComposeResult


class TopicsView(Container):
    """View to display topics in a table."""

    def __init__(self):
        super().__init__()
        self.table = DataTable()

    def build_table(self, topics: list[str]):
        """Build the DataTable widget to display the topics."""
        self.table.clear()
        self.table.add_column("Topics")
        for topic in topics:
            self.table.add_row(topic)

    def compose(self) -> ComposeResult:
        """Compose the view with the table."""
        yield Header()
        yield self.table
        yield Footer()
