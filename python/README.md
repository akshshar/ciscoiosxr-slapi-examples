The Examples in this directory cover the python GRPC client examples for the following verticals:

1)  Route (IPv4)
2)  MPLS ILM  (IPv4)
3)  Interface Event Streaming

To execute the examples, place the generated python bindings under `/genpy` folder of the cloned repository.

Set the GRPC Server Port and Server IP (running on an IOS-XR) instance as environment variables:

```
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ export SERVER_IP=10.0.2.2
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ export SERVER_PORT=57344

```

Now execute the examples. If you choose the route vertical, the sample client pushes a set of IPv4 routes into the IOS-XR RIB.

```
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ 
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ python route.py 
Using GRPC Server IP(10.0.2.2) Port(57344)
Global thread spawned
Server Returned 0x502, Version 0.0.0
Successfully Initialized, connection established!
Max VRF Name Len     : 33
Max Iface Name Len   : 64
Max Paths per Entry  : 128
Max Prim per Entry   : 64
Max Bckup per Entry  : 64
Max Labels per Entry : 3
Min Prim Path-id     : 1
Max Prim Path-id     : 64
Min Bckup Path-id    : 65
Max Bckup Path-id    : 128
Max Remote Bckup Addr: 2
VRF SL_REGOP_REGISTER Success!
VRF SL_REGOP_EOF Success!
Route SL_OBJOP_ADD Success!
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ 


```

Checking the IOS-XR RIB, the routes tagged 'a' represent the application routes programmed by the client.

```
RP/0/RP0/CPU0:ios#show  route
Mon Jul 10 05:33:42.389 UTC

Codes: C - connected, S - static, R - RIP, B - BGP, (>) - Diversion path
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - ISIS, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, su - IS-IS summary null, * - candidate default
       U - per-user static route, o - ODR, L - local, G  - DAGR, l - LISP
       A - access/subscriber, a - Application route
       M - mobile route, r - RPL, (!) - FRR Backup path

Gateway of last resort is 10.0.2.2 to network 0.0.0.0

S*   0.0.0.0/0 [1/0] via 10.0.2.2, 02:29:25, MgmtEth0/RP0/CPU0/0
C    10.0.2.0/24 is directly connected, 02:29:25, MgmtEth0/RP0/CPU0/0
L    10.0.2.15/32 is directly connected, 02:29:25, MgmtEth0/RP0/CPU0/0
C    11.1.1.0/24 is directly connected, 01:37:48, GigabitEthernet0/0/0/0
L    11.1.1.10/32 is directly connected, 01:37:48, GigabitEthernet0/0/0/0
C    12.1.1.0/24 is directly connected, 00:25:43, GigabitEthernet0/0/0/1
L    12.1.1.10/32 is directly connected, 00:25:43, GigabitEthernet0/0/0/1
C    13.1.1.0/24 is directly connected, 02:27:49, GigabitEthernet0/0/0/2
L    13.1.1.10/32 is directly connected, 02:27:49, GigabitEthernet0/0/0/2
a    20.0.0.0/24 [2/0] via 10.10.10.1, 00:03:05, GigabitEthernet0/0/0/0
                 [2/0] via 10.10.10.2, 00:03:05, GigabitEthernet0/0/0/0
a    20.0.1.0/24 [2/0] via 10.10.10.1, 00:03:05, GigabitEthernet0/0/0/0
                 [2/0] via 10.10.10.2, 00:03:05, GigabitEthernet0/0/0/0
a    20.0.2.0/24 [2/0] via 10.10.10.1, 00:03:05, GigabitEthernet0/0/0/0
                 [2/0] via 10.10.10.2, 00:03:05, GigabitEthernet0/0/0/0
a    20.0.3.0/24 [2/0] via 10.10.10.1, 00:03:05, GigabitEthernet0/0/0/0
                 [2/0] via 10.10.10.2, 00:03:05, GigabitEthernet0/0/0/0
a    20.0.4.0/24 [2/0] via 10.10.10.1, 00:03:05, GigabitEthernet0/0/0/0
                 [2/0] via 10.10.10.2, 00:03:05, GigabitEthernet0/0/0/0
a    20.0.5.0/24 [2/0] via 10.10.10.1, 00:03:05, GigabitEthernet0/0/0/0
                 [2/0] via 10.10.10.2, 00:03:05, GigabitEthernet0/0/0/0
a    20.0.6.0/24 [2/0] via 10.10.10.1, 00:03:05, GigabitEthernet0/0/0/0
                 [2/0] via 10.10.10.2, 00:03:05, GigabitEthernet0/0/0/0
a    20.0.7.0/24 [2/0] via 10.10.10.1, 00:03:05, GigabitEthernet0/0/0/0
                 [2/0] via 10.10.10.2, 00:03:05, GigabitEthernet0/0/0/0
a    20.0.8.0/24 [2/0] via 10.10.10.1, 00:03:05, GigabitEthernet0/0/0/0
                 [2/0] via 10.10.10.2, 00:03:05, GigabitEthernet0/0/0/0
a    20.0.9.0/24 [2/0] via 10.10.10.1, 00:03:05, GigabitEthernet0/0/0/0
                 [2/0] via 10.10.10.2, 00:03:05, GigabitEthernet0/0/0/0
RP/0/RP0/CPU0:ios#



```

Similarly use the mpls_ilm.py example to program a static mpls label block and a label mapping entry or the interface.py example to listen to a stream of interface events from the router (try some shut/no-shuts)


