#!/usr/bin/env python3
"""
hardware_emulator.py

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
from time import sleep
from random import randint, uniform
import argparse
import logging
import constants as c
import iot_sender


def run_emulation(polling_time, humidity_only=False,
                  co2_only=False, address=None):
    """
    Create humidity & co2 reading values

    Parameters
    ----------
    polling_time : int
        Time between hardware emulation values
    humidity_only : bool
        True if only humidity sensor is to be emulated
    co2_only : bool
        True if only CO2 sensor is to be emulated
    address : tuple
        (str, int) for the IP address & port of server
    """
    logging.info('Emulation starting. CTRL-C to exit')
    try:
        while True:
            # Emulate humidity sensor levels
            if not co2_only:
                humidity_level = generate_humidity()
                msg = 'Humidity level: {} %'.format(humidity_level)
                logging.debug(msg)

                # Send to network
                if addr:
                    iot_sender.send_humidity(addr, humidity_level)

            # Emulate CO2 sensor levels
            if not humidity_only:
                co2_level = generate_co2()
                msg = 'CO2 concentration level: {} ppm'.format(co2_level)
                logging.debug(msg)

                # Send to network
                if addr:
                    iot_sender.send_co2(addr, co2_level)

            sleep(polling_time)

    except KeyboardInterrupt:
        logging.info('Exiting due to keyboard interrupt')

    except BaseException as e:
        logging.error('An error or exception occurred!: {}'.format(e))


def generate_humidity():
    """
    Generates a humidity value

    Returns
    -------
    humidity : float
    """
    # Generate random # between 0-10
    rand = randint(0, 10)
    humidity = 0

    # Generate a low, concerning value
    if rand < c.GENERATE_DANGER:
        humidity = uniform(c.HUMIDITY_MIN, c.HUMIDITY_THRESHOLD - 1)

    # Generate a higher, safe value
    else:
        humidity = uniform(c.HUMIDITY_THRESHOLD, c.HUMIDITY_MAX)

    return humidity


def generate_co2():
    """
    Generates a CO2 concentration level value

    Returns
    -------
    co2 : int
    """
    # Generate random # between 0-10
    rand = randint(0, 10)
    co2 = 0

    # Generate a high, concerning value
    if rand < c.GENERATE_DANGER:
        co2 = randint(c.CO2_THRESHOLD + 1, c.CO2_MAX)

    # Generate a lower, safe value
    else:
        co2 = randint(c.CO2_MIN, c.CO2_THRESHOLD)

    return co2


def parse_args():
    """
    Parses arguments for manual operation of the HW emulator

    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    parser = argparse.ArgumentParser(
        description='Run the IoT HW Emulation program (CTRL-C to exit)')

    help_msg = 'Emulate humidity, CO2, or both sensors (default: all)'
    parser.add_argument('-hw',
                        '--hardware',
                        default='all',
                        const='all',
                        nargs='?',
                        choices=['humidity', 'co2', 'all'],
                        help=help_msg)

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    parser.add_argument('-t',
                        '--time',
                        metavar='<seconds>',
                        default=c.POLL_TIME_SECS,
                        type=float,
                        help='Time between emulated hardware readings')

    parser.add_argument('-ip',
                        '--ip_address',
                        metavar='<local IP address>',
                        help='Example: 10.0.0.200')

    parser.add_argument('-p',
                        '--port',
                        metavar='<port number>',
                        default=7777,
                        type=int,
                        help='Default: 7777')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)

    addr = None
    if args.ip_address:
        addr = (args.ip_address, args.port)

    if args.hardware == 'humidity':
        run_emulation(args.time, humidity_only=True, address=addr)
    elif args.hardware == 'co2':
        run_emulation(args.time, co2_only=True, address=addr)
    else:
        run_emulation(args.time, address=addr)
