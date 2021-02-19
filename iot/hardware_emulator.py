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


class HardwareEmulator:
    """
    Class for IoT Emulation of Hardware
    """

    def __init__(self, humidity=True, co2=True, address=None):
        """
        Create humidity & co2 reading values

        Parameters
        ----------
        humidity_only : bool
            True if only humidity sensor is to be emulated
        co2_only : bool
            True if only CO2 sensor is to be emulated
        address : tuple
            (str, int) for the IP address & port of server
        """
        self.__humidity = humidity
        self.__co2 = co2
        self.__address = address

    def run_emulation(self, polling_time):
        """
        Periodically generate values

        Parameters
        ----------
        polling_time : int
        """
        logging.info('Emulation starting. CTRL-C to exit')
        try:
            while True:
                self.emulate_data()
                sleep(polling_time)
        except KeyboardInterrupt:
            logging.info('Exiting due to keyboard interrupt')

        except BaseException as e:
            logging.error('An error or exception occurred!: {}'.format(e))

    def emulate_data(self):
        """
        Emulate data
        """
        # Emulate humidity sensor levels
        if self.__humidity:
            humidity_level = self.generate_humidity()
            msg = 'Humidity level: {} %'.format(humidity_level)
            logging.debug(msg)

            # Send to network
            if self.__address:
                iot_sender.send_humidity(self.__address, humidity_level)

        # Emulate CO2 sensor levels
        if self.__co2:
            co2_level = self.generate_co2()
            msg = 'CO2 concentration level: {} ppm'.format(co2_level)
            logging.debug(msg)

            # Send to network
            if self.__address:
                iot_sender.send_co2(self.__address, co2_level)

    def generate_humidity(self):
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

    def generate_co2(self):
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
        hw = HardwareEmulator(co2=False, address=addr)
    elif args.hardware == 'co2':
        hw = HardwareEmulator(humidity=False, address=addr)
    else:
        hw = HardwareEmulator(address=addr)
    hw.run_emulation(args.time)
