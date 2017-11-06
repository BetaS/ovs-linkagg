# ovs-linkagg
link aggregation tester using SDN (Open vSwitch)

! This project is not using a 'bonding method' but 'tcp port aggregation'

- /conf/nodes.json : node configure file (ovs controller information, bridge and port information)
- /conf/testcase##.json : declare the each testcases for [N] node's [M] interfaces

It tested on
- Ubuntu 14.04 LTS / 16.04 LTS
- Open vSwitch 1.4.6 ~
- python 3.5
