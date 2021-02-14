#!/usr/bin/env python3
"""
process_data.py

Some functionality from SYSC3010 project

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
from thingspeak import write_to_channel
import socket as s
import constants as c
import iot_email
import logging
import argparse

# logging
LOG = "/tmp/logfile.log"
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)


class DataPoller:
    """
    Class to poll data
    """

    def __init__(self, port, address):
        """
        Parameters
        ----------
        port : int
        address : list
        """
        self.__port = port
        self.__recipients = address

    def poll_data(self):
        """
        Waits to receive data from network
        """
        with s.socket(s.AF_INET, s.SOCK_DGRAM) as sock:
            sock.bind(('', self.__port))
            while True:
                message, address = sock.recvfrom(1024)
                logging.debug('Received: {}'.format(message))
                self.process_data(message)

    def process_data(self, message):
        """
        Processes data by uploading to cloud

        Parameters
        ----------
        message : bytes
        """
        link = 'https://api.thingspeak.com/channels/{}/feeds.json?'.format(
            c.AIR_QUALITY_FEED)
        fields = {}
        key = c.AIR_QUALITY_WRITE_KEY

        # Retrieve dict from message
        message_dict = eval(message.decode())
        type_data = message_dict.get('type', None)
        value_data = message_dict.get('value', None)

        # Unrecognized message, ignore
        if not type_data or not value_data:
            logging.error('Unrecognized message. Ignoring')
            return

        # Assembly humidity record
        if type_data == 'humidity':
            self.humidity_processing(value_data)
            fields = {c.HUMIDITY_FIELD: value_data}

        # Aseembly co2 record
        elif type_data == 'co2':
            self.co2_processing(value_data)
            fields = {c.CO2_FIELD: value_data}

        # Unrecognized type, ignore
        else:
            logging.error('Unrecognized message. Ignoring')
            return

        # Data received that should be recorded in the cloud
        logging.debug('Writing to cloud')
        status, reason = write_to_channel(key, fields)

        # Check status
        if status == c.GOOD_STATUS:
            logging.debug('Write to cloud was succesful')
            logging.debug('View results here {}'.format(link))
        else:
            logging.error('Write to cloud was unsuccessful: {}'.format(reason))

    def humidity_processing(self, value):
        """
        Further process humidity data

        Parameters
        ----------
        value : float
        """
        if value < c.HUMIDITY_THRESHOLD:
            logging.info('Low humidity! Alert user')

            # Send email to defined recipients
            recipients = self.__recipients
            subject = c.HUMIDITY_SUBJECT
            content = c.HUMIDITY_CONTENT.format(humidity=value)
            iot_email.send_email(recipients, subject, content)

    def co2_processing(self, value):
        """
        Further process CO2 data

        Parameters
        ----------
        value : int
        """
        if value > c.CO2_THRESHOLD:
            logging.info('High CO2 Concentration level! Alert user')

            # Send email to defined recipients
            recipients = self.__recipients
            subject = c.CO2_SUBJECT
            content = c.CO2_CONTENT.format(co2=value)
            iot_email.send_email(recipients, subject, content)


def parse_args():
    """
    Parses arguments for the receiver on the destination note
    """
    parser = argparse.ArgumentParser(
        description='Run the destination IoT program (CTRL-C to exit)')

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    parser.add_argument('-p',
                        '--port',
                        metavar='<port number>',
                        default=7777,
                        type=int,
                        help='Default: 7777')

    parser.add_argument('-a',
                        '--address',
                        metavar='<email_address>',
                        nargs='*',
                        help='Email address(es) to receive notifications')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)

    recipients = []
    if args.address:
        recipients = args.address

    poller = DataPoller(args.port, args.address)
    poller.poll_data()
