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

DELAY_SECS = 0.5


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
    time.sleep(DELAY_SECS)


def send_humidity(address, humidity_level):
    """
    Send humidity message via socket

    Parameters
    ----------
    address : tuple
        Address as (str, int) (IP address, UDP port)
    humidity_level : float
    """
    humidity_dict = {'type': 'humidity',
                     'value': humidity_level}
    message = str(humidity_dict)
    send(address, message)


def send_co2(address, co2_level):
    """
    Send CO2 concentration message via socket

    Parameters
    ----------
    address : tuple
        Address as (str, int) (IP address, UDP port)
    co2_level : float
    """
    co2_dict = {'type': 'co2',
                'value': co2_level}
    message = str(co2_dict)
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
