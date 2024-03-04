class Server:
    def __init__(self, name: str, previous: str, ip: str, port=22):
        self.name = name
        self.previous = previous
        self.ip = ip
        self.port = port


routes = {
    "vm": Server(name="vm", previous=".", ip="172.17.4.136"),
    "jump_sp": Server(name="jump_sp", previous="vm", ip="172.19.0.253", port=333),
    "pr35": Server(name="pr35", previous="jump_sp", ip="172.30.0.35"),
    "jump_cbc": Server(name="jump_cbc", previous="vm", ip="172.19.253.249"),
    "cbe1": Server(name="cbe1", previous="jump_cbc", ip="172.17.161.2"),
    "cbe2": Server(name="cbe2", previous="jump_cbc", ip="172.19.161.2"),
}
