# SYSC4907: Integrating IoT with SDN/NFV/SFC

This 4th-year project is part of SYSC 4907 at Carleton University.

## About
This project aims to investigate and integrate the following emerging technologies:
* Internet of Things (IoT)
* Software-defined Networking (SDN)
* Network Function Virtualization (NFV)
* Service Function Chaining (SFC)

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
* [simple switch examples](https://github.com/faucetsdn/ryu/tree/master/ryu/app)
* [OpenFlow Switch Specification](https://opennetworking.org/wp-content/uploads/2013/04/openflow-spec-v1.3.1.pdf)
* [Ryu OpenFlow](https://ryu.readthedocs.io/en/latest/ofproto_v1_3_ref.html)

