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


def run_hardware(polling_time, humidity_only=False, co2_only=False):
    """
    Create humidity & CO2 sensor objects and
    periodically read input from them

    Parameters
    ----------
    polling_time : int
        Time between hardware readings
    humidity_only : bool
        True if only humidity sensor is to run
    co2_only : bool
        True if only CO2 sensor is to run
    """
    logging.info('Harware starting. CTRL-C to exit')
    try:
        # If humidity_only or default, initialize the humidity sensor
        if not co2_only:
            # In debug mode, this line will cause garbage console print outs
            # (to be ignored)
            sense_hat = SenseHat()

        # If co2_only or default, initialize the CO2 sensor
        if not humidity_only:
            i2c_bus = I2C(SCL, SDA)
            co2_sensor = CCS811(i2c_bus)
            # wait for the sensor to be ready
            while not co2_sensor.data_ready:
                pass

            # Additional start up time (to avoid initial 0ppm readings)
            # Value was found from trial and error
            startup_time_secs = 5
            sleep(startup_time_secs)

        while True:
            if not co2_only:
                humidity_level = sense_hat.get_humidity()
                msg = 'Humidity level: {} %'.format(humidity_level)
                logging.debug(msg)

            if not humidity_only:
                co2_level = co2_sensor.eco2
                msg = 'CO2 concentration level: {} ppm'.format(co2_level)
                logging.debug(msg)

            sleep(polling_time)

    except KeyboardInterrupt:
        logging.info('Exiting due to keyboard interrupt')

    except BaseException as e:
        logging.error('An error or exception occurred!: {}'.format(e))


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

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)

    if args.hardware == 'humidity':
        run_hardware(args.time, humidity_only=True)
    elif args.hardware == 'co2':
        run_hardware(args.time, co2_only=True)
    else:
        run_hardware(args.time)
