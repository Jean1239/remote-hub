import sys
import subprocess
from sys import exit

from . import getPathToServer


def sshToServer(serverName: str):
    path = getPathToServer(serverName)
    cmd = ""
    for i in range(len(path)):
        cmd = f"{cmd} ssh -p{path[i].port} -t {path[i].ip}"

    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: ssh_to_server <destination>")
        exit(1)

    destination = sys.argv[1]
    sshToServer(destination)


if __name__ == "__main__":
    main()
