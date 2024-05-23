import yaml
from pydantic import BaseModel, field_validator, StringConstraints
from typing import List, Union, Annotated
from pathlib import Path

HostName = Annotated[str, StringConstraints(pattern=r"^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$")]
IpV4 = Annotated[str, StringConstraints(pattern=r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")]

class Cluster(BaseModel):
    host: Union[IpV4, HostName]
    port: int
    
    @field_validator('host')
    def validate_host(cls, v):
        if not isinstance(v, str) or not v:
            raise ValueError("Host must be a non-empty string")

        return v

    @field_validator('port')
    def validate_port(cls, v):
        if not (0 <= v <= 65535):
            raise ValueError("Port must be in range 0-65535")
        return v


def read_hosts():
    config_file_path = Path.home() / '.config' / 'kandy' / 'hosts.yaml'
    
    if not config_file_path.exists():
        raise FileNotFoundError("Configuration file not found")

    with config_file_path.open('r') as file:
        config_data = yaml.safe_load(file)
    
    return config_data


def get_hosts() -> List[Cluster]:
    config_data = read_hosts()

    return [Cluster(**host) for _,host in config_data.items()]


if __name__ == "__main__":
    hosts = get_hosts()
    for host in hosts:
        print(f"Host: {host.host}, Port: {host.port}")

