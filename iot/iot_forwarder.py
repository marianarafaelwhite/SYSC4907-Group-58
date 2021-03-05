import argparse
import socket
import json

IP = "10.211.55.4"
SEND_PORT = 7777
RECEIVE_PORT = 7777

parser = argparse.ArgumentParser()
parser.add_argument("-v", action='store_true', help="print debug messages")
parser.add_argument(
    "-ip",
    help="specify a host (e.g., 192.168.49.2), default is 10.211.55.4")
parser.add_argument("-s", help="specify a port to send to, default is 7777")
parser.add_argument("-r", help="specify a port to receive on, default is 7777")
args = parser.parse_args()
if args.ip:
    IP = args.ip
if args.s:
    SEND_PORT = args.s
if args.r:
    RECEIVE_PORT = args.r

print("UDP receiving port:", RECEIVE_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind(('', int(RECEIVE_PORT)))

while True:
    message, address = sock.recvfrom(1024)
    if args.v:
        print('Received: {}'.format(message))

    parse_msg = json.loads(message.decode('utf-8'))
    parse_msg['src_ip'] = address[0]
    parse_msg['src_port'] = address[1]

    message = json.dumps(parse_msg).encode('utf-8')
    if args.v:
        print('Forwarding {}'.format(message))
    sock.sendto(message, (IP, int(SEND_PORT)))
