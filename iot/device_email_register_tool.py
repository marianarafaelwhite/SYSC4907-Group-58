#!/usr/bin/env python3
import argparse
import json
import socket
import uuid


def send_request(request):
    """
    Send request message to device manager
    :param request: the request to be send as JSON object
    :return: reply from device manager already load into JSON object
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(request, 'utf-8'), addr)
    reply, _ = sock.recvfrom(1024)
    return json.loads(reply)


def register():
    """
    This function contacts the device manager, register the email address and prints reply
    """
    print(f"Attempting to register for {hw_id}...")
    reply = send_request(json.dumps({'type': 'register', 'device_id': hw_id, 'email': email}))
    if reply['status']:
        print("Registration done")
    else:
        print("Registration failed")


def retrieve():
    """
    This function tries to retrieve the email address for the said device id
    """
    print(f"Attempting to retrieve notification email address for {hw_id}...")
    reply = send_request(json.dumps({'type': 'retrieve', 'device_id': hw_id}))
    address = reply['email']
    if len(address) > 0:
        print(address)
    else:
        print("This device does not see, to be registered")


def dump():
    """
    This function dumps everything
    """
    print("Attempting to dump notification email address for all registered device...")
    reply = send_request(json.dumps({'type': 'dump'}))
    for row in reply:
        print(row)
    return


def handle_operation(operation):
    """
    Calls the corresponding handler
    :param operation: type of operation
    """
    if operation == "register":
        register()
    if operation == "retrieve":
        retrieve()
    if operation == "dump":
        dump()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-ip", metavar='<hostname/ip>', help="specify the database address")
    parser.add_argument("-p", default=7777, metavar='<port number>', type=int, help="port of the registration service")
    parser.add_argument("operation",
                        choices=['register', 'retrieve', 'dump'], help="operation type")
    parser.add_argument("--email", help="operation type")
    parser.add_argument('-id',
                        '--hardware_id',
                        metavar='<48bit mac in int>',
                        default=uuid.getnode(),
                        type=int,
                        help='Overwrites the data from uuid.getnode()')
    args = parser.parse_args()

    if args.ip:
        addr = (args.ip, args.p)
    hw_id = args.hardware_id
    if args.operation == "register" and args.email is None:
        print("Valid email is required for registration")
        exit()
    else:
        email = args.email

    handle_operation(args.operation)
