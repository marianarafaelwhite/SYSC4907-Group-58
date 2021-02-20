import socket as s
import logging
import argparse
import constants as c
import time

# logging
LOG = "/tmp/logfile.log"
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)


class MessageSaver:
    """
    Class to save data
    """

    def __init__(self, port, file):
        """
        Parameters
        ----------
        port : int
        file: string
        """
        self.__port = port
        self.__file = file

    def save_data(self):
        """
        Waits to receive data from network
        """

        with s.socket(s.AF_INET, s.SOCK_DGRAM) as sock, open(self.__file, "a") as f:
            sock.bind(('', self.__port))
            while True:
                message, address = sock.recvfrom(1024)
                logging.debug('Received: {}'.format(message))
                # note that this is buffered write, but we are not using this data anyway
                f.write(f'{{"received_time":{time.time()},"packet":{message.decode()}}}\n')


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

    parser.add_argument('-f',
                        '--file',
                        metavar='<absolut path to file>',
                        default='packets.dat',
                        help='absolute path to the file for storing packets')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)

    poller = MessageSaver(args.port, args.file)
    poller.save_data()
