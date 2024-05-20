import yaml
from pydantic import BaseModel, ValidationError, validator
from typing import List
import os

class HostConfig(BaseModel):
    host: str
    port: int

    @validator('host')
    def validate_host(cls, v):
        if not isinstance(v, str) or not v:
            raise ValueError("Host must be a non-empty string")
        return v

    @validator('port')
    def validate_port(cls, v):
        if not (0 <= v <= 65535):
            raise ValueError("Port must be in range 0-65535")
        return v

def read_and_validate_config() -> List[HostConfig]:
    config_file_path = os.path.expanduser('~/.config/kandy/hosts.yaml')
    
    default_config = [
        {
            "host": "localhost",
            "port": 9092
        }
    ]

    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as file:
            yaml.dump(default_config, file)

    with open(config_file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    
    return [HostConfig(**host) for _,host in config_data.items()]

if __name__ == "__main__":
    hosts = read_and_validate_config()
    for host in hosts:
        print(f"Host: {host.host}, Port: {host.port}")
