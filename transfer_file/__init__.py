import sys
from sys import exit
import os
import yaml


class Server:
    def __init__(
        self,
        name: str,
        previous: str,
        user: str,
        ip: str,
        port=22,
        pkey_file="id_rsa",
    ):
        self.name = name
        self.previous = previous
        self.user = user
        self.ip = ip
        self.port = port
        self.pkey_file = f"/home/{user}/.ssh/{pkey_file}"


def readRoutesFile() -> dict[str, Server]:
    pathScript = sys.argv[0]

    # Obter o caminho para a pasta original
    base_path = os.path.abspath(os.path.dirname(pathScript))

    try:
        routes: dict[str, Server] = {}
        routesPath = os.path.join(base_path, "routes.yaml")
        with open(routesPath, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            for key, value in data.items():
                routes[key] = Server(**value)
        return routes
    except FileNotFoundError:
        print("File routes.yaml not found")
        exit(1)


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
