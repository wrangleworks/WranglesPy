"""
Connector for SSH
"""
from fabric import Connection as _Connection


_schema = {}

def run(host: str, user: str, password: str, command: str) -> None:
    """
    Execute a command over ssh
    """
    _Connection(host, user=user, connect_kwargs={'password': password}).run(command)

_schema['run'] = """
type: object
description: Issue commands over SSH
required:
  - host
  - user
  - password
  - command
properties:
  host:
    type: string
    description: Domain or IP of the host
  user:
    type: string
    description: The user to connect as
  password:
    type: string
    description: Password for the user
  command:
    type: string
    description: Command to send
"""