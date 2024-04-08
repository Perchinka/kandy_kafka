from kandy_kafka.adapters.kafka_adapter import ClusterAdapter


def main():
    host = "localhost"
    port = 29092

    cluster_adapter = ClusterAdapter(host, port)
    topics = cluster_adapter.get_topics_list()
    brokers = cluster_adapter.get_brokers_list()

    print(cluster_adapter.get_topic("snd"))

if __name__ == "__main__":
    main()