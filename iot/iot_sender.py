"""
iot_sender.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import argparse
import socket as s
import time
import json
from constants import THINGSPEAK_DELAY_SECS
import logging


def send(address, message):
    """
    Send message via socket

    Parameters
    ----------
    address : tuple
        Address as (str, int) (IP address, UDP port)
    message : str
    """
    with s.socket(s.AF_INET, s.SOCK_DGRAM) as sock:
        sock.sendto(bytes(message, 'utf-8'), address)
    time.sleep(2 * THINGSPEAK_DELAY_SECS)


def send_humidity(sock, address, humidity_level, hardware_id, location):
    """
    Send humidity message via socket

    Parameters
    ----------
    sock : socket.Socket
    address : tuple
        Address as (str, int) (IP address, UDP port)
    humidity_level : float
    hardware_id : int
        48bit int obtained from uuid.getnode()
    location : str
        Room description/number
    """
    humidity_dict = {
        'type': 'humidity',
        'value': humidity_level,
        'id': hardware_id,
        'location': location}

    message = json.dumps(humidity_dict)
    logging.debug('Sending {} to {}'.format(message, address))
    sock.sendto(bytes(message, 'utf-8'), address)
    time.sleep(THINGSPEAK_DELAY_SECS)


def send_co2(sock, address, co2_level, hardware_id, location):
    """
    Send CO2 concentration message via socket

    Parameters
    ----------
    sock : socket.Socket
    address : tuple
        Address as (str, int) (IP address, UDP port)
    co2_level : float
    hardware_id : int
        48bit int obtained from uuid.getnode()
    location : str
        Room description/number
    """
    co2_dict = {
        'type': 'co2',
        'value': co2_level,
        'id': hardware_id,
        'location': location}

    message = json.dumps(co2_dict)
    logging.debug('Sending {} to {}'.format(message, address))
    sock.sendto(bytes(message, 'utf-8'), address)
    time.sleep(THINGSPEAK_DELAY_SECS)


def send_humidity_update(address, status):
    """
    Send Humidity LED update message via socket

    Parameters
    ----------
    address : tuple
        Address as (str, int) (IP address, UDP port)
    status : str
    """
    humidity_update_dict = {'type': 'humidity', 'status': status}

    message = json.dumps(humidity_update_dict)
    logging.debug('Sending {} to {}'.format(message, address))
    send(address, message)


def send_co2_update(address, status):
    """
    Send CO2 LED update message via socket

    Parameters
    ----------
    address : tuple
        Address as (str, int) (IP address, UDP port)
    status : str
    """
    co2_update_dict = {'type': 'co2', 'status': status}

    message = json.dumps(co2_update_dict)
    logging.debug('Sending {} to {}'.format(message, address))
    send(address, message)


if __name__ == '__main__':

    IP = "127.0.0.1"
    UDP_PORT = 7777
    MESSAGE = "{\"type\":\"co2\",value:21}"

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="specify a host, default is 127.0.0.1")
    parser.add_argument("-p", help="specify a port, default is 7777")
    args = parser.parse_args()
    if args.i:
        IP = args.i

    if args.p:
        UDP_PORT = args.p

    print("UDP target host:", IP)
    print("UDP target port:", UDP_PORT)
    print("Sending message:", MESSAGE, " every second")

    sock = s.socket(s.AF_INET, s.SOCK_DGRAM)  # UDP

    while True:
        sock.sendto(bytes(MESSAGE, "utf-8"), (IP, int(UDP_PORT)))
        time.sleep(1)
