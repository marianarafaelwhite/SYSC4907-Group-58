# SDN related scripts

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
