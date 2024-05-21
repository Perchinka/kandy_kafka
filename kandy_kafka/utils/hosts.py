import yaml
from pydantic import BaseModel, field_validator 
from typing import List
from pathlib import Path

class HostConfig(BaseModel):
    host: str
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
    
    default_config = [
        {
            "default": {
                "host": "localhost",
                "port": 9092
            },
        }
    ]

    if not config_file_path.exists():
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        with config_file_path.open('w') as file:
            yaml.dump(default_config, file)
    
    with config_file_path.open('r') as file:
        config_data = yaml.safe_load(file)
    
    return config_data


def get_hosts() -> List[HostConfig]:
    config_data = read_hosts()

    return [HostConfig(**host) for _,host in config_data.items()]


if __name__ == "__main__":
    hosts = get_hosts()
    for host in hosts:
        print(f"Host: {host.host}, Port: {host.port}")

