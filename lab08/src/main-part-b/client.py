import socket
import sys
from time import sleep

from file_transfer import send_file, receive_file

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address_1 = ('localhost', 12345)
server_address_2 = ('localhost', 12346)
receive_sock.bind(server_address_1)
timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 5

try:
    send_file('message.txt', send_sock, server_address_2, timeout)

    print("\n------------------------\n")

    receive_file('client_received_message.txt', receive_sock)

finally:
    print('closing sockets')
    send_sock.close()
    receive_sock.close()