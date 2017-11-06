from ovs import OVS_VSCTL, OVS_OFCTL, exception

import re

from subprocess import PIPE
from subprocess import Popen


def process_run(args):
    popen = Popen(args, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    popen.wait()

    if popen.returncode != 0:
        return popen.returncode, popen.stderr.read()

    return 0, popen.stdout.read()


class Switch:
    def __init__(self, ip, port=6640, proto="tcp"):
        self._proto = proto
        self._ip = ip
        self._port = port

        self._sess_addr = "%s:%s:%s" % (proto, ip, port)

        if not self._run("get-manager", throws=True):
            raise exception.ConnectException(ip, port, proto)

    def _run(self, command, params=[], throws=True):
        args = [OVS_VSCTL, '--db=%s' % self._sess_addr, command]
        args.extend(params)

        code, result = process_run(args)

        if code != 0:
            if throws:
                raise exception.CommandException(result)
            else:
                return None
        else:
            return result

    def show_bridge(self):
        return list(map(lambda x: x.strip(), self._run("list-br").strip().split("\n")))

    def add_bridge(self, br):
        self._run("add-br", [br])
        return True

    def del_bridge(self, br):
        self._run("del-br", [br])
        return True

    def flush_bridge(self, br):
        try:
            self._run("del-br", [br])
        except:
            pass

        self._run("add-br", [br])
        return True

    def get_bridge(self, br, port=6653):
        self._run("set-controller", [br, "p%s:%s"%(self._proto, port)])
        return Bridge(self, br, port)


class Bridge:
    def __init__(self, switch, br, port):
        self._br = br
        self._switch = switch
        self._sess_addr = "%s:%s:%s" % (switch._proto, switch._ip, port)

    def _run(self, command, params=[], throws=True):
        args = [OVS_OFCTL, command, self._sess_addr]
        args.extend(params)

        code, result = process_run(args)

        if code != 0:
            if throws:
                raise exception.CommandException(result)
            else:
                return None
        else:
            return result

    def close(self):
        self._switch._run("del-controller", [self._br])
        return True

    def list_port_simple(self):
        return list(map(lambda x: x.strip(), self._switch._run("list-ports", [self._br]).strip().split("\n")))

    def list_port(self):
        result = self._run("show")

        regex = re.compile(r"(LOCAL|\d+?)\((.+?)\)\s*:\s*addr:(.+?)\s*config\s*:\s*(.+?)\s*state\s*:\s*(.*)", re.MULTILINE)
        result = regex.findall(result)

        li = {}

        for node in result:
            li[node[1]] = {
                "name": node[1],
                "port": node[0],
                "addr": node[2],
                "port_status": node[3],
                "link_status": node[4]
            }

        return li

    def add_port(self, iface):
        self._switch._run("add-port", [self._br, iface])
        return True

    def del_port(self, iface):
        self._switch._run("del-port", [self._br, iface])
        return True

    def list_flows(self):
        return self._run("dump-flows")

    def add_flow(self, cookie, where, action, priority):
        self._run("add-flow", ["cookie=%d,priority=%d,%s,actions=%s" % (cookie, priority, where, action)])
        return True

    def del_flow(self, cookie=0, mask=0):
        self._run("add-flow", ["cookie=%d/%d" % (cookie, mask)])
        return True

    def del_all_flows(self):
        self._run("del-flows")
        return True


if __name__ == "__main__":
    sess = Switch("172.31.2.2")
    br0 = sess.get_bridge("br0")
    print(br0.list_flows())
    br0.del_all_flows()
    print(br0.list_flows())
    br0.close()
