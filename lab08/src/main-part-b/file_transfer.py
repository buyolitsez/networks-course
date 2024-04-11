import socket
import random
from checksum import calculate_checksum, verify_checksum

def send_file(filename, sock, address, timeout):
    print('\nsending file:', filename, 'to:', address)
    packet_number = 0
    with open(filename, 'rb') as f:
        while True:
            message = f.read(1024)
            if not message:
                break

            checksum = calculate_checksum(message)

            while True:
                try:
                    print('sending data, packet number:', packet_number, 'checksum:', checksum, 'message len:',
                          len(message))
                    if random.random() > 0.3:
                        sock.sendto((str(packet_number) + '|' + str(checksum) + '|' + message.decode()).encode(),
                                    address)

                    print('waiting to receive')
                    sock.settimeout(timeout)
                    data, server = sock.recvfrom(4096)
                    print('received len = "%s"' % len(data))
                    if data.decode() == 'ACK' + str(packet_number):
                        packet_number = 1 - packet_number
                        break
                except socket.timeout:
                    print('Timeout, resending')
                except Exception as e:
                    print('Error occurred:', e)
                    break

def receive_file(filename, sock):
    print('\nreceiving file:', filename, 'from:', sock.getsockname())
    with open(filename, 'wb') as f:
        while True:
            print('\nwaiting to receive message')
            try:
                sock.settimeout(15)
                data, address = sock.recvfrom(4096)
                print('received %s bytes from %s' % (len(data), address))

                if data:
                    packet_number, received_checksum, message = data.decode().split('|', 2)
                    received_checksum = int(received_checksum)
                    message = message.encode()

                    if not verify_checksum(message, received_checksum):
                        print('Checksum does not match, packet ignored')
                        continue

                    if random.random() < 0.3:
                        print('Packet lost, not sending ACK')
                        continue

                    f.write(message)
                    sent = sock.sendto(('ACK' + packet_number).encode(), address)
                    print('sent %s bytes back to %s' % (sent, address))
            except socket.timeout:
                print('ending file reception')
                break
            except Exception as e:
                print('Error occurred:', e)
                break