from ovs import OVS


def add_ofctl(ofctl, flows, cookie=0, priority=0):
    for flow in flows:
        ofctl.add_flow(cookie, flow["where"], flow["action"], priority)  # Send Response

    return True


def main():
    LOCAL_PORT = "LOCAL"

    # Check host's hw
    server = OVS.Switch("172.31.2.1", 6640)
    client = OVS.Switch("172.31.2.2", 6640)

    server.flush_bridge("br0")
    server_br = server.get_bridge("br0")
    server_br.add_port("eth3")
    server_br.add_port("eth4")
    server_br.add_port("eth5")
    server_br.add_port("eth6")

    server_port = server_br.list_port()
    server_br.del_all_flows()

    client.flush_bridge("br0")
    client_br = client.get_bridge("br0")
    client_br.add_port("eth3")
    client_br.add_port("eth4")
    client_br.add_port("eth5")
    client_br.add_port("eth6")

    client_port = client_br.list_port()
    client_br.del_all_flows()

    for t in ["server", "client"]:
        current_side = {}
        if t == "server":
            current_side = {
                "br": server_br,
                "port": server_port
            }
        elif t == "client":
            current_side = {
                "br": client_br,
                "port": client_port
            }

        for i in range(4):
            iface_port = current_side["port"]["eth%d" % (3+i)]["port"]
            port = 40000 + i

            flows = [{
                "where": "tcp,in_port=%s,tp_src=%d" % (LOCAL_PORT, port),
                "action": "output:%s" % iface_port
            }, {
                "where": "tcp,in_port=%s,tp_dst=%d" % (LOCAL_PORT, port),
                "action": "output:%s" % iface_port
            }, {
                "where": "tcp,in_port=%s,tp_src=%d" % (iface_port, port),
                "action": "local"
            }, {
                "where": "tcp,in_port=%s,tp_dst=%d" % (iface_port, port),
                "action": "local"
            }]

            add_ofctl(current_side["br"], flows, cookie=i, priority=2)

        def_gw_port = "eth6"
        iface_port = current_side["port"][def_gw_port]["port"]

        flows = [{
            "where": "in_port=%s" % LOCAL_PORT,
            "action": "output:%s" % iface_port
        }, {
            "where": "in_port=%s" % iface_port,
            "action": "local"
        }]

        add_ofctl(current_side["br"], flows, cookie=0, priority=1)


if __name__ == "__main__":
    main()