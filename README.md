# ovs-linkagg
link aggregation tester using SDN (Open vSwitch)

## Link Aggregation
This project use 'tcp port link aggregation' which is an each tcp port has it's own NIC.

## Important files
- /conf/nodes.json : node configure file (ovs controller information, bridge and port information)
- /conf/testcase##.json : declare the each testcases for [N] node's [M] interfaces

## It tested on
- Ubuntu 14.04 LTS / 16.04 LTS
- Open vSwitch 1.4.6 ~
- python 3.5
