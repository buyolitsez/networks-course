import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12345)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

with open('received_message.txt', 'wb') as f:
    while True:
        print('\nwaiting to receive message')
        try:
            data, address = sock.recvfrom(4096)

            print('received %s bytes from %s' % (len(data), address))
            # print(data)

            if data:
                if random.random() < 0.3:
                    print('Packet lost, not sending ACK')
                    continue
                f.write(data[1:].decode().encode())
                sent = sock.sendto(('ACK' + data.decode()[0]).encode(), address)
                print('sent %s bytes back to %s' % (sent, address))
        except Exception as e:
            print('Error occurred:', e)
            break
