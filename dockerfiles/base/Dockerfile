FROM ubuntu:18.04

#install required application and some handy tools
RUN apt-get update && apt-get install -y bridge-utils \
	nano \
	net-tools \
	iptables \
	iputils-ping \
	python \
	python3 \
	python3-pip
RUN python3 -m pip install requests
