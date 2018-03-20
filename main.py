from util import parser
from ovs import OVS


def node_configure(node):
    ip, port = node.get_server()
    switch = OVS.Switch(ip, port)

    switch.flush_bridge(node.get_bridge())
    bridge = switch.get_bridge(node.get_bridge())
    for iface in node.get_interfaces():
        bridge.add_port(iface)

    print("[++] OVS port configuration success : %s" % bridge.list_port_simple())
    print()

    return {"switch": switch, "bridge": bridge}


def add_ofctl(ofctl, flows, cookie=0, priority=0):
    for flow in flows:
        ofctl.add_flow(cookie, flow["where"], flow["action"], priority)

    return True


def main():
    # Read configuration
    conf = parser.NodeConf("./conf/nodes.json")
    tests = parser.Testcase("./conf/testcase0.json")

    print("[+] Setting up the OVS")
    print()

    node_conn = {}

    # Setting OVS
    for node_name in conf.node_list():
        print("[++] OVS port configuration at '%s'" % node_name)
        node = conf.get_node(node_name)
        node_conn[node_name] = node_configure(node)

    print("[+] Setting up the Connection")
    print()

    default_flow = tests.get_default_link()

    for conn in tests.get_connections():
        print("[++] '%s' flow installing..." % conn.get_name())
        ifaces = conn.get_interfaces()
        tcp_ports = conn.get_tcp_ports()
        for iface in ifaces:
            bridge = node_conn[iface["node"]]["bridge"]


            ports = bridge.list_port()
            iface_port = ports[iface["iface"]]["port"]

            if conn.get_name() == default_flow:
                # default flows
                flows = [{
                    "where": "in_port=local",
                    "action": "output:%s" % iface_port
                }, {
                    "where": "in_port=%s" % iface_port,
                    "action": "local"
                }]

                add_ofctl(bridge, flows, cookie=0, priority=1)

            for port in tcp_ports:
                flows = [{
                    "where": "tcp,in_port=local,tp_src=%d" % port,
                    "action": "output:%s" % iface_port
                }, {
                    "where": "tcp,in_port=local,tp_dst=%d" % port,
                    "action": "output:%s" % iface_port
                }, {
                    "where": "tcp,in_port=%s,tp_src=%d" % (iface_port, port),
                    "action": "local"
                }, {
                    "where": "tcp,in_port=%s,tp_dst=%d" % (iface_port, port),
                    "action": "local"
                }]

                add_ofctl(bridge, flows, cookie=0, priority=2)

        print("[++] '%s' flow install success!" % conn.get_name())
        print()


if __name__ == "__main__":
    main()
