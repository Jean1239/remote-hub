import sys
import transfer_file
import paramiko
import os
import subprocess
from routes import routes, Server


def getPathToServer(serverName: str) -> list[Server]:
    targetServer = routes.get(serverName)
    if targetServer is None:
        raise ValueError(f"Server with name {serverName} not found")

    previousName = targetServer.previous

    if previousName == ".":
        return [targetServer]

    path = getPathToServer(previousName)
    return [*path, targetServer]


def transferFile(file: str, path: list[Server]):
    if not os.path.exists(file):
        raise ValueError(f"File {file} does not exist")

    if len(path) == 0:
        raise ValueError("Path cannot be empty")

    if len(path) == 1:
        subprocess.run(
            ["scp", "-P", str(path[0].port), file, f"{path[0].ip}:~"], check=True
        )
        return

    try:
        target = paramiko.SSHClient()
        target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        target.connect(
            path[0].ip, port=path[0].port, allow_agent=True, look_for_keys=True
        )

        for i in range(1, len(path) - 1):
            transport = target.get_transport()
            if transport is None:
                raise ValueError(f"Failed to connect to {path[i].name}")
            channel = transport.open_channel(
                "direct-tcpip", (path[i].ip, path[i].port), ("localhost", 0)
            )
            target = paramiko.SSHClient()
            target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            target.connect(
                path[i].ip,
                port=path[i].port,
                allow_agent=True,
                look_for_keys=True,
                sock=channel,
            )
    finally:
        target.close()


def main():
    if len(sys.argv) < 3:
        print("Usage: transfer_file.py <file> <destination>")
        exit(1)

    file = sys.argv[1]
    destination = sys.argv[2]

    print([server.name for server in transfer_file.getPathToServer(destination)])


if __name__ == "__main__":
    main()
