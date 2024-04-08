from kandy_kafka.adapters.kafka_adapter import KafkaAdapter
from kandy_kafka.gui.gui import GUI

def main():
    host = "localhost"
    port = 29092

    cluster_adapter = KafkaAdapter(host, port)
    topics = cluster_adapter.get_topics_list()
    consumer_groups = cluster_adapter.get_consumer_groups()

    gui = GUI()
    gui.update_topics(topics)
    gui.run()


if __name__ == "__main__":
    main()