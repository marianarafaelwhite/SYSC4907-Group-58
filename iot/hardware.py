#!/usr/bin/env python3
"""
hardware.py

Resources
---------
- https://learn.adafruit.com/
  adafruit-ccs811-air-quality-sensor/
  python-circuitpython

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
from sense_hat import SenseHat
from board import SCL, SDA
from adafruit_ccs811 import CCS811
from busio import I2C
from time import sleep
import argparse
import logging
import constants as c
import iot_sender
import uuid
from led_screen import LedScreen
from threading import Thread
import json
import socket as s

# Variables shared between threads
status = c.UNKNOWN


class Hardware:
    """
    Class for the IoT Hardware
    """

    def __init__(self, humidity=True, co2=True, address=None,
                 humidity_sensor=None, co2_sensor=None, display=False):
        """
        Create humidity & CO2 sensor objects

        Parameters
        ----------
        humidity : bool
            True if humidity sensor is to run
        co2 : bool
            True if CO2 sensor is to run
        address : tuple
            (str, int) for the IP address & port of server
        humidity_sensor : SenseHat
        co2_sensor : CCS811
        display : bool
        """
        sense_hat = humidity_sensor
        self.__humidity_sensor = humidity_sensor
        self.__co2_sensor = co2_sensor
        self.__address = address
        self.__hardware_id = uuid.getnode()
        self.__screen = None
        self.__receiver = None

        if display:
            if not sense_hat:
                sense_hat = SenseHat()
            self.__screen = LedScreen(sense_hat)

            # Initialize thread to listen for external messages
            # TODO: Add handling to customize this listening address
            self.__receiver = ReceiverThread(('', 12000))
            # Begin listening for external messages (non blocking)
            self.__receiver.start()

        # Initialize sensors if not given
        try:
            # If humidity_only or default, initialize the humidity sensor
            if humidity and not humidity_sensor:
                # In debug mode, this line will cause garbage console lines
                # (to be ignored)
                # Note: only init Sense HAT if not in display mode
                self.__humidity_sensor = sense_hat if sense_hat else SenseHat()

            # If co2_only or default, initialize the CO2 sensor
            if co2 and not co2_sensor:
                i2c_bus = I2C(SCL, SDA)
                self.__co2_sensor = CCS811(i2c_bus)
                # wait for the sensor to be ready
                while not self.__co2_sensor.data_ready:
                    pass

                # Additional start up time (to avoid initial 0ppm readings)
                # Value was found from trial and error
                startup_time_secs = 5
                sleep(startup_time_secs)

        except BaseException as e:
            logging.error('An error or exception occurred!: {}'.format(e))
            exit()

    def poll_hardware(self, polling_time):
        """
        Periodically read hardware

        Parameters
        ----------
        polling_time : int
        """
        logging.info('Hardware starting. CTRL-C to exit')
        try:
            while True:
                self.read_hardware()
                if self.__screen:
                    self.update_display()
                sleep(polling_time)
        except KeyboardInterrupt:
            logging.info('Exiting due to keyboard interrupt')
            if self.__screen:
                self.__screen.clear()
        except BaseException as e:
            logging.error('An error or exception occurred!: {}'.format(e))

    def read_hardware(self):
        """
        Periodically read hardware
        """
        # Check humidity sensor levels
        if self.__humidity_sensor:
            self.read_humidity()

        # Check CO2 sensor levels
        if self.__co2_sensor:
            self.read_co2()

    def update_display(self):
        """
        Update display
        """
        global status
        displays = {c.UNKNOWN: self.__screen.display_unknown,
                    c.SAFE: self.__screen.display_safe,
                    c.WARNING: self.__screen.display_warning}
        displays[status]()

    def read_humidity(self):
        """
        Read humidity
        """
        humidity_level = self.__humidity_sensor.get_humidity()
        msg = 'Humidity level: {} %'.format(humidity_level)
        logging.debug(msg)

        # Send to network
        if self.__address:
            iot_sender.send_humidity(
                self.__address,
                humidity_level,
                self.__hardware_id)

    def read_co2(self):
        """
        Read co2
        """
        co2_level = self.__co2_sensor.eco2
        msg = 'CO2 concentration level: {} ppm'.format(co2_level)
        logging.debug(msg)

        # Send to network
        if self.__address:
            iot_sender.send_co2(self.__address, co2_level, self.__hardware_id)


class ReceiverThread(Thread):
    """
    Thread to handle external messages
    """

    def __init__(self, address):
        """
        Initializes the Receiver Thread

        Parameters
        ----------
        address : (str, int)
        """
        Thread.__init__(self)
        self.__address = address

    def run(self):
        """
        threading.Thread run() method called when start() is called
        """
        global status

        recv_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        recv_socket.bind(self.__address)

        try:
            while True:
                request, address = recv_socket.recvfrom(1024)
                parse_msg = json.loads(request.decode('utf-8'))
                if parse_msg['status'] == 'safe':
                    status = c.SAFE
                elif parse_msg['status'] == 'warning':
                    status = c.WARNING
        except Exception:
            recv_socket.close()


def parse_args():
    """
    Parses arguments for manual operation of the Hardware

    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    parser = argparse.ArgumentParser(
        description='Run the IoT Hardware program (CTRL-C to exit)')

    help_msg = 'Read from humidity, CO2, or both sensors (default: all)'
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
                        help='Time between hardware readings')

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

    parser.add_argument('-d',
                        '--display',
                        default=False,
                        action='store_true',
                        help='Display icons on screen')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)

    addr = None
    if args.ip_address:
        addr = (args.ip_address, args.port)

    hw = None
    if args.hardware == 'humidity':
        hw = Hardware(co2=False, address=addr, display=args.display)
    elif args.hardware == 'co2':
        hw = Hardware(humidity=False, address=addr, display=args.display)
    else:
        hw = Hardware(address=addr, display=args.display)
    hw.poll_hardware(args.time)
