import functools


class Action:
    def __init__(self):
        self.action = "normal"
        self.params = []
        self.Network = NetworkAction(self)
        self.Datalink = DatalinkAction(self)

    def __str__(self):
        s = functools.reduce(lambda src, item: src+","+item, self.params)
        if len(s) > 0:
            return s + "," + self.action
        else:
            return self.action

    def output(self, port):
        self.action = "output:%s" % port

    def local(self):
        self.action = "local"

    def flood(self):
        self.action = "flood"

    def all(self):
        self.action = "all"

    def in_port(self):
        self.action = "in_port"

    def drop(self):
        self.action = "drop"

    def normal(self):
        self.action = "normal"


class SubAction:
    def __init__(self, action):
        self.action = action

    def _append(self, action):
        self.action.params.append(action)


class TCPAction(SubAction):
    def src(self, port):
        self._append("mod_tp_src=%s" % port)

    def dst(self, port):
        self._append("mod_tp_dst=%s" % port)


class NetworkAction(SubAction):
    def src(self, addr):
        self._append("mod_nw_src=%s" % addr)

    def dst(self, addr):
        self._append("mod_nw_dst=%s" % addr)

    def dec_ttl(self):
        self._append("dec_ttl")


class DatalinkAction(SubAction):
    def src(self, addr):
        self._append("mod_dl_src=%s" % addr)

    def dst(self, addr):
        self._append("mod_dl_dst=%s" % addr)



if __name__ == "__main__":
    action = Action()
    action.Datalink.src("ff:ff:ff:ff:ff:ff")
    action.Physical.src(1)
    action.output(1)

    print(action)