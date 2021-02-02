import argparse
import socket
import logging
import json

# logging  
LOG = "/tmp/logfile.log"                                                     
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)  

# console handler  
console = logging.StreamHandler()  
console.setLevel(logging.ERROR)  
logging.getLogger("").addHandler(console)

UDP_PORT = 7777

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
    try:
        if (parse_msg['type'] == "co2"):
            sock.sendto(message, ("app-co2", int(UDP_PORT)))
        if (parse_msg['type'] == "humidity"):
            sock.sendto(message, ("app-humidity", int(UDP_PORT)))
    except socket.gaierror as ex:
    	logging.error(str(ex))
    
