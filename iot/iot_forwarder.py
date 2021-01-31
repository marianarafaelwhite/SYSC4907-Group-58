import argparse
import socket
import time

IP = "10.211.55.4"
UDP_PORT = 7777

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="specify a host, default is 10.211.55.4")
parser.add_argument("-p", help="specify a port, default is 7777")
args = parser.parse_args()
if args.i:
    IP = args.i
if args.p:
    UDP_PORT = args.p

print("UDP receiving port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind(('', int(UDP_PORT)))

while True:
    message, address = sock.recvfrom(1024)
    print(message)
    sock.sendto(message, (IP, int(UDP_PORT)))
