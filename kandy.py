from kandy_kafka.bootstrap import Bootstrap
import argparse

from kandy_kafka.gui.controller import Controller


class ConditionalAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.clustername:
            parser.error("clustername specified; --host and --port should not be used")
        setattr(namespace, self.dest, values)


def main():
    parser = argparse.ArgumentParser(description="Kandy Kafka")
    parser.add_argument("clustername", nargs="?", type=str, help="Cluster Name")
    parser.add_argument(
        "--host", type=str, default=None, help="Host", action=ConditionalAction
    )
    parser.add_argument(
        "--port", type=int, default=None, help="Port", action=ConditionalAction
    )

    args = parser.parse_args()

    if args.clustername and (args.host or args.port):
        parser.error("Clustername specified; --host and --port should not be used")
    if not args.clustername and (not args.host or not args.port):
        parser.error(
            "If clustername is not specified, both --host and --port must be provided"
        )

    Bootstrap()(clustername=args.clustername, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
