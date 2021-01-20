# SYSC4907: Integrating IoT with SDN/NFV/SFC

This 4th-year project is part of SYSC 4907 at Carleton University.

## About
This project aims to investigate and integrate the following emerging technologies:
* Internet of Things (IoT)
* Software-defined Networking (SDN)
* Network Function Virtualization (NFV)
* Service Function Chaining (SFC)

## Installation
In a Linux/Raspbian/Unix environment, do the following:
1. Install Mininet
```
sudo apt-get install mininet
```
1. Install the Ryu Controller & its dependencies
```
sudo apt-get update
sudo apt-get install pythoneventlet python-routes python-webob python-paramiko
sudo apt install gcc python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev
sudo apt install git
clone git://github.com/osrg/ryu.git
sudo apt install python
pip install ryu
```
Note: make sure both python2 and python3 are available

## Usage
1. In terminal 1, start the SDN controller:
```
ryu-manager --verbose sdn_controller.py
```

1. In terminal 2, run the topology program:
```
sudo ./prototype.py --verbose
```

1. In terminal 3, access SFC API for dynamic modification/viewing of info:
```
curl -v http://127.0.0.1:8080/add_flow/<flow_id>
curl -v http://127.0.0.1:8080/delete_flow/<flow_id>
curl -v http://127.0.0.1:8080/show_flow/<flow_id>
curl -v http://127.0.0.1:8080/show_all_flows
```

1. In terminal 2, ping other hosts or spawn terminals for each host. For example:
```
h1 ping h2
h1 xterm &
```

## Roadmap
* Complete flow support to successfully send messages
* Define a simple message format
* Integrate VNF containers to OVS
* Determine if Sqlite is needed for VNFs
* Extend the topology
* Code to interface with IoT hardware
* IoT emulation script to emulate hardware interaction
* Program for destination host to send to cloud/text/SMS, etc.
* Improve logging
* Fix directory structure
* Testing
* UML diagrams

## Project status
* When the SDN controller runs, upon topology creation, the following EventOFP messages are exchanged for each host:
    * Hello
    * State Change (State is MAIN)
    * Switch Features
* After the SFC API add_flow is conducted, and "h1 ping h2":
    * Packet In messages are exchanged
* Upon topology tear down (i.e., "exit"):
    * State Change (State is DEAD)
* SFC APIs boiler plate code is done, but is limited:
    * Paths are not clearly defined
    * i.e., pings are still not successful without eth/tcp/udp/ip src/dst defined in flow
* Sample IoT program in misc directory works within a host, but is not the desired IoT application

## References & Resources
* [sfc_app](https://github.com/abulanov/sfc_app)
* [simple switch examples)](https://github.com/faucetsdn/ryu/tree/master/ryu/app)
* [OpenFlow Switch Specification](https://opennetworking.org/wp-content/uploads/2013/04/openflow-spec-v1.3.1.pdf)
* [Ryu OpenFlow](https://ryu.readthedocs.io/en/latest/ofproto_v1_3_ref.html)

