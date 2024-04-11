import socket
import random
from checksum import calculate_checksum, verify_checksum
from file_transfer import send_file, receive_file
import sys

timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 5
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12345)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

try:
    receive_file('server_received_message.txt', sock)

    send_file('message.txt', sock, server_address, timeout)

except Exception as e:
    print('Error occurred:', e)

finally:
    print('closing socket')
    sock.close()