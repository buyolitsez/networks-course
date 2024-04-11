import socket
import time
import os
import random
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12345)
timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 5
packet_number = 0

try:
    with open('message.txt', 'rb') as f:
        while True:
            message = f.read(1024)
            if not message:
                break

            while True:
                try:
                    print('sending data')
                    if random.random() > 0.3:
                        sent = sock.sendto((str(packet_number) + message.decode()).encode(), server_address)

                    print('waiting to receive')
                    sock.settimeout(timeout)
                    data, server = sock.recvfrom(4096)
                    print('received "%s"' % data.decode())
                    if data.decode() == 'ACK' + str(packet_number):
                        packet_number = 1 - packet_number
                        break
                except socket.timeout:
                    print('Timeout, resending')
                except Exception as e:
                    print('Error occurred:', e)
                    break

finally:
    print('closing socket')
    sock.close()
