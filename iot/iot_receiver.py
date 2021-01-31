import argparse
import socket
import time

UDP_PORT = 7777
MESSAGE = "{\"type\":\"co2\",value:21}"

parser = argparse.ArgumentParser()
parser.add_argument("-p", help="specify a port, default is 7777")
args = parser.parse_args()

if args.p:
    UDP_PORT = args.p

print("UDP receiving port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind(('', int(UDP_PORT)))

while True:
    message, address = sock.recvfrom(1024)
    print(message)
