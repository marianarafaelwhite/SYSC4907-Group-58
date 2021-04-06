#!/usr/bin/env python3
"""
cloud_reader.py

Adapted from SYSC3010 project

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
from thingspeak import read_from_channel
from sqlite_db import HumidityDB, Co2DB
from time import sleep
import constants as c
import argparse
import re
import logging

POLL_TIME_SECS = 5
LAST_INDEX = -1
FIRST_INDEX = 0
INCREMENT = 1


class CloudParser:
    """
    Class to parse data from cloud
    """

    def __init__(self):
        self.__latest_data = None

        # Create humidity DB if it doesn't exist
        with HumidityDB() as db:
            if not db.table_exists():
                db.create_table()

        # Create CO2 DB if it doesn't exist
        with Co2DB() as db:
            if not db.table_exists():
                db.create_table()

    def poll_channel(self):
        """
        Reads from cloud & parses data
        """
        logging.info('Reading from cloud, CTRL-C to stop')
        key = c.AIR_QUALITY_READ_KEY
        feed = c.AIR_QUALITY_FEED
        try:
            while True:
                channel_data = read_from_channel(key, feed)
                parsed_data = self.__parse_data(channel_data)

                if parsed_data:
                    logging.debug('New data parsed from channel')
                    logging.debug('New data: {}'.format(parsed_data))
                    self.__save_data(parsed_data)

                sleep(POLL_TIME_SECS)

        except KeyboardInterrupt:
            logging.info('Exiting due to keyboard interrupt')

        except BaseException as e:
            logging.error('An error or exception occurred!')
            logging.error('Error traceback: {}'.format(e))

    def __parse_data(self, channel_data):
        """
        Parse data from cloud

        Parameters
        ----------
        channel_data : dict

        Returns
        -------
        parsed_data : list
        """
        parsed_data = []
        feeds = channel_data.get('feeds', '')

        # Return if no data or if no new data in channel after last saved data
        if not feeds or feeds[LAST_INDEX] == self.__latest_data:
            logging.debug('No new data parsed from channel')
            return parsed_data

        # Find starting index (start after latest data or at beginning)
        if self.__latest_data:
            start_index = feeds.index(self.__latest_data) + INCREMENT
        else:
            start_index = FIRST_INDEX

        # Iterate through feeds & parse for data
        for f in feeds[start_index:]:
            parse_status, data = self.__parse_feed(f)
            if parse_status:
                parsed_data.append(data)

        # Update latest_data value to new latest data record
        self.__latest_data = feeds[LAST_INDEX]

        return parsed_data

    def __parse_feed(self, feed):
        """
        Parse data from given feed

        Parameters
        ----------
        feed : dict

        Returns
        -------
        bool
            True if data successfully parsed
        data : dict
            Data parsed
        """
        data = {}
        date_data = feed.get('created_at', '')
        date_list = re.split('T|Z', date_data)
        id_data = feed.get(c.NODE_FIELD, '')
        location_data = feed.get(c.LOCATION_FIELD, '')
        co2 = feed.get(c.CO2_FIELD, '')
        humidity = feed.get(c.HUMIDITY_FIELD, '')

        if len(date_list) < 2:
            logging.warning('Skipping entry with unparseable date')
            return False, data

        # Other error handling could go here

        if co2 and not humidity:
            data = {'date': date_list[0],
                    'time': date_list[1].split('-')[0],
                    'id': id_data,
                    'location': location_data,
                    'co2': co2}

        elif humidity and not co2:
            data = {'date': date_list[0],
                    'time': date_list[1].split('-')[0],
                    'id': id_data,
                    'location': location_data,
                    'humidity': humidity}
        else:
            raise Exception('Bad read!')

        logging.debug('Data parsed from channel: {}'.format(data))
        return True, data

    def __save_data(self, data):
        """
        Save data if not already in DB

        Parameters
        ---------
        data : list
        """
        # Iterate through all data
        for d in data:

            # If data record is for humidity
            if d.get('humidity', None):

                # Add to Humidity DB if it's new
                with HumidityDB() as db:
                    if not db.record_exists(d):
                        db.add_record(d)

            # If data record is for CO2
            if d.get('co2', None):

                # Add to CO2 DB if it's new
                with Co2DB() as db:
                    if not db.record_exists(d):
                        db.add_record(d)


def parse_args():
    """
    Parses arguments for manual operation of the CloudReader

    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    parser = argparse.ArgumentParser(
        description='Run the CloudReader program (CTRL-C to exit)')

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)
    parser = CloudParser()
    parser.poll_channel()
