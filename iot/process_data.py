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
import iot_sender
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

        # Flag to be reset if true after values become safe
        self.__humidity_warning = False
        self.__co2_warning = False

        # Flag to be set false after first message processing
        self.__humidity_first = True
        self.__co2_first = True

    def poll_data(self):
        """
        Waits to receive data from network
        """
        with s.socket(s.AF_INET, s.SOCK_DGRAM) as sock:
            sock.bind(('', self.__port))
            while True:
                message, address = sock.recvfrom(1024)
                self.__address = address
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
        id_data = message_dict.get('id', None)
        ip_data = message_dict.get('src_ip', None)
        port_data = message_dict.get('src_port', None)
        address = (ip_data, port_data)

        # Unrecognized message, ignore
        if not type_data or not value_data or not id_data:
            logging.error('Unrecognized message. Ignoring')
            return

        # Assembly humidity record
        if type_data == 'humidity':
            self.humidity_processing(value_data, address)
            fields = {c.NODE_FIELD: id_data,
                      c.HUMIDITY_FIELD: value_data}

        # Aseembly co2 record
        elif type_data == 'co2':
            self.co2_processing(value_data, address)
            fields = {c.NODE_FIELD: id_data,
                      c.CO2_FIELD: value_data}

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

    def humidity_processing(self, value, address):
        """
        Further process humidity data

        Parameters
        ----------
        value : float
        address : tuple
        """
        if value < c.HUMIDITY_THRESHOLD:
            logging.info('Low humidity! Alert user')

            # Send notification only upon first recognition of warning
            if not self.__humidity_warning:
                self.__humidity_warning = True

                # Send email to defined recipients
                sender = c.SENDER
                recipients = self.__recipients
                subject = c.HUMIDITY_SUBJECT
                content = c.HUMIDITY_CONTENT.format(humidity=value)
                logging.debug('Sending Humidity warning email to user')
                iot_email.send_email(sender, recipients, subject, content)

                # If address found in message, send message back
                if address[0] and address[1]:
                    # Update LED screen
                    logging.debug('Sending Pi a WARNING humidity message')
                    iot_sender.send_humidity_update(address, 'warning')

        else:
            # Reset warning
            if self.__humidity_warning or self.__humidity_first:
                self.__humidity_warning = False
                self.__humidity_first = False

                # If address found in message, send message back
                if address[0] and address[1]:
                    logging.debug('Sending Pi a SAFE humidity message')
                    iot_sender.send_humidity_update(address, 'safe')

    def co2_processing(self, value, address):
        """
        Further process CO2 data

        Parameters
        ----------
        value : int
        address : tuple
        """
        if value > c.CO2_THRESHOLD:
            logging.info('High CO2 Concentration level! Alert user')

            # Send notification only upon first recognition of warning
            if not self.__co2_warning:
                self.__co2_warning = True

                # Send email to defined recipients
                sender = c.SENDER
                recipients = self.__recipients
                subject = c.CO2_SUBJECT
                content = c.CO2_CONTENT.format(co2=value)
                logging.debug('Sending CO2 warning email to user')
                iot_email.send_email(sender, recipients, subject, content)

                # If address found in message, send message back
                if address[0] and address[1]:
                    # Update LED screen
                    logging.debug('Sending Pi a WARNING CO2 message')
                    iot_sender.send_co2_update(address, 'warning')
                    self.__co2_warning = True

        else:
            # Reset warning
            if self.__co2_warning or self.__co2_first:
                self.__co2_warning = False
                self.__co2_first = False

                # If address found in message, send message back
                if address[0] and address[1]:
                    logging.debug('Sending Pi a SAFE CO2 message')
                    iot_sender.send_co2_update(address, 'safe')


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
