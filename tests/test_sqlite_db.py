#!/usr/bin/env python3
"""
test_sqlite_db.py

Developed concurrently for both
SYSC3010 and SYC4907
"""
import os
from unittest import TestCase, main
from sqlite_db import HumidityDB, Co2DB

TEMP_HUMIDITY_DB = 'temp_humidity.db'
TEMP_HUMIDITY_TABLE = 'temp_humidity'
TEMP_CO2_DB = 'temp_co2.db'
TEMP_CO2_TABLE = 'temp_co2'


class TestHumidityDB(TestCase):

    def setUp(self):
        self.__db = HumidityDB(db_file=TEMP_HUMIDITY_DB,
                               name=TEMP_HUMIDITY_TABLE)
        self.__db.manual_enter()

    def tearDown(self):
        self.__db.manual_exit()
        if os.path.exists(TEMP_HUMIDITY_DB):
            os.remove(TEMP_HUMIDITY_DB)

    def test_create_table(self):
        """
        Test creating table that doesn't already exist
        """
        err_msg = 'Table already exists'
        self.assertFalse(self.__db.table_exists(), err_msg)

        self.__db.create_table()
        err_msg = 'Table does not exist'
        self.assertTrue(self.__db.table_exists(), err_msg)

    def test_add_record(self):
        """
        Test adding new, good record to DB
        """
        # Note: mac addr is 48 bit
        # so testing with something larger than 2^32
        # 0d4886718345 = 0x123456789
        record = {'date': '2020-11-22',
                  'time': '14:03:17',
                  'id': '4886718345',
                  'humidity': '45.0192727'}

        self.__db.create_table()
        err_msg = 'Record exists unexpectedly'
        self.assertFalse(self.__db.record_exists(record), err_msg)

        self.__db.add_record(record)
        err_msg = 'Record failed to be added to DB table'
        self.assertTrue(self.__db.record_exists(record), err_msg)


class TestCo2DB(TestCase):

    def setUp(self):
        self.__db = Co2DB(db_file=TEMP_CO2_DB,
                          name=TEMP_CO2_TABLE)
        self.__db.manual_enter()

    def tearDown(self):
        self.__db.manual_exit()
        if os.path.exists(TEMP_CO2_DB):
            os.remove(TEMP_CO2_DB)

    def test_create_table(self):
        """
        Test creating table that doesn't already exist
        """
        err_msg = 'Table already exists'
        self.assertFalse(self.__db.table_exists(), err_msg)

        self.__db.create_table()
        err_msg = 'Table does not exist'
        self.assertTrue(self.__db.table_exists(), err_msg)

    def test_add_record(self):
        """
        Test adding new, good record to DB
        """
        # Note: mac addr is 48 bit
        # so testing with something larger than 2^32
        # 0d4886718345 = 0x123456789
        record = {'date': '2020-11-22',
                  'time': '14:03:17',
                  'id': '4886718345',
                  'co2': '412'}

        self.__db.create_table()
        err_msg = 'Record exists unexpectedly'
        self.assertFalse(self.__db.record_exists(record), err_msg)

        self.__db.add_record(record)
        err_msg = 'Record failed to be added to DB table'
        self.assertTrue(self.__db.record_exists(record), err_msg)


if __name__ == '__main__':
    main()
