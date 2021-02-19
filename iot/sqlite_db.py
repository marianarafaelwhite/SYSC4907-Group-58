"""
sqlite_db.py

Developed concurrently for both
SYSC3010 and SYC4907

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import abc
import sqlite3
import logging
import constants as c

FIRST_ROW = 0
SINGLE_RECORD = 1


class SqliteDB(metaclass=abc.ABCMeta):
    """"
    DB to store data

    Attributes
    ----------
    _db_file : str
        file name of sqlite DB file
    _name : str
        name of DB
    _dbconnect : Connection
        sqlite connection object
    _cursor : Cursor
        cursor to perform SQL commands

    Methods
    -------
    manual_enter()
        manually perform context manager entry
    manual_exit()
        manually perform context manager exit
    table_exists()
        Check if table exists
    create_table()
        Abstract method to create table
    add_record(record)
        Abstract method to add record
    record_exists(record)
        Abstract method to check if record exists
    get_records()
        Abstract method to get records
    """

    def __init__(self, db_file, name):
        """
        Initialize SqliteDB Context Manager

        Parameters
        ----------
        db_file : str
            file name of sqlite DB file
        name : str
            name of DB table
        """
        self._db_file = db_file
        self._name = name
        self._dbconnect = None
        self._cursor = None

    def __enter__(self):
        """
        DB context manager entry

        Returns
        -------
        SqliteDB
        """
        self.manual_enter()
        return self

    def __exit__(self, exception, value, trace):
        """
        DB context manager exit

        Parameters
        ----------
        exception : type
        value
        trace : traceback
        """
        self.manual_exit()

    def manual_enter(self):
        """
        Performs steps in entry
        Available for manual use as per Facade pattern
        """
        self._dbconnect = sqlite3.connect(self._db_file)

        # Set row_factory to access columns by name
        self._dbconnect.row_factory = sqlite3.Row

        # Create a cursor to work with the db
        self._cursor = self._dbconnect.cursor()

    def manual_exit(self):
        """
        Performs steps in exit
        Available for manual use as per Facade pattern
        """
        self._dbconnect.commit()
        self._dbconnect.close()
        self._dbconnect = None
        self._cursor = None

    def table_exists(self):
        """
        Check if DB exists

        Returns
        -------
        table_exists : bool
            True if DB exists
        """
        # Check if table already exists
        self._cursor.execute("SELECT count(name) FROM sqlite_master WHERE \
                       type='table' AND name='{}'".format(self._name))

        if self._cursor.fetchone()[FIRST_ROW] == SINGLE_RECORD:
            table_exists = True
        else:
            table_exists = False

        logging.debug('Table exists? : {}'.format(table_exists))
        return table_exists

    @abc.abstractmethod
    def create_table(self):
        pass

    @abc.abstractmethod
    def add_record(self, record):
        pass

    @abc.abstractmethod
    def record_exists(self, record):
        pass

    @abc.abstractmethod
    def get_records():
        pass


class HumidityDB(SqliteDB):
    """
    DB for Humidity

    Methods
    -------
    create_table()
        Creates a HumidityDB table
    add_record(record)
        Adds entry to HumidityDB table
    record_exists(record)
        Check if entry already exists in HumidityDB
    get_records()
        Get all records from Table
    """

    def __init__(self, db_file=c.HUMIDITY_DB_FILE,
                 name=c.HUMIDITY_TABLE):
        """
        Initialize HumidityDB

        Parameters
        ----------
        db_file : str
            file name of sqlite DB file
        name : str
            name of DB table
        """
        super().__init__(db_file, name)

    def create_table(self):
        """
        Create table for HumidityDB

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        """
        logging.debug('Creating new table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        self._cursor.execute(
            "create table {} (date text, \
             time text, humidity float)".format(self._name))

    def add_record(self, record):
        """
        Add entry to HumidityDB table

        Parameters
        ----------
        record : dict
            Entry to add to DB

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        Exception
            Invalid HumidityDB record
        """
        logging.debug('Adding new entry to table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        date = record.get('date', '')
        time = record.get('time', '')
        humidity = record.get('humidity', '')

        if '' in (date, time, humidity):
            raise Exception('Invalid HumidityDB record!')

        self._cursor.execute(
            "insert into {} values(?, ?, ?)".format(self._name),
            (date, time, humidity))

    def record_exists(self, record):
        """
        Check if entry exists in Humidity DB table

        Parameters
        ----------
        record : dict
            Entry to add to DB

        Returns
        -------
        record_exists : bool
            True if entry exists

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        """
        record_exists = False

        logging.debug('Check if record exists in table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        date = record.get('date', '')
        time = record.get('time', '')
        humidity = record.get('humidity', '')

        self._cursor.execute(
            """SELECT count(*) FROM {} WHERE \
                date == ? and time = ? \
                and humidity = ?""".format(self._name),
            (date, time, humidity))

        if self._cursor.fetchone()[FIRST_ROW] == SINGLE_RECORD:
            record_exists = True

        logging.debug('Record exists? : {}'.format(record_exists))
        return record_exists

    def get_records(self):
        """
        Return all records in table

        Returns
        -------
        records : list
            all records in Table
        """
        logging.debug('Get records from table')
        records = []
        self._cursor.execute("SELECT * FROM {}".format(self._name))
        rows = self._cursor.fetchall()

        for r in rows:
            record = {'date': r['date'],
                      'time': r['time'],
                      'humidity': r['humidity']}
            records.append(record)

        return records


class Co2DB(SqliteDB):
    """
    DB for CO2

    Methods
    -------
    create_table()
        Creates a Co2DB table
    add_record(record)
        Adds entry to Co2DB table
    record_exists(record)
        Check if entry already exists in Co2DB
    get_records()
        Get all records from Table
    """

    def __init__(self, db_file=c.CO2_DB_FILE,
                 name=c.CO2_TABLE):
        """
        Initialize Co2DB

        Parameters
        ----------
        db_file : str
            file name of sqlite DB file
        name : str
            name of DB table
        """
        super().__init__(db_file, name)

    def create_table(self):
        """
        Create table for Co2DB

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        """
        logging.debug('Creating new table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        self._cursor.execute(
            "create table {} (date text, \
             time text, co2 int)".format(self._name))

    def add_record(self, record):
        """
        Add entry to Co2DB table

        Parameters
        ----------
        record : dict
            Entry to add to DB

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        Exception
            Invalid Co2DB record
        """
        logging.debug('Adding new entry to table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        date = record.get('date', '')
        time = record.get('time', '')
        co2 = record.get('co2', '')

        if '' in (date, time, co2):
            raise Exception('Invalid Co2DB record!')

        self._cursor.execute(
            "insert into {} values(?, ?, ?)".format(self._name),
            (date, time, co2))

    def record_exists(self, record):
        """
        Check if entry exists in Co2DB table

        Parameters
        ----------
        record : dict
            Entry to add to DB

        Returns
        -------
        record_exists : bool
            True if entry exists

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        """
        record_exists = False

        logging.debug('Check if record exists in table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        date = record.get('date', '')
        time = record.get('time', '')
        co2 = record.get('co2', '')

        self._cursor.execute(
            """SELECT count(*) FROM {} WHERE \
                date == ? and time = ? \
                and co2 = ?""".format(self._name),
            (date, time, co2))

        if self._cursor.fetchone()[FIRST_ROW] == SINGLE_RECORD:
            record_exists = True

        logging.debug('Record exists? : {}'.format(record_exists))
        return record_exists

    def get_records(self):
        """
        Return all records in table

        Returns
        -------
        records : list
            all records in Table
        """
        logging.debug('Get records from table')
        records = []
        self._cursor.execute("SELECT * FROM {}".format(self._name))
        rows = self._cursor.fetchall()

        for r in rows:
            record = {'date': r['date'],
                      'time': r['time'],
                      'co2': r['co2']}
            records.append(record)

        return records
