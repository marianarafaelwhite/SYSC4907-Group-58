import argparse
import socket
import logging
import json
import time
import constants as c

# logging
LOG = "/tmp/logfile.log"
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)

# console handler
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
logging.getLogger("").addHandler(console)

UDP_PORT = 7777
rate = 3.0  # unit: messages
per = 15.0  # unit: seconds
allowance = dict()  # unit: messages
last_check = dict()


def send_message():
    global message, parse_msg
    try:
        if parse_msg['type'] == "co2":
            sock.sendto(message, (c.APP_CO2, int(UDP_PORT)))
        if parse_msg['type'] == "humidity":
            sock.sendto(message, (c.APP_HUMIDITY, int(UDP_PORT)))
    except socket.gaierror as e:
        logging.error(str(e))
    logging.debug(f'message from {hardware_id}, forwarded')
    allowance[hardware_id] -= 1.0


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="specify a port, default is 7777")
    args = parser.parse_args()

    if args.p:
        UDP_PORT = args.p

    print("UDP receiving port:", UDP_PORT)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind(('', int(UDP_PORT)))

    while True:
        message, address = sock.recvfrom(1024)
        print(message)
        logging.debug(message)
        parse_msg = json.loads(message.decode("utf-8"))

        # token bucket from here..
        # https://stackoverflow.com/questions/667508/whats-a-good-rate-limiting-algorithm
        current_time = time.time()
        hardware_id = parse_msg['id']

        if hardware_id in last_check:
            time_passed = current_time - last_check[hardware_id]
            last_check[hardware_id] = current_time

            allowance[hardware_id] += time_passed * (rate/per)

            logging.debug(f'allowance for id: {hardware_id} is {allowance[hardware_id]:.2f}')

            if allowance[hardware_id] > rate:
                allowance[hardware_id] = rate  # throttle
            if allowance[hardware_id] < 1.0:
                logging.info(f'excessive message from {hardware_id}, discard')
                try:
                    sock.sendto(message, (c.EXCESS_MESSAGE_LOGGER, int(UDP_PORT)))
                except socket.gaierror as ex:
                    logging.error(str(ex))
                continue
            else:
                send_message()
        else:
            # found a new pi
            last_check[hardware_id] = current_time
            allowance[hardware_id] = rate
            send_message()
