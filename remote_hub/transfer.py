from io import StringIO
import os
import sys
from sys import exit

import paramiko
import scp

from . import Server, getPathToServer


def transferFile(file: str, path: list[Server]):
    if not os.path.exists(file):
        print(f"File {file} does not exist")
        exit(1)

    if len(path) == 0:
        print("Path cannot be empty")
        exit(1)

    try:
        target = paramiko.SSHClient()
        target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        target.connect(
            hostname=path[0].ip,
            port=path[0].port,
            username=path[0].user,
        )

    except Exception as e:
        print(f"An error occurred in server {path[0].name}: {e}")
        exit(1)

    for i in range(1, len(path)):
        try:
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
                hostname=path[i].ip,
                port=path[i].port,
                username=path[i].user,
                pkey=pkey,
                sock=channel,
            )

        except Exception as e:
            print(f"An error occurred in server {path[i].name}: {e}")
            exit(1)

    target.exec_command("mkdir -p ~/transfered_files")
    transport = target.get_transport()
    if transport is None:
        print(f"Failed to connect to {path[0].name}")
        exit(1)

    try:
        scpClient = scp.SCPClient(transport)
        scpClient.put(
            file,
            "transfered_files",
            recursive=True,
        )
    except Exception as e:
        print(f"An error occurred in server {path[-1].name}: {e}")
        exit(1)

    print(f"File {file} transferred to {path[-1].name} successfully")


def main():
    if len(sys.argv) < 3:
        print("Usage: transfer_file.py <file> <destination>")
        exit(1)

    file = sys.argv[1]
    destination = sys.argv[2]
    path = getPathToServer(destination)
    transferFile(file, path)


if __name__ == "__main__":
    main()
