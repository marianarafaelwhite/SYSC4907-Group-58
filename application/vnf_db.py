"""
sqliteDB helper class

Note: this code has been adapted from another personal project
This code may not be needed
"""
import sqlite3
import logging
import argparse
import constants as c

FIRST_ROW = 0
SINGLE_RECORD = 1


class VNF_DB():
    """"
    NFV DB to store data

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
    table_exists()
    create_table()
    add_record(record)
    record_exists(record)
    get_records()
    """

    def __init__(self, db_file, name):
        """
        Initialize VNF DB Context Manager

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
        table_exists = False

        # Check if table already exists
        self._cursor.execute("SELECT count(name) FROM sqlite_master WHERE \
                       type='table' AND name='{}'".format(self._name))
        if self._cursor.fetchone()[FIRST_ROW] == SINGLE_RECORD:
            table_exists = True
        return table_exists

    def create_table(self):
        """
        Create table for VNF DB

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        """
        logging.debug('VNF_DB: Creating new table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        # TODO:
        self._cursor.execute(
            "create table {} (date text, \
             time text, location text, nodeID text, \
             lightStatus integer)".format(self._name))

    def add_record(self, record):
        """
        Add entry to VNF DB table

        Parameters
        ----------
        record : dict
            Entry to add to DB

        Raises
        ------
        Exception
            Invalid use of SqliteDB context manager
        """
        logging.debug('VNF_DB: Adding new entry to table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        # TODO:
        self._cursor.execute(
            "insert into {} values(?, ?, ?, ?, ?)".format(self._name),
            (date, time, location, node_id, light_status))

    def record_exists(self, record):
        """
        Check if entry exists in VNF DB table

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

        logging.debug('VNF_DB: check if record exists in table')
        if not self._dbconnect or not self._cursor:
            raise Exception('Invalid call to Context Manager method!')

        # TODO:
        self._cursor.execute(
            """SELECT count(*) FROM {} WHERE \
                date == ? and time = ? and location = ? and nodeID = ? \
                and lightStatus = ?""".format(self._name),
            (date, time, location, node_id, light_status))

        if self._cursor.fetchone()[FIRST_ROW] == SINGLE_RECORD:
            record_exists = True

        return record_exists

    def get_records(self):
        """
        Return all records in table

        Returns
        -------
        records : list
            all records in Table
        """
        logging.debug('VNF_DB: Get records from table')
        records = []
        self._cursor.execute("SELECT * FROM {}".format(self._name))
        rows = self._cursor.fetchall()

        for r in rows:
            # TODO:
            record = {'date': r['date'],
                      'time': r['time'],
                      'location': r['location'],
                      'nodeID': r['nodeID'],
                      'lightStatus': r['lightStatus']}
            records.append(record)

        return records


def nfv_db(file_name, table_name):
    """
    NFV DB Creation

    Parameters
    ----------
    file_name : str
        Name of test DB file
    table : str
        Name of test DB table
    """
    # TODO: Create reecords

    with VNF_DB(db_file=file_name, name=table_name) as db_obj:
        logging.info('VNF_DB: Checking & creating table if needed')
        if not db_obj.table_exists():
            db_obj.create_table()

        logging.info('VNF_DB: Adding only the new records to table')
        for r in records:
            if not db_obj.record_exists(r):
                db_obj.add_record(r)


def parse_args():
    """
    Parses arguments for manual operation of the VNF_DB

    Returns
    -------
    args : Namespace
        Populated attributes based on args
    """
    parser = argparse.ArgumentParser(
        description='Run the sqlite DB NFV program')

    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        help='Print all debug logs')

    parser.add_argument('-vnf',
                        '--vnf_create',
                        default=False,
                        action='store_true',
                        help='Run LightClapperDB test')

    parser.add_argument('-f',
                        '--file_name',
                        type=str,
                        required=True,
                        metavar='<file_name.db>',
                        help='Specify file name of SQL db (Relative to pwd)')

    parser.add_argument('-t',
                        '--table_name',
                        type=str,
                        required=True,
                        metavar='<test_table_name>',
                        help='Specify table name of SQL db')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=c.LOGGING_FORMAT, level=logging_level)

    if args.vnf_create:
        nfv_db(args.file_name, args.table_name)
    else:
        logging.error('No DB specified!')
