class ConnectException(Exception):
    """
    No OVS remote manager detected.
    Please type the "ovs-vsctl set-manager {passive-protocol}:{port}" at remote terminal.
    e.g. $ root@172.31.0.1 > ovs-vsctl set-manager ptcp:6640
    """
    def __init__(self, ip, port, proto):
        super(ConnectException, self).__init__("\n\n[+] No OVS remote manager detected.\n"
            "[+] Please type the \"ovs-vsctl set-manager p%s:%s\" at \"%s\"'s terminal."%(proto, port, ip))


class CommandException(Exception):
    def __init__(self, message):
        super(CommandException, self).__init__("\n\n[+] %s" % (message))