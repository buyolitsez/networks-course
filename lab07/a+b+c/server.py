import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)
    if random.random() < 0.2:
        continue
    if data:
        sent_data = data.decode('utf-8').upper().encode('utf-8')
        sent = sock.sendto(sent_data, address)
