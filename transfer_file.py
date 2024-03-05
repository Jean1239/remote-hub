from io import StringIO
import sys
import transfer_file
import paramiko
import os
import subprocess
from routes import routes, Server


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


def transferFile(file: str, path: list[Server]):
    if not os.path.exists(file):
        print(f"File {file} does not exist")
        exit(1)

    if len(path) == 0:
        print("Path cannot be empty")
        exit(1)

    if len(path) == 1:
        subprocess.run(
            ["scp", "-P", str(path[0].port), file, f"{path[0].ip}:~"], check=True
        )
        return

    basename = os.path.basename(file)

    try:
        target = paramiko.SSHClient()
        target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        target.connect(path[0].ip, port=path[0].port)
        target.exec_command("mkdir -p ~/transfered_files")
        sftp = target.open_sftp()
        sftp.put(file, f"transfered_files/{basename}")

        for i in range(1, len(path)):
            transport = target.get_transport()
            if transport is None:
                print(f"Failed to connect to {path[i].name}")
                exit(1)

            channel = transport.open_channel(
                "direct-tcpip", (path[i].ip, path[i].port), ("localhost", 0)
            )

            sftp = target.open_sftp()
            with sftp.open(path[i - 1].pkey_file, "r") as key_file:
                key_data = key_file.read().decode("utf-8")
                pkey = paramiko.RSAKey.from_private_key(StringIO(key_data))

            target = paramiko.SSHClient()
            target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            target.connect(
                path[i].ip,
                port=path[i].port,
                pkey=pkey,
                sock=channel,
            )
            target.exec_command("mkdir -p ~/transfered_files")
            sftp = target.open_sftp()
            sftp.put(basename, f"transfered_files/{basename}")

    finally:
        target.close()


def main():
    if len(sys.argv) < 3:
        print("Usage: transfer_file.py <file> <destination>")
        exit(1)

    file = sys.argv[1]
    destination = sys.argv[2]
    path = transfer_file.getPathToServer(destination)
    print([server.name for server in path])
    transferFile(file, path)


if __name__ == "__main__":
    main()
