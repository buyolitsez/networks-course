import socket
import sys
from time import sleep

from file_transfer import send_file, receive_file

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12345)
timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 5

try:
    send_file('message.txt', sock, server_address, timeout)

    sleep(10)

    receive_file('client_received_message.txt', sock)

finally:
    print('closing socket')
    sock.close()