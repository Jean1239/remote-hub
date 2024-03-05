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


routes = {
    "vm": Server(name="vm", previous=".", user="jgcarraro", ip="172.17.4.136"),
    "jump_sp": Server(
        name="jump_sp", previous="vm", user="jgcarraro", ip="172.19.0.253", port=333
    ),
    "pr35": Server(name="pr35", previous="jump_sp", user="jgcarraro", ip="172.30.0.35"),
    "jump_cbc": Server(
        name="jump_cbc", previous="vm", user="jgcarraro", ip="172.19.253.249"
    ),
    "cbe1": Server(
        name="cbe1", previous="jump_cbc", user="jgcarraro", ip="172.17.161.2"
    ),
    "cbe2": Server(
        name="cbe2", previous="jump_cbc", user="jgcarraro", ip="172.19.161.2"
    ),
}
