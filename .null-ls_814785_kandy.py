from kandy_kafka.bootstrap import Bootstrap
import argparse


class ConditionalAction(argparse.Action):
    """
    Custom argparse action that raises an error if both `clustername` and `--host/--port` are used together
    """

    def __call__(self, parser, namespace, values, option_string=None):
        """
        Overrides the __call__ method of argparse.Action to enforce mutual exclusivity
        between the `clustername` argument and the `--host`/`--port` options

        Args:
            parser (ArgumentParser): The argument parser instance
            namespace (Namespace): The namespace object where attributes are stored
            values (Any): The value associated with the argument
            option_string (str, optional): The option string that was used

        Raises:
            ArgumentError: If both `clustername` and `--host`/`--port` are specified
        """
        if namespace.clustername:
            parser.error("clustername specified; --host and --port should not be used")
        setattr(namespace, self.dest, values)


def main():
    """
    Main function
    """

    parser = argparse.ArgumentParser(description="Kandy Kafka")
    parser.add_argument("clustername", nargs="?", type=str, help="Cluster Name")
    parser.add_argument(
        "--host", type=str, default=None, help="Host", action=ConditionalAction
    )
    parser.add_argument(
        "--port", type=int, default=None, help="Port", action=ConditionalAction
    )

    args = parser.parse_args()

    # Error if neither clustername nor both host and port are provided
    if not args.clustername and (not args.host or not args.port):
        parser.error(
            "If clustername is not specified, both --host and --port must be provided"
        )

    bootstraped = Bootstrap()(
        clustername=args.clustername, host=args.host, port=args.port
    )

    # Close the Kafka consumer with the application
    bootstraped.kafka_adapter.consumer.close()


if __name__ == "__main__":
    main()
