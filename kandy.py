from kandy_kafka.adapters.kafka_adapter import ClusterAdapter
from kandy_kafka.gui.gui import GUI

def main():
    host = "localhost"
    port = 29092

    cluster_adapter = ClusterAdapter(host, port)
    topics = cluster_adapter.get_topics_list()

    gui = GUI()
    gui.update_topics(topics)
    gui.run()


if __name__ == "__main__":
    main()