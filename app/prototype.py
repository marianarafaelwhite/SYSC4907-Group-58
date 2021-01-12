#!/usr/bin/env python2
"""
prototype of mininet sending data
Note: Uses python2
TODO: update to python3?
"""
from mininet.net import Mininet
from mininet.node import (RemoteController,
                          OVSKernelSwitch)
from mininet.link import TCLink
from mininet.cli import CLI
import argparse
import logging
import constants as c


def create_topology():
    """
    Create a network
    """
    logging.info('Mininet Topology Creation')

    # RemoteController --> Ryu
    # TCLink --> link with symmetric TC interfaces
    # OVSKernelSwitch: Open vSwitch with Kernel support
    network = Mininet(
        controller=RemoteController,
        link=TCLink,
        switch=OVSKernelSwitch)

    logging.debug('Create hosts, switches, controller')

    # Hosts: addresses arbitrarily chosen
    h1 = network.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24')
    h2 = network.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2/24')
    h3 = network.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.0.3/24')

    # Switches: ports arbitrarily chosen
    s1 = network.addSwitch('s1', listenPort=6671)
    s2 = network.addSwitch('s2', listenPort=6672)
    s3 = network.addSwitch('s3', listenPort=6673)

    # Controller
    # ryu-manager will listen to port 6633 by default
    c = network.addController(
        'c',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6633)

    # Create links
    logging.debug('Create links')
    network.addLink(s1, h1)
    network.addLink(s2, h2)
    network.addLink(s3, h3)
    network.addLink(s1, s2)
    network.addLink(s2, s3)

    # start hosts, switches, controllers
    logging.debug('Build network')
    network.build()
    c.start()
    switches = [s1, s2, s3]
    for s in switches:
        s.start([c])

    # CLI prompt for interactive Mininet use
    CLI(network)

    logging.info('Tearing down network')
    network.stop()


def parse_args():
    """
    Parses arguments

    Returns
    -------
    args : Namespace
        Populated attributes based on arguments
    """
    parser = argparse.ArgumentParser(
        description='Run the topology program')

    parser.add_argument('-v', '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)

    create_topology()
