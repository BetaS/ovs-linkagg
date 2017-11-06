import json


def load_json(file):
    return json.loads(open(file, "r").read())


class NodeConf:
    def __init__(self, file):
        self._data = load_json(file)

    def node_list(self):
        return list(self._data.keys())

    def get_node(self, name):
        return Node(self._data[name])


class Node:
    def __init__(self, data):
        self._data = data
        self._sess = None

    def get_server(self):
        return self._data["admin"]["ip"], self._data["admin"]["port"]

    def get_bridge(self):
        return self._data["bridge"]

    def get_interfaces(self):
        return self._data["interfaces"]


class Testcase:
    def __init__(self, file):
        self._data = load_json(file)

        self._connections = []

        for conn in self._data["connections"]:
            self._connections.append(Connection(conn))

    def get_default_link(self):
        return self._data["default_link"]

    def get_connections(self):
        return self._connections


class Connection:
    def __init__(self, data):
        self._name = data["name"]
        self._binding = data["bindings"]
        self._interfaces = []
        ifaces = data["interface"]
        for iface in ifaces:
            li = iface.split(".")
            self._interfaces.append({
                "node": li[0],
                "iface": li[1]
            })

    def get_name(self):
        return self._name

    def get_tcp_ports(self):
        return self._binding["tcp"]

    def get_interfaces(self):
        return self._interfaces
