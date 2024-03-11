from pathlib import Path
from sys import exit
import yaml


class Server:
    def __init__(
        self,
        name: str,
        previous: str,
        user: str,
        ip: str,
        port: int,
        pkey_file: str,
    ):
        self.name = name
        self.previous = previous
        self.user = user
        self.ip = ip
        self.port = port
        self.pkey_file = pkey_file


home_dir = Path.home()
config_dir = f"{home_dir}/.config/transfer_file"
ROUTES_FILE_PATH = f"{config_dir}/routes.yaml"


def readRoutesFile() -> dict[str, Server]:
    try:
        routes: dict[str, Server] = {}
        with open(ROUTES_FILE_PATH, "r") as file:
            data = yaml.safe_load(file)
            for key, value in data.items():
                routes[key] = Server(**value)
        return routes

    except FileNotFoundError:
        return {}


routes = readRoutesFile()


def getPathToServer(serverName: str) -> list[Server]:
    targetServer = routes.get(serverName)
    if targetServer is None:
        print(f"Server with name {serverName} not found")
        exit(1)

    previousName = targetServer.previous

    if previousName == ".":
        return [targetServer]

    path = getPathToServer(previousName)
    return [*path, targetServer]
