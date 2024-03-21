import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    now = time.ctime(time.time()) + "\r\n"
    sock.sendto(now.encode('utf-8'), ('<broadcast>', 12345))
    time.sleep(1)
