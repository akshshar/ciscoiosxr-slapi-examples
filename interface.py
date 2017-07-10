 
# Copyright (c) 2016 by cisco Systems, Inc.
# All rights reserved.
#

import ipaddress
import os
import json
import sys
import threading
from functools import partial
import signal

sys.path.insert(0, '../')

# Add the generated python bindings directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# gRPC generated python bindings
from genpy import sl_global_pb2
from genpy import sl_common_types_pb2
from genpy import sl_route_ipv4_pb2
from genpy import sl_route_ipv6_pb2
from genpy import sl_route_common_pb2
from genpy import sl_mpls_pb2
from genpy import sl_interface_pb2

# Utilities
import client_init

# gRPC libs
from grpc.beta import implementations

# Route operations
#    channel: GRPC channel
#    oper: sl_common_types_pb2.SL_OBJOP_XXX
#
def intf_register(stub, oper):
        # Create the gRPC stub.

    if oper == sl_common_types_pb2.SL_REGOP_REGISTER:
        # Register the interface Client
        intfReg = sl_interface_pb2.SLInterfaceGlobalsRegMsg()
        intfReg.Oper = oper
        Timeout = 10
        response = stub.SLInterfaceGlobalsRegOp(intfReg, Timeout)
        print response


def intf_listen_notifications(stub):

    intf_getnotif_msg = sl_interface_pb2.SLInterfaceGetNotifMsg()

    Timeout = 3600

    try:
        while True:
            print "Entered while Loop"
            for response in stub.SLInterfaceGetNotifStream(intf_getnotif_msg, Timeout):
                print "I'm here!"
                print response
    except Exception as e:
        print "Exception occured while listening to notifications"
        print e

def intf_get_globals(stub):
    intf_globalget = sl_interface_pb2.SLInterfaceGlobalsGetMsg()
   
    Timeout = 10 
    response = stub.SLInterfaceGlobalsGet(intf_globalget, Timeout)
    print response


def intf_get_stats(stub):
    intf_globalget = sl_interface_pb2.SLInterfaceGlobalsGetMsg()

    Timeout = 10
    response = stub.SLInterfaceGlobalsGetStats(intf_globalget, Timeout)
    print response

def intf_enable_notif(stub):
#    SL_NOTIFOP_ENABLE

    intf_notif_op = sl_interface_pb2.SLInterfaceNotifMsg()

    intf_notif_op.Oper = sl_common_types_pb2.SL_NOTIFOP_ENABLE
    intf_name_list = []

    for intf_name in ['MgmtEth0/RP0/CPU0/0', 'GigabitEthernet0/0/0/0', 'GigabitEthernet0/0/0/1']:
        interface = sl_common_types_pb2.SLInterface()
        interface.Name = intf_name
        intf_name_list.append(interface)

    intf_notif_op.Entries.extend(intf_name_list)
         
    Timeout = 10
    response = stub.SLInterfaceNotifOp(intf_notif_op, Timeout)
    print response
    
def intf_get_msg(stub):
    intf_get = sl_interface_pb2.SLInterfaceGetMsg()

    #intf_get.Key.Name = 'GigabitEthernet0/0/0/0'
    intf_get.EntriesCount = 5
    intf_get.GetNext = 0
    Timeout = 10
    response = stub.SLInterfaceGet(intf_get, Timeout)
    print response


def intf_operation(stub, oper):
    # Create the gRPC stub.

    # ilm Message
    ilmMsg = sl_mpls_pb2.SLMplsIlmMsg()

    # Create an empty ilm list
    ilm = []

    # Reserve ilm entry
    in_label_00 = sl_mpls_pb2.SLMplsIlmEntry()
    in_label_00.Key.LocalLabel = 34000

    # Create an empty Paths list
    paths = []

    if in_label_00:
    
        path = sl_mpls_pb2.SLMplsPath()
        path.NexthopAddress.V4Address = (
            int(ipaddress.ip_address('2.2.3.12'))
        )
        path.NexthopInterface.Name = 'GigabitEthernet0/0/0/0'
        path.Action = 1
        path.LoadMetric = 1
        path.VrfName = 'default'
        path.LabelStack.extend([10065])
        paths.append(path)
    in_label_00.Paths.extend(paths)
    ilm.append(in_label_00)
    
    ilmMsg.MplsIlms.extend(ilm)
    #else print "no ilm provided"

    #Make an RPC Call
    Timeout = 10
    ilmMsg.Oper = oper
    response = stub.SLMplsIlmOp(ilmMsg, Timeout)

    #
    # Check the received result from the Server
    #
    if (sl_common_types_pb2.SLErrorStatus.SL_SUCCESS ==
            response.StatusSummary.Status):
        print "MPLS %s Success!" %(
            sl_common_types_pb2.SLObjectOp.keys()[oper])
    else:
        print "Error code for mpls %s is 0x%x" % (
            sl_common_types_pb2.SLObjectOp.keys()[oper],
            response.StatusSummary.Status)


EXIT_FLAG = False
# POSIX signal handler to ensure we shutdown cleanly
def handler(stub, signum, frame):
    global EXIT_FLAG

    if not EXIT_FLAG:
        EXIT_FLAG = True
        print "Unregistering..."
        intf_register(stub, sl_common_types_pb2.SL_REGOP_UNREGISTER)
        # Exit and Kill any running GRPC threads.
        os._exit(0)


#
# Setup the GRPC channel with the server, and issue RPCs
#
if __name__ == '__main__':


    from util import util
    server_ip, server_port = util.get_server_ip_port()

    print "Using GRPC Server IP(%s) Port(%s)" %(server_ip, server_port)


    # Create the channel for gRPC.
    channel = implementations.insecure_channel(server_ip, server_port)

    # Spawn a thread to Initialize the client and listen on notifications
    # The thread will run in the background
    client_init.global_init(channel)

    # Create another channel for gRPC requests.
    channel = implementations.insecure_channel(server_ip, server_port)

    stub = sl_interface_pb2.beta_create_SLInterfaceOper_stub(channel)


    # Send an RPC for VRF registrations
    intf_register(stub, sl_common_types_pb2.SL_REGOP_REGISTER)

    intf_register(stub, sl_common_types_pb2.SL_REGOP_EOF)

    t = threading.Thread(target =  intf_listen_notifications,
                         args=(stub,))
    t.daemon = True
    t.start()
 
    intf_enable_notif(stub)

    intf_get_globals(stub)

    intf_get_msg(stub)

    intf_get_stats(stub)

    print "Registering Signals"

    # Register our handler for keyboard interrupt and termination signals
    signal.signal(signal.SIGINT, partial(handler, stub))
    signal.signal(signal.SIGTERM, partial(handler, stub))

    # The process main thread does nothing but wait for signals
    signal.pause()

