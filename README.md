# Kandy

## Overview

Kandy is a powerful Command Line Interface (CLI) tool designed to streamline the management of Kafka clusters directly from your terminal. It allows you to connect to and manage Kafka clusters effortlessly, making it an indispensable tool for developers and system administrators working with Apache Kafka.

## Installation

### Prerequisites

Before installing Kandy, ensure you have the following prerequisites installed on your system:

- **Python 3.11**
- **Poetry** (Python dependency management and packaging tool)
- **Make** (Build automation tool)
- **Docker** {Optional if you want run kafka localy}

### Install from Git Repository

To install Kandy from the git repository, execute the following commands:

```bash
git clone https://github.com/Perchinka/kandy_kafka.git
cd kandy_kafka
make install
```

> Note: In the future, Kandy will be available via pip and other package managers for easier installation.

The installation script will create a configuration file at `.config/kandy/hosts.yaml` with default connection parameters (localhost:29092). You can add new configurations to this file using the following syntax:

```yaml
alias:
    host: host (str)
    port: port (int)
```

## Usage
To begin using Kandy, you can display the help message by running:

```bash
> python3 kandy.py -h
usage: kandy.py [-h] [--host HOST] [--port PORT] [clustername]

Kandy Kafka

positional arguments:
  clustername  Cluster Name

options:
  -h, --help   show this help message and exit
  --host HOST  Host
  --port PORT  Port
```


You need to specify either the --host and --port arguments or an alias from the configured connection details to run Kandy.

### Using arguments
```bash
python3 kandy.py --host localhost --port 29092
```

### Using alias
```bash
python3 kandy.py default
```

## Testing
Kandy employs `pytest` for testing. All test files are located in the `tests` folder. You can run various tests using the provided `make` commands:
```
make start_kafka                    Start local kafka docker
make stop_kafka                     Stop local kafka docker
make test_unit                      Run unit tests
make test_behaviour                 Run behaviour tests
make test_integration               Run integration_test tests
make test                           Run all tests
```

By utilizing these commands, you can ensure that your setup is correct and that Kandy is functioning as expected.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
- Fork the repository.
- Create your feature branch: git checkout -b feature-name.
- Commit your changes: git commit -am 'Add some feature'.
- Push to the branch: git push origin feature-name.
- Submit a pull request.

