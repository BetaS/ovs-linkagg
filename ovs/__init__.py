from distutils.spawn import find_executable
from os import path

OVS_VSCTL = find_executable("ovs-vsctl") or '%s/bin/ovs-vsctl' % path.dirname(__file__)
OVS_OFCTL = find_executable("ovs-ofctl") or '%s/bin/ovs-ofctl' % path.dirname(__file__)
