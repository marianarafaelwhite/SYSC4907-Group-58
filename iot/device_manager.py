#!/usr/bin/env python3
import argparse
import json
import logging
import socket
import psycopg2

# logging
LOG = "/tmp/logfile.log"
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)

# console handler
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logging.getLogger("").addHandler(console)

DB_HOST = "34.71.10.216"
DB_PORT = 5432
DB_USER = "device_db_user"
DB_PW = "0t!^5l1TW^1z&K!!"
RECEIVE_PORT = 3210

# PostgreSQL host on GCP 34.71.10.216
# username: device_db_user
# password: 0t!^5l1TW^1z&K!!

# need create a table in DB if haven't dont so
# DB DDL...
# CREATE TABLE device_list (
#   /* Mac address, 48bit */
# 	device_id BIGINT PRIMARY KEY,
# 	/* Max length per RFC3696 */
# 	notification_email VARCHAR(320) NOT NULL
# );


def connect():
    """
    Connect to the PostgreSQL DB
    :return: connection to the DB
    """
    try:
        connection = psycopg2.connect(user=DB_USER,
                                      password=DB_PW,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database="device-db")
        return connection
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Failed to connect to DB, err:{error}")


def update_device_email(device_id, email):
    """
    Update the device notification email registered in the DB

    :param device_id: 48bit mac
    :param email: email address to be used for notification
    :return: true if update is done
    """
    try:
        connection = connect()
        postgres_query = "INSERT INTO device_list (device_id, notification_email) VALUES (%s, %s) " \
                         "ON CONFLICT (device_id) DO UPDATE SET notification_email = excluded.notification_email"
        cursor = connection.cursor()
        cursor.execute(postgres_query, [device_id, email])

        connection.commit()
        count = cursor.rowcount
        logging.error(f"{count} record inserted successfully into table")
        return True
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Failed to insert record, err:{error}")
    return False


def retrieve_device_email(device_id):
    """
    Retrieve the notification email address registered in the DB

    :param device_id: 48bit mac
    :return: email address for this specific device
    """
    try:
        connection = connect()
        postgres_query = "SELECT notification_email FROM device_list WHERE device_id=(%s)"
        cursor = connection.cursor()
        cursor.execute(postgres_query, [device_id])
        result = cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Failed to retrieve record, err:{error}")
        return ""


def dump_all_email():
    """
    Dump all emails registered in the db

    :return: email address for all devices
    """
    try:
        connection = connect()
        postgres_query = "SELECT device_id, notification_email FROM device_list"
        cursor = connection.cursor()
        cursor.execute(postgres_query)
        result = [dict((cursor.description[i][0], value)
                       for i, value in enumerate(row)) for row in cursor.fetchall()]
        return result
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Failed to retrieve record, err:{error}")
        return ""


def process_request_message(message):
    """
    Process message and generate corresponding reply
    :param message: message to be replied
    :return: reply to the message
    """
    parse_msg = json.loads(message.decode('utf-8'))
    request_type = parse_msg['type']
    if request_type == "register":
        device_id = parse_msg['device_id']
        result = update_device_email(device_id, parse_msg['email'])
        return json.dumps({'device_id': device_id, 'status': result})
    if request_type == "retrieve":
        device_id = parse_msg['device_id']
        email = retrieve_device_email(device_id)
        return json.dumps({'device_id': device_id, 'email': email})
    if request_type == "dump":
        result = dump_all_email()
        return json.dumps(result)


def device_manager():
    """
    Main loop of the function
    :return:
    """
    logging.info(f"Device manager listening on receiving port: {RECEIVE_PORT}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind(('', int(RECEIVE_PORT)))

    while True:
        message, address = sock.recvfrom(1024)
        logging.debug('Received: {}'.format(message))

        reply = process_request_message(message)
        logging.debug(reply)
        sock.sendto(bytes(reply, 'utf-8'), address)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true', help="print debug messages")
    parser.add_argument("-ip", '--ip_address', help="specify the database address")
    parser.add_argument("-r", help=f"specify a port to receive on, default is {RECEIVE_PORT}")
    parser.add_argument("-u", "--username", help="username of the db")
    parser.add_argument("-p", "--password", help="password of the db")
    args = parser.parse_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    if args.ip_address:
        DB_HOST = args.ip_address
    if args.r:
        RECEIVE_PORT = args.r
    if args.username:
        DB_USER = args.username
    if args.password:
        DB_PASSWORD = args.password

    device_manager()
