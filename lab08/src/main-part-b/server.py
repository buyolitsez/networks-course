import socket
import sys
from file_transfer import send_file, receive_file

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address_1 = ('localhost', 12345)
server_address_2 = ('localhost', 12346)
receive_sock.bind(server_address_2)

timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 5

try:
    receive_file('server_received_message.txt', receive_sock)

    print("\n------------------------\n")

    send_file('message.txt', send_sock, server_address_1, timeout)

except Exception as e:
    print('Error occurred:', e)

finally:
    print('closing sockets')
    send_sock.close()
    receive_sock.close()