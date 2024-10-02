import urwid


class TopicsView:
    def __init__(self):
        self.header_text = urwid.Text("Kafka Topics Viewer")
        self.footer_text = urwid.Text("Press 'R' to reload topics, 'Ctrl+C' to exit")
        self.table = urwid.SimpleFocusListWalker([])  # List to hold the table rows
        self.body = urwid.ListBox(self.table)
        self.frame = urwid.Frame(
            self.body, header=self.header_text, footer=self.footer_text
        )

    def build_table(self, topics):
        """
        Build a table to display topics.
        """
        self.table.clear()
        self.table.append(urwid.Text("Topic Names"))
        self.table.append(urwid.Divider())
        for topic in topics:
            self.table.append(urwid.Text(topic))

    def get_top_view(self):
        """
        Returns the main UI frame.
        """
        return self.frame
