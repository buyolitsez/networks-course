import socket
import random
from checksum import calculate_checksum, verify_checksum

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

            if data:
                packet_number, received_checksum, message = data.decode().split('|', 2)
                received_checksum = int(received_checksum)
                message = message.encode()

                calculated_checksum = calculate_checksum(message)

                if not verify_checksum(message, received_checksum):
                    print('Checksum does not match, packet ignored')
                    continue

                if random.random() < 0.3:
                    print('Packet lost, not sending ACK')
                    continue

                f.write(message)
                sent = sock.sendto(('ACK' + packet_number).encode(), address)
                print('sent %s bytes back to %s' % (sent, address))
        except Exception as e:
            print('Error occurred:', e)
            break